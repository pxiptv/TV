import concurrent.futures
import requests
import time

# 读取IPTV网址列表
def read_urls(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()
    return [url.strip() for url in urls]

# 检测单个URL的响应时间
def check_url(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=2)
        end_time = time.time()
        if response.status_code == 200:
            return url, end_time - start_time
    except requests.RequestException:
        return url, None
    return url, None

# 多线程检测URL
def detect_urls(urls):
    results = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                url, response_time = future.result()
                if response_time is not None:
                    results.append((url, response_time))
            except Exception as e:
                print(f"URL {url} generated an exception: {e}")
    return results

# 将响应速度最快的URL写入文件
def write_best_url(results, file_path):
    if results:
        best_url, best_time = min(results, key=lambda x: x[1])
        with open(file_path, 'w') as file:
            file.write(best_url + '\n')
        print(f"Best URL: {best_url} with response time: {best_time} seconds")
    else:
        print("No valid URL found.")

# 主函数
def main():
    urls = read_urls('iptv.txt')
    results = detect_urls(urls)
    write_best_url(results, 'others.txt')

if __name__ == "__main__":
    main()
