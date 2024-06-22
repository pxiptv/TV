import requests
import time
from datetime import datetime
import os
import re

# 获取URL的直播源数据
def process_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.splitlines()
        else:
            print(f"无法获取 URL: {url}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"请求 URL 时发生错误: {e}")
        return []

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
    
    # 过滤包含特定字符串的行，并保留包含 "://" 的行
    filter_strings = ['#genre#', '192', '198', 'ChiSheng9']
    urls_all_lines = [line for line in urls_all_lines if not any(fs in line for fs in filter_strings) and '://' in line]
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
        
# 文件名
whitelist_file = 'urls_all_lines.txt'

# 定义类别的列表
ys_lines = []
ws_lines = []
ty_lines = []
dy_lines = []
gat_lines = []
gj_lines = []
dhp_lines = []
mx_lines = []
radio_lines = []
gd_lines = []
hn_lines = []
other_lines = []

def process_name_string(input_str):
    parts = input_str.split(',')
    processed_parts = []
    for part in parts:
        processed_part = process_part(part)
        processed_parts.append(processed_part)
    result_str = ','.join(processed_parts)
    return result_str

def process_part(part_str):
    if "CCTV" in part_str and "://" not in part_str:
        part_str = part_str.replace("IPV6", "")
        part_str = part_str.replace("PLUS", "+")
        filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K' or char == '+')
        if not filtered_str.strip():
            filtered_str = part_str.replace("CCTV", "")

        if len(filtered_str) > 2 and re.search(r'4K|8K', filtered_str):
            filtered_str = re.sub(r'(4K|8K).*', r'\1', filtered_str)
            if len(filtered_str) > 2:
                filtered_str = re.sub(r'(4K|8K)', r'(\1)', filtered_str)

        return "CCTV" + filtered_str

    elif "卫视" in part_str:
        pattern = r'卫视「.*」'
        result_str = re.sub(pattern, '卫视', part_str)
        return result_str

    return part_str

def read_txt_to_array(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

ys_dictionary = read_txt_to_array('央视频道.txt')
ws_dictionary = read_txt_to_array('卫视频道.txt')
ty_dictionary = read_txt_to_array('体育频道.txt')
dy_dictionary = read_txt_to_array('电影.txt')
gat_dictionary = read_txt_to_array('港澳台.txt')
gj_dictionary = read_txt_to_array('国际台.txt')
jlp_dictionary = read_txt_to_array('纪录片.txt')
dhp_dictionary = read_txt_to_array('动画片.txt')
mx_dictionary = read_txt_to_array('明星.txt')
radio_dictionary = read_txt_to_array('收音机频道.txt')
gd_dictionary = read_txt_to_array('广东频道.txt')
hn_dictionary = read_txt_to_array('湖南频道.txt')

def load_corrections_name(filename):
    corrections = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                correct_name = parts[0]
                for name in parts[1:]:
                    corrections[name] = correct_name
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return corrections

corrections_name = load_corrections_name('corrections_name.txt')

def correct_name_data(corrections, data):
    corrected_data = []
    for line in data:
        name, url = line.split(',', 1)
        if name in corrections and name != corrections[name]:
            name = corrections[name]
        corrected_data.append(f"{name},{url}")
    return corrected_data

def sort_data(order, data):
    order_dict = {name: i for i, name in enumerate(order)}
    
    def sort_key(line):
        name = line.split(',')[0]
        return order_dict.get(name, len(order))
    
    sorted_data = sorted(data, key=sort_key)
    return sorted_data

def process_whitelist_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                if "#genre#" not in line and "," in line and "://" in line:
                    channel_name = line.split(',')[0].strip()
                    channel_address = line.split(',')[1].strip()
                    
                    if "CCTV" in channel_name:
                        ys_lines.append(process_name_string(line.strip()))
                    elif channel_name in ws_dictionary:
                        ws_lines.append(process_name_string(line.strip()))
                    elif channel_name in ty_dictionary:
                        ty_lines.append(process_name_string(line.strip()))
                    elif channel_name in dy_dictionary:
                        dy_lines.append(process_name_string(line.strip()))
                    elif channel_name in gat_dictionary:
                        gat_lines.append(process_name_string(line.strip()))
                    elif channel_name in gj_dictionary:
                        gj_lines.append(process_name_string(line.strip()))
                    elif channel_name in jlp_dictionary:
                        jlp_lines.append(process_name_string(line.strip()))
                    elif channel_name in dhp_dictionary:
                        dhp_lines.append(process_name_string(line.strip()))
                    elif channel_name in mx_dictionary:
                        mx_lines.append(process_name_string(line.strip()))
                    elif channel_name in radio_dictionary:
                        radio_lines.append(process_name_string(line.strip()))
                    elif channel_name in gd_dictionary:
                        gd_lines.append(process_name_string(line.strip()))
                    elif channel_name in hn_dictionary:
                        hn_lines.append(process_name_string(line.strip()))
                    else:
                        other_lines.append(line.strip())

    except Exception as e:
        print(f"处理文件时发生错误：{e}")

current_directory = os.getcwd()
current_date = datetime.now().strftime("%Y%m%d")

process_whitelist_file(whitelist_file)

def extract_number(s):
    num_str = s.split(',')[0].split('-')[1]
    numbers = re.findall(r'\d+', num_str)
    return int(numbers[-1]) if numbers else 999

def custom_sort(s):
    if "CCTV-4K" in s:
        return 2
    elif "CCTV-8K" in s:
        return 3
    elif "(4K)" in s:
        return 1
    else:
        return 0

version = datetime.now().strftime("%Y%m%d-%H-%M-%S") + ",url"
all_lines = [
    "更新时间,#genre#", version, '\n',
    "央视频道,#genre#", *sort_data(ys_dictionary, set(correct_name_data(corrections_name, ys_lines))), '\n',
    "卫视频道,#genre#", *sort_data(ws_dictionary, set(correct_name_data(corrections_name, ws_lines))), '\n',
    "港澳台,#genre#", *sort_data(gat_dictionary, set(correct_name_data(corrections_name, gat_lines))), '\n',
    "国际台,#genre#", *sort_data(gj_dictionary, set(correct_name_data(corrections_name, gj_lines))), '\n',
    "体育频道,#genre#", *sort_data(ty_dictionary, set(correct_name_data(corrections_name, ty_lines))), '\n',
    "电影频道,#genre#", *sort_data(dy_dictionary, set(correct_name_data(corrections_name, dy_lines))), '\n',
    "明星,#genre#", *sort_data(mx_dictionary, set(correct_name_data(corrections_name, mx_lines))), '\n',
    "纪录片,#genre#", *sort_data(jlp_dictionary, set(correct_name_data(corrections_name, jlp_lines))), '\n',
    "动画片,#genre#", *sorted(set(dhp_lines)), '\n',
    "湖南频道,#genre#", *sorted(set(correct_name_data(corrections_name, hn_lines))), '\n',
    "广东频道,#genre#", *sorted(set(correct_name_data(corrections_name, gd_lines))), '\n',
    "收音机频道,#genre#", *sort_data(radio_dictionary, set(radio_lines))
]

output_file = "ipvt.txt"

try:
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(all_lines))
except Exception as e:
    print(f"写入文件 '{output_file}' 时发生错误: {e}")

print("生成的文件:")
print(f"{output_file} 包含分类后的频道列表")
