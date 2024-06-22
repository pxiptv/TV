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
    whitelist_lines = read_txt_file('whitelist.txt')
    channel_lines = read_txt_file('channel.txt')

    # 删除与 iptv.txt, blacklist.txt 和 others.txt 中相同内容的行
    combined_set = set(all_lines) - set(iptv_lines) - set(blacklist_lines) - set(others_lines)

    # 写入 live.txt 文件
    write_txt_file('live.txt', list(combined_set))

    # 将 live.txt 与 whitelist.txt 合并并删除不包含 "://" 的行，生成 tv.txt 文件
    live_lines = read_txt_file('live.txt')
    combined_lines = live_lines + whitelist_lines
    tv_lines = [line for line in combined_lines if '://' in line]
    write_txt_file('tv.txt', tv_lines)

    # 按 channel.txt 文件的排序找出 tv.txt 文件中包含 channel.txt 文件内容的行，生成全新的 iptv.txt 文件
    sorted_tv_lines = sorted(tv_lines, key=lambda x: channel_lines.index(x.split(',')[0]) if x.split(',')[0] in channel_lines else float('inf'))
    filtered_iptv_lines = [line for line in sorted_tv_lines if any(channel in line for channel in channel_lines)]
    write_txt_file('iptv.txt', filtered_iptv_lines)

    print("文件处理完成。")
