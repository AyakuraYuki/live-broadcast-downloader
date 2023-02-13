# -*- coding: utf-8 -*-

import json
import re


class TSLink:
    def __init__(self, link: str):
        """
        *.ts link parser

        :param link: *.ts file link
        """
        self.link = link
        self.base_url = link
        self.query_string = ''
        self.filename = ''
        self.__parse_link_attributes__()
        self.__parse_filename__()

    def __parse_link_attributes__(self):
        if re.match('^http[s]?://(.*)', self.base_url):
            if '?' in self.link:
                self.base_url = self.link[:self.link.index('?')]
                self.query_string = self.link[self.link.index('?') + 1:]
            else:
                self.base_url = self.link
                self.query_string = ''

    def __parse_filename__(self):
        if re.match('^http[s]?://(.*)', self.base_url):
            self.filename = self.base_url[self.base_url.rindex('/') + 1:]
        else:
            self.filename = self.base_url

    def __str__(self):
        return json.dumps(self.__dict__)


class M3U8Spec(object):
    def __init__(self, m3u8_filename, key_name):
        """
        m3u8 spec

        :param m3u8_filename: m3u8 filename
        :param key_name: (optional) m3u8 decrypt key filename
        """
        self.m3u8_filename = m3u8_filename
        self.key_name = key_name if key_name else ''


class Task(object):
    def __init__(self, prefix, download_dir, view_url='', m3u8_filename='', key_name='', m3u8_spec: M3U8Spec = None):
        """
        init Task

        :param view_url: (eplus only) the url (or link) of stream page
        :param prefix: the url (or link) of ts file without filename, should be ended by slash
                       e.g. https://view.example.com/stream/xxxxxx-xxxxxx-xxxxxx-xxxxxx/index1_0001.ts
                        --> https://view.example.com/stream/xxxxxx-xxxxxx-xxxxxx-xxxxxx/
        :param m3u8_filename: m3u8 filename
        :param key_name: (optional) m3u8 decrypt key filename
        :param download_dir: local storage absolute path
        :param m3u8_spec: m3u8 spec object, which presents `m3u8_filename` and `key_name`
        """

        if not download_dir:
            raise ValueError('missing download_dir')

        self.view_url: str = view_url
        self.prefix: str = prefix
        self.download_dir: str = download_dir

        if m3u8_spec is not None:
            self.m3u8_filename: str = m3u8_spec.m3u8_filename
            self.key_name: str = m3u8_spec.key_name
        else:
            self.m3u8_filename: str = m3u8_filename
            self.key_name: str = key_name

    def __str__(self):
        return json.dumps(self.__dict__)

    def key_url(self):
        if self.key_name:
            return f'{self.prefix}{"" if self.prefix.endswith("/") else "/"}{self.key_name}'
        return ''

    def m3u8_url(self):
        return f'{self.prefix}{"" if self.prefix.endswith("/") else "/"}{self.m3u8_filename}'
