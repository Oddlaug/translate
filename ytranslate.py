# -*- coding:utf-8 -*-
import requests
import os
import json
import sys

API_KEY = r'trnsl.1.1.20190211T031830Z.1d936a8fa3355ce3.fc8bcbd0f2f797a7c1c66d5e48d4b8e7b6e29556'
API_URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def file_exists(f_name):
    if os.path.exists(f_name) and os.path.isfile(f_name):
        return True
    return False


class YandexTranslator:
    def __init__(self, url, api_key, lang_file, lang='en-ru', enc='utf-8'):
        self.__url = url
        self.__params = {'key': api_key, 'lang': lang, }
        self.__lang_file = lang_file
        self.__enc = enc
        self.__foreign_content = ''
        self.__rus_content = ''
        self.__suffix = '_TO_RUS.'

    def __translate(self):
        if self.__foreign_content:
            self.__params['text'] = self.__foreign_content
            response = requests.get(self.__url, self.__params)

            text_dict = json.loads(response.text)
            self.__rus_content = ''.join(text_dict['text'])

    def __f_read(self):
        if self.__lang_file:
            with open(self.__lang_file, encoding=self.__enc) as f:
                self.__foreign_content = f.read()
        else:
            raise FileNotFoundError('Файл с текстом не найден!!')

    def __f_write(self):
        if self.__rus_content:
            _name = os.path.split(self.__lang_file)[1].split('.')[0]
            _ext = os.path.split(self.__lang_file)[1].split('.')[1]
            new_f_name = _name + self.__suffix + _ext

            with open(new_f_name, 'w', encoding=self.__enc) as f:
                f.write(self.__rus_content)

    def translate(self):
        self.__f_read()
        self.__translate()
        self.__f_write()


def user_choice(user_file):

    if file_exists(user_file):
        lang = ''
        while True:
            lang_choice = input(""" 
Переводим на русский:
текст на испанском языке  - 1
текст на немецком языке   - 2
текст на английском языке - 3 
Завершение работы         - q
\nВыберите нужный вариант:""")
            if lang_choice == '1':
                lang = 'es-ru'
                break
            elif lang_choice == '2':
                lang = 'de-ru'
                break
            elif lang_choice == '3':
                lang = 'en-ru'
                break
            elif lang_choice.lower() == 'q':
                return
        return YandexTranslator(API_URL, API_KEY, user_file, lang=lang)


def translate(user_file):
    task = user_choice(user_file)
    task.translate()


if __name__ == '__main__':
    if len(sys.argv) == 2:
        translate(sys.argv[1])
    else:
        print("Укажите файл для перевода!")
