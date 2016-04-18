# -*- coding: utf-8 -*-
import redis
import config

rds0 = redis.StrictRedis(host=config.REDIS_DATA_HOST, 
                         port=config.REDIS_DATA_PORT, 
                         db=config.REDIS_DATA_DB,
                         password=config.REDIS_DATA_PASSWORD)

rds1 = redis.StrictRedis(host=config.REDIS_DATA_HOST, 
                         port=config.REDIS_DATA_PORT, 
                         db=config.REDIS_IM_DB,
                         password=config.REDIS_DATA_PASSWORD)

rds = rds0
