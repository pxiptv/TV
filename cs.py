import requests
import re

# 读取文件内容
def read_txt_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
        return lines
    except FileNotFoundError:
        print(f"文件 '{file_path}' 未找到")
        return []
    except Exception as e:
        print(f"读取文件 '{file_path}' 时发生错误: {e}")
        return []

if __name__ == "__main__":
    # 定义要访问的多个URL
    urls = [
        'https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u',
        'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u',
        'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
        'https://raw.githubusercontent.com/fenxp/iptv/main/live/ipv6.txt', 
        'https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.txt',
        'https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt',
        'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
        'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/wang-tvlive.txt'
    ]
    
    urls_all_lines = []
    
    # 获取所有URL的直播源数据存入urls_all_lines
    for url in urls:
        print(f"处理URL: {url}")
        lines = process_url(url)
        urls_all_lines.extend(lines)
    
    # 过滤包含特定字符串的行，并去重
    filter_strings = ['#genre#', '192', '198', 'ChiSheng9']
    urls_all_lines = [line for line in urls_all_lines if not any(fs in line for fs in filter_strings)]
    urls_all_lines = list(set(urls_all_lines))  # 去重
    
    # 读取 iptv.txt、blacklist_auto.txt 和 others.txt 的内容
    iptv_lines = read_txt_file('iptv.txt')
    blacklist_lines = read_txt_file('blacklist_auto.txt')
    others_lines = read_txt_file('others.txt')
    
    # 将所有文件中的内容合并为一个集合，用于快速查找
    all_lines_set = set(iptv_lines + blacklist_lines + others_lines)
    
    # 进行过滤，保留不在 all_lines_set 中的行
    filtered_lines = [line for line in urls_all_lines if line not in all_lines_set]
    
    # 写回文件 urls_all_lines.txt
    try:
        with open('urls_all_lines.txt', 'w', encoding='utf-8') as file:
            file.write('\n'.join(filtered_lines))
        print("已成功将去重后的内容写入文件 'urls_all_lines.txt'")
    except Exception as e:
        print(f"写入文件 'urls_all_lines.txt' 时发生错误: {e}")
