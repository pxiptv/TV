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
    
    # 读取 channel.txt 文件
    channel_lines = read_txt_file('channel.txt')
    
    # 读取 whitelist.txt 文件
    whitelist_lines = read_txt_file('whitelist.txt')

    # 用于存储结果的列表
    iptv_lines = []

    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            # 直接写入 iptv.txt
            iptv_lines.append(channel_line)
        else:
            # 提取 channel_line 中的前半部分作为匹配条件
            channel_name = channel_line.split(",")[0]
            # 在 whitelist.txt 中查找匹配行
            matching_lines = [whitelist_line for whitelist_line in whitelist_lines if whitelist_line.startswith(channel_name)]
            # 追加匹配行到结果列表
            iptv_lines.extend(matching_lines)

    # 去重
    iptv_lines = remove_duplicates(iptv_lines)
    
    # 将去重后的内容写入 iptv.txt
    write_txt_file('iptv.txt', iptv_lines)

    # 将去重后的内容写入 whitelist.txt
    write_txt_file('whitelist.txt', iptv_lines)

if __name__ == "__main__":
    main()
