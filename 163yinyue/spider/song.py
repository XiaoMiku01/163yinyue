import requests
from bs4 import BeautifulSoup
from spider import setting
from spider import lyric
from spider import comment

class Song:
    def __init__(self):
        self.headers = setting.headers
        self.song_url = setting.song_url
    def get_info(self, song_id):
        url = self.song_url.format(song_id)
        try:
            soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml')
            name = soup.find(attrs={'class': 'f-ff2'}).get_text()
            ps = soup.find_all('p', attrs={'class': 'des s-fc4'})
            author = ps[0].get_text()
            album = ps[1].get_text()
            print('歌曲名：{} {} {}'.format(name, author, album))
            comment.comment().get_comment(song_id, normal=False)
            lyric.Lyric().get_lyric(song_id)
        except Exception as e:
            print("抓取歌曲信息页面存在问题：{} 歌曲ID：{}".format(e, id))

if __name__ == '__main__':
    song = Song()
    song.get_info('545272449')