import urllib.request
import os
import time
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

# 从URL获取文件内容
def fetch_content_from_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

# 处理并过滤URL内容
def process_content(content):
    skip_strings = ['#genre#', '192', '198', 'ChiSheng9']
    required_string = '://'
    lines = content.split('\n')
    filtered_lines = [line for line in lines if not any(skip in line for skip in skip_strings) and required_string in line]
    return filtered_lines

# 读取文件内容
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

# 写入文件内容
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

# 在线检测URL是否可访问
def check_url(url, timeout=10):
    try:
        start_time = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
            if response.status == 200:
                return elapsed_time, True
    except Exception as e:
        print(f"Error checking {url}: {e}")
    return None, False

# 处理单行文本并检测URL
def process_line(line):
    parts = line.split(',')
    if len(parts) == 2:
        name, url = parts
        elapsed_time, is_valid = check_url(url.strip())
        if is_valid:
            return elapsed_time, line.strip()
        else:
            return None, line.strip()
    return None, None

# 多线程处理文本并检测URL
def process_urls_multithreaded(lines, max_workers=18):
    successlist = []
    blacklist = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_line, line): line for line in lines}
        for future in as_completed(futures):
            elapsed_time, result = future.result()
            if result:
                if elapsed_time is not None and elapsed_time <= 10000:
                    successlist.append(result)
                else:
                    blacklist.append(result)
    return successlist, blacklist

# 主函数
if __name__ == "__main__":
    urls = [
        'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
        'https://raw.githubusercontent.com/fenxp/iptv/main/live/ipv6.txt',
        'https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.txt',
        'https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt',
        'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
        'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/wang-tvlive.txt'
    ]

    # 下载并处理所有URL的内容
    all_lines = []
    for url in urls:
        content = fetch_content_from_url(url)
        if content:
            all_lines.extend(process_content(content))

    # 读取本地文件
    iptv_lines = read_txt_file('iptv.txt')
    blacklist_lines = read_txt_file('blacklist.txt')
    others_lines = read_txt_file('others.txt')
    channel_lines = read_txt_file('channel.txt')
    whitelist_lines = read_txt_file('whitelist.txt')

    # 删除与 iptv.txt, blacklist.txt 和 others.txt 中相同内容的行
    combined_set = set(all_lines) - set(iptv_lines) - set(blacklist_lines) - set(others_lines)

    # 根据 channel.txt 的排序找出包含 channel.txt 文件内容的行
    live_lines = sorted(list(combined_set), key=lambda x: channel_lines.index(x.split(',')[0]) if x.split(',')[0] in channel_lines else float('inf'))
    write_txt_file('live.txt', live_lines)

    # 生成 tv.txt 文件
    tv_lines = [line for line in live_lines if any(channel in line for channel in channel_lines)]
    write_txt_file('tv.txt', tv_lines)

    # 在线检测 tv.txt 文件的每行网址
    success_list, blacklist = process_urls_multithreaded(tv_lines)

    # 写入结果文件
    write_txt_file('iptv.txt', success_list + whitelist_lines)
    write_txt_file('blacklist.txt', blacklist)

    print(f"成功生成: iptv.txt")
    print(f"黑名单已更新: blacklist.txt")

    ################# 添加生成m3u文件 #################
    output_text = "#EXTM3U\n"

    with open("iptv.txt", "r", encoding='utf-8') as file:
        input_text = file.read()

    lines = input_text.strip().split("\n")
    group_name = ""
    for line in lines:
        parts = line.split(",")
        if len(parts) == 2 and "#genre#" in line:
            group_name = parts[0]
        elif len(parts) == 2:
            output_text += f"#EXTINF:-1 group-title=\"{group_name}\",{parts[0]}\n"
            output_text += f"{parts[1]}\n"

    with open("iptv.m3u", "w", encoding='utf-8') as file:
        file.write(output_text)

    print("iptv.m3u文件已生成。")
