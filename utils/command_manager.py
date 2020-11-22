# -*- coding: utf-8 -*-
import os
import re
import threading

from utils import constant
from utils import functions


class CommandManager:
    def __init__(self, server):
        self.server = server
        self.logger = server.logger
        self.t = server.t

    def show_status(self):
        self.logger.info(
            self.t('status.version', constant.NAME, constant.VERSION))
        if self.server.receive_server.is_server_running():
            status = self.t('status.receive_server_status.running')
        else:
            status = self.t('status.receive_server_status.stopped')
        self.logger.info(self.t('status.receive_server_status', status))
        self.logger.info(self.t('status.thread_count',
                                threading.active_count()))
        self.logger.info(self.t('status.thread_list'))
        for i in threading.enumerate():
            self.logger.info(f'  - {i.name}')

    def list_plugins(self):
        plugin_list = self.server.plugin_manager.get_loaded_plugin_name_dict()
        self.send_message('plugin_manager.plugin_loaded', len(plugin_list))
        for i in plugin_list.values():
            self.logger.info(f'  - {i.name}')

    def plugin_info(self, plugin_name):
        if plugin_name in self.server.plugin_manager.get_loaded_plugin_name_list():
            plugin = self.server.plugin_manager.get_plugin(plugin_name)
            authors = [] if plugin.authors == [] else ', '.join(plugin.authors)
            self.send_message(
                'plugin_manager.plugin_info',
                plugin.name,
                plugin.version,
                authors,
                functions.get_file_size(plugin.file_path),
                functions.get_file_modify_time(plugin.file_path)
            )
        else:
            self.logger.info(
                self.t('plugin_manager.no_plugin_exist', plugin_name))

    def reload_plugin(self, plugin_name):
        if plugin_name in self.server.plugin_manager.get_loaded_plugin_name_list():
            self.server.plugin_manager.load_plugin(plugin_name)
        else:
            self.logger.info(
                self.t('plugin_manager.no_plugin_exist', plugin_name))

    def send_message(self, text, *args):
        for i in self.t(text, *args).splitlines():
            self.logger.info(i)

    def process_command(self, command: str):
        args = re.split(r'\s+', command.rstrip())
        self.logger.debug(f'Console input split text: "{args}"')

        # help
        if args[0] == 'help':
            self.send_message('message.help_message.all')

        # stop
        elif args[0] == 'stop':
            self.server.stop()

        # status
        elif args[0] == 'status':
            self.show_status()

        # reload
        elif len(args) >= 1 and args[0] == 'reload':
            if len(args) == 1:
                self.send_message('message.help_message.reload')
            elif args[1] == 'all':
                self.server.load_config()
                self.server.receive_server.stop()
                self.server.receive_server.start()
            elif args[1] == 'server':
                self.server.receive_server.stop()
                self.server.receive_server.start()
            elif args[1] == 'config':
                self.server.load_config()
            else:
                self.send_message('message.help_message.reload')

        # server
        elif len(args) >= 1 and args[0] == 'server':
            if len(args) == 1:
                self.send_message('message.help_message.server')
            elif args[1] == 'start':
                self.server.receive_server.start()
            elif args[1] == 'stop':
                self.server.receive_server.stop()
            else:
                self.send_message('message.help_message.server')

        # plugin
        elif len(args) >= 1 and args[0] == 'plugin':
            if len(args) == 1:
                self.send_message('message.help_message.plugin')
            elif args[1] == 'list':
                self.list_plugins()
            elif args[1] == 'info':
                plugin_name, = re.search(r'plugin\s+info\s+(.*)',
                                         command).groups()
                self.plugin_info(plugin_name)
            elif len(args) >= 3 and args[1] == 'reload':
                plugin_name, = re.search(r'plugin\s+reload\s+(.*)',
                                         command).groups()
                self.reload_plugin(plugin_name)
            else:
                self.send_message('message.help_message.plugin')

        self.server.plugin_manager.call(
            'on_command', (self.server.server_interface, command))
