# 读取文件内容
def read_txt_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()

# 写入文件内容
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')

# 写入文件内容
def write_list(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data_list:
            file.write(item + '\n')

# 定义文件路径
live_file_path = 'live.txt'
iptv_file = 'iptv.txt'
whitelist_file_path = 'whitelist.txt'
blacklist_file_path = 'blacklist.txt'

# 读取whitelist.txt文件中的URLs，并存储到集合中
with open(whitelist_file_path, 'r') as whitelist_file:
    whitelist_urls = set(line.strip() for line in whitelist_file if line.strip())

# 读取live.txt文件，并处理每一行
with open(live_file_path, 'r') as live_file, open(blacklist_file_path, 'a') as blacklist_file:
    for line in live_file:
        # 分割字符串，获取URL
        url = line.strip().split(',')[-1]
        
        # 检查URL是否在whitelist中
        if url not in whitelist_urls:
            # 如果不在whitelist中，追加到blacklist.txt中
            blacklist_file.write(line)

print("Blacklist 文件已更新完毕.")

lines = read_txt_file('whitelist.txt')
write_list(iptv_file, lines)

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

    print("iptv.m3u文件已生成。")
