import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from datetime import datetime
import os
from urllib.parse import urlparse


timestart = datetime.now()

# 读取文件内容
def read_txt_file(file_path):
    skip_strings = ['#genre#', '192', '198', 'ChiSheng9', 'epg.pw', 'generationnexxxt.com']  # 定义需要跳过的字符串数组['#', '@', '#genre#'] 
    required_strings = ['://']  # 定义需要包含的字符串数组['必需字符1', '必需字符2'] 

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = [
            line for line in file
            if not any(skip_str in line for skip_str in skip_strings) and all(req_str in line for req_str in required_strings)
        ]
    return lines

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

def append_to_file(file_path, lines):
    with open(file_path, 'a', encoding='utf-8') as file:
        for line in lines:
            file.write(line + '\n')

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
def filter_lines(input_file, comparison_files):
    # 读取对比文件中的所有行
    comparison_lines = set()
    for file in comparison_files:
        comparison_lines.update(read_txt_file(file))

    # 读取输入文件并过滤行
    input_lines = read_txt_file(input_file)
    filtered_lines = [line for line in input_lines if line not in comparison_lines]
    
    return filtered_lines
    
# 写入文件
def write_list(file_path, data_list):
    with open(file_path, 'w', encoding='utf-8') as file:
        for item in data_list:
            file.write(item + '\n')

# 将iptv.txt转换为iptv.m3u文件
def convert_to_m3u(iptv_file, m3u_file):
    lines = read_txt_file(iptv_file)
    with open(m3u_file, 'w', encoding='utf-8') as file:
        file.write("#EXTM3U\n")
        for line in lines:
            parts = line.split(',', 1)
            if len(parts) == 2:
                file.write(f"#EXTINF:-1,{parts[0]}\n")
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
        'https://m3u.ibert.me/txt/fmml_ipv6.txt',
        'https://m3u.ibert.me/txt/fmml_dv6.txt',
        'https://m3u.ibert.me/txt/ycl_iptv.txt',
        'https://m3u.ibert.me/txt/y_g.txt',
        'https://m3u.ibert.me/txt/j_iptv.txt',
        'https://live.zhoujie218.top/dsyy/mylist.txt',
        'https://cdn.jsdelivr.net/gh/shidahuilang/shuyuan@shuyuan/iptv.txt',
        'https://gitee.com/xxy002/zhiboyuan/raw/master/zby.txt',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/wang-tvlive.txt',
        'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt'
    ]
    for url in urls:
        print(f"处理URL: {url}")
        process_url(url)   #读取上面url清单中直播源存入urls_all_lines

    input_file1 = 'iptv.txt'  # 输入文件路径
    input_file2 = 'blacklist.txt'  # 输入文件路径2 
    success_file = 'whitelist.txt'  # 成功清单文件路径
    blacklist_file = 'blacklist.txt'  # 黑名单文件路径

    # 合并 iptv.txt, blacklist.txt 和 others.txt 的所有行
    comparison_files = ['iptv.txt', 'blacklist.txt', 'others.txt']

    # 过滤 新获取的网址中历史文件的重复行
    filtered_live_lines = filter_lines(urls_all_lines, comparison_files)
    
    # 读取输入文件内容
    lines1 = read_txt_file(input_file1)
    #lines2 = read_txt_file(input_file2)
    lines=list(set(filtered_live_lines + lines1))
    
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
    successlist = ["更新时间,#genre#"] +[version] + ['\n'] +\
                  ["RespoTime,whitelist,#genre#"] + successlist
    blacklist = ["更新时间,#genre#"] +[version] + ['\n'] +\
                ["blacklist,#genre#"]  + blacklist

    # 写入成功清单文件
    write_list(success_file, successlist)
    write_list(input_file1, successlist)

    # 写入黑名单文件
    write_list(blacklist_file, blacklist)

    print(f"成功清单文件已生成: {success_file}")
    print(f"黑名单文件已生成: {blacklist_file}")
    print(f"iptv.txt 文件已生成: {input_file1}")

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
