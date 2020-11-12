# -*- coding: utf-8 -*-
import requests


class Bot:
    def __init__(self, server):
        self.logger = server.logger
        self.url = server.config['api_url']

    def request(self, path: str, data: dict = None):
        requests.post(f'{self.url}/{path}', json=data)

    def send_private_msg(self, user_id: int, message: str,
                         auto_escape: bool = False):
        data = {
            'user_id': user_id,
            'message': message,
            'auto_escape': auto_escape
        }
        return self.request('send_private_msg', data)

    def send_group_msg(self, group_id: int, message: str,
                       auto_escape: bool = False):
        data = {
            'group_id': group_id,
            'message': message,
            'auto_escape': auto_escape
        }
        return self.request('send_group_msg', data)

    def send_msg(self, message: str, message_type: str = None,
                 user_id: int = None, group_id: int = None,
                 auto_escape: bool = False):
        data = {
            'message_type': message_type,
            'user_id': user_id,
            'group_id': group_id,
            'message': message,
            'auto_escape': auto_escape
        }
        return self.request('send_msg', data)

    def delete_msg(self, message_id: int):
        data = {
            'message_id': message_id
        }
        return self.request('delete_msg', data)

    def get_msg(self, message_id: int):
        data = {
            'message_id': message_id
        }
        return self.request('get_msg', data)

    def get_forward_msg(self, id: str):
        data = {
            'id': id
        }
        return self.request('get_forward_msg', data)

    def send_like(self, user_id: int, times: int):
        data = {
            'user_id': user_id,
            'times': times
        }
        return self.request('send_like', data)

    def set_group_kick(self, group_id: int, user_id: int,
                       reject_add_request: bool):
        data = {
            'group_id': group_id,
            'user_id': user_id,
            'reject_add_request': reject_add_request
        }
        return self.request('set_group_kick', data)

    def set_group_ban(self, group_id: int, user_id: int,
                      duration: int = 30 * 60):
        data = {
            'group_id': group_id,
            'user_id': user_id,
            'duration': duration
        }
        return self.request('set_group_ban', data)

    def set_group_anonymous_ban(self, group_id: int, anonymous: dict = None,
                                anonymous_flag: str = None,
                                duration: int = 30 * 60):
        data = {
            'group_id': group_id,
            'anonymous_flag': anonymous_flag,
            'duration': duration
        }
        if anonymous is not None:
            data['anonymous'] = anonymous
        return self.request('set_group_anonymous_ban', data)

    def set_group_whole_ban(self, group_id: int, enable: bool):
        data = {
            'group_id': group_id,
            'enable': enable
        }
        return self.request('set_group_whole_ban', data)

    def set_group_admin(self, group_id: int, user_id: int, enable: bool):
        data = {
            'group_id': group_id,
            'user_id': user_id,
            'enable': enable
        }
        return self.request('set_group_admin', data)

    def set_group_anonymous(self, group_id: int, enable: bool):
        data = {
            'group_id': group_id,
            'enable': enable
        }
        return self.request('set_group_anonymous', data)

    def set_group_card(self, group_id: int, user_id: int, card: str = ''):
        data = {
            'group_id': group_id,
            'user_id': user_id,
            'card': card
        }
        return self.request('set_group_card', data)

    def set_group_name(self, group_id: int, group_name: str):
        data = {
            'group_id': group_id,
            'group_name': group_name
        }
        return self.request('set_group_name', data)

    def set_group_special_title(self, group_id: int, user_id: int,
                                special_title: str = '', duration: int = -1):
        data = {
            'group_id': group_id,
            'user_id': user_id,
            'special_title': special_title,
            'duration': duration
        }
        return self.request('set_group_special_title', data)

    def set_friend_add_request(self, flag: str, approve: bool = True,
                               remark: str = ''):
        data = {
            'flag': flag,
            'approve': approve,
            'remark': remark
        }
        return self.request('set_friend_add_request', data)

    def set_group_add_request(self, flag: str, sub_type: str,
                              approve: bool = True, reason: str = ''):
        data = {
            'flag': flag,
            'sub_type ': sub_type,
            'approve': approve,
            'reason': reason
        }
        return self.request('set_group_add_request', data)

    def get_login_info(self):
        return self.request('get_login_info')

    def get_stranger_info(self, user_id: int, no_cache: bool = False):
        data = {
            'user_id': user_id,
            'no_cache ': no_cache
        }
        return self.request('get_stranger_info', data)

    def get_friend_list(self):
        return self.request('get_friend_list')

    def get_group_info(self, group_id: int, no_cache: bool = False):
        data = {
            'group_id': group_id,
            'no_cache ': no_cache
        }
        return self.request('get_group_info', data)

    def get_group_list(self):
        return self.request('get_group_list')

    def get_group_member_info(self, group_id: int, user_id: int,
                              no_cache: bool = False):
        data = {
            'group_id': group_id,
            'user_id': user_id,
            'no_cache ': no_cache
        }
        return self.request('get_group_member_info', data)

    def get_group_member_list(self, group_id: int):
        data = {
            'group_id': group_id
        }
        return self.request('get_group_member_list', data)

    def get_group_honor_info(self, group_id: int, type_: str):
        data = {
            'group_id': group_id,
            'type': type_
        }
        return self.request('get_group_honor_info', data)

    def get_cookies(self, domain: str):
        data = {
            'domain': domain
        }
        return self.request('get_cookies', data)

    def get_csrf_token(self):
        return self.request('get_csrf_token')

    def get_credentials(self, domain: str):
        data = {
            'domain': domain
        }
        return self.request('get_credentials', data)

    def get_record(self, file: str, out_format: str):
        data = {
            'file': file,
            'out_format': out_format
        }
        return self.request('get_record', data)

    def get_image(self, file: str):
        data = {
            'file': file
        }
        return self.request('get_image', data)

    def can_send_image(self):
        return self.request('can_send_image')

    def can_send_record(self):
        return self.request('can_send_record')

    def get_status(self):
        return self.request('get_status')

    def get_version_info(self):
        return self.request('get_version_info')

    def set_restart(self, delay: int = 0):
        data = {
            'delay': delay
        }
        return self.request('get_version_info', data)

    def clean_cache(self):
        return self.request('clean_cache')
