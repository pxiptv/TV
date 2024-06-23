def read_txt_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return [line.strip() for line in lines]
    return []

def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

def append_to_file(file_path, line):
    with open(file_path, 'a', encoding='utf-8') as file:
        file.write(line + '\n')

def process_files(channel_file, tv_file, iptv_file):
    # 清空 iptv.txt 文件
    open(iptv_file, 'w').close()

    # 读取 channel.txt 和 tv.txt 文件内容
    channel_lines = read_txt_file(channel_file)
    tv_lines = read_txt_file(tv_file)

    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file(iptv_file, channel_line)
        else:
            matching_lines = [line for line in tv_lines if channel_line in line]
            for match in matching_lines:
                append_to_file(iptv_file, match)

if __name__ == "__main__":
    channel_file = 'channel.txt'
    tv_file = 'tv.txt'
    iptv_file = 'iptv.txt'

    process_files(channel_file, tv_file, iptv_file)

    print("文件处理完成。")
