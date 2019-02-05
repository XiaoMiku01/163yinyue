import requests
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
from spider import setting
from utils import pysql
import settings as st

class songsheet:
    def __init__(self):
        self.headers = setting.headers
        self.songsheet_url = setting.songsheet_url
        self.sql_session = st.Session()

    def get_songsheet(self, page, style='全部'):
        session = requests.Session()
        songsheet_url = self.songsheet_url.format(style, 35*(page-1))
        try:
            soup = BeautifulSoup(session.get(songsheet_url, headers=self.headers).text, 'lxml')
            ul = soup.find('ul', attrs={'class': 'm-cvrlst f-cb'})
            for li in ul.find_all('li'):
                target = li.find('a', attrs={'class': 'tit f-thide s-fc0'})
                title = target['title']
                songsheet_id = target['href'].replace("/playlist?id=", "")
                clicks = li.find('span', attrs={'class': 'nb'}).get_text().strip().replace('万', '0000')
                # print(title, songsheet_id, clicks)
                if pysql.single("songsheet163", "songsheet_id", songsheet_id) is True:
                    pl = pysql.Song_sheet163(title=title, songsheet_id=songsheet_id, cnt=int(clicks), dsc="曲风：{}".format(style))
                    self.sql_session.add(pl)
                    self.sql_session.commit()
        except Exception as e:
            print("抓取歌单出现问题：{} 歌单类型：{} 页码：{}".format(e, style, page))

    def show_classify(self):
        table = [['类别', '风格列表']]
        for kind, styles in setting.classify.items():
            num = 0
            msg = ''
            for style in styles:
                num += 1
                if num % 5 == 0:
                    msg += style + '\n'
                else:
                    msg += style + '，'
            table.append([kind, msg])
        print(AsciiTable(table).table)



if __name__ == "__main__":
    st.configure_orm()
    songsheet_test = songsheet()
    songsheet_test.get_songsheet(2)


