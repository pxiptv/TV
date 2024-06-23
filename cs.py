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

# 追加写入文件内容
def append_to_file(file_path, lines):
    with open(file_path, 'a', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')

# 去重
def remove_duplicates(lines):
    return list(set(lines))

# 主函数
def main():
    # 清空 iptv.txt 文件
    open('iptv.txt', 'w').close()
    
    # 读取 channel.txt 和 tv.txt 文件
    channel_lines = read_txt_file('channel.txt')
    whitelist_lines = read_txt_file('whitelist.txt')

    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file(iptv_file, [channel_line])
        else:
            channel_name = channel_line
            matching_lines = [whitelist_lines for whitelist_lines in whitelist_lines if whitelist_lines.split(",http")[0] == channel_name]
            append_to_file(iptv_file, matching_lines)

    # 去重
    iptv_lines = remove_duplicates(iptv_lines)
    
    # 将去重后的内容写入 whitelist.txt
    write_txt_file('whitelist.txt', iptv_lines)

if __name__ == "__main__":
    main()
