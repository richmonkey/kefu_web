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

store_id=55
#设置客服模式
url = URL + "/stores/%s"%store_id
r = requests.patch(url, data={"mode":BROADCAST_MODE}, headers=headers)
print "set mode:", r.status_code

#创建seller
url = URL + "/stores/%s/sellers"%store_id
r = requests.post(url, data={"name":"test", "password":"111111"}, headers = headers)
print r.content
obj = json.loads(r.content)
seller_id = obj['seller_id']


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



