# -*- coding: utf-8 -*-

import requests
import urllib
import urllib2
try:
    import urlparse
except ImportError:
    import urllib.parse as urlparse

import threading
import json
import sys
import base64
import md5

#URL = "http://192.168.33.10"
URL = "http://dev.kefu.gobelieve.io/api"

email = "houxuehua49@gmail.com"
password = "111111"
auth = "Basic %s"%base64.b64encode("%s:%s"%(email, password))
headers = {
    "Authorization":auth,
    "Content-Type":"application/x-www-form-urlencoded"
}

#创建store
url = URL + "/stores"
r = requests.post(url, data={"name":"test"}, headers = headers)
print r.content
obj = json.loads(r.content)
store_id = obj['store_id']
 
#获取store列表
url = URL + "/stores"
r = requests.get(url, headers=headers)
print r.content

FIX_MODE = 1
ONLINE_MODE = 2
BROADCAST_MODE = 3

#设置客服模式
url = URL + "/stores/%s"%store_id
r = requests.patch(url, data={"mode":BROADCAST_MODE}, headers=headers)
print "set mode:", r.status_code


salt = "123456"
#创建seller
url = URL + "/stores/%s/sellers"%store_id
password = md5.new("111111").hexdigest()
password = md5.new(password+salt).hexdigest()
r = requests.post(url, data={"name":"test", "md5_password":password, "salt":salt}, headers = headers)
print r.content
obj = json.loads(r.content)
seller_id = obj['seller_id']

#修改销售名称和密码
url = URL + "/stores/%s/sellers/%s"%(store_id, seller_id)
password = md5.new("123456").hexdigest()
password = md5.new(password+salt).hexdigest()
r = requests.patch(url, data={"name":"test_name", "md5_password":password, "salt":salt}, headers = headers)
print "set name/password:", r.status_code

#获取销售员列表
url = URL + "/stores/%s/sellers"%store_id
r = requests.get(url, headers = headers)
print r.content

#删除销售人员
url = URL + "/stores/%s/sellers/%s"%(store_id, seller_id)
r = requests.delete(url, headers = headers)
print r.status_code
 
#删除store
url = URL + "/stores/%s"%store_id
r = requests.delete(url, headers = headers)
print r.status_code



