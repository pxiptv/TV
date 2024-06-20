import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

timestart = datetime.now()

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def remove_blacklisted_lines(input_file, blacklist_file, output_file, header_lines_count=5):
    # 读取输入文件和黑名单文件
    input_lines = read_file(input_file)
    blacklist_lines = set(read_file(blacklist_file))

    # 保留前header_lines_count行内容
    header_lines = input_lines[:header_lines_count]

    # 去除黑名单中的行
    filtered_lines = [line for line in input_lines[header_lines_count:] if line not in blacklist_lines]

    # 合并保留的前header_lines_count行和过滤后的内容
    result_lines = header_lines + filtered_lines

    # 写入输出文件
    write_file(output_file, result_lines)

if __name__ == "__main__":
    input_file = 'merged_output.txt'
    blacklist_file = 'blacklist_auto.txt'
    output_file = 'filtered_output.txt'  # 过滤后的输出文件

    remove_blacklisted_lines(input_file, blacklist_file, output_file)
    print(f"已生成过滤后的文件: {output_file}")
