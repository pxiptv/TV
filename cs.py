import urllib.request
from urllib.parse import urlparse
import re #正则
import os
from datetime import datetime

# 定义要访问的多个URL
urls = [
    'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u',
    'https://raw.githubusercontent.com/joevess/IPTV/main/iptv.m3u8',
    'https://raw.githubusercontent.com/Supprise0901/TVBox_live/main/live.txt',
    'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
    'https://raw.githubusercontent.com/fenxp/iptv/main/live/ipv6.txt',
    'https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.txt',
    'https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt',
    'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
    'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
    'https://m3u.ibert.me/txt/fmml_ipv6.txt',
    'https://m3u.ibert.me/txt/fmml_dv6.txt',
    'https://m3u.ibert.me/txt/ycl_iptv.txt',
    'https://m3u.ibert.me/txt/y_g.txt',
    'https://m3u.ibert.me/txt/j_iptv.txt',
    'https://live.zhoujie218.top/dsyy/mylist.txt',
    'https://cdn.jsdelivr.net/gh/shidahuilang/shuyuan@shuyuan/iptv.txt',
    'https://gitee.com/xxy002/zhiboyuan/raw/master/zby.txt',
    'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt'
]

#read BlackList 2024-06-17 15:02
def read_blacklist_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    BlackList = [line.split(',')[1].strip() for line in lines if ',' in line]
    return BlackList

blacklist=read_blacklist_from_txt('blacklist.txt') 
blacklist_manual=read_blacklist_from_txt('blacklist_manual.txt') 
combined_blacklist = list(set(blacklist + blacklist_manual))

# 定义多个对象用于存储不同内容的行文本
ys_lines = [] #央视
ws_lines = [] #卫视频道
ty_lines = [] #体育频道
dy_lines = [] #电影
gat_lines = [] #港澳台
gj_lines = [] #国际台
jlp_lines = [] #记录片
dhp_lines = [] #动画片
mx_lines = [] #明星
radio_lines = [] #收音机频道
gd_lines = [] #广东频道
hn_lines = [] #湖南频道
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
    # 处理逻辑
    if "CCTV" in part_str  and "://" not in part_str:
        part_str=part_str.replace("IPV6", "")  #先剔除IPV6字样
        part_str=part_str.replace("PLUS", "+")  #替换PLUS
        part_str=part_str.replace("1080", "")  #替换1080
        part_str=part_str.replace("CCTV-", "CCTV")  #替换 -
        filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K' or char == '+')
        if not filtered_str.strip(): #处理特殊情况，如果发现没有找到频道数字返回原名称
            filtered_str=part_str.replace("CCTV", "")

        if len(filtered_str) > 2 and re.search(r'4K|8K', filtered_str):   # 特殊处理CCTV中部分4K和8K名称
            # 使用正则表达式替换，删除4K或8K后面的字符，并且保留4K或8K
            filtered_str = re.sub(r'(4K|8K).*', r'\1', filtered_str)
            if len(filtered_str) > 2: 
                # 给4K或8K添加括号
                filtered_str = re.sub(r'(4K|8K)', r'(\1)', filtered_str)

        return "CCTV"+filtered_str 
        
    elif "卫视" in part_str:
        # 定义正则表达式模式，匹配“卫视”后面的内容
        pattern = r'卫视「.*」'
        # 使用sub函数替换匹配的内容为空字符串
        result_str = re.sub(pattern, '卫视', part_str)
        return result_str
    
    return part_str

# 准备支持m3u格式
def get_url_file_extension(url):
    # 解析URL
    parsed_url = urlparse(url)
    # 获取路径部分
    path = parsed_url.path
    # 提取文件扩展名
    extension = os.path.splitext(path)[1]
    return extension

def convert_m3u_to_txt(m3u_content):
    # 分行处理
    lines = m3u_content.split('\n')
    
    # 用于存储结果的列表
    txt_lines = []
    
    # 临时变量用于存储频道名称
    channel_name = ""
    
    for line in lines:
        # 过滤掉 #EXTM3U 开头的行
        if line.startswith("#EXTM3U"):
            continue
        # 处理 #EXTINF 开头的行
        if line.startswith("#EXTINF"):
            # 获取频道名称（假设频道名称在引号后）
            channel_name = line.split(',')[-1].strip()
        # 处理 URL 行
        elif line.startswith("http"):
            txt_lines.append(f"{channel_name},{line.strip()}")
    
    # 将结果合并成一个字符串，以换行符分隔
    return '\n'.join(txt_lines)

