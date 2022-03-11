# -*- coding: utf-8 -*-

import os
from time import sleep

from driver import chrome, process
from proxy import ProxyOption
from util import cleanup_download_temporary_cache, validate, create_folder

m3u8_url = ''  # m3u8地址
ts_host_url = ''  # ts文件地址前缀
key_url = ''  # AES-128 Key地址
user_home = os.path.expanduser('~')
download_dir = os.path.join(user_home, 'Videos', 'ts_video_asobistage')


def main():
    driver = chrome(download_dir=download_dir, proxy=ProxyOption())
    driver.get(key_url)
    driver.get(m3u8_url)
    process(driver=driver, dest_dir=download_dir, m3u8_url=m3u8_url, host_url=ts_host_url, min_wait=5, max_wait=15)


if __name__ == '__main__':
    create_folder(download_dir)
    while True:
        try:
            cleanup_download_temporary_cache(download_dir)
            main()
        except Exception as e:
            print('Exception occurred, restarting...')
            print(f'Error: {e}')
            cleanup_download_temporary_cache(download_dir)
            sleep(10)
        else:
            break
    validate(download_dir)
    # 手动合并（进入下载文件夹）：ffmpeg -allowed_extensions ALL -i 6000k_.m3u8 -c copy output.mp4
    print('Done!')
