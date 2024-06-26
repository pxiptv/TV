import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import os
import re #正则
from urllib.parse import urlparse


timestart = datetime.now()

# 读取文件内容
def read_txt_file(file_path):
    skip_strings = ['#genre#', '192', '198', 'ChiSheng9', 'epg.pw', '/udp/', '(576p)', '(540p)', '(360p)', '(480p)', '(180p)', '(404p)', 'generationnexxxt', 'live.goodiptv.club']  # 定义需要跳过的字符串数组['#', '@', '#genre#'] 
    required_strings = ['://']  # 定义需要包含的字符串数组['必需字符1', '必需字符2'] 

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [
            line for line in file
            if not any(skip_str in line for skip_str in skip_strings) and all(req_str in line for req_str in required_strings)
        ]
    return lines

def read_txt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.readlines()

def append_to_file(filename, lines):
    with open(filename, 'a', encoding='utf-8') as f:
        for line in lines:
            f.write(line)

# 格式化频道名称
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
    part_str = part_str.replace("「IPV6」", "")  # 剔除 「IPV6」
    part_str = part_str.replace("IPV6", "")  # 剔除 IPV6
    part_str = part_str.replace("「IPV4」", "")  # 剔除 「IPV4」
    part_str = part_str.replace("IPV4", "")  # 剔除 IPV4 
    part_str = part_str.replace("[V4]", "")  # 剔除 [V4]
    part_str = part_str.replace("[V6]", "")  # 剔除 [V6]
    part_str = part_str.replace("𝟘", "0")  # 替换 𝟘
    part_str = part_str.replace("𝟙", "1")  # 替换 𝟙
    part_str = part_str.replace("𝟚", "2")  # 替换 𝟚
    part_str = part_str.replace("𝟛", "3")  # 替换 𝟛
    part_str = part_str.replace("𝟜", "4")  # 替换 𝟜
    part_str = part_str.replace("𝟝", "5")  # 替换 𝟝
    part_str = part_str.replace("𝟞", "6")  # 替换 𝟞
    part_str = part_str.replace("𝟟", "7")  # 替换 𝟟
    part_str = part_str.replace("𝟠", "8")  # 替换 𝟠
    part_str = part_str.replace("𝟡", "9")  # 替换 𝟡
    part_str = part_str.replace("移动咪咕直播", "咪咕体育")  # 替换 移动咪咕直播
    part_str = part_str.replace("咪咕直播", "咪咕体育")  # 替换 咪咕直播
    part_str = part_str.replace("咪咕视频", "咪咕体育")  # 替换 咪咕视频
    part_str = part_str.replace("咪咕体育-", "咪咕体育")  # 替换 咪咕体育
    part_str = part_str.replace("咪咕体育_", "咪咕体育")  # 替换 咪咕体育
    part_str = part_str.replace("•", "")  # 先剔除 •  
    part_str = part_str.replace(" (1080p)", "")  # 替换 1080p
    part_str = part_str.replace(" (900p)", "")  # 替换 900p
    part_str = part_str.replace(" (720p)", "")  # 替换 720p
    part_str = part_str.replace(" (576p)", "")  # 替换 576p
    part_str = part_str.replace(" (540p)", "")  # 替换 540p
    part_str = part_str.replace(" (480p)", "")  # 替换 480p
    part_str = part_str.replace(" (360p)", "")  # 替换 360p
    part_str = part_str.replace(" (240p)", "")  # 替换 240p
    part_str = part_str.replace(" (180p)", "")  # 替换 180p
    part_str = part_str.replace("  [Geo-blocked]", "")  # 替换[Geo-blocked]
    
    if "CCTV" in part_str and "://" not in part_str:
        part_str = part_str.replace("PLUS", "+")  # 替换 PLUS
        part_str = part_str.replace("1080", "")  # 替换 1080
        filtered_str = ''.join(char for char in part_str if char.isdigit() or char == 'K' or char == '+')
        if not filtered_str.strip():  # 处理特殊情况，如果发现没有找到频道数字返回原名称
            filtered_str = part_str.replace("CCTV", "")
        if len(filtered_str) > 2 and re.search(r'4K|8K', filtered_str):  # 特殊处理CCTV中部分4K和8K名称
            # 使用正则表达式替换，删除4K或8K后面的字符，并且保留4K或8K
            filtered_str = re.sub(r'(4K|8K).*', r'\1', filtered_str)
            if len(filtered_str) > 2: 
                # 给4K或8K添加括号
                filtered_str = re.sub(r'(4K|8K)', r'(\1)', filtered_str)
        return "CCTV" + filtered_str 
    elif "卫视" in part_str:
        part_str = part_str.replace("-卫视", "卫视")  # 替换 -卫视
        # 定义正则表达式模式，匹配“卫视”后面的内容
        pattern = r'卫视「.*」'
        # 使用sub函数替换匹配的内容为空字符串
        result_str = re.sub(pattern, '卫视', part_str)
        return result_str
    return part_str

