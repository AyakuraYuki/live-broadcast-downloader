# -*- coding: utf-8 -*-

from time import sleep

from driver import chrome, process
from proxy import ProxyOption
from util import cleanup_download_temporary_cache, validate, create_folder

m3u8_url = ''  # m3u8地址
ts_host_url = ''  # ts文件地址前缀
view_url = ''  # eplus视听地址
download_dir = 'D:/Video/ts_video'


def main():
    driver = chrome(download_dir, proxy=ProxyOption())
    driver.get(view_url)
    driver.get(m3u8_url)
    process(driver=driver, download_dir=download_dir, m3u8_url=m3u8_url,
            ts_host_url=ts_host_url)


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
            sleep(100)
        else:
            break
    validate(download_dir)
    # 手动合并（进入下载文件夹）：ffmpeg -i index_4.m3u8 -c copy output.mp4
    print('Done!')
