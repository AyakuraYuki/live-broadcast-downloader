# -*- coding: utf-8 -*-

from time import sleep

from driver import chrome, process
from model import M3U8Spec, Task
from proxy import ProxyOption
from util import cleanup_download_temporary_cache, validate, create_folder

resolution_1080p = M3U8Spec(m3u8_filename='index_6m.m3u8', key_name='aes128.key')
resolution_720p = M3U8Spec(m3u8_filename='index_2m.m3u8', key_name='aes128.key')
resolution_540p = M3U8Spec(m3u8_filename='index_1m.m3u8', key_name='aes128.key')
resolution_270p = M3U8Spec(m3u8_filename='index_500k.m3u8', key_name='aes128.key')

tasks = [
    Task(prefix='', download_dir='', m3u8_spec=resolution_1080p),
]


def task(t: Task):
    driver = chrome(download_dir=t.download_dir, proxy=ProxyOption())
    driver.get(t.key_url())
    driver.get(t.m3u8_url())
    process(driver=driver, dest_dir=t.download_dir, m3u8_url=t.m3u8_url(), host_url=t.prefix, min_wait=3, max_wait=5)


def main():
    if len(tasks) == 0:
        exit(1)
    for t in tasks:
        create_folder(t.download_dir)
        while True:
            try:
                cleanup_download_temporary_cache(t.download_dir)
                print(f'task start: {t.prefix}')
                task(t)
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
