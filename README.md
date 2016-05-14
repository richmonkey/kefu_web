#狗不理客服


## 前端依赖

1. `npm install` 安装依赖模块
2. grunt生成发布版本的js, 具体见 Gruntfile.js

## 运行依赖

1. `pip install -r requirements.txt`

## 本机运行:

1. `cp configs/config_development.py ./config.py`
2. `python www.py`


### 接口授权
- 请求地址: 所有可供第三方服务端访问的接口
- 请求头部: Authorization: Basic $base64(email:password)

##创建商店
- 请求地址：** POST /api/stores**
- 是否认证：是
- 请求内容: application/x-www-form-urlencoded

      name=商店名称
        
- 成功响应：200

        {
            "store_id":"商店id(整型)"
        }
    
- 操作失败：
  400 非法参数


##获取商店列表
- 请求地址：** GET /api/stores**
- 是否认证：是

- 成功响应：200

    [{"id":"商店id", "name":"商店名称"},....]
    

##添加销售人员
- 请求地址：** POST /api/stores/{store_id}/sellers**
- 是否认证：是
- 请求内容: application/x-www-form-urlencoded

    name=销售人员名称&password=登录密码&number=登录名

- 成功响应：200

        {
            "seller_id":"客服id(整型)"
        }


###修改销售人员名称和密码
- 请求地址：** PATCH /api/stores/{store_id}/sellers/{seller_id}**
- 是否认证：是
- 请求内容: application/x-www-form-urlencoded

    name=销售人员名称&password=登录密码

- 成功响应：200

##获取销售人员列表

- 请求地址：** GET /api/stores/{store_id}/sellers**
- 是否认证：是

- 成功响应：200

    [{"id":"商店id", "name":"商店名称"},....]
    

##删除商店
- 请求地址：** DELETE /api/stores/{store_id}**
- 是否认证：是
- 成功响应：200


##删除销售人员
- 请求地址：** DELETE /api/stores/{store_id}/sellers/{seller_id}**
- 是否认证：是
- 成功响应：200
    
