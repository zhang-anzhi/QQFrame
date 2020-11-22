# -*- coding: utf-8 -*-
import os

from utils import constant
from utils import functions as func
from utils.plugin import Plugin


class PluginManager:
    def __init__(self, server):
        self.server = server
        self.logger = server.logger
        self.plugin_folder = constant.PLUGIN_FOLDER
        self.plugins = []

        # Touch plugin and config folder
        func.touch_folder(self.plugin_folder)
        func.touch_folder(constant.PLUGIN_CONFIG_FOLDER)

    def get_plugin_file_list(self):
        """Get .py file list in plugin folder"""
        return func.list_file(self.plugin_folder,
                              constant.PLUGIN_FILE_SUFFIX)

    def get_loaded_plugin_name_dict(self):
        """Get a dict, which key is the plugin name; value is plugin instance"""
        return {plugin.name: plugin for plugin in self.plugins}

    def get_loaded_plugin_file_name_dict(self):
        """
        Get a dict,
        which key is the plugin file name; value is plugin instance
        """
        return {plugin.file_name: plugin for plugin in self.plugins}

    def get_loaded_plugin_name_list(self):
        """Get loaded plugin name list"""
        return list(self.get_loaded_plugin_name_dict().keys())

    def get_loaded_plugin_file_name_list(self):
        """Get loaded plugin file name list"""
        return list(self.get_loaded_plugin_file_name_dict().keys())

    def get_plugin(self, obj: Plugin or str) -> Plugin:
        """Get plugin object"""
        if isinstance(obj, Plugin):
            return obj
        elif isinstance(obj, str):
            plugin = self.get_loaded_plugin_file_name_dict().get(obj, None)
            if plugin is not None:
                return plugin
            else:
                return self.get_loaded_plugin_name_dict().get(obj, None)
        else:
            raise TypeError('The object to load needs to be a Plugin or a str')

    # -----------------------
    # Single plugin operation
    # -----------------------

    def load_plugin(self, file_name: str) -> bool:
        """Load or reload plugin with file name or plugin name"""
        file_name = os.path.basename(file_name)
        plugin = self.get_plugin(file_name)
        try:
            if isinstance(plugin, Plugin):
                plugin.unload()
            else:
                plugin = Plugin(self.server,
                                os.path.join(self.plugin_folder, file_name))
            plugin.load()
            if plugin not in self.plugins:
                self.plugins.append(plugin)
            self.logger.info(
                self.server.t('plugin_manager.load_plugin.success',
                              plugin.name))
            return True
        except:
            self.logger.exception(
                self.server.t('plugin_manager.load_plugin.fail',
                              plugin.file_name))
            if plugin in self.plugins:
                self.plugins.remove(plugin)
            return False

    # -------------------------
    # Multiple plugin operation
    # -------------------------

    def load_all_plugins(self):
        """Load all plugins in plugin folder"""
        self.logger.info(self.server.t('plugin_manager.loading'))
        for file_name in self.get_plugin_file_list():
            self.load_plugin(os.path.basename(file_name))
        self.logger.info(self.server.t('plugin_manager.plugin_loaded',
                                       len(self.get_loaded_plugin_name_list())))

    # ----------
    # Event call
    # ----------

    def call(self, func_name, args=()):
        """Call a event in all plugins"""
        for plugin in self.plugins:
            plugin.call(func_name, args)
