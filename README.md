# 163yinyue
网易云音乐爬虫(欢迎STAR)

## 如何使用？
- 需要先安装mysql和Beautifulsoup，sqlalchemy
- 创建名为163yinyue的数据库并修改163yinyue.conf下数据库用户名，密码，端口，数据库名称
- 命令行运行cli.py

### [1.0.0] - 2019-01-27
- 增加爬虫comment用于爬取歌曲热评和普通评论
- 增加爬虫djradio用于爬取电台
- 增加爬虫lyric用于爬取歌曲歌词
- 增加爬虫music用于爬取歌单歌曲信息
- 增加爬虫singer用于爬取信息
- 增加爬虫comment用于爬取歌曲热评和普通评论
- 增加爬虫song_sheet用于爬取歌单信息

### TODO
简化运行指令
重构代码
添加用户登录后相关信息爬取

## 使用指南

```console
$ python cli.py -M comment  --id 1062642
$ # 歌曲id获取该歌曲全部评论
```
```console
$ python cli.py -M comment  --page 1 --id 1062642
$ # 歌曲id获取该歌曲指定页的评论
```
```console
$ python cli.py -M comment  --page 1 --id 1062642 --normal False
$ # 歌曲id获取该歌曲热门评论
```
```console
$ python cli.py -M lyric --id 1062642
$ # 歌曲id获取该歌曲歌词
```
```console
$ python cli.py -M song_sheet --show True
$ # 获取歌单风格类型
```
```console
$ python cli.py -M song_sheet --page 1 --style '全部'
$ # 获取指定类型指定页的所有歌单
```
```console
$ python cli.py -M singer --id 8103
$ # 歌手id获取该信息
```


