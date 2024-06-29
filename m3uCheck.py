import concurrent.futures
import requests
import time

# 读取IPTV网址列表
def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [(url.strip().split(',')[0], url.strip().split(',')[1]) for url in urls]

# 检测单个URL的响应时间
def check_url(channel, url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=8)
        end_time = time.time()
        if response.status_code == 200:
            response_time = end_time - start_time
            print(f"Channel: {channel}, URL: {url}, Status: Success, Response Time: {response_time:.2f} seconds")
            return channel, url, response_time
        else:
            print(f"Channel: {channel}, URL: {url}, Status: Failed, Response Time: N/A")
    except requests.RequestException:
        print(f"Channel: {channel}, URL: {url}, Status: Failed, Response Time: N/A")
    return channel, url, None

# 多线程检测URL
def detect_urls(urls):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(check_url, channel, url): (channel, url) for channel, url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                channel, url, response_time = future.result()
                if response_time is not None:
                    results.append((channel, url, response_time))
            except Exception as e:
                print(f"URL {future_to_url[future]} generated an exception: {e}")
    return results

# 将每个频道响应速度最快的URL写入文件
def write_best_urls(results, file_path):
    best_results = {}
    for channel, url, response_time in results:
        if channel not in best_results or response_time < best_results[channel][1]:
            best_results[channel] = (url, response_time)
    
    with open(file_path, 'w') as file:
        for channel, (url, response_time) in best_results.items():
            file.write(f"{channel},{url}\n")
            print(f"Best URL for {channel}: {url} with response time: {response_time:.2f} seconds")

# 主函数
def main():
    urls = read_urls('iptv.txt')
    results = detect_urls(urls)
    write_best_urls(results, 'live.txt')

if __name__ == "__main__":
    main()
