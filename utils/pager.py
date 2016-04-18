# -*- coding: utf-8 -*-


class Pager(object):
    __slots__ = ('_dict',)
    MAX_LIMIT = 100

    def __init__(self, request_args={}):
        """
        传入request.args参数
        分页方式:
            rows_found
            limit
            offset

        流方式:
            limit
            since or until
        """
        self_dict = {
            'limit': int(request_args.get('limit', self.MAX_LIMIT))
        }

        if request_args.get('offset') is not None:
            self_dict['rows_found'] = 0
            self_dict['offset'] = int(request_args.get('offset', 0))

        elif request_args.get('since') is not None:
            since = request_args.get('since').split(':', 2)
            if len(since) == 1:
                self_dict['key'] = 'id'
                self_dict['since'] = since[0]
            else:
                self_dict['key'], self_dict['since'] = since

        elif request_args.get('until') is not None:
            until = request_args.get('until').split(':', 2)
            if len(until) == 1:
                self_dict['key'] = 'id'
                self_dict['until'] = until[0]
            else:
                self_dict['key'], self_dict['until'] = until

        else:
            self_dict = {}

        object.__setattr__(self, '_dict', self_dict)

    def __setattr__(self, key, value):
        #所有对属性的赋值都会调用
        self_dict = object.__getattribute__(self, '_dict')
        if key in self_dict:
            self_dict[key] = value

    def __getattr__(self, item):
        #属性不存在再来调用此方法
        self_dict = object.__getattribute__(self, '_dict')
        return self_dict.get(item)

    def __len__(self):
        return True if self.present() else False

    def present(self):
        return object.__getattribute__(self, '_dict') or None

    def setdefault(self, limit=MAX_LIMIT, offset=0):
        if not self:
            self_dict = object.__getattribute__(self, '_dict')
            self_dict['limit'] = limit
            self_dict['offset'] = offset
            self_dict['rows_found'] = 0

        return self

    def update(self, **kwargs):
        self_dict = object.__getattribute__(self, '_dict')
        self_dict.update(kwargs)