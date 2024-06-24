import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import os
from urllib.parse import urlparse


timestart = datetime.now()

# 读取文件内容
def read_txt_file(file_path):
    skip_strings = ['#genre#', '192', '198', 'ChiSheng9', 'epg.pw', '(576p)', '(540p)', '(360p)', '(480p)', '(180p)', '(404p)', 'generationnexxxt']  # 定义需要跳过的字符串数组['#', '@', '#genre#'] 
    required_strings = ['://']  # 定义需要包含的字符串数组['必需字符1', '必需字符2'] 

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [
            line for line in file
            if not any(skip_str in line for skip_str in skip_strings) and all(req_str in line for req_str in required_strings)
        ]
    return lines

# 写入文件内容
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

def append_to_file(file_path, lines):
    with open(file_path, 'a', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')
            
# 写入文件
def write_list(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data_list:
            file.write(item + '\n')

# 合并两个文件的内容并写入输出文件
def merge_files(file1, file2, output_file):
    lines1 = read_txt_file(file1)
    lines2 = read_txt_file(file2)

# 合并并去重
    merged_lines = list(set(lines1 + lines2))
    write_txt_file(output_file, merged_lines)
    
# 删除重复行
def remove_duplicates(lines, file_paths):
    for file_path in file_paths:
        file_lines = read_txt_file(file_path)
        lines = [line for line in lines if line not in file_lines]
    return lines
    
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
    


if __name__ == "__main__":
    
    # 清空 iptv.txt 文件后读取 channel.txt 文件
    open('iptv.txt', 'w').close()
    channel_lines = read_txt_file('channel.txt')
    tv_lines = read_txt_file('tv.txt')

    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file('iptv.txt', [channel_line])
        else:
            channel_name = channel_line
            matching_lines = [tv_line for tv_line in tv_lines if tv_line.split(",http")[0] == channel_name]
            append_to_file('iptv.txt', matching_lines)

    print("待检测文件已生成。")

    
