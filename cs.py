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
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    return []

# 写入文件内容
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

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

# 按channel.txt的顺序过滤行
def filter_by_channel(lines, channel_lines):
    filtered_lines = [line for line in lines if "#genre#" in line or any(channel in line for channel in channel_lines)]
    return filtered_lines

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

    # 读取 tv.txt 和 channel.txt 文件，按 channel.txt 的排序过滤行生成 iptv.txt 文件
    channel_lines = read_txt_file('channel.txt')
    tv_lines = read_txt_file('tv.txt')
    filtered_iptv_lines = filter_by_channel(tv_lines, channel_lines)
    write_txt_file('iptv.txt', filtered_iptv_lines)

    print("文件处理完成。")
