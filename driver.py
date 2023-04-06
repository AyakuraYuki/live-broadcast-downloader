# -*- coding: utf-8 -*-

import os
import random
from time import sleep

from alive_progress import alive_it
from selenium.webdriver import Chrome, Edge
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from model import TSLink
from proxy import ProxyOption
from util import parse_m3u8


def _build_prefs(download_dir: str):
    prefs = {
        "download.default_directory": download_dir,
        "download.directory_upgrade": True,
        "download.prompt_for_download": False,
        "download.extensions_to_open": ""
    }
    return prefs


def chrome(download_dir: str, proxy: ProxyOption):
    chrome_options = ChromeOptions()
    prefs = _build_prefs(download_dir)
    chrome_options.add_experimental_option("prefs", prefs)
    if proxy:
        chrome_options.add_argument(f"--proxy-server={proxy.get_proxy_server()}")
    chrome_options.add_argument("--headless")
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
    return Chrome(service=chrome_service, options=chrome_options)


def edge(download_dir: str, proxy: ProxyOption):
    edge_options = EdgeOptions()
    prefs = _build_prefs(download_dir)
    edge_options.add_experimental_option("prefs", prefs)
    if proxy:
        edge_options.add_argument(f"--proxy-server={proxy.get_proxy_server()}")
    edge_options.add_argument("--headless")
    edge_service = EdgeService(executable_path=EdgeChromiumDriverManager().install())
    return Edge(service=edge_service, options=edge_options)


def download_ts(driver, ts_link: TSLink, download_dir: str, ts_host_url: str):
    path = os.path.join(download_dir, ts_link.filename)
    if ts_host_url is not None and ts_host_url != "" and not ts_host_url.endswith('/'):
        ts_host_url = f'{ts_host_url}/'
    if os.path.exists(path):
        print(f'[message] skip exist file: {path}')
        return False
    driver.get(f'{ts_host_url}{ts_link.link}')
    return True


def process(driver, dest_dir: str, m3u8_url: str, host_url: str, min_wait: int = 20, max_wait: int = 40):
    m3u8_filename = os.path.join(dest_dir, m3u8_url[m3u8_url.rindex('/') + 1:])
    if '?' in m3u8_filename:
        m3u8_filename = m3u8_filename[:m3u8_filename.index('?')]
    ts_paths = parse_m3u8(m3u8_filename)
    downloading = 0
    for path in alive_it(ts_paths, bar='fish', spinner='stars', length=60):
        if download_ts(driver, path, dest_dir, host_url):
            downloading += 1
        if downloading == 50:
            wait = random.randint(min_wait, max_wait)
            print(f'[message] cool down in {wait} seconds')
            sleep(wait)
            downloading = 0
