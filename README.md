# dictionary-api

An API to query dictionary sites.

This small project creates a flask API in the localhost. The API queries dictionary sites to get the word translations. I use it in my self-hosted [LWT](https://github.com/HugoFara/lwt) server to learn new words.

The available dictionaries are [Glosbe](https://glosbe.com/), [Pons](https://en.pons.com/translate) and [Linguee](https://www.linguee.com/).

In the data folder there are dictionaries in the tsv format that were compiled from freedict and wikidict dictionaries.

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

If you wish to use the local dictionaries (only Portuguese as target language), you need to put the local name in the API call. The code names are also different. In this case, we use the 3 letters code. 

```shell
curl http://localhost:5555/local/eng/por/language
```

