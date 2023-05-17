import json
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup  # bs4.__versions__ == 4.11.1
import re


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


def query(word, langFrom, langTo):

    available_languages = ['pt', 'en', 'es', 'fr', 'de', 'it', 'ro', 'ca']
    if langFrom not in available_languages:
        return 'error in language definition'
    if langTo not in available_languages:
        return 'error in language definition'

    text = {}

    URL_GLOSBE = 'https://pt.glosbe.com/%s/%s/%s' % (langFrom, langTo, word)

    print(URL_GLOSBE)
    response = requests.get(URL_GLOSBE, headers={
                            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
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
                            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
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
                            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
    soup = BeautifulSoup(response.content, 'html.parser')

    wordsList = []
    for div in soup.findAll('div', {'class': 'translation sortablemg'}):
        t = re.sub('\n', '', div.text)
        wordsList.append(t)

    text3[word] = wordsList

    output = {'GLOSBE': text, 'PONS': text2, 'LINGUEE': text3}
    return output


app = Flask(__name__)


@app.route('/<string:langFrom>/<string:langTo>/<string:word>', methods=['GET'])
def queryDictionary(word, langFrom, langTo):
    output = query(word, langFrom, langTo)
    return jsonify({'resposta': output})


if __name__ == '__main__':
    app.run(host="localhost", port=5555, debug=True)
