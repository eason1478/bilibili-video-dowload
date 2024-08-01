import requests
import json
import os
import platform
from lxml import etree


session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Accept-Language': 'Chinese',
    'referer':'https://www.bilibili.com/',

}
url = input('bilibili url:')

try:
    resp = session.get(url, headers=headers)
except requests.exceptions.ConnectionError:
    print("E:Connection error")
    input()
    exit()
except requests.exceptions.MissingSchema:
    print("E:Invaild url")
    input()
    exit()
resp.encoding = 'utf-8'
tree = etree.HTML(resp.text)
title = '1'
play_info = tree.xpath('/html/head/script[4]/text()')

try:
    play_info = play_info[0][20:]
except IndexError:
    print('E:Unknown error')
    input()
    exit()
play_info_json = json.loads(play_info)
video_url = play_info_json['data']['dash']['video'][0]['baseUrl']
audio_url = play_info_json['data']['dash']['audio'][0]['baseUrl']
path = os.path.dirname(os.path.abspath(__file__))+'/bilibili_video/'

def download_file(url, file_name):
    # 发送GET请求
    response = requests.get(url,headers=headers,stream=True)
    # 检查请求是否成功
    if response.status_code == 200:
        # 打开一个文件用于写入二进制数据
        with open(file_name, 'wb') as f:
            if file_name[-1] == "4":
                print("Downloading video...")
            else:
                print("Downloading audio...")
            # 遍历响应内容的每一个二进制块，写入到文件中
            for chunk in response.iter_content(1024):
                f.write(chunk)   
    else:
        print(f"E:Download failed\nstatu code:{response.status_code}")
        print(video_url+"\n"+audio_url)
        input()
        exit()

try:
    download_file(video_url,path+'1.mp4')
    download_file(audio_url,path+'1.mp3')
except requests.exceptions.ConnectionError:
    print("E:Connection error")
video_content = requests.get(url=video_url,headers=headers).content
audio_content = requests.get(url=audio_url,headers=headers).content

if not os.path.exists('./bilibili_video'):
    os.mkdir('./bilibili_video')


with open ('./bilibili_video/'+title+'.mp4','wb') as fp1:
    fp1.write(video_content)
    fp1 = path+title+'.mp4'
    
with open ('./bilibili_video/'+title+'.mp3','wb') as fp2:
    fp2.write(audio_content)
    fp2 = path+title+'.mp3'

os.system('ffmpeg -i '+path+'1.mp4'+' -i '+path+'1.mp3'+' -c copy '+path+'2.mp4')
print("Removing temporary files...")
system = platform.system()
if system == "Windows":
    os.system(f'del {path}/1.mp3')
    os.system(f'del {path}/1.mp4')
else:
    os.system(f'rm {path}/1.mp3')
    os.system(f'rm {path}/1.mp4')

print('Task accomplished')
print(f'Video is in:{path[:-1]}')
input()


