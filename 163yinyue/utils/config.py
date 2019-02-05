import os
import re
import configparser
import version

PATH = os.environ.get("HOMEPATH") + "\\163yinyue"
if os.environ.get("163YINYUE_PATH") is not None:
    PATH = os.environ.get("163YINYUE_PATH")

if not os.path.exists(PATH):
    os.makedirs(PATH)
cf = configparser.ConfigParser()
if not os.path.exists(PATH + "\\163yinyue.conf"):
    print("请在默认路径 " + PATH + " 下增加配置文件 spider163.conf 格式参照官方")
    cf.read("{}\\template\\163yinyue.conf".format(version.root_path))
else:
    cf.read(PATH + "\\163yinyue.conf")


def get_db():
    try:
        return cf.get("core", "db")
    except Exception as e:
        print("配置文件存在问题，请在 {}/spider163.conf 中配置db=xxx选项".format(PATH))
        print("错误详情： {}".format(e))
        raise e

def get_mysql():
    link = get_db()
    db = re.search('(?<=/)[^/]+(?=\?)', link).group(0)
    uri = re.search('.*(?=/)', link).group(0)
    return {"db": db, "uri": uri}

def get_use():
    return cf.get("core", "use")

