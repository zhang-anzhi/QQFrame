# -*- coding: utf-8 -*-
import os
import re

# basic information
VERSION = '0.1.0'
NAME = 'QQFrame'

# file
LOG_FOLDER = 'logs'
LOGGING_FILE = os.path.join(LOG_FOLDER, 'latest.log')
CONFIG_FILE = 'config.yml'
LANG_FOLDER = 'lang'
PLUGIN_FOLDER = 'plugins'
PLUGIN_CONFIG_FOLDER = 'config'
UPDATE_DOWNLOAD_FOLDER = f'{NAME}_update'

# pattern
URL_PATTERN = re.compile(r'http(s)?://'
                         r'(?P<host>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):'
                         r'(?P<port>\d{1,5})(?P<path>/.+)?')

# suffix
PLUGIN_FILE_SUFFIX = '.py'
DISABLED_PLUGIN_FILE_SUFFIX = '.disabled'
LANG_FILE_SUFFIX = '.yml'

# plugin info
PLUGIN_INFO = 'PLUGIN_INFO'
PLUGIN_INFO_NEEDED = ['name', 'version']
