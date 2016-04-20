# -*- coding: utf-8 -*-
""" 程序入口
"""
import config
import time, math
from utils.func import init_logger

init_logger(None)

from flask import Flask, Markup, render_template, request

app = Flask(__name__)
app.config.from_object(config)


@app.context_processor
def pjax_processor():
    def get_template(base, pjax=None):
        pjax = pjax or 'pjax.html'
        if 'X-PJAX' in request.headers:
            return pjax
        else:
            return base

    return dict(pjax=get_template)


@app.context_processor
def pagination_processor():
    def pagination(url, pager, template=None, params={}):
        template = template or 'mod/pagination.html'
        pager._dict['current'] = int(math.ceil(( pager.offset + 1 ) / float(pager.limit)))
        pager._dict['total_page'] = int(math.ceil(pager.rows_found / float(pager.limit)))
        prev_offset = pager.offset - pager.limit
        pager._dict['prev_offset'] = prev_offset if prev_offset >= 0 else 0
        pager._dict['params'] = params
        pager._dict['url'] = url
        return Markup(render_template(template, data=pager))

    return dict(pagination=pagination)


@app.template_filter('datetime')
def datetime_filter(n, format='%Y-%m-%d %H:%M'):
    arr = time.localtime(n)
    return time.strftime(format, arr)


from website import init_app
from utils.session import RedisSession

init_app(app)
RedisSession.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=15204)
