import urllib.request
import re
import os
from datetime import datetime

urls = [
    'https://raw.bgithub.xyz/Supprise0901/TVBox_live/main/live.txt',
    'https://raw.bgithub.xyz/Guovin/TV/gd/result.txt',
    'https://raw.bgithub.xyz/ssili126/tv/main/itvlist.txt',
    'https://m3u.ibert.me/txt/fmml_ipv6.txt',
    'https://m3u.ibert.me/txt/ycl_iptv.txt',
    'https://m3u.ibert.me/txt/y_g.txt',
    'https://m3u.ibert.me/txt/j_home.txt',
    'https://raw.bgithub.xyz/gaotianliuyun/gao/master/list.txt',
    'https://gitee.com/xxy002/zhiboyuan/raw/master/zby.txt',
    'https://raw.bgithub.xyz/mlvjfchen/TV/main/iptv_list.txt',
    'https://raw.bgithub.xyz/fenxp/iptv/main/live/ipv6.txt',
    'https://raw.bgithub.xyz/fenxp/iptv/main/live/tvlive.txt',
    'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt'
]

ys_lines = []
ws_lines = []
ty_lines = []
dy_lines = []
dsj_lines = []
gat_lines = []
gj_lines = []
jlp_lines = []
dhp_lines = []
xq_lines = []
js_lines = []
cw_lines = []
mx_lines = []
ztp_lines = []
zy_lines = []
yy_lines = []
game_lines = []
radio_lines = []
gd_lines = []
hn_lines = []
other_lines = []

def process_name_string(input_str):
    parts = input_str.split(',')
    processed_parts = []
    for part in parts:
        processed_part = process_part(part)
        processed_parts.append(processed_part)
    result_str = ','.join(processed_parts)
    return result_str

def process_part(part_str):
    if "CCTV" in part_str and "://" not in part_str:
        part_str = part_str.replace("IPV6", "")
        part_str = part_str.replace("PLUS", "+")
        filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K' or char == '+')
        if not filtered_str.strip():
            filtered_str = part_str.replace("CCTV", "")

        if len(filtered_str) > 2 and re.search(r'4K|8K', filtered_str):
            filtered_str = re.sub(r'(4K|8K).*', r'\1', filtered_str)
            if len(filtered_str) > 2:
                filtered_str = re.sub(r'(4K|8K)', r'(\1)', filtered_str)

        return "CCTV" + filtered_str

    elif "卫视" in part_str:
        pattern = r'卫视「.*」'
        result_str = re.sub(pattern, '卫视', part_str)
        return result_str

    return part_str

def process_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            text = data.decode('utf-8')

            lines = text.split('\n')
            for line in lines:
                if "#genre#" not in line and "," in line and "://" in line:
                    channel_name = line.split(',')[0].strip()
                    channel_address = line.split(',')[1].strip()
                    
                    if "CCTV" in channel_name:
                        ys_lines.append(process_name_string(line.strip()))
                    elif channel_name in ws_dictionary:
                        ws_lines.append(process_name_string(line.strip()))
                    elif channel_name in ty_dictionary:
                        ty_lines.append(process_name_string(line.strip()))
                    elif channel_name in dy_dictionary:
                        dy_lines.append(process_name_string(line.strip()))
                    elif channel_name in dsj_dictionary:
                        dsj_lines.append(process_name_string(line.strip()))
                    elif channel_name in gat_dictionary:
                        gat_lines.append(process_name_string(line.strip()))
                    elif channel_name in gj_dictionary:
                        gj_lines.append(process_name_string(line.strip()))
                    elif channel_name in jlp_dictionary:
                        jlp_lines.append(process_name_string(line.strip()))
                    elif channel_name in dhp_dictionary:
                        dhp_lines.append(process_name_string(line.strip()))
                    elif channel_name in xq_dictionary:
                        xq_lines.append(process_name_string(line.strip()))
                    elif channel_name in js_dictionary:
                        js_lines.append(process_name_string(line.strip()))
                    elif channel_name in cw_dictionary:
                        cw_lines.append(process_name_string(line.strip()))
                    elif channel_name in mx_dictionary:
                        mx_lines.append(process_name_string(line.strip()))
                    elif channel_name in ztp_dictionary:
                        ztp_lines.append(process_name_string(line.strip()))
                    elif channel_name in zy_dictionary:
                        zy_lines.append(process_name_string(line.strip()))
                    elif channel_name in yy_dictionary:
                        yy_lines.append(process_name_string(line.strip()))
                    elif channel_name in game_dictionary:
                        game_lines.append(process_name_string(line.strip()))
                    elif channel_name in radio_dictionary:
                        radio_lines.append(process_name_string(line.strip()))
                    elif channel_name in gd_dictionary:
                        gd_lines.append(process_name_string(line.strip()))
                    elif channel_name in hn_dictionary:
                        hn_lines.append(process_name_string(line.strip()))
                    else:
                        other_lines.append(line.strip())

    except Exception as e:
        print(f"处理URL时发生错误：{e}")

