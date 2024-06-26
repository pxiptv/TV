import csv
import json
import os
import re
import traceback
import requests
import time
import shutil
from ffmpy import FFprobe
from subprocess import PIPE
from datetime import datetime
from func_timeout import func_set_timeout, FunctionTimedOut
from requests.adapters import HTTPAdapter

dt = datetime.now()

SKIP_FFPROBE_MESSAGES = [re.compile(pattern) for pattern in (
    'Last message repeated',
    'mmco: unref short failure',
    'number of reference frames .+ exceeds max',
)]

uniqueList = []

@func_set_timeout(18)
def get_stream(num, uri):
    try:
        ffprobe = FFprobe(
            inputs={uri: '-v error -show_format -show_streams -print_format json'})
        cdata = json.loads(ffprobe.run(
            stdout=PIPE, stderr=PIPE)[0].decode('utf-8'))
        return cdata
    except Exception as e:
        print('[{}] Error:{}'.format(str(num), str(e)))
        return False

def check_channel(uri, num):
    requests.adapters.DEFAULT_RETRIES = 3
    try:
        r = requests.get(uri, timeout=10)
        if r.status_code == requests.codes.ok:
            cdata = get_stream(num, uri)
            if cdata:
                flagAudio = 0
                flagVideo = 0
                for stream in cdata['streams']:
                    if stream['codec_type'] == 'video':
                        flagVideo = 1
                    elif stream['codec_type'] == 'audio':
                        flagAudio = 1
                if flagAudio == 0 or flagVideo == 0:
                    return False
                return True
        else:
            return False
    except Exception as e:
        print('[{}] Error:{}'.format(str(num), str(e)))
        return False

def print_info():
    print('Time: {}-{}-{} {}:{}'.format(dt.year, dt.month, dt.day, dt.hour, dt.minute))

def rm_files(target, selection):
    if selection == 1:
        try:
            shutil.rmtree(target)
        except OSError:
            pass
        try:
            os.mkdir(target)
        except OSError:
            pass
    else:
        try:
            os.remove(target)
        except OSError:
            pass

def main():
    print_info()
    with open('live.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    valid_urls = []
    for num, line in enumerate(lines, start=1):
        print(f"Processing line {num}: {line.strip()}")
        if '#genre#' in line:
            valid_urls.append(line.strip())
            print(f"Line {num} contains #genre#, skipping URL check.")
            continue

        parts = line.strip().split(',')
        if len(parts) < 2:
            print(f"Line {num} format is incorrect, skipping.")
            continue

        url = parts[1]
        if url in uniqueList:
            print(f"Line {num} URL already checked, skipping.")
            continue

        uniqueList.append(url)
        try:
            if check_channel(url, num):
                valid_urls.append(line.strip())
                print(f"Line {num} URL is valid.")
            else:
                print(f"Line {num} URL is invalid.")
        except FunctionTimedOut:
            print(f"Line {num} URL check timed out.")
            continue

    with open('iptv.txt', 'w', encoding='utf-8') as f:
        for url in valid_urls:
            f.write(url + '\n')

if __name__ == '__main__':
    main()
