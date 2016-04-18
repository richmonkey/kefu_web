# -*- coding: utf-8 -*-


class TypeMeta(type):
    def __init__(cls, name, bases, attrs):
        cls._dict = {attr: val for attr, val in attrs.items() if attr[0] != '_' and not isinstance(val, classmethod)}


class TypeDefinition(object):
    __metaclass__ = TypeMeta
    _dict = None

    @classmethod
    def isdefined(cls, value):
        """
        判断值是否定义
        """
        return value in cls._dict.values()

    @classmethod
    def get_dict(cls):
        """
        输出键和值字典
        """
        return cls._dict

    @classmethod
    def literal(cls, type_val):
        """
        根据值输出key名称
        """
        name = None
        for k, v in cls._dict.items():
            if v == type_val:
                name = k.lower()
                break

        return name