# coding=utf-8
# 拨号间隔
ADSL_CYCLE = 300
ADSL_STEP = 4
# 拨号出错重试间隔
ADSL_ERROR_CYCLE = 5

# ADSL命令
ADSL_BASH = 'adsl-stop;adsl-start'
ADSL_BASH_START = 'adsl-start'
ADSL_BASH_STOP = 'adsl-stop'

# 代理运行端口
PROXY_PORT = 8888

# 客户端唯一标识
CLIENT_NAME = 'adsl1'

# 拨号网卡
ADSL_IFNAME = 'ppp0'

# Redis数据库IP
REDIS_HOST = 'localhost'

# Redis数据库密码, 如无则填None
REDIS_PASSWORD = 'foobared'

# Redis数据库端口
REDIS_PORT = 6379

# 代理池键名
PROXY_KEY = 'adsl'

# 测试URL
TEST_URL = 'https://www.zhihu.com/api/v4/members/kun-kun?include=allow_message,is_followed,' \
           'is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'

# 测试超时时间
TEST_TIMEOUT = 20

# API端口
API_PORT = 8000
