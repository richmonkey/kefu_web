# -*- coding: utf-8 -*-
from flask import g
from utils.response_meta import ResponseMeta
from utils.type_definition import TypeDefinition
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from config import SECRET_KEY, TOKEN_SALT


class MainException(object):
    """接口错误定义
    """
    # 请求已成功，请求所希望的响应头或数据体将随此响应返回。
    OK = ResponseMeta(code=200, http_code=200)
    # 请求已经被实现，而且有一个新的资源已经依据请求的需要而创建。
    CREATED = ResponseMeta(code=201, http_code=201)
    # 资源已经删除。
    NO_CONTENT = ResponseMeta(code=204, http_code=204)
    # 由于包含语法错误，当前请求无法被服务器理解。
    BAD_REQUEST = ResponseMeta(code=400, http_code=400)
    # 当前请求需要用户验证。
    UNAUTHORIZED = ResponseMeta(code=401, http_code=401)
    # 服务器已经理解请求，但是拒绝执行它。
    FORBIDDEN = ResponseMeta(code=403, http_code=403)
    # 请求失败，请求所希望得到的资源未被在服务器上发现。
    NOT_FOUND = ResponseMeta(code=404, http_code=404)
    # 请求行中指定的请求方法不能被用于请求相应的资源。
    METHOD_NOT_ALLOWED = ResponseMeta(code=405, http_code=405)
    # 请求的资源的内容特性无法满足请求头中的条件，因而无法生成响应实体。
    NOT_ACCEPTABLE = ResponseMeta(code=406, http_code=406)
    # 服务器遇到了一个未曾预料的状况，导致了它无法完成对请求的处理。
    INTERNAL_SERVER_ERROR = ResponseMeta(code=500, http_code=500)
    # 作为网关或者代理工作的服务器尝试执行请求时，从上游服务器接收到无效的响应。
    BAD_GATEWAY = ResponseMeta(code=502, http_code=502)
    # 由于临时的服务器维护或者过载，服务器当前无法处理请求。
    SERVICE_UNAVAILABLE = ResponseMeta(code=503, http_code=503)
    # 未能及时从上游服务器收到响应。
    GATEWAY_TIMEOUT = ResponseMeta(code=504, http_code=504)

    OAUTH2_CLIENT_NOT_FOUND = ResponseMeta(1001, 'client不存在')
    OAUTH2_INVALID_GRANT_TYPE = ResponseMeta(1002, 'grant type错误')
    OAUTH2_CLIENT_FORBIDDEN = ResponseMeta(1003, 'client无权限')
    OAUTH2_INVALID_REFRESH_TOKEN = ResponseMeta(1004, 'refresh token错误')
    OAUTH2_INVALID_CLIENT_SECRET = ResponseMeta(1005, 'client secret错误')
    OAUTH2_INVALID_SMS_CODE = ResponseMeta(1006, '验证码错误')
    OAUTH2_USER_NOT_FOUND = ResponseMeta(1007, '无此用户')
    SMS_ERROR_COUNT_LIMITED = ResponseMeta(1008, '验证错误次数超过5此重新验证')
    SMS_CODE_TIMEOUT = ResponseMeta(1009, '验证码过期')
    SMS_CODE_CHECKED = ResponseMeta(1010, '验证码已经验证过')
    SMS_INVALID_CODE = ResponseMeta(1011, '错误验证码')
    SMS_UNAUTHORIZED_CODE = ResponseMeta(1012, '无效验证码')
    SMS_TOO_OFTEN = ResponseMeta(1013, '短信请求太频繁')
    SMS_INVALID_MOBILE = ResponseMeta(1014, '手机号格式错误')
    OAUTH2_INVALID_SNS_TYPE = ResponseMeta(1015, '不支持的社交网站')
    OAUTH2_REFRESH_TOKEN_EXPIRED = ResponseMeta(1016, 'refresh token过期')
    EMAIL_TOO_OFTEN = ResponseMeta(1017, '邮件发送太频繁')
    INVALID_MOBILE = ResponseMeta(1018, '手机号格式错误')

    USER_NOT_ACTIVATED = ResponseMeta(2001, '账号未激活')
    USER_NOT_FOUND = ResponseMeta(2002, '账号不存在')
    USER_INVALID_PASSWORD = ResponseMeta(2003, '密码错误')
    USER_INVALID_NICKNAME = ResponseMeta(2004, '昵称不能为空')
    USER_NAME_EXIST = ResponseMeta(2005, '用户名重复')
    USER_INVALID_AVATAR = ResponseMeta(2006, '用户头像不能为空')
    USER_INVALID_NAME = ResponseMeta(2007, '用户名不能为空')
    USER_MOBILE_BOUND = ResponseMeta(2008, '用户名手机已绑定')
    USER_MOBILE_EXIST = ResponseMeta(2009, '用户手机已经存在')

    NO_FILE_DATA = ResponseMeta(3001, '上传文件数据为空')
    PHOTO_DATA_ERROR = ResponseMeta(3002, '上传文件数据错误')
    PHOTO_FORMAT_FORBIDDEN = ResponseMeta(3003, '不支持的图片类型')
    PHOTO_THUMB_MODE_INVALID = ResponseMeta(3004, '缩略图方式未定义')
    PHOTO_OSS_GET_FAIL = ResponseMeta(3005, '无法获取原图数据')
    PHOTO_URL_PARSE_ERROR = ResponseMeta(3006, '图片地址解析错误')
    UPLOAD_ERROR = ResponseMeta(3007, '上传失败')
    PHOTO_USAGE_TYPE_INVALID = ResponseMeta(3008, '图片类型未定义')
    VIDEO_DATA_ERROR = ResponseMeta(3009, '上传文件数据错误')
    FILE_NOT_SUPPORT = ResponseMeta(3010, '不支持的文件格式')
    CHUNK_UPLOAD_MD5_ERROR = ResponseMeta(3011, '校验失败')
    CHUNK_UPLOAD_ERROR = ResponseMeta(3012, '上传失败')

    ACCOUNT_PASSWORD_INVALID = ResponseMeta(4001, '密码格式错误')
    ACCOUNT_DUPLICATE = ResponseMeta(4002, '账号重复')
    ACCOUNT_EMAIL_CB_INVALID = ResponseMeta(4003, '邮件回调地址不能为空')
    ACCOUNT_PASSWORD_WRONG = ResponseMeta(4004, '密码错误')
    ACCOUNT_NOT_FOUND = ResponseMeta(4005, '账号不存在')
    ACCOUNT_ADD_FAILED = ResponseMeta(4006, '账号添加失败')
    ACCOUNT_EMAIL_CHECKED = ResponseMeta(4007, '邮箱已经验证')
    ACCOUNT_INVALID_EMAIL_CODE = ResponseMeta(4008, '邮件验证码错误')
    ACCOUNT_CREDENTIAL_CREATED = ResponseMeta(4009, '资料已经成功创建，无需重复创建')
    ACCOUNT_PROFILE_INVALID_COUNTRY = ResponseMeta(4010, '国家代码错误')
    ACCOUNT_PROFILE_INVALID_PROVINCE_CITY = ResponseMeta(4011, '省市必填')
    ACCOUNT_PROFILE_INVALID_ATTRIBUTE = ResponseMeta(4012, '所有项目必填')
    ACCOUNT_PROFILE_PIN_TYPE_UNDEFINED = ResponseMeta(4013, '不支持的身份识别类型')
    ACCOUNT_PROFILE_INVALID_CREDENTIAL_TYPE = ResponseMeta(4014, '不支持的资料类型')
    DEVELOPER_ROLE_FORBIDDEN = ResponseMeta(4015, '角色无操作权限')
    DEVELOPER_BEEN_EXIST = ResponseMeta(4016, '已经创建过开发商')
    DEVELOPER_ADD_EMPTY_DATA = ResponseMeta(4017, '开发商资料为空')
    DEVELOPER_ADD_FAILED = ResponseMeta(4018, '开发商添加失败')
    APP_LACK_PARAMS = ResponseMeta(4019, '添加应用缺乏参数')
    APP_NOT_FOUND = ResponseMeta(4020, '应用不存在')
    CLIENT_INVALID_PLATFORM_TYPE = ResponseMeta(4021, '客户端类型错误')
    ACCOUNT_INVALID_PROPERTY = ResponseMeta(4022, '错误的账号角色')
    ACCOUNT_INVALID_PROPERTY_DEVELOPER = ResponseMeta(4023, '开发商类型错误')
    APP_NO_ACTIVE_CLIENT = ResponseMeta(4024, '没有激活的客户端')
    CLIENT_NOT_FOUND = ResponseMeta(4025, '客户端不存在')
    ACCOUNT_INVALID_PROPERTY_CHANNEL = ResponseMeta(4026, '账号关联渠道错误')
    DEVELOPER_NOT_FOUND = ResponseMeta(4027, '无此开发商')
    CHANNEL_INVALID_PARAMS = ResponseMeta(4028, '渠道参数不合法')
    CHANNEL_WRONG_ACCOUNT = ResponseMeta(4029, '账号关联渠道不是本渠道')
    CHANNEL_INVALID_ACCOUNT = ResponseMeta(4029, '不是渠道账号')
    CHANNEL_SAVE_FAILED = ResponseMeta(4030, '渠道添加失败')
    CHANNEL_ADMIN_SAVE_FAILED = ResponseMeta(4031, '渠道管理员添加失败')
    CHANNEL_NOT_FOUND = ResponseMeta(4032, '渠道不存在')
    CHANNEL_IN_USAGE = ResponseMeta(4033, '渠道有数据不能删除')
    CHANNEL_ADMIN_NEEDED = ResponseMeta(4034, '必须指定一名管理员')
    CHANNEL_ADMIN_EMAIL_NEEDED = ResponseMeta(4035, '必须指定渠道管理员的邮件地址')
    ACCOUNT_NAME_NOT_NULL = ResponseMeta(4036, '必须指定账号名称')
    CLIENT_APNS_CERT_ERROR = ResponseMeta(4037, '证书文件错误')
    CLIENT_APNS_CERT_EMPTY = ResponseMeta(4038, '至少上传一个证书')
    ACCOUNT_ROLE_ERROR = ResponseMeta(4039, '账号类型错误')
    TEST_DEVICE_NAME_EMPTY = ResponseMeta(4040, '测试设备名为空')
    TEST_DEVICE_TOKEN_EMPTY = ResponseMeta(4041, '测试设备token为空')

    PKG_NOT_FOUND = ResponseMeta(5001, '没有升级包', http_code=200)

    PUSH_NO_CONTENT = ResponseMeta(6001, '推送消息内容为空')
    PUSH_NO_DEVICE_TOKEN = ResponseMeta(6002, 'device token为空')
    PUSH_NO_WEBURL = ResponseMeta(6003, '必须指定打开的网站地址')
    PUSH_NO_PAGE = ResponseMeta(6004, '必须指定app的启动页面')
    PUSH_NO_DOWNLOAD_URL = ResponseMeta(6005, '必须指定下载的url')
    PUSH_NO_POPUP_CONTENT = ResponseMeta(6006, '弹出框内容为空')
    PUSH_INVALID_TYPE = ResponseMeta(6007, "错误的通知类型")
    PUSH_CREATE_TASK_FAIL = ResponseMeta(6008, "创建推送任务失败")
    PUSH_NO_BODY = ResponseMeta(6009, "post的内容为空")
    PUSH_INVALID_JSON = ResponseMeta(6010, "非法的json对象")
    PUSH_INVALID_CLIENTID = ResponseMeta(6011, "非法的clientid")
    PUSH_REQUEST_FAIL = ResponseMeta(6099, "内部错误")
    PUSH_INVALID_ORDER_TIME = ResponseMeta(6021, "指定时间无效")
    PUSH_INVALID_NOTICE_ID = ResponseMeta(6022, "通知ID非法")

    PUSH_DEVICE_APP_ID_EMPTY = ResponseMeta(6012, "应用ID为空")
    PUSH_DEVICE_PLAYER_ID_EMPTY = ResponseMeta(6013, "玩家ID为空")
    PUSH_DEVICE_TOKEN_EMPTY = ResponseMeta(6014, "设备ID为空")
    PUSH_DEVICE_PLATFORM_ID_INVALID = ResponseMeta(6015, "平台ID不合法")

    PUSH_RULE_NAME_EMPTY = ResponseMeta(6016, "规则名为空")
    PUSH_RULE_NAME_EXIST = ResponseMeta(6017, "规则名已存在")
    PUSH_RULE_ITEM_EMPTY = ResponseMeta(6018, "规则项目为空")
    PUSH_RULE_NOT_EXIST = ResponseMeta(6019, "规则不存在")
    PUSH_RULE_DELETE_FAIL = ResponseMeta(6020, "规则删除失败")

    VIRTUAL_INVALID_APP_ID = ResponseMeta(7001, "非法应用ID")
    VIRTUAL_MISSING_SIGN = ResponseMeta(7002, "缺少签名")
    VIRTUAL_SIGN_TYPE_NO_SUPPORT = ResponseMeta(7003, "不支持的签名方式")
    VIRTUAL_SIGN_VERIFY_FAIL = ResponseMeta(7003, "签名验证失败")


