import requests
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}


def request_song(song_id):
    request_url = 'http://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)
    music = requests.get(request_url, headers=headers)
    # print(music.content)
    response_content_type = dict(music.headers)['Content-Type']
    if 'audio' in response_content_type:    # 为True时代表得到的是音乐文件
        file_url = os.getcwd() + r'\core\spider\spider_files\music\{}.mp3'.format(song_id)
        # print(file_url)
        if os.path.isfile(file_url):
            return True
        with open(file_url, 'wb') as f:
            f.write(music.content)
        return True
    elif 'html' in response_content_type:   # 为True代表得到的是html文件，一般为没有版权或者需要vip
        return False


if __name__ == '__main__':
    # 可以听的
    request_song(1463165983)
    # 需要购买
    # request_song(1407358755)
