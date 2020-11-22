# -*- coding: utf-8 -*-
import time

from utils.plugin import Plugin
from utils.parser.message_parser import MessageParser


def log(func):
    def wrap(self, *args, **kwargs):
        self.logger.debug(
            f'Plugin called {func.__name__}(), args amount: {len(args)}')
        for arg in args:
            self.logger.debug(f'  - type: {type(arg).__name__}, content: {arg}')
        return func(self, *args, **kwargs)

    return wrap


class ServerInterface:
    """API for plugin"""

    def __init__(self, server):
        from utils.server import Server
        from utils.bot import Bot
        self.__server: Server = server
        self.logger = server.logger
        self.bot: Bot = self.__server.bot

    # --------------
    # System control
    # --------------

    @log
    def reload_config(self):
        """Reload config"""
        self.__server.load_config()

    @log
    def exit(self):
        """Exit the QQFrame"""
        self.__server.stop()

    # -------
    # Message
    # -------

    @log
    def reply(self, info: MessageParser, message: str):
        """Automatic reply to source"""
        if info.message_type == 'private':
            return self.__server.bot.send_private_msg(info.user_id, message)
        elif info.message_type == 'group':
            return self.__server.bot.send_group_msg(info.group_id, message)

    # --------------
    # Receive Server
    # --------------

    @log
    def is_server_running(self) -> bool:
        """Return True if the receive server is running else False"""
        return self.__server.receive_server.is_server_running()

    @log
    def start(self):
        """Start the receive server"""
        self.__server.receive_server.start()

    @log
    def stop(self):
        """Stop the receive server"""
        self.__server.receive_server.stop()
        while self.__server.receive_server.is_server_running():
            time.sleep(0.01)

    @log
    def restart(self):
        """Restart the receive server"""
        self.stop()
        self.start()

    # ------
    # Plugin
    # ------

    @log
    def get_plugin_list(self) -> list:
        """
        Return a str list containing all loaded plugin name
        Like ["pluginA", "pluginB"]
        :return: list[str]
        """
        return self.__server.plugin_manager.get_loaded_plugin_name_list()

    @log
    def get_plugin_info(self, plugin_name: str) -> dict:
        """
        Get the plugin info dict

        :param plugin_name: Plugin name
        :return: Plugin info dict
        """
        if plugin_name in self.server.plugin_manager.get_loaded_plugin_name_list():
            plugin = self.server.plugin_manager.get_plugin(plugin_name)
            return plugin.plugin_info

    @log
    def reload_plugin(self, plugin_name: str) -> bool:
        """
        Reload the plugin

        :param plugin_name: Plugin name
        :return: Return True if Load succeeded without exception else False
        """
        if plugin_name in self.server.plugin_manager.get_loaded_plugin_name_list():
            self.server.plugin_manager.load_plugin(plugin_name)
            return True
        else:
            return False

    @log
    def get_plugin_instance(self, plugin_name: str) -> Plugin:
        """
        Return the current loaded plugin instance.
        Plugin instance get from this method is same as QQFrame used.

        :param plugin_name: The name of the plugin not file name..
        :return: A current loaded plugin instance.
        Return None if plugin not found.
        """
        plugin = self.__server.plugin_manager.get_plugin(plugin_name)
        if plugin is not None:
            plugin = plugin.module
        return plugin

    @log
    def call_event(self, plugin_name: str, func_name: str,
                   args: tuple = ()) -> bool:
        """
        Call a function with new thread in other loaded plugin
        :param plugin_name: Loaded plugin name
        :param func_name: Function name in the plugin
        :param args: Arguments which function need
        :return: bool Call success(plugin loaded and created new thread)
        """
        plugin = self.__server.plugin_manager.get_plugin(plugin_name)
        if plugin is not None:
            if plugin.call(func_name, args):
                return True
        return False
