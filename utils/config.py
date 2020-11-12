# -*- coding: utf-8 -*-
import os
import yaml

from utils import constant
from utils.exception import ConfigurationItemError


class Config:
    def __init__(self, logger):
        self.logger = logger
        self.data = {}
        self.file_name = constant.CONFIG_FILE
        if os.path.isfile(self.file_name):
            with open(self.file_name, encoding='utf-8') as f:
                self.data = yaml.safe_load(f)
        self.check_config()
        self.check_url()

    def touch(self, key, default):
        if key not in self.data.keys():
            self.data[key] = default
            with open(self.file_name, 'a', encoding='utf-8') as f:
                yaml.dump({key: default}, f)
            self.logger.warning(f'Option "{key}" missing, '
                                f'use default value "{default}"')

    def check_config(self):
        self.touch('lang', 'zh_cn')
        self.touch('api_url', 'http://127.0.0.1:5700')
        self.touch('receive_url', 'http://127.0.0.1:5701/post')
        self.touch('debug_mode', False)

    def check_url(self):
        if not constant.URL_PATTERN.fullmatch(self.get('receive_url')):
            raise ConfigurationItemError('Error format of receive url')
        if not constant.URL_PATTERN.fullmatch(self.get('api_url')):
            raise ConfigurationItemError('Error format of api url')

    def get(self, item, default=None):
        return self.data.get(item, default)

    def __getitem__(self, item):
        return self.get(item)
