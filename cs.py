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

def append_to_file(file_path, lines):
    with open(file_path, 'a', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')

# 去重
def remove_duplicates(lines):
    return list(set(lines))

# 过滤掉在 comparison_files 中出现的行
def filter_lines(input_file, comparison_files):
    # 读取对比文件中的所有行
    comparison_lines = set()
    for file in comparison_files:
        comparison_lines.update(read_txt_file(file))

    # 读取输入文件并过滤行
    input_lines = read_txt_file(input_file)
    filtered_lines = [line for line in input_lines if line not in comparison_lines]
    
    return filtered_lines

# 在线检测URL是否可访问
def check_url_availability(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return True, response.elapsed.total_seconds() * 1000
    except requests.RequestException:
        pass
    return False, 0

# 将iptv.txt转换为iptv.m3u文件
def convert_to_m3u(iptv_file, m3u_file):
    lines = read_txt_file(iptv_file)
    with open(m3u_file, 'w', encoding='utf-8') as file:
        file.write("#EXTM3U\n")
        for line in lines:
            parts = line.split(',', 1)
            if len(parts) == 2:
                file.write(f"#EXTINF:-1,{parts[0]}\n")
                file.write(f"{parts[1]}\n")
                
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
    # 写入 online.txt 文件
    write_txt_file('online.txt', all_lines)
    input_file = 'online.txt'
    
    # 合并 iptv.txt, blacklist.txt 和 others.txt 的所有行
    comparison_files = ['iptv.txt', 'blacklist.txt', 'others.txt']

    # 过滤 live.txt 中的重复行
    filtered_live_lines = filter_lines(input_file, comparison_files)

    # 清空 live.txt 文件
    open('live.txt', 'w').close()

    # 过滤后写入 live.txt 文件
    write_txt_file('live.txt', filtered_live_lines)
    
    # 读取 channel.txt 和 tv.txt 文件
    channel_lines = read_txt_file('channel.txt')
    live_lines = read_txt_file('live.txt')

    # 用于存储结果的列表
    tv_lines = []
    
    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            tv_lines.append(channel_line)
        else:
            channel_name = channel_line
            matching_lines = [live_lines for live_lines in live_lines if live_lines.split(",http")[0] == channel_name]
            tv_lines.extend(matching_lines)

    # 清空 tv.txt 文件,将重新排序后的内容写入 tv.txt
    open('tv.txt', 'w').close()
    write_txt_file('tv.txt', tv_lines)
    append_to_file('tv.txt', 'whitelist.txt')

if __name__ == "__main__":
    main()
