from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from utils import config




def configure_orm():
    global engine
    global Session
    engine_args = {}
    try:
        create_engine(config.get_use(), echo=False).execute("create database IF NOT EXISTS  {} DEFAULT CHARACTER SET utf8".format(config.get_mysql()['db']))
        engine = create_engine(config.get_use(), **engine_args)
        Session = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=engine))
    except Exception as e:
       print("初始化数据库出现问题： {}".format(e))