def filter_and_save_channel_names(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    processed_lines = []
    for line in lines:
        if ',' in line:
            channel_name, url = line.split(',', 1)
            processed_channel_name = process_name_string(channel_name)
            processed_line = f"{processed_channel_name},{url}"
            processed_lines.append(processed_line)
        else:
            processed_lines.append(line)
    
    with open(input_file, 'w', encoding='utf-8') as out_file:
        for line in processed_lines:
            out_file.write(line)
            
# 检测URL是否可访问并记录响应时间
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}
def check_url(url, timeout=8):
    try:
    	if  "://" in url:
            start_time = time.time()
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
                if response.status == 200:
                    return elapsed_time, True
    except Exception as e:
        print(f"Error checking {url}: {e}")
    return None, False

# 处理单行文本并检测URL
def process_line(line):
    if "#genre#" in line or "://" not in line :
        return None, None  # 跳过包含“#genre#”的行
    parts = line.split(',')
    if len(parts) == 2:
        name, url = parts
        elapsed_time, is_valid = check_url(url.strip())
        if is_valid:
            return elapsed_time, line.strip()
        else:
            return None, line.strip()
    return None, None

# 多线程处理文本并检测URL
def process_urls_multithreaded(lines, max_workers=18):
    blacklist =  [] 
    successlist = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_line, line): line for line in lines}
        for future in as_completed(futures):
            elapsed_time, result = future.result()
            if result:
                if elapsed_time is not None:
                    successlist.append(f"{elapsed_time:.2f}ms,{result}")
                else:
                    blacklist.append(result)
    return successlist, blacklist