current_directory = os.getcwd()

def read_txt_to_array(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            lines = [line.strip() for line in lines]
            return lines
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

ys_dictionary = read_txt_to_array('CCTV.txt')
ws_dictionary = read_txt_to_array('卫视频道.txt')
ty_dictionary = read_txt_to_array('体育频道.txt')
dy_dictionary = read_txt_to_array('电影.txt')
dsj_dictionary = read_txt_to_array('电视剧.txt')
gat_dictionary = read_txt_to_array('港澳台.txt')
gj_dictionary = read_txt_to_array('国际台.txt')
jlp_dictionary = read_txt_to_array('纪录片.txt')
dhp_dictionary = read_txt_to_array('动画片.txt')
xq_dictionary = read_txt_to_array('戏曲频道.txt')
js_dictionary = read_txt_to_array('解说频道.txt')
cw_dictionary = read_txt_to_array('春晚.txt')
mx_dictionary = read_txt_to_array('明星.txt')
ztp_dictionary = read_txt_to_array('主题片.txt')
zy_dictionary = read_txt_to_array('综艺频道.txt')
yy_dictionary = read_txt_to_array('音乐频道.txt')
game_dictionary = read_txt_to_array('游戏频道.txt')
radio_dictionary = read_txt_to_array('收音机频道.txt')
gd_dictionary = read_txt_to_array('地方台/广东频道.txt')
hn_dictionary = read_txt_to_array('地方台/湖南频道.txt')

def load_corrections_name(filename):
    corrections = {}
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split(',')
                correct_name = parts[0]
                for name in parts[1:]:
                    corrections[name] = correct_name
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return corrections

corrections_name = load_corrections_name('corrections_name.txt')

def correct_name_data(corrections, data):
    corrected_data = []
    for line in data:
        name, url = line.split(',', 1)
        if name in corrections and name != corrections[name]:
            name = corrections[name]
        corrected_data.append(f"{name},{url}")
    return corrected_data

def sort_data(order, data):
    order_dict = {name: i for i, name in enumerate(order)}
    
    def sort_key(line):
        name = line.split(',')[0]
        return order_dict.get(name, len(order))
    
    sorted_data = sorted(data, key=sort_key)
    return sorted_data

current_date = datetime.now().strftime("%Y%m%d")

def save_data(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for item in data:
                file.write("%s\n" % item)
    except Exception as e:
        print(f"An error occurred while saving the file '{filename}': {e}")

for url in urls:
    process_url(url)

# 定义一个函数，提取每行中逗号前面的数字部分作为排序的依据
def extract_number():
    num_str = s.split(',')[0].split('-')[1]  # 提取逗号前面的数字部分
    numbers = re.findall(r'\d+', num_str)   #因为有+和K
    return int(numbers[-1]) if numbers else 999
# 定义一个自定义排序函数
def custom_sort():
    if "CCTV-4K" in s:
        return 2  # 将包含 "4K" 的字符串排在后面
    elif "CCTV-8K" in s:
        return 3  # 将包含 "8K" 的字符串排在后面 
    elif "(4K)" in s:
        return 1  # 将包含 " (4K)" 的字符串排在后面
    else:
        return 0  # 其他字符串保持原顺序

# 合并所有对象中的行文本（去重，排序后拼接）
#["上海频道,#genre#"] + sorted(set(sh_lines)) + ['\n'] + \
#["央视频道,#genre#"] + sorted(sorted(set(ys_lines),key=lambda x: extract_number(x)), key=custom_sort) + ['\n'] + \
#["卫视频道,#genre#"] + sorted(set(ws_lines)) + ['\n'] + \
#["春晚,#genre#"] + sorted(set(cw_lines))
#["主题片,#genre#"] + sorted(set(ztp_lines)) + ['\n'] + \
#["电视剧频道,#genre#"] + sorted(set(dsj_lines)) + ['\n'] + \
version=datetime.now().strftime("%Y%m%d-%H-%M-%S")+",url"
all_lines =  ["更新时间,#genre#"] +[version] + ['\n'] +\
             ["央视频道,#genre#"] + sort_data(ys_dictionary,set(correct_name_data(corrections_name,ys_lines))) + ['\n'] + \
             ["卫视频道,#genre#"] + sort_data(ws_dictionary,set(correct_name_data(corrections_name,ws_lines))) + ['\n'] + \
             ["体育频道,#genre#"] + sort_data(ty_dictionary,set(correct_name_data(corrections_name,ty_lines))) + ['\n'] + \
             ["电影频道,#genre#"] + sort_data(dy_dictionary,set(correct_name_data(corrections_name,dy_lines))) + ['\n'] + \
             ["电视剧频道,#genre#"] + sort_data(dsj_dictionary,set(correct_name_data(corrections_name,dsj_lines))) + ['\n'] + \
             ["明星,#genre#"] + sort_data(mx_dictionary,set(correct_name_data(corrections_name,mx_lines))) + ['\n'] + \
             ["主题片,#genre#"] + sort_data(ztp_dictionary,set(correct_name_data(corrections_name,ztp_lines))) + ['\n'] + \
             ["港澳台,#genre#"] + sort_data(gat_dictionary,set(correct_name_data(corrections_name,gat_lines))) + ['\n'] + \
             ["国际台,#genre#"] + sort_data(gj_dictionary,set(correct_name_data(corrections_name,gj_lines))) + ['\n'] + \
             ["纪录片,#genre#"] + sort_data(jlp_dictionary,set(correct_name_data(corrections_name,jlp_lines)))+ ['\n'] + \
             ["动画片,#genre#"] + sorted(set(dhp_lines)) + ['\n'] + \
             ["戏曲频道,#genre#"] + sort_data(xq_dictionary,set(correct_name_data(corrections_name,xq_lines))) + ['\n'] + \
             ["解说频道,#genre#"] + sorted(set(js_lines)) + ['\n'] + \
             ["综艺频道,#genre#"] + sorted(set(correct_name_data(corrections_name,zy_lines))) + ['\n'] + \
             ["音乐频道,#genre#"] + sorted(set(yy_lines)) + ['\n'] + \
             ["游戏频道,#genre#"] + sorted(set(game_lines)) + ['\n'] + \
             ["湖南频道,#genre#"] + sorted(set(correct_name_data(corrections_name,hn_lines))) + ['\n'] + \
             ["广东频道,#genre#"] + sorted(set(correct_name_data(corrections_name,gd_lines))) + ['\n'] + \
             ["春晚,#genre#"] + sort_data(cw_dictionary,set(cw_lines))  + ['\n'] + \
             ["收音机频道,#genre#"] + sort_data(radio_dictionary,set(radio_lines)) 

# 将合并后的文本写入文件
output_file = "iptv.txt"
others_file = "others.txt"
try:
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in all_lines:
            f.write(line + '\n')
    print(f"合并后的文本已保存到文件: {output_file}")

    with open(others_file, 'w', encoding='utf-8') as f:
        for line in other_lines:
            f.write(line + '\n')
    print(f"Others已保存到文件: {others_file}")

except Exception as e:
    print(f"保存文件时发生错误：{e}")

################# 添加生成m3u文件
output_text = "#EXTM3U\n"

with open(output_file, "r", encoding='utf-8') as file:
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
