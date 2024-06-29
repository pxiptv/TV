import requests
import time
import os
from multiprocessing import Pool
def welcome():
    msg = '''
=========================================================================
888b     d888  .d8888b.  888     888      88888888888                888 
8888b   d8888 d88P  Y88b 888     888          888                    888 
88888b.d88888      .d88P 888     888          888                    888 
888Y88888P888     8888"  888     888          888   .d88b.   .d88b.  888 
888 Y888P 888      "Y8b. 888     888          888  d88""88b d88""88b 888 
888  Y8P  888 888    888 888     888          888  888  888 888  888 888 
888   "   888 Y88b  d88P Y88b. .d88P          888  Y88..88P Y88..88P 888 
888       888  "Y8888P"   "Y88888P"           888   "Y88P"   "Y88P"  888
=========================================================================
'''
    return msg

def get(url,GetStatus=0):
    headers = {
        'Accept-Language': "zh-CN,zh",
        'User-Agent': "Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36",
        'Accept-Encoding': "gzip"
    }
    try:
        res = requests.request("GET", url, headers=headers, timeout=1)  #此处设置超时时间
    except:
        return 0
    if GetStatus == 1:
        return res.status_code
    else:
        if res.status_code == 200:
            res = str(res.content,'utf-8')
        else:
            res = 0
        return res

def checkLink(url):
    res = get(url,1)
    if res == 200:
        return 1
    else:
        return 0

def displayMsg(workname='Default',msg=''):
    now = time.asctime( time.localtime(time.time()) )
    print(f'{now} - {workname}: ' + msg)

def writeFile(filename,content):
    with open(filename,'w',encoding='utf8') as file:
        file.write(content)

def endWith(fileName, *endstring):
    array = map(fileName.endswith, endstring)
    if True in array:
        return True
    else:
        return False

def m3u_filelist(path):
    fileList = os.listdir(path)
    files = []
    for filename in fileList:
        if endWith(filename, '.m3u'):
            files.append(filename)  # 所有m3u文件列表
    return files


def m3u_load(m3uFile):
    channel = {}
    errorNum = 0
    status = 0   # 实时改变步骤状态
    with open(m3uFile, 'r', encoding='utf8') as file:
        displayMsg('m3u_load', f'当前载入列表：{m3uFile}')
        for line in file:
            # 如果当前是描述行：
            if line.startswith('#EXTINF:-1'):
                if status !=0:
                    displayMsg('m3u_load', f'{m3uFile}当前列表缺少行')
                    errorNum+=1
                    exit()
                channelInfo = str(line).replace('\n','')
                status = 1

            # 如果当前是URL行
            if line.startswith('http') or line.startswith('rtsp'): # 当前行为URL
                if status != 1:
                    displayMsg('m3u_load', f'{m3uFile}当前列表缺少行')
                    errorNum += 1
                    exit()
                channel[channelInfo] = str(line).replace('\n','')
                status = 2
            # 上述判断完成
            if status == 2: # 上述步骤处理完毕
                status = 0
        displayMsg('m3u_load', f'{m3uFile} 解析完毕')
        return channel

def work(m3u_data,outputFile,workname='Default'):
    for data in m3u_data:
        txt1 = data.split(',') # 分割节目名称与标签属性
        name = txt1[1] # 电视名称
        url= m3u_data[data] # 播放链接
        if checkLink(url):
            displayMsg(workname, f'{name} 访问成功')
            with open(outputFile, 'a',encoding='utf8') as file:
                file.write(data + '\n')
                file.write(url + '\n')
        else:
            displayMsg(workname, f'{name} 【失败】！')

if __name__ == '__main__':
    print(welcome())

    outputFile = 'checkOutput.m3u'

    displayMsg('Master','开始读取文件列表：')
    fileList = m3u_filelist(os.getcwd())
    
    if outputFile in fileList: # 除去输出文件本身
        fileList.remove(outputFile)

    writeFile(outputFile,'#EXTM3U\n')

    p = Pool(4)
    for file in fileList:
        p.apply_async(work, args=(m3u_load(file),outputFile,file))
    p.close()
    p.join()
