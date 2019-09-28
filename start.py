#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/28 13:43
# @Author  : Meta_Chen
# @File    : start.py
# @Software: PyCharm
# @Target: 开启Redis数据库服务,检查ip

import os
from utils.sendip import SendEmail
import logging

redisPasswd = os.getenv('REDISPASSWORD')
emailPassword = os.getenv('163AUTHCODE')
if __name__ == '__main__':
    sender = SendEmail(emailPassword)
    logging.info("IP Checker started")
    sender.timeJob()
