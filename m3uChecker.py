import urllib.request
import subprocess
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

def check_url(url, timeout=8):
    try:
        if "://" in url:
            start_time = time.time()
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
                if response.status == 200:
                    print(f"成功检测到网址：{url}, 响应时间：{elapsed_time:.2f}ms")
                    return elapsed_time, True
        elif url.startswith("[240"):  # 检测是否为IPv6地址
            start_time = time.time()
            result = subprocess.run(["ping6", "-c", "1", "-W", str(timeout), url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
            if result.returncode == 0:
                print(f"成功检测到IPv6地址：{url}, 响应时间：{elapsed_time:.2f}ms")
                return elapsed_time, True
    except Exception as e:
        print(f"网址检测发现错误： {url}: {e}")
    return None, False

def main():
    channel_urls = {}

    # 读取 iptv.txt 文件
    with open('iptv.txt', 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if "://" in line:
                channel, url = line.split(",", 1)
                print(f"正在检测频道：{channel}, URL：{url}")
                response_time, success = check_url(url)
                if success:
                    if channel not in channel_urls or response_time < channel_urls[channel][0]:
                        channel_urls[channel] = (response_time, url)
                else:
                    print(f"检测失败：{url}")

    # 写入 live.txt 文件
    with open('live.txt', 'w', encoding='utf-8') as file:
        for channel, (response_time, url) in channel_urls.items():
            file.write(f"{channel},{url}\n")
            print(f"写入频道：{channel}, URL：{url}, 响应时间：{response_time:.2f}ms")

if __name__ == "__main__":
    main()
