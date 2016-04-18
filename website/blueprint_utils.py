# -*- coding: utf-8 -*-
from functools import wraps
import flask
from flask import session, url_for, redirect, request, g
from werkzeug.security import generate_password_hash, check_password_hash
import logging
import json
import base64
from models import Account

def make_response(status_code, data = None):
    if data:
        res = flask.make_response(json.dumps(data), status_code)
        res.headers['Content-Type'] = "application/json"
    else:
        res = flask.make_response("", status_code)

    return res

def INVALID_AUTHORIZATION():
    e = {"message":"非法的认证信息", "code":400}
    logging.warn("非法的认证信息")
    return make_response(400, e)

def INVALID_USER():
    e = {"message":"用户不存在", "code":400}
    logging.warn("用户不存在")
    return make_response(400, e)

def INVALID_PASSWORD():
    e = {"message":"密码错误", "code":400}
    logging.warn("密码错误")
    return make_response(400, e)

def login_required(function=None, redirect_url_for=None):
    def actual_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' in session and session['user'].get('id'):
                if session['user']['role'] == 1:
                    if session['user'].get('email_checked') == 0:
                        return redirect(url_for('account.register_valid'))
                    else:
                        return f(*args, **kwargs)
                elif session['user']['role'] == 2 or session['user']['role'] == 3:
                    return f(*args, **kwargs)

            return redirect(url_for('account.login',
                                    redirect_url=url_for(redirect_url_for)
                                    if redirect_url_for else None))

        return decorated_function

    if function:
        return actual_decorator(function)

    return actual_decorator


def require_basic_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'Authorization' in request.headers:
            basic = request.headers.get('Authorization')[6:]
        else:
            return INVALID_AUTHORIZATION()
        basic = base64.b64decode(basic)
        sp = basic.split(":", 1)
        if len(sp) != 2:
            return INVALID_AUTHORIZATION()

        email = sp[0]
        password = sp[1]
        account = Account.get_account_with_email(g._db, email)
        if not account:
            return INVALID_USER()
        account_password = account.get('password')
        if not check_password_hash(account_password, password):
            return INVALID_PASSWORD()
        g.developer_id = account.get('id')
        return f(*args, **kwargs)
    return wrapper

