import os

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
def main():
    # 读取 live.txt, iptv.txt, blacklist.txt 和 others.txt 文件
    live_lines = read_txt_file('live.txt')
    iptv_lines = read_txt_file('iptv.txt')
    blacklist_lines = read_txt_file('blacklist.txt')
    others_lines = read_txt_file('others.txt')
    
    # 合并 iptv.txt, blacklist.txt 和 others.txt 的所有行
    combined_lines = set(iptv_lines + blacklist_lines + others_lines)

    # 过滤 live.txt 中的重复行
    filtered_live_lines = [line for line in live_lines if line and line not in combined_lines]

    # 写入去重后的 live.txt 文件
    write_txt_file('live.txt', filtered_live_lines)

if __name__ == "__main__":
    main()