class AppType(TypeDefinition):
    """客户端类型
    """
    CONFIDENTIAL = 2
    PUBLIC = 1


class PlatformType(TypeDefinition):
    """客户端类型
    """
    ANDROID = 1
    IOS = 2


class ObjectType(TypeDefinition):
    """全局对象类型
    """
    USER = 1
    ACCOUNT = 2
    DEVELOPER = 3
    CHANNEL = 4
    APP = 5
    CLIENT = 6
    PACKAGE = 7


class RoleType(TypeDefinition):
    """角色对象类型
    """
    DEVELOPER = 1
    CHANNEL = 2
    PLATFORM = 3


class EmailUsageType(TypeDefinition):
    """邮件类型
    """
    DEVELOPER_VERIFY = 1
    DEVELOPER_RESET_PWD = 2


class GrantType(TypeDefinition):
    SMS_CODE = 1
    CLIENT_CREDENTIALS = 2
    ACCOUNT_CREDENTIALS = 3
    SNS_TOKEN = 4


class DeveloperPermType(TypeDefinition):
    """
    权限掩码
    """
    # 1
    STATS = 0b0000000000000001
    # 2
    RECONCILIATION = 0b0000000000000010
    # 4
    PUSH = 0b0000000000000100
    # 8
    APPS = 0b0000000000001000
    # 16
    ACCOUNT = 0b0000000000010000
    # 65535
    ADMIN = 0b1111111111111111


