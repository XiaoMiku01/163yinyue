import requests
import json
import base64
import codecs
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from spider import setting

Type = {1: '单曲', 10: '专辑', 100: '歌手', 1000: '歌单', 1002: '用户', 1004: 'MV', 1006: '歌词', 1009: '主播电台'}


class Search:
    def __init__(self):
        self.headers = setting.headers
        self.search_url = setting.search_url
        self.encSecKey = self.rsaEncrypt()

    def searchSong(self, keyword):
        data = {'s': keyword, 'offset': 0, 'limit': 30, 'type': 1}
        try:
            soup = BeautifulSoup(requests.post(self.search_url, data=data, headers=self.headers).text, 'lxml')
            result = json.loads(soup.find('p').get_text())['result']
            if result['songCount'] == 0:
                print('搜索{}, 没有找到歌曲'.format(keyword))
                return
            for song in result['songs']:
                artist_li = []
                for one in song['artists']:
                    artist_li.append(one['name'])
                name = song['name'] + '(' + song['alias'][0] + ')' if len(song['alias']) > 0 else song['name']
                song_id = song['id']
                artist = '/'.join(artist_li)
                artist_id = song['artists'][0]['id']
                album_name = song['album']['name']
                print('歌曲名：{} 歌曲id：{} 作者：{} 作者id：{} 专辑名：{}'.format(name, song_id, artist, artist_id, album_name))
        except Exception as e:
            print("抓取搜索关键词页面存在问题：{} ".format(e))

    def searchAlbum(self, keyword):
        data = {'s': keyword, 'offset': 0, 'limit': 30, 'type': 10}
        try:
            soup = BeautifulSoup(requests.post(self.search_url, data=data, headers=self.headers).text, 'lxml')
            result = json.loads(soup.find('p').get_text())['result']
            if result['albumCount'] == 0:
                print('搜索{}, 没有找到专辑'.format(keyword))
                return
            for album in result['albums']:
                name = album['name']
                id = album['id']
                size = album['size']
                company = album['company']
                artist_li = []
                for one in album['artists']:
                    artist_li.append(one['name'])
                artist = '/'.join(artist_li)
                print('专辑名：{} 专辑ID：{} 包含歌曲数：{} 发行公司：{} 歌手：{}'.format(name, id, company, size, artist))
        except Exception as e:
            print("抓取搜索关键词页面存在问题：{} ".format(e))

    def searchSinger(self, keyword):
        data = {'s': keyword, 'offset': 0, 'limit': 30, 'type': 100}
        try:
            soup = BeautifulSoup(requests.post(self.search_url, data=data, headers=self.headers).text, 'lxml')
            result = json.loads(soup.find('p').get_text())['result']
            if result['artistCount'] == 0:
                print('搜索{}, 没有找到歌手'.format(keyword))
                return
            for singer in result['artists']:
                name = singer['name'] + '(' + singer['alias'][0] + ')' if len(singer['alias']) > 0 else singer['name']
                id = singer['id']
                albumSize = singer['albumSize']
                mvSize = singer['mvSize']
                print('歌手名：{} 歌手ID：{} 专辑数：{} MV数：{}'.format(name, id, albumSize, mvSize))
        except Exception as e:
            print("抓取搜索关键词页面存在问题：{} ".format(e))

    def searchPlaylist(self, keyword):
        data = {'s': keyword, 'offset': 0, 'limit': 30, 'type': 1000}
        try:
            soup = BeautifulSoup(requests.post(self.search_url, data=data, headers=self.headers).text, 'lxml')
            result = json.loads(soup.find('p').get_text())['result']
            if result['playlistCount'] == 0:
                print('搜索{}, 没有找到歌单'.format(keyword))
                return
            for playlist in result['playlists']:
                name = playlist['name']
                playlist_id = playlist['id']
                trackCount = playlist['trackCount']
                creator = playlist['creator']['nickname']
                playCount = playlist['playCount']
                bookCount = playlist['bookCount']
                print('歌单名：{} 歌单ID：{} 包含歌曲数：{} 创建者：{} 播放次数：{} 收藏数：{}'.format(name, playlist_id, trackCount, creator, playCount, bookCount))
        except Exception as e:
            print("抓取搜索关键词页面存在问题：{} ".format(e))

    def searchUser(self, keyword):
        data = {'s': keyword, 'offset': 0, 'limit': 30, 'type': 1002}
        try:
            soup = BeautifulSoup(requests.post(self.search_url, data=data, headers=self.headers).text, 'lxml')
            result = json.loads(soup.find('p').get_text())['result']
            if result['userprofileCount'] == 0:
                print('搜索{}, 没有找到用户'.format(keyword))
                return
            for user in result['userprofiles']:
                name = user['nickname']
                id = user['userId']
                signature = user['signature']
                followeds = user['followeds']
                playlistCount = user['playlistCount']
                print('用户名：{} 用户ID：{} 签名：{} 粉丝数：{} 歌单数：{}'.format(name, id, signature, followeds, playlistCount))
        except Exception as e:
            print("抓取搜索关键词页面存在问题：{} ".format(e))

    def searchMV(self, keyword):
        data = {'s': keyword, 'offset': 0, 'limit': 30, 'type': 1004}
        try:
            soup = BeautifulSoup(requests.post(self.search_url, data=data, headers=self.headers).text, 'lxml')
            result = json.loads(soup.find('p').get_text())['result']
            if result['mvCount'] == 0:
                print('搜索{}, 没有找到MV'.format(keyword))
                return
            for mv in result['mvs']:
                name = mv['name']
                id = mv['id']
                artistName = mv['artistName']
                print('MV名：{} MVID：{} 歌手名：{}'.format(name, id, artistName))
        except Exception as e:
            print("抓取搜索关键词页面存在问题：{} ".format(e))


    def buildParams(self, keyword):
        text = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","s":"%s","type":"1014","offset":"0","total":"true","limit":"20","csrf_token":""}' % (keyword)
        temp1 = '0CoJUm6Qyw8W8jud'.encode('utf-8')
        temp2 = 'LcHzRT70oY58peUv'.encode('utf-8')
        encText = self.aesEncrypt(self.aesEncrypt(text, temp1), temp2)
        return encText

    def aesEncrypt(self, text, key):
        text = text.encode('utf-8')
        pad = 16 - len(text) % 16
        text = text + pad * bytes(chr(pad), encoding='utf-8')
        encryptor = AES.new(key, AES.MODE_CBC, '0102030405060708'.encode('utf-8'))
        ciphertext = encryptor.encrypt(text)
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext.decode('utf-8')

    def rsaEncrypt(self):
        temp1 = 'LcHzRT70oY58peUv'[::-1].encode('utf-8')
        temp2 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        rs = int(codecs.encode(temp1, encoding='hex'), 16) ** int('010001', 16) % int(temp2, 16)
        return format(rs, 'x').zfill(256)

    def searchVideo(self, keyword):
        data = {'params': self.buildParams(keyword), 'encSecKey': self.encSecKey}
        url = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
        header = self.headers.copy()
        header['Referer'] = 'https://music.163.com/search/'
        try:
            soup = BeautifulSoup(requests.post(url, data=data, headers=self.headers).text, 'lxml')
            result = json.loads(soup.find('p').get_text())['result']
            if result['videoCount'] == 0:
                print('搜索{}, 没有找到视频'.format(keyword))
                return
            for video in result['videos']:
                creator_li = []
                for i in video['creator']:
                    creator_li.append(i['userName'])
                creator = '/'.join(creator_li)
                name = video['title']
                playTime = '%.1f' % (int(video['playTime'])/10000) + '万'
                print('视频名：{} 播放数：{} BY：{}'.format(name, playTime, creator))
        except Exception as e:
            print("抓取搜索关键词页面存在问题：{} ".format(e))

if __name__ == '__main__':
    search = Search()
    search.searchVideo('蔡依林')



