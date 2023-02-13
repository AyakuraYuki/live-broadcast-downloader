# -*- coding: utf-8 -*-

import os
from time import sleep

from driver import chrome, process
from model import Task
from proxy import ProxyOption
from util import cleanup_download_temporary_cache, validate, create_folder

tasks = [
    # view_url: eplus viewing page url
    # prefix: prefix of *.ts file (ts link: `https://example.com/1080p_1.ts` -> prefix: `https://example.com/`)
    Task(view_url='', prefix='', download_dir=os.path.join('driver', 'path'))
]


def task(t: Task):
    driver = chrome(t.download_dir, proxy=ProxyOption())
    driver.get(t.view_url)
    driver.get(t.m3u8_url())
    process(driver=driver, dest_dir=t.download_dir, m3u8_url=t.m3u8_url(), host_url=t.prefix, min_wait=10, max_wait=30)


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
        #     ffmpeg -i <m3u8_filename> -c copy output.mp4


if __name__ == '__main__':
    main()
