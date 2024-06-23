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

# 删除重复行
def remove_duplicates(lines, file_paths):
    for file_path in file_paths:
        file_lines = read_txt_file(file_path)
        lines = [line for line in lines if line not in file_lines]
    return lines

# 从URL列表下载和处理文件内容
def download_and_process_files(urls):
    all_lines = set()
    for url in urls:
        content = fetch_content_from_url(url)
        if content:
            all_lines.update(process_content(content))
    return list(all_lines)

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

    # 1. 下载并处理所有URL的内容
    all_lines = download_and_process_files(urls)

    # 写入 live.txt 文件
    write_txt_file('live.txt', all_lines)

    # 读取 live.txt 文件并删除与 iptv.txt, blacklist.txt 和 others.txt 中相同内容的行
    live_lines = read_txt_file('live.txt')
    live_lines = remove_duplicates(live_lines, ['iptv.txt', 'blacklist.txt', 'others.txt'])

    # 写入过滤后的 live.txt 文件
    write_txt_file('live.txt', live_lines)

    # 读取 live.txt 和 whitelist.txt，合并去重，删除不包含 "://" 的行，生成 tv.txt 文件
    whitelist_lines = read_txt_file('whitelist.txt')
    combined_lines = set(live_lines + whitelist_lines)
    tv_lines = [line for line in combined_lines if '://' in line]
    write_txt_file('tv.txt', tv_lines)

    # 2. 清空 iptv.txt 文件后读取 channel.txt 文件
    open('iptv.txt', 'w').close()
    channel_lines = read_txt_file('channel.txt')

    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file('iptv.txt', [channel_line])
        else:
            channel_name = channel_line.split(",")[0]
            matching_lines = [tv_line for tv_line in tv_lines if tv_line.split(",http")[0] == channel_name]
            append_to_file('iptv.txt', matching_lines)

    # 3. 在线检测 iptv.txt 文件的每行网址
    iptv_lines = read_txt_file('iptv.txt')
    valid_lines = []
    invalid_lines = []
    for line in iptv_lines:
        url = line.split(",")[1]
        is_valid, response_time = check_url_availability(url)
        if is_valid and response_time < 10000:
            valid_lines.append(line)
        else:
            invalid_lines.append(line)

    # 将无效的行添加到 blacklist.txt 文件
    append_to_file('blacklist.txt', invalid_lines)

    # 清空 tv.txt 文件，将有效的行写入 tv.txt 文件
    write_txt_file('tv.txt', valid_lines)

    # 4. 再次清空 iptv.txt 文件并处理
    open('iptv.txt', 'w').close()
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file('iptv.txt', [channel_line])
        else:
            channel_name = channel_line.split(",")[0]
            matching_lines = [tv_line for tv_line in valid_lines if tv_line.split(",http")[0] == channel_name]
            append_to_file('iptv.txt', matching_lines)

    # 5. 将 iptv.txt 转换为 iptv.m3u 并保存
    convert_to_m3u('iptv.txt', 'iptv.m3u')

    print("文件处理完成。")
