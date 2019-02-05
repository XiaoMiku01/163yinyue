import random

from sqlalchemy import Column, Integer, String, TIMESTAMP, Index, extract
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.mysql import MEDIUMTEXT

import settings

Base = declarative_base()

def initdb():
    try:
        Base.metadata.create_all(settings.engine)
    except Exception as e:
        print("自动生成数据库表出现问题: {}".format(e))

def dropdb():
    try:
        Base.metadata.drop_all(settings.engine)
    except Exception as e:
        print("自动删除数据库表出现问题: {}".format(e))

def single(table, k, v):
    cnt = settings.engine.execute('select count(*) from ' + table + ' where ' + k + '=\'' + str(v) + '\'').fetchone()
    if cnt[0] == 0:
        return True
    else:
        return False


class Song_sheet163(Base):
    __tablename__ = "songsheet163"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    title = Column(String(5000), server_default="System Title")
    songsheet_id = Column(String(255), server_default="No Link")
    cnt = Column(Integer(), server_default="-1")
    dsc = Column(String(255), server_default="No Description")
    create_time = Column(TIMESTAMP, server_default=func.now())
    over = Column(String(255), server_default="N")
    over_link = Index("over_link", over, songsheet_id)

class Comment163(Base):
    __tablename__ = "comment163"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    song_id = Column(Integer())
    txt = Column(MEDIUMTEXT)
    author = Column(String(3000), server_default="No Author")
    liked = Column(Integer(), server_default="0")
    Index("liked_song_id", liked, song_id)
    Index("song_id_liked", song_id, liked)

class Music163(Base):
    __tablename__ = "music163"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    song_id = Column(Integer())
    song_name = Column(String(3072), server_default="No Name")
    author = Column(String(3000), server_default="No Author")
    over = Column(String(255), server_default="N")
    has_lyric = Column(String(255), server_default="N")
    create_time = Column(TIMESTAMP, server_default=func.now())
    comment = Column(Integer(), server_default="-1")
    over_id = Index("over_id", over,id)
    key_author = Index("author", author)
    song_id_comment = Index("song_id_comment", song_id, comment)

class Lyric163(Base):
    __tablename__ = "lyric163"
    id = Column(Integer(), primary_key=True, autoincrement=True)
    song_id = Column(Integer())
    txt = Column(MEDIUMTEXT)
    key_song_id = Index("song_id", song_id)