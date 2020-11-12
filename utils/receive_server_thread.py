# -*- coding: utf-8 -*-
import json
import logging
from threading import Thread
from flask import Flask, request

from utils.constant import URL_PATTERN
from utils.parser.message_parser import MessageParser
from utils.parser.notice_parser import NoticeParser


class ReceiveServerThread(Thread):
    def __init__(self, server):
        super().__init__(name='ReceiveServer')
        self.server = server

    def run(self):
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        app = Flask(__name__)
        receive_url = URL_PATTERN.search(
            self.server.config['receive_url']).groups()
        _, host, port, path = receive_url

        @app.route(path, methods=['POST'])
        def receive():
            data = json.loads(request.get_data())
            # self.server.logger.debug('Receive post data:{}'.format(
            #     json.dumps(data, indent=4, ensure_ascii=False)))
            if data['post_type'] == 'message':
                self.server.plugin_manager.call(
                    'on_message',
                    (self.server.server_interface, MessageParser(data))
                )
            elif data['post_type'] == 'message':
                self.server.plugin_manager.call(
                    'on_notice',
                    (self.server.server_interface, NoticeParser(data))
                )
            return ''

        @app.route('/stop', methods=['POST'])
        def stop():
            try:
                data = json.loads(request.get_data())
            except json.decoder.JSONDecodeError:
                return 'Form data format error'
            else:
                if data.get('stop', False) is True:
                    func = request.environ.get('werkzeug.server.shutdown')
                    if func is None:
                        raise RuntimeError
                    func()
                    return {'operation': 'StopServer', 'code': 0}
                else:
                    return {'operation': 'StopServer', 'code': -1}

        app.run(port=port, host=host, threaded=False)
