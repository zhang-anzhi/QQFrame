# -*- coding: utf-8 -*-
import os
import sys

from utils import functions
from utils import constant
from utils.plugin_thread import PluginThread
from utils.exception import PluginInfoError


class Plugin:
    def __init__(self, server, file_path):
        self.server = server
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)

        self.plugin_info = None
        self.name = None
        self.version = None
        self.authors = None

        self.module = None
        self.old_module = None
        self.loaded_modules = None

    def call(self, func_name, args=()):
        if hasattr(self.module, func_name):
            target = self.module.__dict__[func_name]
            if callable(target):
                thread = PluginThread(
                    self.server, target, args, self.name, func_name)
                thread.start()
                return thread
        return False

    def load(self):
        self.old_module = self.module
        previous_modules = sys.modules.copy()
        self.module = functions.load_source(self.file_path)
        self.loaded_modules = [module for module in sys.modules.copy() if
                               module not in previous_modules]

        # Plugin info dict
        if hasattr(self.module, constant.PLUGIN_INFO):
            self.plugin_info = self.module.__dict__[constant.PLUGIN_INFO]
            if not isinstance(self.plugin_info, dict):
                self.unload_modules()
                raise PluginInfoError(
                    f'Can\'t find plugin info of {self.file_name}')
            else:
                for i in constant.PLUGIN_INFO_NEEDED:
                    if i not in self.plugin_info.keys():
                        self.unload_modules()
                        raise PluginInfoError(
                            f'Missing plugin info "{i}" of {self.file_name}')
                self.name = self.plugin_info['name']
                self.version = self.plugin_info['version']
                self.authors = self.plugin_info.get('authors', [])
                self.server.logger.debug(f'Plugin {self.name} loaded')
                self.call('on_load',
                          (self.server.server_interface, self.old_module))
        else:
            self.unload_modules()
            raise PluginInfoError(
                f'Can\'t find plugin info of {self.file_name}')

    def unload(self):
        self.server.logger.debug(f'Plugin {self.name} unloaded')
        self.call('on_unload', (self.server.server_interface,))
        self.unload_modules()

    def unload_modules(self):
        for module in self.loaded_modules:
            try:
                del sys.modules[module]
            except KeyError:
                self.server.logger.critical(
                    f'Module {module} not found '
                    f'when unloading plugin {self.name}')
            else:
                self.server.logger.debug(
                    f'Removed module {module} '
                    f'when unloading plugin {self.name}')
            self.loaded_modules = []
