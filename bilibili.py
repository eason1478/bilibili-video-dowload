import requests
import json
import os
from lxml import etree
import subprocess

# 初始化会话和请求头
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 ...',
    'Accept-Language': 'Chinese',
    'referer': 'https://www.bilibili.com/',
}

url = input('bilibili url:')
try:
    resp = session.get(url, headers=headers)
except requests.exceptions.SSLError:
    print('E:Connection error');input();exit()
except requests.exceptions.ConnectionError:
    print('E:Connection error');input();exit()
except requests.exceptions.MissingSchema:
    print('E:Invalid url');input();exit()
except requests.exceptions.InvalidURL:
    print('E:Invalid url');input();exit()
except requests.exceptions.InvalidSchema:
    print('E:Invalid url');input();exit()
except:
    print('E:Unknown error')
    
resp.encoding = 'utf-8'
tree = etree.HTML(resp.text)

# 获取视频和音频的 URL
play_info = tree.xpath('/html/head/script[4]/text()')
title = tree.xpath('//*[@id="viewbox_report"]/div[1]/div/h1/text()')[0]
play_info_json = json.loads(play_info[0][20:])
try:
    video_url = play_info_json['data']['dash']['video'][0]['baseUrl']
    audio_url = play_info_json['data']['dash']['audio'][0]['baseUrl']
except IndexError:
    print('E:Unknown error');input();exit()

# 创建目录
w = os.getcwd()
video_dir = f'{w}\\bilibili_video'
if not os.path.exists(video_dir):
    os.mkdir(video_dir)

# 下载视频和音频
def download_file(url, file_name):
    response = requests.get(url, headers=headers, stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        with open(file_name, 'wb') as f:
            if file_name[-1] == '4':
                print(f"Downloading video...")
            elif file_name[-1] == '3':
                print(f"Downloading audio...")
            else:
                print('E:Unknown error');input();exit()

            for chunk in response.iter_content(4096):
                f.write(chunk)

    else:
        print(f"E:Download failed\nstatus code:{response.status_code}")
        input()
        exit()

download_file(video_url, os.path.join(video_dir, f'{title}(1).mp4'))
download_file(audio_url, os.path.join(video_dir, f'{title}(1).mp3'))

# 合并文件
ffmpeg_path = f'{w}\\ffmpeg\\bin\\ffmpeg'
output_file = os.path.join(video_dir, f'{title}.mp4')
with open(output_file,'w') as f:
    pass
merge_command = fr'"{ffmpeg_path}" -i "{os.path.join(video_dir, f"{title}(1).mp4")}" -i "{os.path.join(video_dir, f"{title}(1).mp3")}" -c copy "{output_file}"'
try:
    os.remove(os.path.join(video_dir, f'{title}.mp4'))
    result = subprocess.run(merge_command, shell=True, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
except subprocess.CalledProcessError as e:
    print(f"E:Unknown error\n{e.returncode}")
    print(f"{e.stderr}")  # 打印错误输出


# 清理临时文件
print("Removing temporary files...")
os.remove(os.path.join(video_dir, f'{title}(1).mp3'))
os.remove(os.path.join(video_dir, f'{title}(1).mp4'))

print('Task accomplished')
print(f'Video is in: {os.getcwd()}\\bilibili_video')
input()
