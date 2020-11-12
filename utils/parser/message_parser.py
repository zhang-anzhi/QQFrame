# -*- coding: utf-8 -*-
import re

from utils.parser.base_parser import BaseParser
from utils.parser.sender import Sender
from utils.parser.anonymous import Anonymous


class MessageParser(BaseParser):
    def __init__(self, data: dict):
        super().__init__(data)
        self.message_type = self.get('message_type')
        self.sub_type = self.get('sub_type')
        self.message_id = self.get('message_id')
        self.user_id = self.get('user_id')
        self.message = self.get('message')
        self.raw_message = self.get('raw_message')
        self.content = self.content_parse()
        self.font = self.get('font')
        self.sender = Sender(self.get('sender'))

        # Group message extra
        self.group_id = self.get('group_id')
        self.anonymous = Anonymous(self.get('anonymous'))

    def content_parse(self):
        content = self.raw_message
        content = re.sub(r'\[CQ:image,file=.*?\]', '[图片]', content)
        content = re.sub(r'\[CQ:share,file=.*?\]', '[链接]', content)
        content = re.sub(r'\[CQ:face,id=.*?\]', '[表情]', content)
        content = re.sub(r'\[CQ:record,file=.*?\]', '[语音]', content)
        content = content.replace('CQ:at,qq=', '@')
        return content
