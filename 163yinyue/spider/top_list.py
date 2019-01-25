import requests
import json
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
from spider import setting


class Toplist:
    def __init__(self):
        self.headers = setting.headers
        self.toplist_url = setting.toplist_url

    def show_toplist(self):
        table = [['榜单类型', '榜单名', '榜单ID']]
        for kind, li in setting.top_list.items():
            for top in li:
                key, value = list(top.items())[0]
                table.append([kind, key, value])
        print(AsciiTable(table).table)


    def get_toplist_info(self, id):
        if id not in setting.top_dict:
            print('榜单ID {} 不存在'.format(id))
            return
        top_name = setting.top_dict[id]
        print(top_name)
        url = self.toplist_url.format(id)
        try:
            soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml')
            textarea = soup.find('textarea', attrs={'id': 'song-list-pre-data'}).get_text()

            table = [['排名', '歌曲名', '时长', '歌曲ID', '歌手名']]
            cnt = 0
            for song in json.loads(textarea):
                cnt += 1
                name = song['name'].strip()
                if len(song['alias']) != 0:
                    name += '(' + song['alias'][0] + ')'
                song_id = song['id']
                artists_li = []
                for one in song['artists']:
                    artists_li.append(one['name'])
                artists = '/'.join(artists_li)
                duration = int(int(song['duration'])/1000)
                minute = int(duration/60)
                second = duration % 60
                minute = str(minute) if minute >= 10 else '0' + str(minute)
                second = str(second) if second >= 10 else '0' + str(second)
                duration = minute + ':' + second
                table.append([cnt, name, duration, song_id, artists])
            print(AsciiTable(table).table)
        except Exception as e:
            print("抓取榜单出现问题：{} ID：{}".format(e, id))

if __name__ == "__main__":
    toplist = Toplist()

    # toplist.show_toplist()
    toplist.get_toplist_info('2629421353')

