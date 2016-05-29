# -*- coding: utf-8 -*-

from flask import Blueprint, render_template,request, send_from_directory, redirect, url_for, g
import os,time
from utils.func import init_logger
from config import APP_MODE,APP_ID,APP_SECRET
import requests
from utils.wx_sign import Sign

LOGGER = init_logger(__name__)

web = Blueprint('web', __name__, template_folder='templates', static_folder='static')


def get_ticket():
    path = './ticket.json'
    if os.path.isfile(path):
        fh = open(path)
        l = fh.read()
        if l:
            arr = l.split('|')
            s = arr[0]
            t = arr[1]
            if int(t) + 7000 > int(time.time()):
                fh.close()
                return s
    access_token_url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + APP_ID + '&secret=' + APP_SECRET
    ret = requests.get(access_token_url)
    rs = ret.json()
    gicket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=' + rs['access_token'] + '&type=jsapi'
    ret = requests.get(gicket_url)
    rs = ret.json()
    m_file = open(path, 'w')
    m_file.write(rs['ticket'] + '|' + str(int(time.time())))
    m_file.close()
    return rs['ticket']


def get_weixin_sign():
    if APP_MODE != 'Development':
        ticket = get_ticket()
        sign = Sign(ticket, request.url)
        sign = sign.sign()
        sign['appid'] = APP_ID
    else:
        sign = {
            'timestamp': '',
            'nonceStr': '',
            'signature': '',
            'appid': ''
        }
    return sign


@web.errorhandler
def generic_error_handler(err):
    LOGGER.exception(err)
    return render_template('error.html', description=str(err)), 500


@web.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(os.path.dirname(web.root_path), 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@web.route('/')
def index():
    sign = get_weixin_sign()
    g.uri_path = '/'
    return render_template('index/index.html', sign=sign)


@web.route('/contact')
def contact():
    sign = get_weixin_sign()
    return render_template('index/contact.html', sign=sign)


@web.route('/price')
def price():
    sign = get_weixin_sign()
    return render_template('index/price.html', sign=sign)


@web.route('/docs')
def doc():
    return redirect(url_for('web.static', filename='docs/im/Server.html'))

