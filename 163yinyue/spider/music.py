import requests
import json
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
from spider import setting
from utils import pysql
import settings

class music:
    def __init__(self):
        self.headers = setting.headers
        self.music_url = setting.music_url
        self.session = settings.Session()

    def get_songs_info(self, id):
        self.session.query(pysql.Song_sheet163).filter(pysql.Song_sheet163.songsheet_id == id).update({'over': 'Y'})
        music_url = self.music_url.format(id)
        session = requests.Session()
        try:
            soup = BeautifulSoup(session.get(music_url, headers=self.headers).text, 'lxml')
            songs = json.loads(soup.find('p').get_text())['result']['tracks']
            # table = [['歌曲名', '歌曲ID', '创作者', '创作者ID', '所属专辑']]
            exist = 0
            for song in songs:
                artist_li = []
                for one in song['artists']:
                    artist_li.append(one['name'])
                name = song['name'] + '(' + song['alias'][0] + ')' if len(song['alias']) > 0 else song['name']
                song_id = song['id']
                artist = '/'.join(artist_li)
                artist_id = song['artists'][0]['id']
                album_name = song['album']['name']
                # print('歌曲名：{} 歌曲id：{} 作者：{} 作者id：{} 专辑名：{}'.format(name, song_id, artist, artist_id, album_name))
                if pysql.single("music163", "song_id", (song_id)) is True:
                    self.session.add(pysql.Music163(song_id=song_id, song_name=name, author=artist))
                    self.session.commit()
                    exist = exist + 1
                else:
                    print('{} : {} {}'.format("重复抓取歌曲", name, "取消持久化"))
            #     table.append([name, song_id, artist, artist_id, album_name])
            # print(AsciiTable(table).table)
            print("歌单包含歌曲 {} 首,数据库 merge 歌曲 {} 首 \r\n".format(len(songs), exist))
        except Exception as e:
            print("抓取歌单歌曲页面存在问题：{} 歌单ID：{}".format(e, id))

    def get_songsheet_info(self, id):
        url = self.music_url.format(id)
        session = requests.Session()
        try:
            soup = BeautifulSoup(session.get(url, headers=self.headers).text, 'lxml')
            infos = json.loads(soup.find('p').get_text())['result']
            author = infos['creator']['nickname']
            playCount = infos['playCount']
            subscribedCount = infos['subscribedCount']
            shareCount = infos['shareCount']
            commentCount = infos['commentCount']
            tags = ','.join(infos['tags'])
            description = infos['description']
            print("维护者：{}  播放：{} 关注：{} 分享：{} 评论：{}".format(author, playCount, subscribedCount, shareCount, commentCount))
            print("描述：{}".format(description))
            print("标签：{}".format(tags))
            songs = json.loads(soup.find('p').get_text())['result']['tracks']
            print('歌单包含歌曲{}首'.format(len(songs)))

            # table = [['歌曲名', '歌曲ID', '创作者', '创作者ID', '所属专辑']]
            exist = 0
            for song in songs:
                artist_li = []
                for one in song['artists']:
                    artist_li.append(one['name'])
                name = song['name'] + '(' + song['alias'][0] + ')' if len(song['alias']) > 0 else song['name']
                song_id = song['id']
                artist = '/'.join(artist_li)
                artist_id = song['artists'][0]['id']
                album_name = song['album']['name']
                # print('歌曲名：{} 歌曲id：{} 作者：{} 作者id：{} 专辑名：{}'.format(name, song_id, artist, artist_id, album_name))
                if pysql.single("music163", "song_id", (song_id)) is True:
                    self.session.add(pysql.Music163(song_id=song_id, song_name=name, author=artist))
                    self.session.commit()
                    exist = exist + 1
                else:
                    print('{} : {} {}'.format("重复抓取歌曲", name, "取消持久化"))
            #     table.append([name, song_id, artist, artist_id, album_name])
            # print(AsciiTable(table).table)
            print("歌单包含歌曲 {} 首,数据库 merge 歌曲 {} 首 \r\n".format(len(songs), exist))
        except Exception as e:
            print("抓取歌单详情存在问题：{} 歌单ID：{}".format(e, id))

if __name__ == "__main__":
    test = music()
    test.get_songsheet_info('2511714039')