# -*- coding: utf-8 -*-

import os
from time import sleep

from driver import chrome, process
from proxy import ProxyOption
from util import cleanup_download_temporary_cache, validate, create_folder

# link of .m3u8 file
m3u8_url = ''
# prefix of *.ts file (ts link: `https://example.com/1080p_1.ts` -> ts_host_url: `https://example.com/`)
ts_host_url = ''
# eplus viewing page url
view_url = ''
user_home = os.path.expanduser('~')
download_dir = os.path.join(user_home, 'Videos', 'ts_video_eplus')


def main():
    driver = chrome(download_dir, proxy=ProxyOption())
    driver.get(view_url)
    driver.get(m3u8_url)
    process(driver=driver, dest_dir=download_dir, m3u8_url=m3u8_url, host_url=ts_host_url, min_wait=10, max_wait=30)


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
    print('Done!')
    # then jump into the download folder and fire this cmd:
    #     ffmpeg -i <m3u8_filename> -c copy output.mp4
