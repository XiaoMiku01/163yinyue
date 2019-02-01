import requests
import re
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
from spider import setting

class Singer:
    def __init__(self):
        self.headers = setting.headers
        self.singer_page_url = setting.singer_url
        self.intro_url = setting.singer_intro_url
        self.hot_url = setting.singer_hot_url
        self.album_url = setting.singer_album_url
        self.mv_url = setting.singer_MV_url

    def show_classify(self):
        table = [['歌手类型', 'ID']]
        for k, v in setting.singer_dict.items():
            table.append([k, v])
        print(AsciiTable(table).table)

    def get_singers(self, Type='华语女歌手', inital='热门'):
        inital = setting.singer_initial[inital]
        id = setting.singer_dict[Type]
        url = self.singer_page_url.format(id, inital)
        try:
            table = [['歌手名字', 'ID']]
            soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml')
            for singer in soup.find('ul', attrs={'id': 'm-artist-box'}).find_all('li'):
                msg = singer.find('a', attrs={'class': 'nm nm-icn f-thide s-fc0'})
                name = msg.get_text()
                id = re.search(r'id=(\d+)', msg['href']).group(1)
                table.append([name, id])
            print(AsciiTable(table).table)
        except Exception as e:
            print("抓取歌手出现问题：{} 类型：{}".format(e, Type))

    def get_singer_introduction(self, id):
        url = self.intro_url.format(id)
        soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml').find('div', attrs={'class': 'n-artdesc'})
        h2 = soup.find_all('h2')
        p = soup.find_all('p')
        table = []
        for i in range(len(h2)):
            intr = ''
            cnt = 0
            for word in p[i].get_text():
                cnt += 1
                intr += word
                if cnt % 60 == 0:
                    intr += '\n'
            table.append([h2[i].get_text(), intr])
        print(AsciiTable(table).table)

    def get_singer_hot(self, id):
        url = self.hot_url.format(id)
        soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml').find('ul', attrs={'class': 'f-hide'})
        table = [['歌曲名', 'ID']]
        for song in soup.find_all('li'):
            name = song.find('a').get_text()
            song_id = re.search(r'id=(\d+)', song.find('a')['href']).group(1)
            table.append([name, song_id])
        print(AsciiTable(table).table)

    def get_singer_album(self, id, page):
        url = self.album_url.format(id, str((int(page)-1)*12))
        soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml').find('ul', attrs={'id': 'm-song-module'})
        table = [['专辑名', '日期', 'ID']]
        for album in soup.find_all('li'):
            name = album.find('a', attrs={'class': 'tit s-fc0'}).get_text()
            album_id = re.search(r'id=(\d+)', album.find('a', attrs={'class': 'tit s-fc0'})['href']).group(1)
            date = album.find('span', attrs={'class': 's-fc3'}).get_text()
            table.append([name, date, album_id])
        print(AsciiTable(table).table)

    def get_singer_mv(self, id, page):
        url = self.mv_url.format(id, str((int(page)-1)*12))
        soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml').find('ul', attrs={'id': 'm-mv-module'})
        table = [['MV名', 'ID']]
        for mv in soup.find_all('li'):
            dec = mv.find('p', attrs={'class': 'dec'}).find('a')
            name = dec.get_text()
            mv_id = re.search(r'id=(\d+)', dec['href']).group(1)
            table.append([name, mv_id])
        print(AsciiTable(table).table)


if __name__ == "__main__":
    singer = Singer()
    # singer.show_classify()
    # singer.get_singers()
    # singer.get_singer_introduction('8103')
    # singer.get_singer_hot('10559')
    # singer.get_singer_album('10559', '1')
    singer.get_singer_mv('10559', '1')




