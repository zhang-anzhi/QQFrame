# -*- coding: utf-8 -*-
import logging
from colorlog import ColoredFormatter

from utils import constant
from utils import functions


class Logger:
    console_fmt = ColoredFormatter(
        '[%(asctime)s] [%(threadName)s/%(log_color)s%(levelname)s%(reset)s]: '
        '%(message_log_color)s%(message)s%(reset)s',
        log_colors={
            'DEBUG': 'blue',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        },
        secondary_log_colors={
            'message': {
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'bold_red'
            }
        },
        datefmt='%H:%M:%S'
    )
    file_fmt = logging.Formatter(
        '[%(asctime)s] [%(threadName)s/%(levelname)s]: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    def __init__(self):
        functions.touch_folder(constant.LOG_FOLDER)
        functions.backup_log(constant.LOGGING_FILE)
        self.logger = logging.getLogger(constant.NAME)

        ch = logging.StreamHandler()
        ch.setFormatter(self.console_fmt)
        self.logger.addHandler(ch)
        fh = logging.FileHandler(constant.LOGGING_FILE, encoding='utf-8')
        fh.setFormatter(self.file_fmt)
        self.logger.addHandler(fh)

        self.set_level()
        self.debug = self.logger.debug
        self.info = self.logger.info
        self.warning = self.logger.warning
        self.error = self.logger.error
        self.critical = self.logger.critical
        self.exception = self.logger.exception

    def set_level(self, debug=False):
        if debug:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
