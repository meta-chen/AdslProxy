#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/28 12:30
# @Author  : Meta_Chen
# @File    : getip.py
# @Software: PyCharm
# @Target: 获取公网ip

import requests
import re

class GetIP:
    '''
    获取本机IP
    '''
    response = requests.get("http://txt.go.sohu.com/ip/soip")

    def getip(self):
        text = self.response.text
        myip = re.findall(r'\d+.\d+.\d+.\d+',text)
        return myip[0]

def main():
    getip = GetIP()
    print(getip.getip())

if __name__ == '__main__':
    main()