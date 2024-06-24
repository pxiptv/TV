import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import os
from urllib.parse import urlparse

# 读取文件内容
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file if '://' in line]
    return lines

# 检测URL是否可访问并记录响应时间
def check_url(url, timeout=10):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }
    try:
        start_time = time.time()
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
            if response.status == 200:
                return elapsed_time, True
    except Exception as e:
        print(f"Error checking {url}: {e}")
    return None, False

# 处理单行文本并检测URL
def process_line(line):
    url = line.strip()
    elapsed_time, is_valid = check_url(url)
    if is_valid:
        return elapsed_time, url
    else:
        return None, url

# 多线程处理文本并检测URL
def process_urls_multithreaded(lines, max_workers=18):
    whitelist = []
    blacklist = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_line, line): line for line in lines}
        for future in as_completed(futures):
            elapsed_time, result = future.result()
            if result:
                if elapsed_time is not None:
                    whitelist.append(f"{elapsed_time:.2f}ms,{result}")
                else:
                    blacklist.append(result)
    return whitelist, blacklist

# 写入文件
def write_list(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data_list:
            file.write(item + '\n')

if __name__ == "__main__":
    timestart = datetime.now()
    
    input_file = 'iptv.txt'  # 输入文件路径
    whitelist_file = 'whitelist.txt'  # 白名单文件路径
    blacklist_file = 'blacklist.txt'  # 黑名单文件路径

    # 读取输入文件内容
    lines = read_txt_file(input_file)

    # 处理URL并生成白名单和黑名单
    whitelist, blacklist = process_urls_multithreaded(lines)
    
    # 写入白名单文件
    write_list(whitelist_file, whitelist)
    
    # 写入黑名单文件
    write_list(blacklist_file, blacklist)

    timeend = datetime.now()
    elapsed_time = timeend - timestart
    total_seconds = elapsed_time.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    print(f"开始时间: {timestart.strftime('%Y%m%d_%H_%M_%S')}")
    print(f"结束时间: {timeend.strftime('%Y%m%d_%H_%M_%S')}")
    print(f"执行时间: {minutes} 分 {seconds} 秒")
    print(f"总URL数量: {len(lines)}")
    print(f"成功URL数量: {len(whitelist)}")
    print(f"失败URL数量: {len(blacklist)}")
