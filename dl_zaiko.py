# -*- coding: utf-8 -*-

from time import sleep

from driver import edge, process
from model import Task, M3U8Spec
from proxy import ProxyOption
from util import cleanup_download_temporary_cache, validate, create_folder

spec = M3U8Spec(m3u8_filename='index_4.m3u8', key_name='')

tasks = [
    Task(prefix='', download_dir='', m3u8_spec=spec)
]


def task(t: Task):
    driver = edge(t.download_dir, proxy=ProxyOption(), executable_path='./msedgedriver')
    driver.get(t.m3u8_url())
    process(driver=driver, dest_dir=t.download_dir, m3u8_url=t.m3u8_url(), host_url=t.prefix, min_wait=5, max_wait=20)


def main():
    if len(tasks) == 0:
        exit(1)
    for t in tasks:
        create_folder(t.download_dir)
        while True:
            try:
                cleanup_download_temporary_cache(t.download_dir)
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
