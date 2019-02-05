import settings
from utils import pysql

settings.configure_orm()
pysql.initdb()