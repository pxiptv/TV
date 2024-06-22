import urllib.request
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
    lines = content.split('\n')
    filtered_lines = [line for line in lines if not any(skip in line for skip in skip_strings)]
    return filtered_lines

# 读取文件内容
def read_txt_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip() for line in file]

# 写入文件内容
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

def append_to_file(file_path, lines):
    with open(file_path, 'a', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')

def process_files(channel_file, tv_file, iptv_file):
    # 清空 iptv.txt 文件
    open(iptv_file, 'w').close()

    # 读取 channel.txt 和 tv.txt 文件
    channel_lines = read_txt_file(channel_file)
    tv_lines = read_txt_file(tv_file)

    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file(iptv_file, [channel_line])
        else:
            channel_name = channel_line.split(",")[0]
            matching_lines = [tv_line for tv_line in tv_lines if tv_line.split(",http")[0] == channel_name]
            append_to_file(iptv_file, matching_lines)

# 从URL列表下载和处理文件内容
def download_and_process_files(urls):
    all_lines = set()
    for url in urls:
        content = fetch_content_from_url(url)
        if content:
            all_lines.update(process_content(content))
    return list(all_lines)

# 删除与本地文件重复的行
def remove_duplicates(lines, file_paths):
    for file_path in file_paths:
        file_lines = read_txt_file(file_path)
        lines = [line for line in lines if line not in file_lines]
    return lines

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

    # 清空 iptv.txt 文件后读取 channel.txt 文件，如行中包含“#genre#“的直接写入 iptv.txt 后换行，以每行的内容为条件，在 tv.txt 中查找与 “,http” 前字符相同的行，逐行添加到 iptv.txt
    process_files('channel.txt', 'tv.txt', 'iptv.txt')

    print("文件处理完成。")
