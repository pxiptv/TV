import urllib.request
from urllib.parse import urlparse
import os

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
        lines = [line.strip() for line in file]
    return lines

# 写入文件内容
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')

# 主函数
if __name__ == "__main__":
    # 定义要访问的多个URL
    urls = [
        'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
        'https://raw.githubusercontent.com/fenxp/iptv/main/live/ipv6.txt', 
        'https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.txt',
        'https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt',
        'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
        'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/wang-tvlive.txt'
    ]

    # 合并所有URL内容
    combined_lines = []
    for url in urls:
        print(f"Fetching content from URL: {url}")
        content = fetch_content_from_url(url)
        filtered_lines = process_content(content)
        combined_lines.extend(filtered_lines)
    
    # 读取过滤文件内容
    iptv_lines = read_txt_file('iptv.txt')
    blacklist_lines = read_txt_file('blacklist_auto.txt')
    others_lines = read_txt_file('others.txt')
    
    # 删除与 iptv.txt、blacklist_auto.txt 和 others.txt 中相同的行
    unique_lines = list(set(combined_lines) - set(iptv_lines) - set(blacklist_lines) - set(others_lines))
    
    # 根据 channel.txt 文件排序并保留特定内容的行
    channel_lines = read_txt_file('channel.txt')
    sorted_lines = [line for line in channel_lines if line in unique_lines]
    
    # 写入 live.txt 文件
    write_txt_file('live.txt', sorted_lines)

    print(f"Successfully created live.txt with {len(sorted_lines)} lines")
