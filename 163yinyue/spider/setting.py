classify = {
    "语种": ["华语", "欧美", "日语", "韩语", "粤语", "小语种", ],
    "风格": ["流行", "摇滚", "民谣", "电子", "舞曲", "说唱", "轻音乐", "爵士", "乡村", "R&B/Soul", "古典", "民族", "英伦", "金属", "朋克", "蓝调", "雷鬼", "世界音乐", "拉丁", "另类/独立", "New Age", "古风", "后摇", "Bossa Nova"],
    "场景": ["清晨", "夜晚", "学习", "工作", "午休", "下午茶", "地铁", "驾车", "运动", "旅行", "散步", "酒吧"],
    "情感": ["怀旧", "清新", "浪漫", "性感", "伤感", "治愈", "放松", "孤独", "感动", "兴奋", "快乐", "安静", "思念"],
    "主题": ["影视原声", "ACG", "校园", "游戏", "70后", "80后", "90后", "网络歌曲", "KTV", "经典", "翻唱", "吉他", "钢琴", "器乐", "榜单", "00后"]
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
    'Referer': 'https://music.163.com/',
    'Host': 'music.163.com'
}

songsheet_url = 'https://music.163.com/discover/playlist/?order=hot&cat={}&limit=35&offset={}'
music_url = 'https://music.163.com/api/playlist/detail?id={}'
lyric_url = 'http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1'

comment_url = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='
comment_api = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}?limit=20&offset={}'

song_url = 'https://music.163.com/song?id={}'
search_url = 'http://music.163.com/api/search/pc'