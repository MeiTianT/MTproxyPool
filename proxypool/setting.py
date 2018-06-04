#redis数据库配置
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None
#有序集合的键名，通过它获取代理存储所使用的有序集合
REDIS_KEY = 'proxies'

#代理分数
'''
100：最可用，检测到不可用则-1
0：最不可用，移除
10：新获取的ip为10分，经测试可用则变为100，不可用则-1
'''
MAX_SCORE = 100
MIN_SCORE = 0
ININTIAL_SCORE = 10
#可用状态码
VALID_STATUS_CODES = [200,302]

#代理池数量界限
POOL_UPPER_THRESHOLD = 50000

#检查周期
TESTER_CYCLE = 20
#获取周期
GETTER_CYCLE = 300

#测试API，建议抓哪个网站测哪个
TEST_URL= 'http://www.baidu.com'

#API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

#开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

#最大批量测试
BATCH_TEST_SIZE = 10