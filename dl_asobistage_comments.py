# -*- coding: utf-8 -*-

import asyncio
import os
import re
import sys

import websockets

max_tick = 20000

args = sys.argv
target_url = args[1]


def extract_info_from_url(url):
    patterns = [
        r"https://asobistage.asobistore.jp/event/([^/]+)/archive/([^/]+)",
        r"wss://replay.asobistore.jp/([^/]+)_([^/]+)_ch1/archive"
    ]
    for pattern in patterns:
        match = re.match(pattern, url)
        if match:
            _event = match.group(1)
            _day = match.group(2)
            return _event, _day
    raise ValueError("Invalid URL format\nUsage:ascomments-dl [ASOBISTAGE LIVE Archive Page URL]")


async def download(url):
    print("Connecting comment server (archive) via WebSocket...")
    async with websockets.connect(url) as ws:
        await ws.recv()
        none_count = 0
        for tick in range(max_tick):
            send_message = f'{{"func":"archive-get","time":"{str(5 * tick)}"}}'
            await ws.send(send_message)
            rsp = await ws.recv()
            comments = rsp[12:-2]

            if tick > 0 and len(comments) != 0:
                f.write(",")
            f.write(str(comments))

            if len(comments) == 0:
                none_count += 1
            else:
                none_count = 0

            if none_count > 19:
                break

            print(f"Downloading... Tick: {tick}, Sending: {send_message}, Empty: {none_count}", end='\r', flush=True)

        print()
        print("Closing and saving...")


event, day = extract_info_from_url(target_url)
downloading_from = f"wss://replay.asobistore.jp/{event}_{day}_ch1/archive"
save_to = f"{event}_{day}_comments.json"

print(f"""This is a program that downloads comments from Asobistage live broadcast archives.
The page url is: https://https://asobistage.asobistore.jp/event/{event}/archive/{day}
Downloading from: {downloading_from}""")

if os.path.exists(save_to):
    overwrite = input("File already exists. Do you want to overwrite it? (y/N): ")
    if overwrite.lower() == "y":
        print("Overwriting", save_to)
        with open(save_to, 'w', encoding='UTF-8') as f:
            f.write("[")
            asyncio.run(download(downloading_from))
            f.write("]")
    else:
        print("File not overwritten.")
else:
    print("Saving into", save_to)
    with open(save_to, 'w', encoding='UTF-8') as f:
        f.write("[")
        asyncio.run(download(downloading_from))
        f.write("]")
