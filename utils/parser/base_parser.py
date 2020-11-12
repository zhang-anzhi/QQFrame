# -*- coding: utf-8 -*-


class BaseParser:
    def __init__(self, data: dict):
        self.data = data
        self.time = self.get('time')
        self.self_id = self.get('self_id')
        self.post_type = self.get('post_type')

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item):
        return self.data.get(item, None)
