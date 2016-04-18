# -*- coding: utf-8 -*-
""" 接口加载器
包含相对路径import的python脚本不能直接运行，只能作为module被引用。
"""
from flask import g, request, render_template
from utils.pager import Pager
from utils.response_meta import ResponseMeta
from utils.request import Request
from utils.func import init_logger
from utils.mysql import Mysql
from config import APP_MODE
from config import MYSQL
from config import MYSQL_IM

LOGGER = init_logger(__name__)

from rds import rds
from rds import rds0
from rds import rds1

def http_error_handler(err):
    LOGGER.error(err)
    return render_template('error.html', description=str(err))


def response_meta_handler(response_meta):
    return response_meta.get_response()


def generic_error_handler(err):
    LOGGER.exception(err)
    return ResponseMeta(http_code=500, description='Server Internal Error!' if APP_MODE == 'Production' else str(err))


def before_request():
    g.headers = {}
    g.pagination = Pager(request.args)
    g.request = Request(request)
    g.auth = None
    g.perms = {}

    g.rds = rds
    g.im_rds = rds1

    g._db = None
    db = getattr(g, '_db', None)
    if db is None:
        cnf = MYSQL
        g._db = Mysql(*cnf)

    
    db = getattr(g, '_imdb', None)
    if db is None:
        cnf = MYSQL_IM
        g._imdb = Mysql(*cnf)


def app_teardown(exception):
    # LOGGER.debug('app_teardown')
    try:
        db = getattr(g, '_db', None)
        if db:
            db.close()

    except Exception:
        pass


    try:
        db = getattr(g, '_imdb', None)
        if db:
            db.close()

    except Exception:
        pass


# 初始化接口
def init_app(app):
    app.teardown_appcontext(app_teardown)
    app.before_request(before_request)
    for error in range(400, 420) + range(500, 506):
        app.error_handler_spec[None][error] = http_error_handler
    app.register_error_handler(ResponseMeta, response_meta_handler)
    app.register_error_handler(Exception, generic_error_handler)

    from utils.mail import Mail
    from utils.sentry import Sentry

    Mail.init_app(app)
    Sentry.init_app(app)
    # 注册接口
    from api import api
    from web import web
    from store import store
    from account import account

    app.register_blueprint(web)
    app.register_blueprint(api)
    app.register_blueprint(store)
    app.register_blueprint(account)
