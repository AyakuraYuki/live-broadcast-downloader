# -*- coding: utf-8 -*-

from time import sleep

from driver import chrome, process
from proxy import ProxyOption
from util import cleanup_download_temporary_cache, validate, create_folder

tasks = [
    # Task(prefix='https://host.example.net/path-to-m3u8_ts_key/', download_dir='<download_place>'),
]


def task(prefix, download_dir):
    key_url = f'{prefix}aes128.key'
    m3u8_url = f'{prefix}index_6m.m3u8'
    driver = chrome(download_dir=download_dir, proxy=ProxyOption())
    driver.get(key_url)
    driver.get(m3u8_url)
    process(driver=driver, dest_dir=download_dir, m3u8_url=m3u8_url, host_url=prefix, min_wait=3, max_wait=5)


def main():
    if len(tasks) == 0:
        exit(1)
    for t in tasks:
        create_folder(t.download_dir)
        while True:
            try:
                cleanup_download_temporary_cache(t.download_dir)
                print(f'task start: {t.prefix}')
                task(t.prefix, t.download_dir)
            except Exception as e:
                print('Exception occurred, restarting...')
                print(f'Error: {e}')
                cleanup_download_temporary_cache(t.download_dir)
                sleep(10)
            else:
                break
        validate(t.download_dir)
        print('Done!')
        # then jump into the download folder and fire this cmd:
        #     ffmpeg -allowed_extensions ALL -i <m3u8_filename> -c copy output.mp4


if __name__ == '__main__':
    main()
