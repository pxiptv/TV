import urllib.request
import re
import os
from datetime import datetime

# 定义要访问的多个URL
urls = [
    'https://raw.githubusercontent.com/Supprise0901/TVBox_live/main/live.txt',
    'https://raw.githubusercontent.com/Guovin/TV/gd/result.txt',
    'https://raw.githubusercontent.com/ssili126/tv/main/itvlist.txt',
    'https://m3u.ibert.me/txt/fmml_ipv6.txt',
    'https://m3u.ibert.me/txt/ycl_iptv.txt',
    'https://m3u.ibert.me/txt/y_g.txt',
    'https://m3u.ibert.me/txt/j_home.txt',
    'https://raw.githubusercontent.com/gaotianliuyun/gao/master/list.txt',
    'https://gitee.com/xxy002/zhiboyuan/raw/master/zby.txt',
    'https://raw.githubusercontent.com/mlvjfchen/TV/main/iptv_list.txt',
    'https://raw.githubusercontent.com/fenxp/iptv/main/live/ipv6.txt',
    'https://raw.githubusercontent.com/fenxp/iptv/main/live/tvlive.txt',
    'https://gitlab.com/p2v5/wangtv/-/raw/main/lunbo.txt'
]

# 定义多个对象用于存储不同内容的行文本
ys_lines = []  # 央视频道
ws_lines = []  # 卫视频道
ty_lines = []  # 体育频道
dy_lines = []
dsj_lines = []
gat_lines = []  # 港澳台
gj_lines = []  # 国际台
jlp_lines = []  # 记录片
dhp_lines = []  # 动画片
xq_lines = []  # 戏曲
js_lines = []  # 解说
cw_lines = []  # 春晚
mx_lines = []  # 明星
ztp_lines = []  # 主题片
zy_lines = []  # 综艺频道
yy_lines = []  # 音乐频道
game_lines = []  # 游戏频道
radio_lines = []  # 收音机频道
gd_lines = []  # 地方台-广东频道
hn_lines = []  # 地方台-湖南频道

other_lines = []

def process_url(url):
    try:
        # 打开URL并读取内容
        with urllib.请求.urlopen(url) as response:
            # 以二进制方式读取数据
            data = response.read()
            # 将二进制数据解码为字符串
            text = data.decode('utf-8')
            
            # 逐行处理内容
            lines = text.split('\n')
            for line in lines:
                if "#genre#" not in line and "," in line and "://" in line:
                    channel_name = line.split(',')[0].strip()
                    channel_address = line.split(',')[1].strip()
                    # 根据行内容判断存入哪个对象
                    if "CCTV" in channel_name:
                        ys_lines.append(line.strip())
                    elif "卫视" in channel_name:
                        ws_lines.append(line.strip())
                    elif "体育" in channel_name:
                        ty_lines.append(line.strip())
                    elif "电影" in channel_name:
                        dy_lines.append(line.strip())
                    elif "电视剧" in channel_name:
                        dsj_lines.append(line.strip())
                    elif "港澳台" in channel_name:
                        gat_lines.append(line.strip())
                    elif "国际台" in channel_name:
                        gj_lines.append(line.strip())
                    elif "纪录片" in channel_name:
                        jlp_lines.append(line.strip())
                    elif "动画片" in channel_name:
                        dhp_lines.append(line.strip())
                    elif "戏曲" in channel_name:
                        xq_lines.append(line.strip())
                    elif "解说" in channel_name:
                        js_lines.append(line.strip())
                    elif "春晚" in channel_name:
                        cw_lines.append(line.strip())
                    elif "明星" in channel_name:
                        mx_lines.append(line.strip())
                    elif "主题片" in channel_name:
                        ztp_lines.append(line.strip())
                    elif "综艺" in channel_name:
                        zy_lines.append(line.strip())
                    elif "音乐" in channel_name:
                        yy_lines.append(line.strip())
                    elif "游戏" in channel_name:
                        game_lines.append(line.strip())
                    elif "收音机" in channel_name:
                        radio_lines.append(line.strip())
                    elif "广东" in channel_name:
                        gd_lines.append(line.strip())
                    elif "湖南" in channel_name:
                        hn_lines.append(line.strip())
                    else:
                        other_lines.append(line.strip())
            
    except Exception as e:
        print(f"处理URL时发生错误：{e}")

# 循环处理每个URL
for url in urls:
    print(f"处理URL: {url}")
    process_url(url)

# 将处理后的数据写入文件
output_file = "cctv.txt"
others_file = "others_output.txt"

try:
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in ys_lines + ws_lines + ty_lines + dy_lines + dsj_lines + gat_lines + gj_lines + jlp_lines + dhp_lines + xq_lines + js_lines + cw_lines + mx_lines + ztp_lines + zy_lines + yy_lines + game_lines + radio_lines + gd_lines + hn_lines:
            f.write(line + '\n')
    print(f"合并后的文本已保存到文件: {output_file}")

    with open(others_file, 'w', encoding='utf-8') as f:
        for line in other_lines:
            f.write(line + '\n')
    print(f"Others已保存到文件: {others_file}")

except Exception as e:
    print(f"保存文件时发生错误：{e}")

# 生成M3U文件
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

with open("cctv.m3u", "w", encoding='utf-8') as file:
    file.write(output_text)

print("cctv.m3u文件已生成。")
