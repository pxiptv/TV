import subprocess
import time

def check_url(url):
    try:
        # 使用ffmpeg检测URL，5秒无响应则跳过
        result = subprocess.run(['ffmpeg', '-i', url, '-f', 'null', '-'],
                                timeout=5, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False

def process_file(input_file, output_file):
    with open(input_file, 'r') as f, open(output_file, 'w') as out:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) < 2:
                continue
            key, url = parts[0], parts[1]
            if check_url(url):
                out.write(f"{key},{url}\n")
                print(f"检测成功: {key} -> {url}")
            else:
                print(f"检测失败: {key} -> {url}")

if __name__ == "__main__":
    process_file('test.txt', 'others.txt')
