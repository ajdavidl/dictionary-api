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


def query(word, langFrom, langTo):

    available_languages = ['pt', 'en', 'es']
    if langFrom not in available_languages:
        return 'error in language definition'
    if langTo not in available_languages:
        return 'error in language definition'

    text = {}
    text['0'] = 'GLOSBE'

    URL_GLOSBE = 'https://pt.glosbe.com/%s/%s/%s' % (langFrom, langTo, word)

    response = requests.get(URL_GLOSBE, headers={
                            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'})
    soup = BeautifulSoup(response.content, 'html.parser')

    words = {}
    for div in soup.findAll('h3'):
        words[word] = div.text

    text['words'] = words

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
    text2['0'] = 'PONS'

    URL_PONS = 'https://en.pons.com/translate/%s-%s/%s' % (
        languageName(langFrom), languageName(langTo), word)
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

    output = {'dict1': text, 'dict2': text2}
    return output


app = Flask(__name__)


@app.route('/<string:word>', methods=['GET'])
def queryDictionary(word):
    output = query(word, 'en', 'pt')
    return jsonify({'resposta': output})


if __name__ == '__main__':
    app.run(host="localhost", port=5555, debug=True)
