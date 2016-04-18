# -*- coding: utf-8 -*-
from flask import json
from .response_meta import ResponseMeta


class Request(object):
    def __init__(self, request):
        self.request = request
        self._json_body = None

    def json(self, raw_str=None):
        if self._json_body is not None:
            return self._json_body

        if raw_str is None:
            raw_str = self.request.get_data()

        # print raw_str, '\n'
        try:
            self._json_body = json.loads(raw_str)
            return self._json_body
        except:
            raise ResponseMeta(http_code=406)