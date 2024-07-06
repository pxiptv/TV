import subprocess
import time

def check_url_with_ffmpeg(url):
    try:
        # 使用 ffmpeg -i 检查 URL
        result = subprocess.run(
            ["ffmpeg", "-i", url, "-t", "2", "-f", "null", "-"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
        if result.returncode == 0:
            return True
        else:
            return False
    except subprocess.TimeoutExpired:
        return False
    except Exception as e:
        return False

# 读取 live.txt 文件
with open('live.txt', 'r') as file:
    lines = file.readlines()

# 打开 whitelist.txt 和 blacklist.txt 文件
with open('whitelist.txt', 'w') as whitelist, open('blacklist.txt', 'w') as blacklist:
    for line in lines:
        line = line.strip()
        if "://" in line:
            url = line.split(',')[1].strip()
            print(f"正在检测: {url}")
            if check_url_with_ffmpeg(url):
                whitelist.write(line + '\n')
                print(f"{url} 可访问，已存入 whitelist.txt")
            else:
                blacklist.write(line + '\n')
                print(f"{url} 无法访问，已存入 blacklist.txt")
            time.sleep(2)

print("频道检测完毕 whitelist.txt  blacklist.txt 文件已生成。")