# 分发直播源，归类，把这部分从process_url剥离出来，为以后加入whitelist源清单做准备。
def process_channel_line(line):
    if  "#genre#" not in line and "," in line and "://" in line:
        channel_name=line.split(',')[0].strip()
        channel_address=line.split(',')[1].strip()
        if channel_address not in combined_blacklist: # 判断当前源是否在blacklist中
            # 根据行内容判断存入哪个对象，开始分发
            if "CCTV" in channel_name: #央视频道
                ys_lines.append(process_name_string(line.strip()))
            elif channel_name in ws_dictionary: #卫视频道
                ws_lines.append(process_name_string(line.strip()))
            elif channel_name in  ty_dictionary:  #体育频道
                ty_lines.append(process_name_string(line.strip()))
            elif channel_name in dy_dictionary:  #电影频道
                dy_lines.append(process_name_string(line.strip()))
            elif channel_name in gat_dictionary:  #港澳台
                gat_lines.append(process_name_string(line.strip()))
            elif channel_name in gj_dictionary:  #国际台
                gj_lines.append(process_name_string(line.strip()))
            elif channel_name in jlp_dictionary:  #纪录片
                jlp_lines.append(process_name_string(line.strip()))
            elif channel_name in dhp_dictionary:  #动画片
                dhp_lines.append(process_name_string(line.strip()))
            elif channel_name in mx_dictionary:  #明星
                mx_lines.append(process_name_string(line.strip()))
            elif channel_name in radio_dictionary:  #收音机频道
                radio_lines.append(process_name_string(line.strip()))
            elif channel_name in gd_dictionary:  #广东频道
                gd_lines.append(process_name_string(line.strip()))
            elif channel_name in hn_dictionary:  #湖南频道
                hn_lines.append(process_name_string(line.strip()))
            else:
                other_lines.append(line.strip())

def process_url(url):
    try:
        # 打开URL并读取内容
        with urllib.request.urlopen(url) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            channel_name=""
            channel_address=""

            #处理m3u和m3u8，提取channel_name和channel_address
            if get_url_file_extension(url)==".m3u" or get_url_file_extension(url)==".m3u8":
                text=convert_m3u_to_txt(text)

            # 逐行处理内容
            lines = text.split('\n')
            for line in lines:
                process_channel_line(line) # 每行按照规则进行分发

    except Exception as e:
        print(f"处理URL时发生错误：{e}")

current_directory = os.getcwd()  #准备读取txt

#读取文本方法
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
#读取文本
ys_dictionary=read_txt_to_array('央视频道.txt') #仅排序用
ws_dictionary=read_txt_to_array('卫视频道.txt') #过滤+排序
ty_dictionary=read_txt_to_array('体育频道.txt') #过滤
dy_dictionary=read_txt_to_array('电影.txt') #过滤
gat_dictionary=read_txt_to_array('港澳台.txt') #过滤
gj_dictionary=read_txt_to_array('国际台.txt') #过滤
jlp_dictionary=read_txt_to_array('纪录片.txt') #过滤
dhp_dictionary=read_txt_to_array('动画片.txt') #过滤
mx_dictionary=read_txt_to_array('明星.txt') #过滤
radio_dictionary=read_txt_to_array('收音机频道.txt') #过滤
gd_dictionary=read_txt_to_array('广东频道.txt') #过滤
hn_dictionary=read_txt_to_array('湖南频道.txt') #过滤

#读取纠错频道名称方法
def load_corrections_name(filename):
    corrections = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split(',')
            correct_name = parts[0]
            for name in parts[1:]:
                corrections[name] = correct_name
    return corrections

#读取纠错文件
corrections_name = load_corrections_name('corrections_name.txt')

