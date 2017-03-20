# -*- coding: utf-8 -*-

import os
import random
import requests
from fuzzywuzzy.process import extractOne as fuzzy_extract

from flask import Flask
from flask_ask import Ask, statement


app = Flask(__name__)
ask = Ask(app, '/')

EXAMPLE = 'E.g. To French: https://www.googleapis.com/language/translate/v2?q=Example&target=fr&key=<your_key>'
API = 'https://www.googleapis.com/language/translate/v2'
API_KEY = os.environ.get('C3PO_API_KEY', None)
if not API_KEY:
    raise Exception('Please export C3PO_API_KEY=<your_key>\n%s' % EXAMPLE)


# https://cloud.google.com/translate/docs/languages
LANGUAGES = {
    'spanish': 'es',
    'french': 'fr',
    'dutch': 'nl',
    'german': 'de',
    'polish': 'pl',
    'korean': 'ko',
    'japanese': 'jw',
    'italian': 'it',
    'irish': 'ga',
    'icelandic': 'is',
    'hawaiian': 'haw',
    'norwegian': 'no',
    'afrikaans': 'af',
    'english': 'en',
    'greek': 'el',
    'danish': 'da',
    'filipino': 'tl',
    'finnish': 'fi',
    'hebrew': 'iw',
    'georgian': 'ka',
    'latin': 'la',
    'swedish': 'sv',

    # None == TODO
    'thai': None, # 'th',
    'hindi': None, #'hi',
    'vietnamese': None, # 'vi',
    'welsh': 'cy',
    'yiddish': None, # 'yi',

    'russian': None, # 'ru',
    'chinese': None, # 'zh-CN',
    'mandarin': None, # 'zh-CN',
    'lithuanian': None, # 'lt',

    'albanian': None, # 'sq',
    'amharic': None, # 'am',
    'arabic': None, # 'ar',
    'armenian': None, # 'hy',
    'azeerbaijani': None, # 'az',
    'basque': None, # 'eu',
    'belarusian': None, # 'be',
    'bengali': None, # 'bn',
    'bosnian': None, # 'bs',
    'bulgarian': None, # 'bg',
    'catalan': None, # 'ca',
    'cebuano': None, # 'ceb',
    'chichewa': None, # 'ny',
    'chinese (Simplified)': None, # 'zh',-CN
    'chinese (Traditional)': None, # 'zh',-TW
    'corsican': None, # 'co',
    'croatian': None, # 'hr',
    'czech': None, # 'cs',
    'esperanto': None, # 'eo',
    'estonian': None, # 'et',
    'frisian': None, # 'fy',
    'galician': None, # 'gl',
    'gujarati': None, # 'gu',
    'haitian Creole': None, # 'ht',
    'hausa': None, # 'ha',
    'hmong': None, # 'hmn',
    'hungarian': None, # 'hu',
    'igbo': None, # 'ig',
    'indonesian': None, # 'id',
    'javanese': None, # 'jw',
    'kannada': None, # 'kn',
    'kazakh': None, # 'kk',
    'khmer': None, # 'km',
    'kurdish': None, # 'ku',
    'kyrgyz': None, # 'ky',
    'lao': None, # 'lo',
    'latvian': None, # 'lv',
    'luxembourgish': None, # 'lb',
    'macedonian': None, # 'mk',
    'malagasy': None, # 'mg',
    'malay': None, # 'ms',
    'malayalam': None, # 'ml',
    'maltese': None, # 'mt',
    'maori': None, # 'mi',
    'marathi': None, # 'mr',
    'mongolian': None, # 'mn',
    'burmese': None, # 'my',
    'nepali': None, # 'ne',
    'pashto': None, # 'ps',
    'persian': None, # 'fa',
    'portuguese': None, # 'pt',
    'punjabi': None, # 'ma',
    'romanian': None, # 'ro',
    'samoan': None, # 'sm',
    'scots Gaelic': None, # 'gd',
    'serbian': None, # 'sr',
    'sesotho': None, # 'st',
    'shona': None, # 'sn',
    'sindhi': None, # 'sd',
    'sinhala': None, # 'si',
    'slovak': None, # 'sk',
    'slovenian': None, # 'sl',
    'somali': None, # 'so',
    'sundanese': None, # 'su',
    'swahili': None, # 'sw',
    'tajik': None, # 'tg',
    'tamil': None, # 'ta',
    'telugu': None, # 'te',
    'turkish': None, # 'tr',
    'ukrainian': None, # 'uk',
    'urdu': None, # 'ur',
    'uzbek': None, # 'uz',
    'xhosa': None, # 'xh',
    'yoruba': None, # 'yo',
    'zulu': None, # 'zu',

}


