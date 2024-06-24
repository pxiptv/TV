import requests
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 定义超时时间
TIMEOUT = 10000  # 响应时间限制，单位毫秒
CHECK_TIMEOUT = 20000  # 检查超时时间，单位毫秒

# 定义一个自定义异常，用于超过CHECK_TIMEOUT时抛出
class TimeoutError(Exception):
    pass

# 定义一个函数来检测单个网址
def check_url(channel_name, url):
    start_time = time.time()
    try:
        # 设置一个超时时间，如果请求时间超过CHECK_TIMEOUT，则抛出TimeoutError
        response = requests.get(url, timeout=(CHECK_TIMEOUT / 1000))  # 将毫秒转换为秒
        if (time.time() - start_time) * 1000 > CHECK_TIMEOUT:
            raise TimeoutError("请求超时")
        response.raise_for_status()  # 检查请求是否成功
        elapsed_time = (time.time() - start_time) * 1000  # 转换为毫秒
        return channel_name, url, elapsed_time
    except requests.exceptions.RequestException as e:
        # 捕获请求异常，记录无响应或响应错误
        return channel_name, url, f"{e}"
    except TimeoutError as e:
        # 捕获自定义的TimeoutError异常，记录超时信息
        return channel_name, url, str(e)

# 定义一个函数来处理检测结果并写入文件
def process_result(channel_name, url, result, file_a, file_b):
    if isinstance(result, str) and "ms" in result:
        # 如果结果包含"ms"，说明是正常响应时间
        file_a.write(f'{channel_name}：{url} - {result}\n')
    elif isinstance(result, str) and "RequestException" in result:
        # 如果结果包含"RequestException"，说明请求异常
        file_b.write(f'{channel_name}：{url} - 错误：{result}\n')
    else:
        # 如果结果为TimeoutError，写入超时信息
        file_b.write(f'{channel_name}：{url} - 超时：{result}\n')

# 读取iptv.txt文件
with open('iptv.txt', 'r') as file:
    lines = file.readlines()

# 打开whitelist.txt和blacklist.txt文件，准备写入结果
with open('whitelist.txt', 'w') as file_a, open('blacklist.txt', 'w') as file_b:
    # 使用线程池
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_url = {executor.submit(check_url, line.split('，')[0].strip(), line.split('，')[1].strip()): line for line in lines}
        for future in as_completed(future_to_url):
            line = future_to_url[future]
            channel_name, url, result = future.result()
            process_result(channel_name, url, result, file_a, file_b)

print("检测完成，结果已分别存入whitelist.txt和blacklist.txt。")
