# -*- coding: utf-8 -*-
from threading import Thread


class PluginThread(Thread):
    def __init__(self, server, target, args, plugin_name, func_name):
        self.server = server
        self.plugin_name = plugin_name
        self.func_name = func_name
        super().__init__(
            target=target,
            args=args,
            name=f'{func_name}@{self.plugin_name}'
        )
        self.setDaemon(True)

    def run(self):
        try:
            super().run()
        except:
            self.server.logger.exception(
                f'Error calling {self.func_name} in plugin {self.plugin_name}')
