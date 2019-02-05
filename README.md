# 163yinyue
网易云音乐爬虫(欢迎STAR)

## 如何使用？
- 需要先安装mysql和Beautifulsoup，sqlalchemy
- 创建名为163yinyue的数据库并修改163yinyue.conf下数据库用户名，密码，端口，数据库名称
- 进入spider文件夹下运行各个spider

### [1.0.0] - 2019-01-27
- 增加爬虫comment用于爬取歌曲热评和普通评论
- 增加爬虫djradio用于爬取电台
- 增加爬虫lyric用于爬取歌曲歌词
- 增加爬虫music用于爬取歌单歌曲信息
- 增加爬虫singer用于爬取信息
- 增加爬虫comment用于爬取歌曲热评和普通评论
- 增加爬虫song_sheet用于爬取歌单信息

### TODO
整合统一接口直接安装使用，不再分别进入各个spider运行
重构代码
添加用户登录后相关信息爬取


