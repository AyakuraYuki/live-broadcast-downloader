# -*- coding: utf-8 -*-

import json
import re


class TSLink:
    def __init__(self, link: str):
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


class Task:
    def __init__(self, prefix, download_dir):
        self.prefix = prefix
        self.download_dir = download_dir

    def __str__(self):
        return json.dumps(self.__dict__)
