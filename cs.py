import csv
import json
import os
import re
import traceback
import requests
import subprocess
import time
import shutil
from ffmpy import FFprobe
from subprocess import PIPE
from datetime import datetime
from func_timeout import func_set_timeout, FunctionTimedOut
from requests.adapters import HTTPAdapter
from tqdm import tqdm

dt = datetime.now()

SKIP_FFPROBE_MESSAGES = [re.compile(pattern) for pattern in (
    'Last message repeated',
    'mmco: unref short failure',
    'number of reference frames .+ exceeds max',
)]


uniqueList = []


@func_set_timeout(18)
def get_stream(uri):
    try:
        ffprobe = FFprobe(inputs={uri: '-v error -show_format -show_streams -print_format json'})
        cdata = json.loads(ffprobe.run(stdout=PIPE, stderr=PIPE)[0].decode('utf-8'))
        return cdata
    except Exception as e:
        print(f"Error getting stream info for {uri}: {str(e)}")
        return False


def check_channel(uri):
    requests.adapters.DEFAULT_RETRIES = 3
    try:
        start_time = time.time()
        r = requests.get(uri, timeout=3)
        response_time = (time.time() - start_time) * 1000  # in milliseconds
        if r.status_code == requests.codes.ok:
            cdata = get_stream(uri)
            if cdata:
                flagAudio = 0
                flagVideo = 0
                for i in cdata['streams']:
                    if i['codec_type'] == 'video':
                        flagVideo = 1
                    elif i['codec_type'] == 'audio':
                        flagAudio = 1
                if flagAudio == 0 or flagVideo == 0:
                    print(f"Error: Video or Audio Only for {uri}")
                    return False, float('inf')
                return True, response_time
        else:
            print(f"Error: {r.status_code} for {uri}")
            return False, float('inf')
    except Exception as e:
        print(f"Error checking channel for {uri}: {str(e)}")
        return False, float('inf')


def main():
    urls = []
    with open('online.txt', 'r') as f:
        urls = [line.strip() for line in f.readlines()]

    valid_urls = []

    for num, url in tqdm(enumerate(urls, 1), desc="Checking URLs", total=len(urls)):
        if url in uniqueList:
            continue
        uniqueList.append(url)
        try:
            ret, response_time = check_channel(url)
            if ret:
                valid_urls.append((url, response_time))
        except FunctionTimedOut as e:
            print(f"Timeout for {url}: {str(e)}")
    
    # Sort by response time, ascending
    valid_urls.sort(key=lambda x: x[1])

    # Write valid URLs to iptv.txt
    with open('iptv.txt', 'w') as f:
        for url, _ in valid_urls:
            f.write(f"{url}\n")

    print(f"Total valid URLs: {len(valid_urls)}")


if __name__ == '__main__':
    main()
