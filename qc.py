import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

timestart = datetime.now()

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return set(file.readlines())

def write_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def remove_blacklisted_lines(input_file, blacklist_file, output_file):
    # 读取输入文件和黑名单文件
    input_lines = read_file(input_file)
    blacklist_lines = read_file(blacklist_file)

    # 计算差集
    filtered_lines = input_lines - blacklist_lines

    # 写入输出文件
    write_file(output_file, filtered_lines)

if __name__ == "__main__":
    input_file = 'merged_output.txt'
    blacklist_file = 'blacklist_auto.txt'
    output_file = 'filtered_output.txt'  # 过滤后的输出文件

    remove_blacklisted_lines(input_file, blacklist_file, output_file)
    print(f"已生成过滤后的文件: {output_file}")
