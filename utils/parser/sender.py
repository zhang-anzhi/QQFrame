# -*- coding: utf-8 -*-
class Sender:
    """Class to describe a sender"""
    def __init__(self, data):
        self.data = data
        self.user_id = self.get('user_id')
        self.nickname = self.get('nickname')
        self.sex = self.get('sex')
        self.age = self.get('age')
        self.card = self.get('card')
        self.area = self.get('area')
        self.level = self.get('level')
        self.role = self.get('role')
        self.title = self.get('title')

    def __getitem__(self, item):
        return self.get(item)

    def get(self, item):
        return self.data.get(item, None)
