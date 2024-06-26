import aiohttp
import asyncio
import os

timeout = 10

async def fetch(url, session):
    try:
        async with session.get(url, timeout=timeout) as response:
            await response.text()
            return url, response.status, response
    except Exception as e:
        return url, None, None

async def check_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.ensure_future(fetch(url, session))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

def load_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

def save_urls(file_path, urls):
    with open(file_path, 'w') as file:
        for url in urls:
            file.write(f"{url}\n")

def main():
    input_file = 'online.txt'
    output_file = 'iptv.txt'

    urls = load_urls(input_file)

    loop = asyncio.get_event_loop()
    responses = loop.run_until_complete(check_urls(urls))

    valid_urls = [url for url, status, response in responses if status == 200]

    save_urls(output_file, valid_urls)

if __name__ == '__main__':
    main()
