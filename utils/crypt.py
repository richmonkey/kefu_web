# !-*- coding:utf-8 -*-

import base64
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5, AES
from Crypto.Hash import SHA
from Crypto.Signature import PKCS1_v1_5 as Pk
from Crypto.PublicKey import RSA
import os
import hashlib
from collections import OrderedDict
import json


class SignUtils(object):
    @classmethod
    def get_sign_string(cls, params, filter_params=None):
        """获取待签名字符串
        :param params: 请求参数
        :type params: dict
        :param filter_params: 不参与签名参数
        :type filter_params: list
        :return: 待签名字符串
        :rtype: str
        """
        # 除去待签名参数数组中的空值和签名参数
        filtered_params = cls.para_filter(params, filter_params=filter_params)

        # 对待签名参数数组排序
        sorted_params = cls.arg_sort(filtered_params)

        # 把数组所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串
        return cls.create_link_string(sorted_params).encode('utf8')

    @staticmethod
    def to_string(val):
        if isinstance(val, bool):
            return str(int(val))
        elif isinstance(val, int) or isinstance(val, long) or isinstance(val, float):
            return str(val)
        elif isinstance(val, list) or isinstance(val, dict):
            # dict是无序，需要根据KEY排序，不转换unicode字符，紧凑分隔符（不包含空格）
            return json.dumps(val, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
        else:
            return val

    @staticmethod
    def para_filter(params, filter_params=None):
        """除去数组中的空值和签名参数

        :param params: dict 签名参数组
        """
        filtered_params = OrderedDict()

        if filter_params is None:
            filter_params = ['sign', 'sign_type']

        for key, val in params.iteritems():
            if key not in filter_params and val != '' and val is not None:
                filtered_params[key] = val
        return filtered_params

    @staticmethod
    def arg_sort(d):
        """对数组排序

        :param d: dict 排序前的数组
        """
        return OrderedDict(sorted(d.items(), key=lambda t: t[0]))

    @classmethod
    def create_link_string(cls, params):
        """把字典所有元素，按照“参数=参数值”的模式用“&”字符拼接成字符串

        :param params: dict 需要拼接的数组
        :rtype unicode
        """
        args = ''
        for key, val in params.iteritems():
            args += key + '=' + cls.to_string(val) + '&'

        return args[0:-1]


class CryptException(Exception):
    pass


class RSAUtils(object):
    """RSA辅助类
    """
    public_key = None
    private_key = None

    def __init__(self, public_key=None, private_key=None):
        self.public_key = public_key
        self.private_key = private_key

    def rsa_base64_encrypt(self, data, public_key=None):
        """ rsa加密
        1. rsa encrypt
        2. base64 encrypt
        :param data: 数据
        :param public_key: 公钥
        """
        public_key = self.get_public_key(public_key)

        cipher = PKCS1_v1_5.new(public_key)
        return base64.b64encode(cipher.encrypt(data))

    def rsa_base64_decrypt(self, data, private_key=None):
        """
        :param data: 数据
        :param private_key: 私钥

        1. base64 decrypt
        2. rsa decrypt
        示例代码

        >>> key = RSA.importKey(open('privkey.der').read())
        >>>
        >>> dsize = SHA.digest_size
        >>> sentinel = Random.new().read(15+dsize)      # Let's assume that average data length is 15
        >>>
        >>> cipher = PKCS1_v1_5.new(key)
        >>> message = cipher.decrypt(ciphertext, sentinel)
        >>>
        >>> digest = SHA.new(message[:-dsize]).digest()
        >>> if digest==message[-dsize:]:                # Note how we DO NOT look for the sentinel
        >>>     print "Encryption was correct."
        >>> else:
        >>>     print "Encryption was not correct."
        """
        private_key = self.get_private_key(private_key)

        try:
            cipher = PKCS1_v1_5.new(private_key)
            return cipher.decrypt(base64.b64decode(data), Random.new().read(15 + SHA.digest_size))
        except TypeError:
            raise CryptException(message='decrypt fail, content: ' + data)
        except ValueError:
            raise CryptException(message='decrypt fail, content: ' + data)

    def sign(self, sign_data, private_key=None):
        """ RSA签名
        :param private_key: 私钥
        :param sign_data: 需要签名的字符串
        """

        private_key = self.get_private_key(private_key)

        h = SHA.new(sign_data)
        signer = Pk.new(private_key)
        signn = signer.sign(h)
        signn = base64.b64encode(signn)
        return signn

    def verify(self, data, sign, public_key=None):
        """
        RSA验签
        结果：如果验签通过，则返回True
             如果验签不通过，则返回False
        :param data: str 数据
        :param sign: str 签名
        :param public_key: str 公钥
        """

        public_key = self.get_public_key(public_key)

        signn = base64.b64decode(sign)
        verifier = Pk.new(public_key)
        return verifier.verify(SHA.new(data), signn)

    def get_public_key(self, public_key):
        if public_key is None:
            public_key = self.public_key

        if public_key:
            try:
                if os.path.isfile(public_key):
                    return RSA.importKey(open(public_key, 'r').read())
                elif public_key:
                    return RSA.importKey('-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----')
            except Exception:
                raise CryptException(message='public key error')
        else:
            raise CryptException(message='public key empty')

    def get_private_key(self, private_key):
        if private_key is None:
            private_key = self.private_key

        if private_key:
            try:
                if os.path.isfile(private_key):
                    return RSA.importKey(open(private_key, 'r').read())
                elif private_key:
                    return RSA.importKey(
                        '-----BEGIN RSA PRIVATE KEY-----\n' + private_key + '\n-----END RSA PRIVATE KEY-----')
            except Exception:
                raise CryptException('private key error')
        else:
            raise CryptException('private key empty')


class Md5Utils(object):
    @classmethod
    def sign(cls, data, key):
        return hashlib.md5(str(data) + str(key)).hexdigest()

    @classmethod
    def verify(cls, data, sign, key):
        return cls.sign(data, key) == sign
