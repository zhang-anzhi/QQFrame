# -*- coding: utf-8 -*-
class Anonymous:
    """Class to describe a anonymous"""

    def __init__(self, data):
        if data is None:
            return
        self.data = data
        self.id = self.get('id')
        self.name = self.get('name')
        self.flag = self.get('flag')

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item):
        return self.data.get(item, None)
