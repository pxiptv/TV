# 读取文件内容
def read_txt_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()

# 写入文件内容
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

# 追加文件内容
def append_to_file(filename, lines):
    with open(filename, 'a', encoding='utf-8') as f:
        for line in lines:
            f.write(line)
            
# 定义文件路径
live_file_path = 'live.txt'
iptv_file = 'iptv.txt'
whitelist_file_path = 'whitelist.txt'
blacklist_file_path = 'blacklist.txt'

# 读取whitelist.txt文件中的所有行到一个集合中
with open(whitelist_file_path, 'r') as whitelist_file:
    whitelist_lines = set(whitelist_file.read().splitlines())

# 准备一个列表来存储最终结果
blacklist_lines = []

# 读取live.txt文件，找出不包含特定文本且不在whitelist中的行
with open(live_file_path, 'r') as live_file:
    for line in live_file:
        # 检查行是否包含特定文本
        if '#genre#' in line:
            continue  # 如果包含，跳过这一行
            
        # 如果行不在whitelist中，添加到blacklist_lines列表
        if line.strip() not in whitelist_lines:
            blacklist_lines.append(line)

# 将结果追加到blacklist.txt文件中
with open(blacklist_file_path, 'a') as blacklist_file:
    blacklist_file.writelines(blacklist_lines)

print("Blacklist 已更新")

# 清空 iptv.txt 文件后读取 channel.txt 文件
channel_lines = read_txt_file('channel.txt')
tv_lines = read_txt_file('whitelist.txt')
open('iptv.txt', 'w').close()

# 处理 channel.txt 文件中的每一行
for channel_line in channel_lines:
    if "#genre#" in channel_line:
        append_to_file('iptv.txt', [channel_line])
    else:
        channel_name = channel_line.split(",")[0].strip()
        matching_lines = [tv_line for tv_line in tv_lines if tv_line.split(",http")[0].strip() == channel_name]
        append_to_file('iptv.txt', matching_lines)
        
print("iptv.m3u 文件已生成。")

output_text = '#EXTM3U x-tvg-url="https://raw.bgithub.xyz/Troray/IPTV/main/tvxml.xml,https://raw.bgithub.xyz/Meroser/EPG-test/main/tvxml-test.xml.gz"\n'

with open("iptv.txt", "r", encoding='utf-8') as file:
    input_text = file.read()

lines = input_text.strip().split("\n")
group_name = ""
for line in lines:
    parts = line.split(",")
    if len(parts) == 2 and "#genre#" in line:
        group_name = parts[0]
    elif len(parts) == 2:
        output_text += f"#EXTINF:-1 group-title=\"{group_name}\",{parts[0]}\n"
        output_text += f"{parts[1]}\n"

with open("iptv.m3u", "w", encoding='utf-8') as file:
    file.write(output_text)

print("iptv.m3u 文件已生成。")
