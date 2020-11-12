# -*- coding: utf-8 -*-
import requests
import time

from utils.constant import URL_PATTERN
from utils.receive_server_thread import ReceiveServerThread


class ReceiveServer:
    def __init__(self, server):
        self.server = server
        self.running_flag = False
        self.server_thread = None

    def is_server_running(self) -> bool:
        """Return True if receive server thread is running else False"""
        return self.running_flag is True

    def start(self) -> bool:
        """Start receive server thread"""
        if self.is_server_running():
            self.server.logger.warning(self.server.t('server.start.twice'))
            return False
        self.server.logger.debug('ReceiveServer thread starting')
        self.server.logger.info(self.server.t('server.start.starting'))
        self.server_thread = ReceiveServerThread(self.server)
        self.server_thread.start()
        time.sleep(0.1)
        self.server.plugin_manager.call(
            'on_server_start', (self.server.server_interface,))
        self.running_flag = True
        return True

    def stop(self) -> bool:
        """Stop receive server thread"""
        if not self.is_server_running():
            self.server.logger.warning(self.server.t('server.stop.twice'))
            return False
        self.server.logger.debug('ReceiveServer thread stopping')
        self.server.logger.info(self.server.t('server.stop.stopping'))
        _, host, port, path = URL_PATTERN.search(
            self.server.config['receive_url']).groups()
        requests.post(f'http{"" if _ is None else _}://{host}:{port}/stop',
                      json={'stop': True})
        self.server.plugin_manager.call(
            'on_server_stop', (self.server.server_interface,))
        self.running_flag = False
        return True
