# -*- coding: utf-8 -*-
from flask import Blueprint, session, request, g, render_template, url_for, abort, Response, redirect

from website.web import web
from website.blueprint_utils import login_required

from models import Store
from models import Group
from models import Seller
from models import Question
import md5
import os
import time
import logging
import xmlrpclib
import config

store = Blueprint('store', __name__, template_folder='templates', static_folder='static')
rpc = xmlrpclib.ServerProxy(config.RPC)

def publish_message(rds, channel, msg):
    rds.publish(channel, msg)

def make_response(status_code, data = None):
    if data:
        res = flask.make_response(json.dumps(data), status_code)
        res.headers['Content-Type'] = "application/json"
    else:
        res = flask.make_response("", status_code)

    return res


def INVALID_PARAM():
    e = {"error":"非法输入"}
    logging.warn("非法输入")
    return make_response(400, e)

def _im_login_required(f):
    return login_required(f, redirect_url_for='.store_index')


@store.before_request
def before_request():
    g.uri_path = request.path


@store.route('/store')
@_im_login_required
def store_index():
    """
    store 模块首页

    """
    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    developer_id = session['user']['id']

    print offset, limit, developer_id
    db = g._imdb
    count = Store.get_store_count(db, developer_id)
    stores = Store.get_page_stores(db, developer_id, offset, limit)

    g.pagination.setdefault()
    g.pagination.rows_found = count
    g.pagination.limit = limit
    g.pagination.offset = offset

    return render_template('store/index.html',
                           data={'offset': offset, 'list': stores,
                                 'pagination': g.pagination,
                                 })

@store.route('/store/add')
@_im_login_required
def store_add():
    """
    store 添加商店

    """
    return render_template('store/add.html')


@store.route('/store/detail/<int:store_id>')
@_im_login_required
def store_detail(store_id):
    """
    store 详情

    """
    db = g._imdb
    store_info = Store.get_store(db, store_id)

    return render_template('store/detail.html', data={'store_info': store_info})


@store.route('/store/<int:store_id>/seller')
@_im_login_required
def store_seller(store_id):
    """
    store 销售人员

    """
    db = g._imdb

    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    rows_found = Seller.get_seller_count(db, store_id)
    sellers = Seller.get_page_seller(db, store_id, offset, limit)
    store_info = Store.get_store(db, store_id)

    g.pagination.setdefault()
    g.pagination.rows_found = rows_found
    g.pagination.limit = limit
    g.pagination.offset = offset

    return render_template('store/seller.html',
                           data={'offset': offset,
                                 'list': sellers,
                                 'store_info': store_info,
                                 'pagination': g.pagination,
                                 })


@store.route('/store/<int:store_id>/seller/add')
@_im_login_required
def store_seller_add(store_id):
    """
    store 添加销售人员

    """
    return render_template('store/seller_add.html', data={"store_id":store_id})

@store.route('/store', methods=["POST"])
@_im_login_required
def store_add_post():
    """
    store 添加商店

    """
    db = g._imdb
    developer_id = session['user']['id']
    
    appid = config.KEFU_APPID
    name = request.form['name'] if request.form.has_key('name') else None
    if not name:
        return INVALID_PARAM()

    db.begin()
    gid = Group.create_group(db, appid, 0, name, False)
    store_id = Store.create_store(db, name, gid, developer_id)
    db.commit()

    #将名称存储redis,用于后台推送
    Store.set_store_name(g.im_rds, store_id, name)

    content = "%d,%d,%d"%(gid, appid, 0)
    publish_message(g.im_rds, "group_create", content)

    obj = {"store_id":store_id}

    return redirect(url_for('.store_index'))


@store.route('/store/<int:store_id>/seller', methods=["POST"])
@_im_login_required
def store_seller_post(store_id):
    """
    store 添加商店人员

    """
    db = g._imdb
    developer_id = session['user']['id']

    form = request.form
    name = form.get('name', '')
    password = form.get('password', '')
    number = form.get('number', '')
    if not name or not password or not store_id:
        return INVALID_PARAM()
        
    if not number:
        number = None
    password = md5.new(password).hexdigest()

    group_id = Store.get_store_gid(db, store_id)

    db.begin()
    seller_id = Seller.add_seller(db, name, password, store_id, group_id, number)
    Group.add_group_member(db, group_id, seller_id)
    db.commit()

    content = "%d,%d"%(group_id, seller_id)
    publish_message(g.im_rds, "group_member_add", content)
    
    return redirect(url_for('.store_seller', store_id=store_id))


@store.route("/store/<int:store_id>/question", methods = ["GET"])
@_im_login_required
def store_question(store_id):
    db = g._imdb

    offset = int(request.args.get('offset', 0))
    limit = int(request.args.get('limit', 10))

    rows_found = Question.get_question_count(db, store_id)
    sellers = Question.get_page_question(db, store_id, offset, limit)
    store_info = Store.get_store(db, store_id)

    g.pagination.setdefault()
    g.pagination.rows_found = rows_found
    g.pagination.limit = limit
    g.pagination.offset = offset

    return render_template('store/question.html',
                           data={'offset': offset,
                                 'list': sellers,
                                 'store_info': store_info,
                                 'pagination': g.pagination,
                                 })



@store.route("/store/<int:store_id>/question", methods = ["POST"])
@_im_login_required
def store_question_post(store_id):
    q = request.form.get('question', '')
    a = request.form.get('answer', '')
    if not q or not a:
        return "0"

    qid = Question.add(g._db, q, a, store_id)

    #更新robotd的问题库
    try:
        rpc.refresh_questions()
    except xmlrpclib.ProtocolError as err:
        logging.warning("refresh questions err:%s", err)
    except Exception as err:
        logging.warning("refresh questions err:%s", err)

    return redirect(url_for('.store_question', store_id=store_id))


@store.route("/store/<int:store_id>/question/add", methods = ["GET"])
@_im_login_required
def store_question_add(store_id):
    return render_template('store/question_add.html', data={"store_id":store_id})

