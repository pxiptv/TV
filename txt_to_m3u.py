# 导入sys模块，用于处理命令行参数
import sys

# 定义一个函数convert，参数为txt_file和m3u_file，分别表示输入的文本文件和输出的M3U文件
def convert(txt_file, m3u_file):
    # 以读模式打开txt_file，以写模式打开m3u_file
    with open(txt_file, 'r') as txt, open(m3u_file, 'w') as m3u:
        # 向m3u文件写入M3U文件的头部标识
        m3u.write("#EXTM3U\n")

        # 初始化group_name变量，用于存储组名
        group_name = ""
        # 逐行读取txt文件
        for line in txt:
            # 去除行首尾的空白字符
            line = line.strip()
            # 按逗号分割行，得到一个包含两个元素的列表parts
            parts = line.split(",")
            # 如果parts长度为2且行中包含"#genre#"字符串，表示这是一个组名行
            if len(parts) == 2 and "#genre#" in line:
                # 更新group_name为parts的第一个元素
                group_name = parts[0]
            # 如果parts长度为2但不包含"#genre#"字符串，表示这是一个普通的媒体行
            elif len(parts) == 2:
                # 向m3u文件写入媒体信息行，包括组名和媒体标题
                m3u.write(f"#EXTINF:-1 group-title=\"{group_name}\",{parts[0]}\n")
                # 向m3u文件写入媒体URL
                m3u.write(f"{parts[1]}\n")

# 如果当前脚本是主程序（即不是被其他模块导入）
if __name__ == "__main__":
    # 检查命令行参数的数量是否等于3（脚本名+两个参数）
    if len(sys.argv) != 3:
        # 如果不是，打印用法提示并退出程序，返回状态码1表示错误
        print("Usage: convert_txt_to_m3u.py <input.txt> <output.m3u>")
        sys.exit(1)
    
    # 获取第一个和第二个命令行参数，分别表示输入的txt文件和输出的m3u文件
    input_txt = sys.argv[1]
    output_m3u = sys.argv[2]
    # 调用convert函数进行转换
    convert(input_txt, output_m3u)