VARIANTS = [
    u'For "{orig}" in {lang}, you would say, "{trans}"',
    u'"{orig}" in {lang} would be, "{trans}"',
    u'In {lang}, "{orig}" is, "{trans}"',
    u'It is, "{trans}".',
    u'Hmm. It\'s "{trans}".',
    u'That would be "{trans}".',
    ]


def words_after_translate(text):
    first, _, rest = text.partition(' ')
    return rest or first


def fuzzy_match_language(incorrect_language):
    choices = random.choice([lang for lang, code in LANGUAGES.items() if code])
    best, ratio = fuzzy_extract(incorrect_language, choices)
    print(best, ratio)
    if ratio < 75:
        return False, best, ratio
    return True, best, ratio


def handle(text, language):
    if not text:
        message = random.choice(['Say what?', 'Huh?', 'What?!', 'I beg your pardon, but what did you say?'])
        return statement(message)
    if not language:
        message = random.choice(['Oh dear, didn\'t catch that language.', 'What language?', 'Didn\'t catch that language.', 'In what language?'])
        return statement(message)

    language = language.lower()

    check_fuzzy = False
    try:
        target_language = LANGUAGES[language]
    except KeyError:
        target_language = None
        check_fuzzy = True

    if not target_language and not check_fuzzy:
        message = random.choice([
            'Support for {lang} coming soon!'.format(lang=language),
            'I\'ll support {lang} soon!'.format(lang=language),
            ])
        rand = random.choice([lang for lang, code in LANGUAGES.items() if code])
        message += random.choice([' Maybe try "{rand}"', ' Try my second language, "{rand}"']).format(rand=rand)
        return statement(message)

    if check_fuzzy:
        good_enough, fuzzy_lang, ratio = fuzzy_match_language(language)
        print('fuzzy: %s' % fuzzy_lang)
        if not good_enough:
            message = random.choice(['I heard "{lang}" and only {ratio} percent think that may have been {fuzzy}. Please try again.',
                                     'No match. "{lang}" is only {ratio} percent like {fuzzy}. Try again, please.',
                                     '"{lang}" is {ratio} percent like {fuzzy}. Please try again.']).format(
                lang=language, ratio=ratio, fuzzy=fuzzy_lang)
            return statement(message)
        target_language = LANGUAGES[fuzzy_lang]

    params = {
        'q': text,
        'target': target_language,
        'key': API_KEY
    }
    api_response = requests.get(API, params=params)
    data = api_response.json()
    print(api_response.status_code, data)

    if api_response.status_code != 200:
        message = random.choice(['A {code}. Curse my metal body!', 'Oh dear, a {code}!', 'Oh no! {code}', 'Artwo, a {code}!'])
        return statement(message.format(code=api_response.status_code))

    translation_data = data['data']['translations'][0]
    # TODO: apply source language. Currently English only. Maybe Ewok.
    # detected_source_language = translation_data['detectedSourceLanguage']
    translated_text = translation_data['translatedText']

    # TODO: translate
    variant = VARIANTS[random.randint(0, len(VARIANTS) - 1)]
    speech_text = variant.format(orig=text, lang=language, trans=translated_text).encode('utf-8')

    print(variant, translated_text, speech_text)
    return statement(speech_text).simple_card(speech_text[:60], speech_text)


@ask.intent('translate')
def hello(text, language):
    print('translate keyword')
    text = words_after_translate(text)
    print(text, language)
    if text == 'translate':
        message = random.choice(['Translate what?', 'Come again?'])
        return statement(message)

    return handle(text, language)


if __name__ == '__main__':
    app.run()
