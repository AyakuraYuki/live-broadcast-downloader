# -*- coding: utf-8 -*-

from enum import Enum


class ProxyType(Enum):
    SOCKS5 = 'socks5'
    SOCKS4 = 'socks4'
    HTTPS = 'https'
    HTTP = 'http'


class ProxyOption:
    def __init__(self, host: str = '127.0.0.1', port: int = 7890, proxy_type: ProxyType = ProxyType.SOCKS5):
        self.h = host
        self.p = port
        self.pt = proxy_type

    def get_proxy_server(self):
        return f'{self.pt.value}://{self.h}:{self.p}'
