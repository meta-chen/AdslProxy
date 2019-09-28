# coding=utf-8
from adslproxy.api import server
from adslproxy.db import RedisClient
import os
passwd = os.getenv('REDISPASSWORD')
if __name__ == '__main__':
    redis = RedisClient(host='', password=passwd)
    server(redis=redis,port=8000)
