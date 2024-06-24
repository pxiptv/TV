import requests
import concurrent.futures
import time

# 读取iptv.txt文件
def read_iptv_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip().split(',') for line in lines]

# 写入whitelist.txt文件
def write_to_whitelist(filename, data):
    with open(filename, 'a', encoding='utf-8') as file:
        for name, url, response_time in data:
            file.write(f"{name},{url},{response_time}\n")

# 写入blacklist.txt文件
def write_to_blacklist(filename, data):
    with open(filename, 'a', encoding='utf-8') as file:
        for name, url, response_time in data:
            file.write(f"{name},{url},{response_time}\n")

# 检测URL响应时间
def check_url(name, url, timeout=20):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=timeout)
        response_time = (time.time() - start_time) * 1000  # 转换为毫秒
        if response.status_code == 200 and response_time < 10000:
            return (name, url, response_time, True)
        else:
            return (name, url, response_time, False)
    except requests.RequestException:
        return (name, url, None, False)

# 处理单个结果
def handle_result(result):
    name, url, response_time, is_whitelisted = result
    if is_whitelisted:
        whitelist.append((name, url, response_time))
    else:
        blacklist.append((name, url, response_time if response_time is not None else "No response"))

# 主函数
if __name__ == "__main__":
    iptv_list = read_iptv_file('iptv.txt')
    whitelist = []
    blacklist = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(check_url, name, url): (name, url) for name, url in iptv_list}
        for future in concurrent.futures.as_completed(future_to_url):
            try:
                result = future.result()
                handle_result(result)
            except Exception as e:
                name, url = future_to_url[future]
                blacklist.append((name, url, "Error"))

    write_to_whitelist('whitelist.txt', whitelist)
    write_to_blacklist('blacklist.txt', blacklist)

    print("检测完成，结果已写入whitelist.txt和blacklist.txt")
