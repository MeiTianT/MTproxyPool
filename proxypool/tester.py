import asyncio
#异步请求库，requests为同步请求库，程序需要等待
#网页加载完成之后才能继续执行，这个过程会阻塞等待响应
import aiohttp
#异步请求：在请求发出之后，程序可以继续执行其他事情
#当响应到达时，程序再去处理这个过程
import time,sys

try:
    from aiohttp import ClientError
except:
    from aiohttp import ClientProxyConnectionError as ProxyConnectionError
from proxypool.db import RedisClient
from proxypool.setting import *

class Tester(object):
    def __init__(self):
        #创建对象，供该对象中其他方法使用
        self.redis = RedisClient()

    #异步方法，aiohttp写法
    async def test_single_proxy(self,proxy):
        '''
        测试单个代理
        :param proxy:
        :return:
        '''
        conn=aiohttp.TCPConnector(verify_ssl=False)
        #创建ClientSession对象，类似于requests的session对象
        #可直接调用该对象的get方法访问网页
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy,bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                print('正在测试',proxy)
                #通过proxy传递参数给get()
                #TEST_URL测试url
                async with session.get(TEST_URL,proxy=real_proxy,timeout=15,allow_redirects=False) as response:
                    #VALID_STATUS_CODES,状态码列表
                    if response.status in VALID_STATUS_CODES:
                        #max()将代理分数设为100
                        self.redis.max(proxy)
                        print('代理可用',proxy)
                    else:
                        #decrease()代理分数-1
                        self.redis.decrease(proxy)
                        print('请求响应码不合法',response.status,'IP',proxy)
            except (ClientError, aiohttp.client_exceptions.ClientConnectorError, asyncio.TimeoutError, AttributeError):
                self.redis.decrease(proxy)
                print('请求代理失败',proxy)

    def run(self):
        '''
        测试主函数
        :return:
        '''
        print('测试器开始运行')
        try:
            count=self.redis.count()
            print('当前剩余', count, '个代理')
            #BATCH_TEST_SIZE最大测试数
            for i in range(0, count, BATCH_TEST_SIZE):
                start = i
                stop = min(i+BATCH_TEST_SIZE, count)
                print('正在测试第', start + 1, '-', stop, '个代理')
                #获取测试代理
                test_proxies = self.redis.batch(start,stop)
                loop=asyncio.get_event_loop()
                tasks=[self.test_single_proxy(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sys.stdout.flush()
                time.sleep(5)
        except Exception as e:
            print('测试器发生错误', e.args)



