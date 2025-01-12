# coding=utf-8
import re
import time
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from adslproxy.db import RedisClient
from adslproxy.config import *
import platform
from tqdm import tqdm

if platform.python_version().startswith('2.'):
    import commands as subprocess
elif platform.python_version().startswith('3.'):
    import subprocess
else:
    raise ValueError('python version must be 2 or 3')


class Sender():
    def get_ip(self, ifname=ADSL_IFNAME):
        """
        获取本机IP
        :param ifname: 网卡名称
        :return:
        """
        (status, output) = subprocess.getstatusoutput('ifconfig')
        if status == 0:
            pattern = re.compile(ifname + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?netmask', re.S)
            result = re.search(pattern, output)
            if result:
                ip = result.group(1)
                return ip

    def test_proxy(self, proxy):
        """
        测试代理
        :param proxy: 代理
        :return: 测试结果
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }
            response = requests.get(TEST_URL, headers=headers, proxies={
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }, timeout=TEST_TIMEOUT)
            if response.status_code == 200:
                return True
        except (ConnectionError, ReadTimeout):
            return False

    def remove_proxy(self):
        """
        移除代理
        :return: None
        """
        self.redis = RedisClient()
        self.redis.remove(CLIENT_NAME)
        print('Successfully Removed Proxy')

    def set_proxy(self, proxy):
        """
        设置代理
        :param proxy: 代理
        :return: None
        """
        self.redis = RedisClient()
        if self.redis.set(CLIENT_NAME, proxy):
            print('Successfully Set Proxy', proxy)

    def adsl(self):
        """
        拨号主进程
        :return: None
        """
        while True:
            print('ADSL Start, Remove Proxy, Please wait')
            try:
                self.remove_proxy()
            except:
                while True:
                    # (status, output) = subprocess.getstatusoutput(ADSL_BASH)
                    (status, output) = subprocess.getstatusoutput(ADSL_BASH_STOP)
                    if status == 0:
                        print("adsl-start after {} seconds".format(ADSL_STEP))
                        time.sleep(ADSL_STEP)
                    (status, output) = subprocess.getstatusoutput(ADSL_BASH_START)
                    if status == 0:
                        self.remove_proxy()
                        break
            # adsl-stop;adsl-start间隔太短会造成IP不能改变
            # (status, output) = subprocess.getstatusoutput(ADSL_BASH)
            (status, output) = subprocess.getstatusoutput(ADSL_BASH_STOP)
            if status == 0:
                print("adsl-start after {} seconds".format(ADSL_STEP))
                time.sleep(ADSL_STEP)
            (status, output) = subprocess.getstatusoutput(ADSL_BASH_START)
            if status == 0:
                print('ADSL Successfully')
                ip = self.get_ip()
                if ip:
                    print('Now IP', ip)
                    print('Testing Proxy, Please Wait')
                    proxy = '{ip}:{port}'.format(ip=ip, port=PROXY_PORT)
                    if self.test_proxy(proxy):
                        print('Valid Proxy')
                        self.set_proxy(proxy)
                        print('Sleeping')
                        pbar = tqdm(total=ADSL_CYCLE)
                        for i in range(int(ADSL_CYCLE/2)):
                            time.sleep(2)
                            pbar.update(2)
                        pbar.close()
                        # time.sleep(ADSL_CYCLE)
                    else:
                        print('Invalid Proxy')
                else:
                    print('Get IP Failed, Re Dialing')
                    time.sleep(ADSL_ERROR_CYCLE)
            else:
                print('ADSL Failed, Please Check')
                time.sleep(ADSL_ERROR_CYCLE)


def run():
    sender = Sender()
    sender.adsl()


if __name__ == '__main__':
    run()
