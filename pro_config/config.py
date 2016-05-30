# -*- coding: utf-8 -*-
"""
http://flask.pocoo.org/docs/config/
"""
import os

APP_MODE = 'Production'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

#和developer.gobelieve.io使用同一个session
SESSION_COOKIE_NAME = 'sid'
SESSION_COOKIE_DOMAIN = '.91lace.com'
SESSION_COOKIE_PATH = '/'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False
PERMANENT_SESSION_LIFETIME = 7200 * 12

SESSION_KEY_PREFIX = 'session:developer:'
SESSION_REDIS_HOST = '10.168.188.86'
SESSION_REDIS_PORT = 6380
SESSION_REDIS_DB = 0
SESSION_REDIS_PASSWORD = None

#发送群组变更的通知消息到im服务器
REDIS_HOST = "10.168.188.86"
REDIS_PORT = 6380
REDIS_DB = 0
REDIS_PASSWORD = None


MYSQL_HOST = "rdsme36vin2uqrn.mysql.rds.aliyuncs.com"
MYSQL_HOST = "10.251.43.254"
MYSQL_PORT = 3306
MYSQL_AUTOCOMMIT = True
MYSQL_CHARSET = 'utf8'

MYSQL_USER = "gobelieve"
MYSQL_PASSWD = "123456"

MYSQL_DATABASE = "gobelieve"
# host,port,user,password,db,auto_commit,charset
MYSQL = (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DATABASE, MYSQL_AUTOCOMMIT, MYSQL_CHARSET)

# mail
MAIL_SERVER = ''
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_DEFAULT_SENDER = ''
MAIL_DEBUG = True
MAIL_SUPPRESS_SEND = False


# 日志目录
LOG_DIR = os.path.join(APP_ROOT, '.logs')

#微信
APP_ID = ''
APP_SECRET = ''


KEFU_APPID = 17

#robotd
RPC = ""
