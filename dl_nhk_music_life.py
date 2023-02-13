# -*- coding: utf-8 -*-

from time import sleep

from driver import chrome, process
from model import Task
from proxy import ProxyOption
from util import cleanup_download_temporary_cache, create_folder, validate

tasks = [
    Task(prefix='', download_dir='', m3u8_filename='', key_name='')
]


def task(t: Task):
    driver = chrome(t.download_dir, proxy=ProxyOption())
    driver.get(t.key_url())
    driver.get(t.m3u8_url())
    process(driver=driver, dest_dir=t.download_dir, m3u8_url=t.m3u8_url(), host_url='', min_wait=3, max_wait=5)


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


if __name__ == '__main__':
    main()
