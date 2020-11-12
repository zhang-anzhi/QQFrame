# -*- coding: utf-8 -*-
from utils.parser.base_parser import BaseParser
from utils.parser.file import File


class NoticeParser(BaseParser):
    def __init__(self, data):
        super().__init__(data)
        self.notice_type = self.get('notice_type')

        # group_upload
        self.group_id = self.get('group_id')
        self.user_id = self.get('user_id')
        self.file = File(self.get('file'))

        # group_admin
        self.sub_type = self.get('sub_type')

        # group_decrease
        self.operator_id = self.get('operator_id')

        # group_increase

        # group_ban
        self.duration = self.get('duration')

        # friend_add

        # group_recall
        self.message_id = self.get('message_id')

        # friend_recall

        # notify
        self.target_id = self.get('target_id')

        # lucky_king

        # honor
        self.honor_type = self.get('honor_type')
