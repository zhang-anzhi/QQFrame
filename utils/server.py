# -*- coding: utf-8 -*-
import time

from utils import functions as func
from utils.logger import Logger
from utils.config import Config
from utils.bot import Bot
from utils.language import Language
from utils.plugin_manager import PluginManager
from utils.server_interface import ServerInterface
from utils.command_manager import CommandManager
from utils.receive_server import ReceiveServer


class Server:
    def __init__(self):
        self.logger = Logger()
        self.config = None
        self.bot = None
        self.language = Language(self)
        self.plugin_manager = PluginManager(self)
        self.command_manager = CommandManager(self)
        self.server_interface = None

        self.console_input_thread = None
        self.receive_server = ReceiveServer(self)

        self.should_keep_looping = True  # loop keep flag

    def t(self, text, *args):
        return self.language.translate(text, *args)

    def load_config(self):
        self.config = Config(self.logger)

        # Language
        language = self.config['lang']
        self.language.set_language(language)
        self.logger.info(self.t('server.load_config.set_lang', language))

        # api_url and receive_url
        self.logger.info(self.t('server.load_config.set_api_url',
                                self.config['api_url']))
        self.logger.info(self.t('server.load_config.set_receive_url',
                                self.config['receive_url']))

        # Bot
        self.bot = Bot(self)

        # Debug mode
        if self.config['debug_mode'] is True:
            self.logger.set_level(debug=True)
            self.logger.info(self.t('server.load_config.debug_on'))
        else:
            self.logger.set_level(debug=False)
            self.logger.info(self.t('server.load_config.debug_off'))

    def start(self):
        # Load config
        self.load_config()

        # Load plugin
        self.server_interface = ServerInterface(self)
        self.plugin_manager.load_all_plugins()

        # Start Server
        self.receive_server.start()

        # Start Console
        self.logger.debug('Console thread starting')
        self.console_input_thread = func.start_thread(self.console_input,
                                                      name='Console')

        # Main loop
        self.loop()

    def stop(self):
        """Stop and exit"""
        # Receive server stop
        if self.receive_server.is_server_running():
            self.receive_server.stop()
        # Main loop stop
        self.should_keep_looping = False
        self.logger.info(self.t('bye'))

    def loop(self):
        """Main loop to keep main thread alive"""
        while self.should_keep_looping:
            try:
                time.sleep(0.01)
            except KeyboardInterrupt:
                break

    def console_input(self):
        """Console input thread"""
        while True:
            try:
                self.command_manager.process_command(input())
            except (KeyboardInterrupt, EOFError, SystemExit, IOError):
                self.stop()
                break
            except:
                self.logger.exception(self.t('server.console_input.error'))
