import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime

timestart = datetime.now()

def extract_unique_lines(merged_output.txt, blacklist_auto.txt):
    # 读取b.txt的内容到集合中
    with open(file_b, 'r', encoding='utf-8') as f_b:
        lines_b = set(line.strip() for line in f_b)  # 移除行尾的换行符，并将行作为集合元素

    # 遍历a.txt中的每一行，并检查该行是否不在b.txt的集合中
    with open(file_a, 'r', encoding='utf-8') as f_a:
        for line in f_a:
            stripped_line = line.strip()  # 移除行尾的换行符
            if stripped_line not in lines_b:
                print(stripped_line)  # 打印出不重复的行

# 使用函数
extract_unique_lines('merged_output.txt', 'blacklist_auto.txt')
