from selenium import webdriver
from aiohttp_retry import RetryClient, ExponentialRetry
import asyncio
from time import time
import re
import datetime
import os
import urllib.parse
import ipaddress
from urllib.parse import urlparse
import requests
import re
from bs4 import BeautifulSoup
from bs4 import NavigableString
import fofa_map
from collections import defaultdict
from tqdm.asyncio import tqdm_asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
import concurrent.futures
import sys
import importlib.util
from time import sleep

timeout = 10
max_retries = 3

def retry_func(func, retries=max_retries + 1, name=""):
    for i in range(retries):
        try:
            return func()
        except Exception as e:
            if name and i < retries - 1:
                print(f"Failed to connect to the {name}. Retrying {i + 1}...")
            if i == retries - 1:
                raise e

async def get_speed(url, timeout=timeout):
    retry_options = ExponentialRetry(attempts=1, max_timeout=timeout)
    retry_client = RetryClient(raise_for_status=False, retry_options=retry_options)
    start = time()
    try:
        async with retry_client.get(url) as response:
            end = time()
            if response.status == 200:
                return int(round((end - start) * 1000))
            else:
                return float("inf")
    except Exception as e:
        print(f"Error on {url}: {e}")
        return float("inf")
    finally:
        await retry_client.close()

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    return driver

async def check_urls_from_file():
    with open("online.txt", "r") as file:
        urls = [line.strip() for line in file]

    response_times = await asyncio.gather(*(get_speed(url) for url in urls))

    url_response_times = list(zip(urls, response_times))
    url_response_times.sort(key=lambda x: x[1])

    with open("iptv.txt", "w") as file:
        for url, response_time in url_response_times:
            if response_time != float("inf"):
                file.write(f"{url}\n")

asyncio.run(check_urls_from_file())
