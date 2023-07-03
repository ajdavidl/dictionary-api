# dictionary-api

An API to query dictionary sites.

This small project creates a flask API in the localhost. The API queries dictionary sites to get the word translations. I use it in my self-hosted [LWT](https://github.com/HugoFara/lwt) server to learn new words.

The available dictionaries are [Glosbe](https://glosbe.com/), [Pons](https://en.pons.com/translate) and [Linguee](https://www.linguee.com/).

## Usage

```shell
git clone https://github.com/ajdavidl/dictionary-api.git
cd dictionary-api
pip install -r requirements.txt
python app.py
```

Now you can query the API using `curl`. 

Example: to query the English word `language` in Portuguese.

```shell
curl http://localhost:5555/en/pt/language
```

Or you can browse the address `http://localhost:5555/en/pt/language` in your favorite browser.