# -*- coding: utf-8 -*-

import os


def parse_m3u8(filename):
    _ts_paths = []
    with open(filename) as f:
        for line in f.readlines():
            line = line.strip()
            if line.endswith('.ts'):
                _ts_paths.append(line)
    return _ts_paths


def create_folder(path: str):
    if path and not os.path.exists(path):
        os.makedirs(path)
        abspath = os.path.abspath(path)
        print(f'[message] path created at {abspath}')


def cleanup_download_temporary_cache(out_dir):
    for file in os.listdir(out_dir):
        if file.endswith('.crdownload'):
            remove_file = os.path.join(os.path.abspath(out_dir), file)
            print(f'remove {remove_file}')
            os.remove(remove_file)


def validate(path: str):
    if not os.path.exists(path):
        print('[Error] please execute download script.')
        exit(1)

    downloaded_files = os.listdir(path)
    ts_paths = []
    for file in downloaded_files:
        if file.endswith('m3u8'):
            ts_paths = parse_m3u8(os.path.join(path, file))

    missing_amount = 0
    for ts_filename in ts_paths:
        full_path = os.path.join(path, ts_filename)
        if not os.path.exists(full_path):
            print(f'[Error] missing file: {ts_filename}')
            missing_amount += 1

    if not missing_amount:
        print('[message] download completed')
    else:
        print(f'[Error] missing {missing_amount} files')