# 写入文件内容
def write_txt_file(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')
            
# 写入文件
def write_list(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data_list:
            file.write(item + '\n')

# 合并两个文件的内容并写入输出文件
def merge_files(file1, file2, output_file):
    lines1 = read_txt_file(file1)
    lines2 = read_txt_file(file2)

# 合并并去重
    merged_lines = list(set(lines1 + lines2))
    write_txt_file(output_file, merged_lines)
    
# 删除重复行
def remove_duplicates(lines, file_paths):
    for file_path in file_paths:
        file_lines = read_txt_file(file_path)
        lines = [line for line in lines if line not in file_lines]
    return lines
    
# 过滤掉在 comparison_files 中出现的行
def extract_lines_with_colon(files):
    lines_with_colon = []

    for file in files:
        lines = read_txt_file(file)
        for line in lines:
            if ',' in line:
                parts = line.split(',', 1)  # 以第一个逗号为分割点
                if '://' in parts[1]:
                    lines_with_colon.append(parts[1].strip())

    return lines_with_colon

# 将iptv.txt转换为iptv.m3u文件
def convert_to_m3u(iptv_file, m3u_file):
    lines = read_txt(iptv_file)
    with open(m3u_file, 'w', encoding='utf-8') as file:
        file.write("#EXTM3U\n")
        for line in lines:
            parts = line.split(',', 1)
            if len(parts) == 2:
                file.write(f"#EXTINF:-1 group-title=\"{group_name}\",{parts[0]}\n")
                file.write(f"{parts[1]}\n")
                
# 增加外部url到检测清单，同时支持检测m3u格式url
# urls里所有的源都读到这里。
urls_all_lines = []

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

def process_url(url):
    try:
        # 打开URL并读取内容
        with urllib.request.urlopen(url) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            if get_url_file_extension(url)==".m3u" or get_url_file_extension(url)==".m3u8":
                urls_all_lines.append(convert_m3u_to_txt(text))
            elif get_url_file_extension(url)==".txt":
                lines = text.split('\n')
                for line in lines:
                    if  "#genre#" not in line and "," in line and "://" in line:
                        #channel_name=line.split(',')[0].strip()
                        #channel_address=line.split(',')[1].strip()
                        urls_all_lines.append(line.strip())
    
    except Exception as e:
        print(f"处理URL时发生错误：{e}")


if __name__ == "__main__":
    # 定义要访问的多个URL
    urls = [
        'https://raw.githubusercontent.com/YueChan/Live/main/IPTV.m3u',
        'https://raw.githubusercontent.com/BurningC4/Chinese-IPTV/master/TV-IPV4.m3u',
        'https://raw.githubusercontent.com/suxuang/myIPTV/main/ipv6.m3u',
        'https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u',
        'https://raw.githubusercontent.com/iptv-org/iptv/master/streams/cn.m3u',
        'https://raw.githubusercontent.com/kimwang1978/tvbox/main/%E5%A4%A9%E5%A4%A9%E5%BC%80%E5%BF%83/lives/%E2%91%AD%E5%BC%80%E5%BF%83%E7%BA%BF%E8%B7%AF.txt',
        'https://raw.githubusercontent.com/joevess/IPTV/main/iptv.m3u8',
        'https://raw.githubusercontent.com/Supprise0901/TVBox_live/main/live.txt',
        'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
        'https://raw.githubusercontent.com/fenxp/iptv/main/live/ipv6.txt',
        'https://raw.githubusercontent.com/yuanzl77/IPTV/main/live.txt',
        'https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt',
        'https://raw.githubusercontent.com/maitel2020/iptv-self-use/main/iptv.txt',
        'https://raw.githubusercontent.com/zwc456baby/iptv_alive/master/live.txt',
        'https://raw.githubusercontent.com/zjykfy/ykfy/main/all.m3u',
        'https://m3u.ibert.me/txt/fmml_ipv6.txt',
        'https://m3u.ibert.me/txt/fmml_dv6.txt',
        'https://m3u.ibert.me/txt/ycl_iptv.txt',
        'https://m3u.ibert.me/txt/y_g.txt',
        'https://m3u.ibert.me/txt/j_iptv.txt',
        'https://live.zhoujie218.top/dsyy/mylist.txt',
        'https://iptv-org.github.io/iptv/countries/cn.m3u',
        'https://live.fanmingming.com/tv/m3u/ipv6.m3u',
        'https://cdn.jsdelivr.net/gh/shidahuilang/shuyuan@shuyuan/iptv.txt',
        'https://gitee.com/xxy002/zhiboyuan/raw/master/zby.txt',
        'https://gitee.com/happy-is-not-closed/IPTV/raw/main/IPTV.m3u',
        'https://gitee.com/guangshanleige/iptv/raw/master/iptv.m3u',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/wang-tvlive.txt',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt'
    ]
    for url in urls:
        print(f"处理URL: {url}")
        process_url(url)   #读取上面url清单中直播源存入urls_all_lines

    # 写入 online.txt 文件
    write_txt_file('online.txt',urls_all_lines)
    online_file = 'online.txt'
    filter_and_save_channel_names(online_file)
    
    input_file1 = 'iptv.txt'  # 输入文件路径
    input_file2 = 'blacklist.txt'  # 输入文件路径2 
    success_file = 'whitelist.txt'  # 成功清单文件路径
    blacklist_file = 'blacklist.txt'  # 黑名单文件路径

    # 合并 iptv.txt, blacklist.txt 的所有行
    comparison_files = ['iptv.txt', 'blacklist.txt']

    # 过滤 新获取的网址与历史文件的重复行
    LS_lines = extract_lines_with_colon(comparison_files)
    
    # 提取 online_file 中逗号之后并包含 "://" 的内容
    online_lines = read_txt_file(online_file)
    OL_lines = [line.split(',', 1)[1].strip() for line in online_lines if ',' in line and '://' in line.split(',', 1)[1]]

    # 将 OL_lines 中不在 LS_lines 的行存入 filtered_live_lines
    filtered_live_lines = [line for line in OL_lines if line not in LS_lines]
    
    # 读取输入文件内容
    lines1 = read_txt_file(input_file1)
    lines2 = read_txt_file(input_file2)
    lines=list(set(filtered_live_lines + lines1))
    lines = [line.strip() for line in lines if line.strip()]
    write_txt_file('tv.txt',lines)

    # 清空 live.txt 文件后读取 channel.txt 文件
    open('live.txt', 'w').close()
    channel_lines = read_txt('channel.txt')
    tv_lines = read_txt_file('tv.txt')

    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file('live.txt', [channel_line])
        else:
            channel_name = channel_line.split(",")[0].strip()
            print(f"Processing channel: {channel_name}")  # 调试信息
            matching_lines = [tv_line for tv_line in tv_lines if tv_line.split(",http")[0].strip() == channel_name]
            append_to_file('live.txt', matching_lines)

    print("待检测文件已生成。")
    
    lines = read_txt_file('live.txt')

    # 计算合并后合计个数
    urls_hj = len(lines)
    
    # 处理URL并生成成功清单和黑名单
    successlist, blacklist = process_urls_multithreaded(lines)
    
    # 给successlist, blacklist排序
    # 定义排序函数
    def successlist_sort_key(item):
        time_str = item.split(',')[0].replace('ms', '')
        return float(time_str)
    
    successlist=sorted(successlist, key=successlist_sort_key)
    blacklist=sorted(blacklist)

    # 计算check后ok和ng个数
    urls_ok = len(successlist)
    urls_ng = len(blacklist)

    # 把successlist整理一下，生成一个可以直接引用的源，方便用zyplayer手动check
    def remove_prefix_from_lines(lines):
        result = []
        for line in lines:
            if  "#genre#" not in line and "," in line and "://" in line:
                parts = line.split(",")
                result.append(",".join(parts[1:]))
        return result

    # 加时间戳等
    version=datetime.now().strftime("%Y%m%d-%H-%M-%S")+",url"
    successlist_tv = ["更新时间,#genre#"] +[version] + ['\n'] +\
                  ["whitelist,#genre#"] + remove_prefix_from_lines(successlist)
    successlist = ["更新时间,#genre#"] +[version] + ['\n'] +\
                  ["RespoTime,whitelist,#genre#"] + successlist
    blacklist = ["更新时间,#genre#"] +[version] + ['\n'] +\
                ["blacklist,#genre#"]  + blacklist

    # 写入成功清单文件
    write_list(success_file, successlist_tv)
    write_list(input_file1, successlist_tv)

    # 写入黑名单文件
    merged_lines = list(set(blacklist + lines2))
    merged_lines = [line.strip() for line in merged_lines if line.strip()]
    write_txt_file(blacklist_file, merged_lines)

    print(f"成功清单文件已生成: {success_file}")
    print(f"黑名单文件已生成: {blacklist_file}")
    print(f"iptv.txt 文件已生成: {input_file1}")

    # 清空 iptv.txt 文件后读取 channel.txt 文件
    channel_lines = read_txt('channel.txt')
    tv_lines = read_txt_file('iptv.txt')
    open('iptv.txt', 'w').close()

    # 处理 channel.txt 文件中的每一行
    for channel_line in channel_lines:
        if "#genre#" in channel_line:
            append_to_file('iptv.txt', [channel_line])
        else:
            channel_name = channel_line.split(",")[0].strip()
            matching_lines = [tv_line for tv_line in tv_lines if tv_line.split(",http")[0].strip() == channel_name]
            append_to_file('iptv.txt', matching_lines)
            
    # 生成 iptv.m3u 文件 x-tvg-url="https://raw.bgithub.xyz/Troray/IPTV/main/tvxml.xml,https://raw.bgithub.xyz/Meroser/EPG-test/main/tvxml-test.xml.gz" catchup="append" catchup-source="?playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"

    output_text = '#EXTM3U x-tvg-url="https://raw.bgithub.xyz/Troray/IPTV/main/tvxml.xml,https://raw.bgithub.xyz/Meroser/EPG-test/main/tvxml-test.xml.gz" catchup="append" catchup-source="?playseek=${(b)yyyyMMddHHmmss}-${(e)yyyyMMddHHmmss}"
\n'

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

    # 执行的代码
    timeend = datetime.now()

    # 计算时间差
    elapsed_time = timeend - timestart
    total_seconds = elapsed_time.total_seconds()

    # 转换为分钟和秒
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    # 格式化开始和结束时间
    timestart_str = timestart.strftime("%Y%m%d_%H_%M_%S")
    timeend_str = timeend.strftime("%Y%m%d_%H_%M_%S")

    print(f"开始时间: {timestart_str}")
    print(f"结束时间: {timeend_str}")
    print(f"执行时间: {minutes} 分 {seconds} 秒")
    print(f"urls_hj: {urls_hj} ")
    print(f"urls_ok: {urls_ok} ")
    print(f"urls_ng: {urls_ng} ")


