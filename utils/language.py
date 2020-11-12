# -*- coding: utf-8 -*-
import os
import yaml

from utils import constant
from utils import functions


class Language:
    def __init__(self, server):
        self.server = server
        self.language = None
        self.data = {}
        functions.touch_folder(constant.LANG_FOLDER)
        for i in os.listdir(constant.LANG_FOLDER):
            lang = i.replace(constant.LANG_FILE_SUFFIX, '')
            file_name = os.path.join(constant.LANG_FOLDER, i)
            with open(file_name, encoding='utf-8') as f:
                self.data[lang] = yaml.safe_load(f)

    def set_language(self, language):
        self.language = language

    def translate(self, text, *args, language=None):
        if language is None:
            language = self.language
        try:
            result = self.data[language].get(text, None).strip()
            return result.format(*args)
        except:
            self.server.logger.error(
                f'Error translate text "{text}" to language {language}')
