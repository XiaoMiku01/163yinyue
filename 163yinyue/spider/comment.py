import requests
import codecs
import base64
from Crypto.Cipher import AES
from spider import setting

class comment:
    def __init__(self):
        self.headers = setting.headers
        self.comment_url = setting.comment_url
        self.comment_api = setting.comment_api
        self.encSecKey = self.rsaEncrypt()

    def buildParams(self, song_id, page):
        if page == 1:
            text = '{"csrf_token":""}'
        else:
            text = '{"rid":"R_SO_4_%s","offset":"%s","total":"false","limit":"20","csrf_token":""}' % (song_id, str(20*(page-1)))
        temp1 = '0CoJUm6Qyw8W8jud'.encode('utf-8')
        # temp2 = (16 * 'F').encode('utf-8')
        temp2 = 'Kbc65e73nh1jzBol'.encode('utf-8')
        encText = self.aesEncrypt(self.aesEncrypt(text, temp1), temp2)
        return encText

    def aesEncrypt(self, text, key):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, '0102030405060708'.encode('utf-8'))
        ciphertext = encryptor.encrypt(text.encode('utf-8'))
        ciphertext = base64.b64encode(ciphertext)
        return ciphertext.decode('utf-8')

    def rsaEncrypt(self):
        # temp1 = (16 * 'F').encode('utf-8')
        temp1 = 'Kbc65e73nh1jzBol'[::-1].encode('utf-8')
        temp2 = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        rs = int(codecs.encode(temp1, encoding='hex'), 16) ** int('010001', 16) % int(temp2, 16)
        return format(rs, 'x').zfill(256)

    def get_all_comments(self, song_id):
        pages_num = self.get_comment(song_id)
        now_page = 2
        if pages_num > 1:
            while now_page <= pages_num:
                self.get_comment(song_id, now_page)
                now_page += 1

    def get_comment(self, song_id, page=1, normal=True):
        data = {'params': self.buildParams(song_id, page), 'encSecKey': self.encSecKey}
        url = self.comment_url.format(song_id)
        api = self.comment_api.format(song_id, str(20*(page-1)))
        try:
            response = requests.post(url, headers=self.headers, data=data, timeout=10)
            total = response.json()['total']
            if normal:
                for comment in response.json()['comments']:
                    author = comment['user']['nickname']
                    likecount = comment['likedCount']
                    content = comment['content']
                    print('作者：{} 评论：{} 点赞：{}'.format(author, content, likecount))
            if page == 1:
                for comment in response.json()['hotComments']:
                    author = comment['user']['nickname']
                    likecount = comment['likedCount']
                    content = comment['content']
                    print('作者：{} 评论：{} 点赞：{}'.format(author, content, likecount))
            # print('api获取内容')
            # response = requests.get(api, headers=self.headers, timeout=10)
            # print(response.json().keys())
            # print(response.json()['more'])
            # total = response.json()['total']
            # print(total)
            # for comment in response.json()['comments']:
            #     author = comment['user']['nickname']
            #     likecount = comment['likedCount']
            #     content = comment['content']
            #     print(author, likecount, content)
            # if page == 1:
            #     for comment in response.json()['hotComments']:
            #         author = comment['user']['nickname']
            #         likecount = comment['likedCount']
            #         content = comment['content']
            #         print(author, likecount, content)
            return int(total)//20 + 1
        except Exception as e:
            print("抓取评论页面存在问题：{} 歌曲ID：{}".format(e, id))


if __name__ == '__main__':
    comment = comment()
    comment.get_all_comments('1062642')
