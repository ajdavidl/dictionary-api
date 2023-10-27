import json
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
from transformers import pipeline

TRANSLATOR = pipeline("translation", model="Helsinki-NLP/opus-mt-ine-ine")


def loadDictionaries(file):
    """
    Load the local dictionaries.
    """
    with open(file, 'r') as f:
        lines = f.readlines()
    lines = [line.split('\t') for line in lines]
    return {key: re.sub("\n", "", value) for key, value in lines}


def languageName(lang):
    if lang == 'en':
        return 'english'
    elif lang == 'pt':
        return 'portuguese'
    elif lang == 'es':
        return 'spanish'
    elif lang == 'fr':
        return 'french'
    elif lang == 'de':
        return 'german'
    elif lang == 'it':
        return 'italian'
    elif lang == 'ro':
        return 'romanian'
    elif lang == 'ca':
        return 'catalan'
    elif lang == 'la':
        return 'latin'


def languageName2(lang):
    if lang == 'en':
        return 'eng'
    elif lang == 'pt':
        return 'por'
    elif lang == 'es':
        return 'spa'
    elif lang == 'fr':
        return 'fre'
    elif lang == 'de':
        return 'deu'
    elif lang == 'it':
        return 'ita'
    elif lang == 'ro':
        return 'ron'
    elif lang == 'ca':
        return 'cat'
    elif lang == 'la':
        return 'latin'


def query(word, langFrom, langTo):
    """
    Query the dictionaries in the Internet.
    """
    available_languages = ['pt', 'en', 'es',
                           'fr', 'de', 'it', 'ro', 'ca', 'la']
    if langFrom not in available_languages:
        return 'error in language definition'
    if langTo not in available_languages:
        return 'error in language definition'
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"

    text = {}

    URL_GLOSBE = 'https://pt.glosbe.com/%s/%s/%s' % (langFrom, langTo, word)

    print(URL_GLOSBE)
    response = requests.get(URL_GLOSBE, headers={
                            'User-agent': user_agent})
    soup = BeautifulSoup(response.content, 'html.parser')

    words = []
    for div in soup.findAll('h3'):
        words.append(div.text)

    text[word] = words

    expressions = {}
    for li in soup.findAll('li', {'class': 'px-2 py-1 flex even:bg-slate-100'}):
        a = li.find('a')
        div = li.findAll('div')
        s = re.sub('\n', ' ', a.text)
        try:
            t = re.sub('\n', ' ', div[1].text)
            expressions[s] = t
        except:
            pass
    text['expressions'] = expressions

    text2 = {}

    URL_PONS = 'https://en.pons.com/translate/%s-%s/%s' % (
        languageName(langFrom), languageName(langTo), word)
    print(URL_PONS)

    response = requests.get(URL_PONS, headers={
                            'User-agent': user_agent})
    soup = BeautifulSoup(response.content, 'html.parser')

    wordsSource = []
    wordsTarget = []

    for div in soup.findAll('div', {'class': 'source'}):
        wordsSource.append(div.text)

    for div in soup.findAll('div', {'class': 'target'}):
        wordsTarget.append(div.text)

    if len(wordsSource) == len(wordsTarget):
        for i in range(1, len(wordsTarget)):
            s = re.sub('\n', '', wordsSource[i])
            t = re.sub('\n', '', wordsTarget[i])
            text2[s] = t

    text3 = {}

    URL_LINGUEE = 'https://www.linguee.com/%s-%s/search?source=auto&query=%s' % (
        languageName(langFrom), languageName(langTo), word)
    print(URL_LINGUEE)

    response = requests.get(URL_LINGUEE, headers={
                            'User-agent': user_agent})
    soup = BeautifulSoup(response.content, 'html.parser')

    wordsList = []
    for div in soup.findAll('div', {'class': 'translation sortablemg'}):
        t = re.sub('\n', '', div.text)
        wordsList.append(t)

    text3[word] = wordsList

    try:
        blob = TextBlob(word).translate(to=langTo, from_lang=langFrom)
        text4 = str(blob)
    except:
        text4 = ""

    text5 = TRANSLATOR(">>%s<< %s" % (languageName2(langTo), word))
    text5 = text5[0]['translation_text']

    output = {'GLOSBE': text, 'PONS': text2,
              'LINGUEE': text3, 'GOOGLE TRANSLATE': text4,
              'HUGGINGFACE': text5}
    return output


spa_por = loadDictionaries('data/spa-por.tsv')
deu_por = loadDictionaries('data/deu-por.tsv')
eng_por = loadDictionaries('data/eng-por.tsv')
fre_por = loadDictionaries('data/fre-por.tsv')
ita_por = loadDictionaries('data/ita-por.tsv')
lat_por = loadDictionaries('data/lat-por.tsv')


def queryLocal(word, langFrom, langTo):
    """
    Query the local dictionary.
    """
    if langFrom == 'spa' and langTo == 'por':
        dictionary = spa_por
    elif langFrom == 'deu' and langTo == 'por':
        dictionary = deu_por
    elif langFrom == 'eng' and langTo == 'por':
        dictionary = eng_por
    elif langFrom == 'fre' and langTo == 'por':
        dictionary = fre_por
    elif langFrom == 'ita' and langTo == 'por':
        dictionary = ita_por
    elif langFrom == 'latin' and langTo == 'por':
        dictionary = lat_por
    else:
        return {'message': '%s-%s Dictionary not available.' % (langFrom, langTo)}
    if word in dictionary:
        return {word: dictionary[word]}
    else:
        return{word: []}


app = Flask(__name__)


# internet dictionary query


@app.route('/<string:langFrom>/<string:langTo>/<string:word>', methods=['GET'])
# this endpoint will be removed
def queryDictionary(word, langFrom, langTo):
    output = query(word, langFrom, langTo)
    return jsonify({'result': output})


@app.route('/web/<string:langFrom>/<string:langTo>/<string:word>', methods=['GET'])
def queryWebDictionary(word, langFrom, langTo):
    output = query(word, langFrom, langTo)
    return jsonify({'result': output})
# local dictionary query


@app.route('/local/<string:langFrom>/<string:langTo>/<string:word>', methods=['GET'])
def queryLocalDictionary(word, langFrom, langTo):
    langFrom = languageName2(langFrom)
    langTo = languageName2(langTo)
    output = queryLocal(word, langFrom, langTo)
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(host="localhost", port=5555, debug=True)
