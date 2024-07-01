import subprocess
import time

# 定义超时时间
TIMEOUT = 2

# 读取test.txt文件
with open('test.txt', 'r') as file:
    for line in file:
        # 分割字符串，获取URL
        parts = line.strip().split(',')
        if len(parts) > 1:
            prefix = ','.join(parts[:-1])
            url = parts[-1].strip()

            # 尝试使用ffmpeg检测URL
            try:
                result = subprocess.run(
                    ['ffmpeg', '-i', url, '-f', 'null', '-'],
                    stdout=subprocess.DEVNULL,  # 不打印输出
                    stderr=subprocess.DEVNULL,  # 不打印错误
                    timeout=TIMEOUT
                )
                # 如果ffmpeg没有超时，说明URL是有效的
                if result.returncode == 0:
                    with open('live.txt', 'a') as live_file:
                        live_file.write(f"{prefix},{url}\n")
            except subprocess.TimeoutExpired:
                # 如果ffmpeg超时，跳过当前URL
                print(f"Timeout occurred for URL: {url}")

print("Script completed.")
