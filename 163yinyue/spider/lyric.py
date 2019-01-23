import requests
import json
from bs4 import BeautifulSoup
from spider import setting

class Lyric:
    def __init__(self):
        self.headers = setting.headers
        self.lyric_url = setting.lyric_url

    def get_lyric(self, id):
        lyric_url = self.lyric_url.format(id)
        session = requests.Session()
        try:
            soup = BeautifulSoup(session.post(lyric_url, headers=self.headers).text, 'lxml')
            lyric = json.loads(soup.find('p').get_text())['lrc']['lyric']
            print(lyric)
        except Exception as e:
            print("抓取歌词页面存在问题：{} 歌曲ID：{}".format(e, id))


if __name__ == '__main__':
    lyric = Lyric()
    lyric.get_lyric('106348')
