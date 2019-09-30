#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/28 12:39
# @Author  : Meta_Chen
# @File    : sendip.py
# @Software: PyCharm
# @Target: 以邮件形式发送ip

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from utils.getip import GetIP
from apscheduler.schedulers.blocking import BlockingScheduler
import os
import logging
import configparser

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(name)s %(levelname)s %(message)s",
                    datefmt = '%Y-%m-%d  %H:%M:%S %a')    #注意月份和天数不要搞乱了，这里的格式化符与time模块相同
class SendEmail:
    # 设置smtplib所需的参数
    # 下面的发件人，收件人是用于邮件传输的。
    smtpserver = 'smtp.163.com'
    username = 'meta_chen@163.com'
    sender = 'meta_chen@163.com'
    # receiver='XXX@126.com'
    # 收件人为多个收件人
    receiver = ['meta_chen@163.com']

    # subject = 'Python email test'
    # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
    subject = 'IP地址变更'
    subject=Header(subject, 'utf-8').encode()

    # 构造邮件对象MIMEMultipart对象
    # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = 'meta_chen <{}>'.format(sender)
    # msg['To'] = 'XXX@126.com'
    # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
    msg['To'] = ";".join(receiver)
    # msg['Date']='2012-3-16'
    config = configparser.ConfigParser()
    config.read("./conf.ini", encoding="utf-8")

    def __init__(self,password):
        self.password = password

    def mailsender(self):
        '''
        构造文字内容,2小时检测一次
        :return:
        '''
        logging.info("Start Check IP")
        checkip = GetIP()
        myip = checkip.getip()
        oldip = self.config.get('ip','oldip')
        if myip != oldip:
            logging.info('IP has Changed to : {} from {}'.format(myip,oldip))
            self.config.set('ip','oldip',str(myip))
            self.config.write(open("./conf.ini", "w"))
        else:
            logging.info("Nothing changed")
            return False

        text = 'Host Ip has Changed :{}'.format(myip)
        text_plain = MIMEText(text, 'plain', 'utf-8')
        self.msg.attach(text_plain)


        # 发送邮件
        smtp = smtplib.SMTP()
        smtp.connect('smtp.163.com')
        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
        smtp.set_debuglevel(1)
        smtp.login(self.username, self.password)
        smtp.sendmail(self.sender, self.receiver, self.msg.as_string())
        smtp.quit()
        return True

    def timeJob(self):
        '''
        定时检查ip
        :return:
        '''
        scheduler = BlockingScheduler()
        # 每2小时触发
        scheduler.add_job(self.mailsender, 'interval', days=1)
        scheduler.start()

def main():
    emailPassword = os.getenv('163AUTHCODE')
    sender = SendEmail(emailPassword)
    sender.timeJob()


if __name__ == '__main__':
    main()