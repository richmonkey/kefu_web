# -*- coding: utf-8 -*-
"""
http://flask.pocoo.org/docs/config/
"""
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = 'hello mantou'

SESSION_COOKIE_NAME = 'sid_dev'
SESSION_COOKIE_DOMAIN = '172.25.1.155'
SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
PERMANENT_SESSION_LIFETIME = 7200 * 12

SESSION_KEY_PREFIX = 'session:developer:'
SESSION_REDIS_HOST = '172.25.1.111'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
SESSION_REDIS_PASSWORD = None

MYSQL_HOST = "172.25.1.111"
MYSQL_PORT = 3306
MYSQL_AUTOCOMMIT = True
MYSQL_CHARSET = 'utf8'

# 游戏中心数据库
MYSQL_GC_USER = "ngds_user"
MYSQL_GC_PASSWD = "ngds_user.mysql"
MYSQL_GC_DATABASE = "im"

# host,port,user,password,db,auto_commit,charset
MYSQL_GC = (MYSQL_HOST, MYSQL_PORT, MYSQL_GC_USER, MYSQL_GC_PASSWD, MYSQL_GC_DATABASE, MYSQL_AUTOCOMMIT, MYSQL_CHARSET)
# 默认数据库
MYSQL = MYSQL_GC

# mail
MAIL_SERVER = 'smtp.exmail.qq.com'
MAIL_USERNAME = 'webmaster@gobelieve.io'
MAIL_PASSWORD = 'gbpassw0rd'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = 'webmaster@gobelieve.io'
MAIL_DEBUG = True
MAIL_SUPPRESS_SEND = False


# 日志目录
LOG_DIR = os.path.join(APP_ROOT, '.logs')

SENTRY_DSN = ''

APP_MODE = 'Development'

TOKEN_SALT = '20140606'

REDIS_DATA_HOST = "172.25.1.111"
REDIS_DATA_PORT = 6379
REDIS_DATA_DB = 1
REDIS_DATA_PASSWORD = None

CA_KEY = os.path.join(APP_ROOT, 'configs', 'root.key')
CA_CER = os.path.join(APP_ROOT, 'configs', 'root.cer')

APP_ID = 'wxa5ed698cbbfe36e0'
APP_SECRET = 'cd8c074afcb83815a9d0f278bfadf30b'