class PushAppType(TypeDefinition):
    """推送应用类型
    """
    GAME = 1
    APP = 2


class PushType(TypeDefinition):
    """推送类型
    1-4 通知(1打开应用,3打开网页,4打开应用指定页面),5 消息
    """
    OPEN_APP = 1
    OPEN_URL = 3
    OPEN_APP_ACTIVITY = 4
    MESSAGE = 5
    OPEN_SELF_APP = 6
    OPEN_SELF_APP_ACTIVITY = 7


class PushChannelType(TypeDefinition):
    """ 推送渠道类型
    """
    CHANNEL_WEB = 0  # 网页推送
    CHANNEL_SMART = 1  # 规则推送
    CHANNEL_VIRTUAL = 2  # 虚拟推送


class Permission(object):
    @classmethod
    def require(cls):
        if cls in g.perms:
            return g.perms[cls]
        else:
            perm = cls()
            with perm:
                pass

            return perm

    def can(self):
        raise NotImplementedError('Subclasses should implement this!')

    @property
    def auth(self):
        return g.auth

    @auth.setter
    def auth(self, value):
        g.auth = value

    def __call__(self, f):
        @wraps(f)
        def _decorated(*args, **kw):
            with self:
                rv = f(*args, **kw)
            return rv

        return _decorated

    def __enter__(self):
        if self.__class__ in g.perms:
            return

        if not self.can():
            raise MainException.FORBIDDEN
        else:
            g.perms[self.__class__] = self

    def __exit__(self, *args):
        return False


def token_serializer(token_type):
    return URLSafeTimedSerializer(SECRET_KEY, salt="{}.{}".format(TOKEN_SALT, token_type))
