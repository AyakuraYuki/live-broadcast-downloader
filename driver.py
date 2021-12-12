# -*- coding: utf-8 -*-

import os
import random
from time import sleep

from alive_progress import alive_it
from selenium import webdriver

from proxy import ProxyOption
from util import parse_m3u8


def chrome(download_dir: str, proxy: ProxyOption):
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_settings.popups': 0,
        'download.default_directory': os.path.abspath(download_dir)
    }
    options.add_experimental_option('prefs', prefs)
    if proxy:
        options.add_argument(f'--proxy-server={proxy.get_proxy_server()}')
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path='chromedriver', options=options)
    return driver


def download_ts(driver: webdriver.Chrome, ts_path: str, download_dir: str, ts_host_url: str):
    path = os.path.join(download_dir, ts_path)
    if os.path.exists(path):
        print(f'[message] skip exist file: {path}')
        return False
    driver.get(f'{ts_host_url}{ts_path}')
    return True


def process(driver: webdriver.Chrome,
            download_dir: str, m3u8_url: str, ts_host_url: str,
            min_wait: int = 20, max_wait: int = 40):
    ts_paths = parse_m3u8(os.path.join(download_dir, m3u8_url[m3u8_url.rindex('/') + 1:]))
    downloading = 0
    for path in alive_it(ts_paths, bar='fish', spinner='stars', length=60):
        if download_ts(driver, path, download_dir, ts_host_url):
            downloading += 1
        if downloading == 20:
            wait = random.randint(min_wait, max_wait)
            print(f'[message] cool down in {wait} seconds')
            sleep(wait)
            downloading = 0
