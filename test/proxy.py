from adslproxy import RedisClient
import os
passwd = os.getenv('REDISPASSWORD')
client = RedisClient(host='', password=passwd)
random = client.random()
all = client.all()
names = client.names()
proxies = client.proxies()
count = client.count()

print('RANDOM:', random)
print('ALL:', all)
print('NAMES:', names)
print('PROXIES:', proxies)
print('COUNT:', count)
