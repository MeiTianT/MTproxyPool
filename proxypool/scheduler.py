import time
from multiprocessing import Process
from proxypool.api import app
from proxypool.getter import Getter
from proxypool.tester import Tester
from proxypool.setting import *

#调度模块调用上面三个模块，将这3个模块通过多进程的形式运行起来
class Scheduler():
    def schedule_tester(selfself,cycle=TESTER_CYCLE):
        '''
        定时测试代理
        :param cycle:
        :return:
        '''
        tester = Tester()
        #死循环调用run
        while True:
            print('测试器开始运行')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self,cycle=GETTER_CYCLE):
        '''
        定数获取代理
        :param cycle:
        :return:
        '''
        getter = Getter()
        while True:
            print('开始抓取代理')
            getter.run()
            time.sleep(cycle)

    def schedule_api(self):
        '''
        开启API
        :return:
        '''
        app.run(API_HOST,API_PORT)

    #启动入口
    def run(self):
        print('代理池开始运行')
        if TESTER_ENABLED:
            test_process=Process(target=self.schedule_tester)
            test_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process = Process(target=self.schedule_api)
            api_process.start()