#纠错频道名称
#correct_name_data(corrections_name,xxxx)
def correct_name_data(corrections, data):
    corrected_data = []
    for line in data:
        name, url = line.split(',', 1)
        if name in corrections and name != corrections[name]:
            name = corrections[name]
        corrected_data.append(f"{name},{url}")
    return corrected_data

def sort_data(order, data):
    # 创建一个字典来存储每行数据的索引
    order_dict = {name: i for i, name in enumerate(order)}
    
    # 定义一个排序键函数，处理不在 order_dict 中的字符串
    def sort_key(line):
        name = line.split(',')[0]
        return order_dict.get(name, len(order))
    
    # 按照 order 中的顺序对数据进行排序
    sorted_data = sorted(data, key=sort_key)
    return sorted_data

# 循环处理每个URL
for url in urls:
    print(f"处理URL: {url}")
    process_url(url)

# 定义一个函数，提取每行中逗号前面的数字部分作为排序的依据
def extract_number(s):
    num_str = s.split(',')[0].split('-')[1]  # 提取逗号前面的数字部分
    numbers = re.findall(r'\d+', num_str)   #因为有+和K
    return int(numbers[-1]) if numbers else 999
# 定义一个自定义排序函数
def custom_sort(s):
    if "CCTV-4K" in s:
        return 2  # 将包含 "4K" 的字符串排在后面
    elif "CCTV-8K" in s:
        return 3  # 将包含 "8K" 的字符串排在后面 
    elif "(4K)" in s:
        return 1  # 将包含 " (4K)" 的字符串排在后面
    else:
        return 0  # 其他字符串保持原顺序

#读取whitelist,把高响应源从白名单中抽出加入iptv。
whitelist_lines=read_txt_to_array('whitelist.txt') 
for whitelist_line in whitelist_lines:
    if  "#genre#" not in whitelist_line and "," in whitelist_line and "://" in whitelist_line:
        whitelist_parts = whitelist_line.split(",")
        try:
            response_time = float(whitelist_parts[0].replace("ms", ""))
        except ValueError:
            print(f"response_time转换失败: {whitelist_line}")
            response_time = 60000  # 单位毫秒，转换失败给个60秒
        if response_time < 2000:  #2s以内的高响应源
            process_channel_line(",".join(whitelist_parts[1:]))

# 合并所有对象中的行文本（去重，排序后拼接）
version=datetime.now().strftime("%Y%m%d-%H-%M-%S")+",url"
all_lines =  ["更新时间,#genre#"] +[version] + ['\n'] +\
             ["央视频道,#genre#"] + sort_data(ys_dictionary,set(correct_name_data(corrections_name,ys_lines))) + ['\n'] + \
             ["卫视频道,#genre#"] + sort_data(ws_dictionary,set(correct_name_data(corrections_name,ws_lines))) + ['\n'] + \
             ["体育频道,#genre#"] + sort_data(ty_dictionary,set(correct_name_data(corrections_name,ty_lines))) + ['\n'] + \
             ["电影频道,#genre#"] + sort_data(dy_dictionary,set(correct_name_data(corrections_name,dy_lines))) + ['\n'] + \
             ["明星,#genre#"] + sort_data(mx_dictionary,set(correct_name_data(corrections_name,mx_lines))) + ['\n'] + \
             ["港澳台,#genre#"] + sort_data(gat_dictionary,set(correct_name_data(corrections_name,gat_lines))) + ['\n'] + \
             ["国际台,#genre#"] + sort_data(gj_dictionary,set(correct_name_data(corrections_name,gj_lines))) + ['\n'] + \
             ["纪录片,#genre#"] + sort_data(jlp_dictionary,set(correct_name_data(corrections_name,jlp_lines)))+ ['\n'] + \
             ["动画片,#genre#"] + sorted(set(dhp_lines)) + ['\n'] + \
             ["湖南频道,#genre#"] + sorted(set(correct_name_data(corrections_name,hn_lines))) + ['\n'] + \
             ["广东频道,#genre#"] + sorted(set(correct_name_data(corrections_name,gd_lines))) + ['\n'] + \
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

#备用1：http://tonkiang.us
#备用2：
#备用3：
