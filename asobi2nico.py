# -*- coding: utf-8 -*-

import datetime
import json
import sys
from decimal import Decimal, ROUND_HALF_UP

args = sys.argv
filename = str(args[1])

print("Converting Asobistage comments json to niconico comments xml...")
with open(filename + ".xml", 'x', encoding='UTF-8') as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<packet>\n')

    with open(filename, 'r', encoding='UTF-8') as json_file:
        json_object = json.load(json_file)

    for i in range(len(json_object)):
        f.write(f'<chat thread="" no="{str(i + 1)}" ')

        # vpos変換
        vpos = str(Decimal(str(float(json_object[i]['playtime']) * 100)).quantize(Decimal('0'), rounding=ROUND_HALF_UP))
        f.write(f'vpos="{vpos}" ')

        # 日時変換
        dte = datetime.datetime.strptime(str(json_object[i]['time'])[:-3], '%Y-%m-%d %H:%M:%S.%f')
        date = int(dte.timestamp())

        username = str(json_object[i]['data']['userName']).replace("\\u3000", "　").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("\'", "&apos;")

        f.write(f'date="{str(date)}" mail="184" user_id="" user_name="{username}" user_color="{str(json_object[i]["data"]["color"])}" anonymity="1" ')
        f.write(f'date_usec="{dte.strftime("%f")}">')
        f.write(str(json_object[i]['data']['comment'])[2:-2].replace("\\u3000", "　").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\"", "&quot;").replace("\'", "&apos;"))
        f.write('</char>\n')

    f.write("</packet>")
