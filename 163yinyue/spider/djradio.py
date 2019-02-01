import requests
import re
from bs4 import BeautifulSoup
from terminaltables import AsciiTable
from spider import setting

class Djradio:
    def __init__(self):
        self.djradio_url = setting.djradio_url
        self.headers = setting.headers
        self.radio_url = setting.radio_url

    def show_classify(self):
        table = [['类别', 'ID']]
        for kind, id in setting.djradio_dict.items():
            table.append([kind, id])
        print(AsciiTable(table).table)

    def get_radios_top(self, id, page, order='上升最快'):
        order = {'上升最快': '1', '最热电台': '0'}[order]
        # page 最大是34
        url = self.djradio_url.format(id, order, str(30*(int(page)-1)))
        try:
            table = [['电台名称', '电台ID', '作者', '期数', '订阅数']]
            soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml')
            for one in soup.find('ul', attrs={'class': 'rdilist rdilist-2 f-cb'}).find_all('li'):
                name = one.find('h3', attrs={'class': 'f-fs3'}).find('a').get_text().strip()
                link = one.find('h3', attrs={'class': 'f-fs3'}).find('a')['href']
                id = re.search(r'id=(\d+)', link).group(1)
                author = one.find('p', attrs={'class': 'note'}).find('a').get_text().strip()
                msg = one.find('p', attrs={'class': 's-fc4'}).get_text()
                stage = re.search(r'共(\d+)期', msg).group(1)
                follows = re.search(r'订阅(\d+)次', msg).group(1)
                table.append([name, id, author, '共{}期'.format(stage), '订阅{}次'.format(follows)])
            print(AsciiTable(table).table)
        except Exception as e:
            print("抓取电台榜单出现问题：{} 页码：{}".format(e, page))

    def get_radio(self, id, page, order='降序'):
        order = {'降序': '1', '升序': '2'}[order]
        url = self.radio_url.format(id, order, str(100*(int(page)-1)))
        try:
            table = [['期数', '标题', '播放次数', '点赞数', '播出日期', '时长']]
            soup = BeautifulSoup(requests.get(url, headers=self.headers).text, 'lxml')
            description = soup.find('meta', attrs={'name': 'description'})['content']
            print(description)
            total = soup.find('span', attrs={'class': 'sub s-fc4'}).get_text()
            total = re.search(r'共(\d+)期', total).group(1)
            cnt = int(int(total) / 100) if int(total) % 100 == 0 else int(int(total) / 100) + 1
            if int(page) > cnt:
                print('页数过大')
                return
            for one in soup.find('table', attrs={'class': 'm-table m-table-program'}).find('tbody').find_all('tr'):
                num = one.find('td', attrs={'class': 'col1'}).find('span', attrs={'class': 'num'}).get_text()
                titel = one.find('td', attrs={'class': 'col2'}).find('div', attrs={'class': 'tt f-thide'}).find(
                    'a').get_text()
                play_time = one.find('td', attrs={'class': 'col3'}).find('span').get_text()
                play_time_show = re.search(r'播放(\d+)', play_time).group(1)
                if '万' in play_time:
                    play_time = re.search(r'播放(\d+)万', play_time).group(1)
                else:
                    play_time = re.search(r'播放(\d+)', play_time).group(1)
                zan = one.find('td', attrs={'class': 'col4'}).find('span').get_text()
                zan = re.search(r'赞(\d+)', zan).group(1)
                date = one.find('td', attrs={'class': 'col5'}).find('span').get_text()
                duration = one.find('td', attrs={'class': 'f-pr'}).find('span').get_text()
                table.append([num, titel, '播放{}'.format(play_time_show), '赞{}'.format(zan), date, duration])
            print(AsciiTable(table).table)
        except Exception as e:
            print("抓取电台榜单出现问题：{} 榜单ID：{}".format(e, id))


if __name__ == "__main__":
    radio = Djradio()
    # radio.get_radios_top('3', '1', '上升最快')
    radio.get_radio('527104641', '1', '升序')
    # radio.show_classify()