# -*- coding: utf-8 -*-
from website.web import web
from website.blueprint_utils import login_required
from flask import Blueprint, request, g, render_template, redirect, url_for, session
from models import Account
from core import EmailUsageType
import time

def get_user(db):
    user_id = session.get('user', {}).get('id')
    if user_id:
        account_obj = Account.get_account(db, user_id)
        return account_obj
    else:
        return {}


def update_session(db):
    result = get_user(db)
    if result:
        session['user']['id'] = result.get('id')
        session['user']['email'] = result.get('email')
        session['user']['email_checked'] = result.get('email_checked')
        session['user']['role'] = result.get('role')


account = Blueprint('account', __name__, template_folder='templates', static_folder='static')

@account.before_request
def before_request():
    g.uri_path = request.path


@account.route('/login')
def login():
    return render_template('user/login.html')


@account.route('/register')
def user_register():
    return render_template('user/register.html')


@account.route('/logout')
def logout():
    session['user'] = {}
    redirect_url = request.args.get('redirect_url')
    return redirect(url_for('.login', redirect_url=redirect_url))


@account.route('/register/valid')
def register_valid():
    code = request.args.get('code', '')
    error = ''
    expires_in=86400
    if code:
        if 'user' in session:
            account_obj = get_user(g._db)
            verify_email = Account.get_verify_email(g._db, code, EmailUsageType.DEVELOPER_VERIFY)
            confirm = False
            if verify_email and \
               verify_email['ctime'] + expires_in > time.time():
                confirm = True

            Account.delete_verify_email(g._db, code, EmailUsageType.DEVELOPER_VERIFY)
            if confirm:
                Account.set_email_checked(g._db, verify_email['ro_id'], 1)
                session['user']['email_checked'] = 1
                return redirect(url_for('.im_index'))
            else:
                error = '确认邮件失败'

    if 'user' in session and session['user'].get('id'):
        update_session(g._db)

    if 'user' in session and session['user'].get('email'):
        mail = session['user'].get('email')
        if session['user'].get('email_checked') == 1:
            return redirect(url_for('.im_index'))
    else:
        return redirect(url_for('.login'))

    if mail:
        suffix = mail.split('@')[1]
        suffix = suffix.lower()
        url = 'http://'
        if suffix == '163.com':
            url += 'mail.163.com'
        elif suffix == 'vip.163.com':
            url += 'vip.163.com'
        elif suffix == '126.com':
            url += 'mail.126.com'
        elif suffix == 'qq.com' or suffix == 'vip.qq.com' or suffix == 'foxmail.com':
            url += 'mail.qq.com'
        elif suffix == 'gmail.com':
            url += 'mail.google.com'
        elif suffix == 'sohu.com':
            url += 'mail.sohu.com'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'vip.sina.com':
            url += 'vip.sina.com'
        elif suffix == 'sina.com.cn' or suffix == 'sina.com':
            url += 'mail.sina.com.cn'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'yahoo.com.cn' or suffix == 'yahoo.cn':
            url += 'mail.cn.yahoo.com'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'yeah.net':
            url += 'www.yeah.net'
        elif suffix == '21cn.com':
            url += 'mail.21cn.com'
        elif suffix == 'hotmail.com':
            url += 'www.hotmail.com'
        elif suffix == 'sogou.com':
            url += 'mail.sogou.com'
        elif suffix == '188.com':
            url += 'www.188.com'
        elif suffix == '139.com':
            url += 'mail.10086.cn'
        elif suffix == '189.cn':
            url += 'webmail15.189.cn/webmail'
        elif suffix == 'wo.com.cn':
            url += 'mail.wo.com.cn/smsmail'
        elif suffix == '139.com':
            url += 'mail.10086.cn'
        else:
            url = ''
    else:
        url = ''

    return render_template('user/register_valid.html', data={'mail': mail, 'redirect': url, 'error': error})


@account.route('/user/info')
@login_required
def user_info():
    """
    个人中心——基本资料
    """
    return render_template('user/info.html', data={'data': get_user(g._db)})


@account.route('/user/password')
@login_required
def user_password():
    """
    个人中心——修改密码
    """
    return render_template('user/password.html')


@account.route('/forget')
def password_forget():
    """
    忘记密码
    """
    return render_template('user/forget.html')


@account.route('/forget/valid')
def password_forget_check():
    """
    忘记密码——发送邮件
    """
    code = request.args.get('code', '')
    error = ''
    url = ''
    mail = request.args.get('mail', '')
    if mail:
        if 'user' not in session:
            session['user'] = {}
        session['user']['email'] = mail

    if code and mail:
        return render_template('user/reset_password.html', data={'code': code, 'mail': mail})

    if 'user' in session and session['user'].get('id'):
        update_session(g._db)

    if mail:
        suffix = mail.split('@')[1]
        suffix = suffix.lower()
        url = 'http://'
        if suffix == '163.com':
            url += 'mail.163.com'
        elif suffix == 'vip.163.com':
            url += 'vip.163.com'
        elif suffix == '126.com':
            url += 'mail.126.com'
        elif suffix == 'qq.com' or suffix == 'vip.qq.com' or suffix == 'foxmail.com':
            url += 'mail.qq.com'
        elif suffix == 'gmail.com':
            url += 'mail.google.com'
        elif suffix == 'sohu.com':
            url += 'mail.sohu.com'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'vip.sina.com':
            url += 'vip.sina.com'
        elif suffix == 'sina.com.cn' or suffix == 'sina.com':
            url += 'mail.sina.com.cn'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'yahoo.com.cn' or suffix == 'yahoo.cn':
            url += 'mail.cn.yahoo.com'
        elif suffix == 'tom.com':
            url += 'mail.tom.com'
        elif suffix == 'yeah.net':
            url += 'www.yeah.net'
        elif suffix == '21cn.com':
            url += 'mail.21cn.com'
        elif suffix == 'hotmail.com':
            url += 'www.hotmail.com'
        elif suffix == 'sogou.com':
            url += 'mail.sogou.com'
        elif suffix == '188.com':
            url += 'www.188.com'
        elif suffix == '139.com':
            url += 'mail.10086.cn'
        elif suffix == '189.cn':
            url += 'webmail15.189.cn/webmail'
        elif suffix == 'wo.com.cn':
            url += 'mail.wo.com.cn/smsmail'
        elif suffix == '139.com':
            url += 'mail.10086.cn'
        else:
            url = ''

    return render_template('user/forget_valid.html', data={'mail': mail, 'redirect': url, 'error': error})
