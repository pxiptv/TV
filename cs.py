import urllib.request
import os
import requests

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
    lines = content.split('\n')
    filtered_lines = [line for line in lines if not any(skip in line for skip in skip_strings)]
    return filtered_lines
    
# 从URL列表下载和处理文件内容
def download_and_process_files(urls):
    all_lines = set()
    for url in urls:
        content = fetch_content_from_url(url)
        if content:
            all_lines.update(process_content(content))
    return list(all_lines)
    
# 读取文件内容
def read_txt_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    return []

# 写入文件内容
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

# 去重
def remove_duplicates(lines):
    return list(set(lines))
    
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

    # 下载并处理所有URL的内容并去重
    all_lines = remove_duplicates(download_and_process_files(urls))
    
def main():
    # 读取 iptv.txt, blacklist.txt 和 others.txt 文件
    iptv_lines = read_txt_file('iptv.txt')
    blacklist_lines = read_txt_file('blacklist.txt')
    others_lines = read_txt_file('others.txt')
    
    # 合并 iptv.txt, blacklist.txt 和 others.txt 的所有行
    combined_lines = set(iptv_lines + blacklist_lines + others_lines)

    # 过滤 live.txt 中的重复行
    filtered_live_lines = [line for line in all_lines if line and line not in combined_lines]

    # 写入去重后的 live.txt 文件
    write_txt_file('live.txt', filtered_live_lines)
    
    # 清空 iptv.txt 文件
    open('iptv.txt', 'w').close()
    
    # 读取 channel.txt 和 tv.txt 文件
    channel_lines = read_txt_file('channel.txt')
    live_lines = read_txt_file('live.txt')

    # 用于存储结果的列表
    iptv_lines = []
    
    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            iptv_lines.append(channel_line)
        else:
            channel_name = channel_line
            matching_lines = [live_lines for live_lines in live_lines if live_lines.split(",http")[0] == channel_name]
            iptv_lines.extend(matching_lines)
    
    # 将去重后的内容写入 iptv.txt
    write_txt_file('iptv.txt', remove_duplicates(iptv_lines))

if __name__ == "__main__":
    main()
