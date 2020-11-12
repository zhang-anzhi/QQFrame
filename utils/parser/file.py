# -*- coding: utf-8 -*-
class File:
    """Class to describe a file"""

    def __init__(self, data):
        self.data = data
        self.id = self.get('id')
        self.name = self.get('name')
        self.size = self.get('size')
        self.busid = self.get('busid')

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item):
        return self.data.get(item, None)
