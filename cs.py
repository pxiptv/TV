import csv
import json
import os
import re
import requests
import time
from ffmpy import FFprobe
from subprocess import PIPE
from datetime import datetime
from func_timeout import func_set_timeout, FunctionTimedOut

dt = datetime.now()

uniqueList = []

@func_set_timeout(18)
def get_stream(uri):
    try:
        ffprobe = FFprobe(inputs={uri: '-v error -show_format -show_streams -print_format json'})
        cdata = json.loads(ffprobe.run(stdout=PIPE, stderr=PIPE)[0].decode('utf-8'))
        return cdata
    except Exception as e:
        return False

def check_channel(row, num):
    uri = row[1]
    try:
        r = requests.get(uri, timeout=3)
        if r.status_code == requests.codes.ok:
            cdata = get_stream(uri)
            if cdata:
                flagAudio = 0
                flagVideo = 0
                flagHDR = 0
                flagHEVC = 0
                vwidth = 0
                vheight = 0
                for stream in cdata['streams']:
                    if stream['codec_type'] == 'video':
                        flagVideo = 1
                        if 'color_space' in stream and 'bt2020' in stream['color_space']:
                            flagHDR = 1
                        if stream['codec_name'] == 'hevc':
                            flagHEVC = 1
                        if vwidth <= stream['coded_width']:
                            vwidth = stream['coded_width']
                            vheight = stream['coded_height']
                    elif stream['codec_type'] == 'audio':
                        flagAudio = 1
                if flagAudio == 0 or flagVideo == 0:
                    return False
                return True
        else:
            return False
    except Exception as e:
        return False

def main():
    with open('live.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    valid_urls = []
    for num, line in enumerate(lines, start=1):
        if '#genre#' in line:
            valid_urls.append(line.strip())
            continue

        parts = line.strip().split(',')
        if len(parts) < 2:
            continue

        url = parts[1]
        if url in uniqueList:
            continue

        uniqueList.append(url)
        try:
            if check_channel(parts, num):
                valid_urls.append(line.strip())
        except FunctionTimedOut:
            continue

    with open('iptv.txt', 'w', encoding='utf-8') as f:
        for url in valid_urls:
            f.write(url + '\n')

if __name__ == '__main__':
    main()
