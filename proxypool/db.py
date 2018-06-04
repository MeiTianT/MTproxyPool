#存储模块
#Redis的有序集合，集合的每一个元素都不重复
import redis,re
from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD,REDIS_KEY
from proxypool.setting import MAX_SCORE,MIN_SCORE,ININTIAL_SCORE
from random import choice

class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        '''
        初始化
        :param host: 地址
        :param port: 端口
        :param password: 密码
        '''
        #StrictRedis用于实现Redis大部分官方的命令,并使用官方的语法和命令
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def add(self,proxy,score=ININTIAL_SCORE):
        '''
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return:添加结果
        '''
        if not re.match('\d+\.\d+\.\d+\.\d+',proxy):
            print('代理不合规范',proxy,'丢弃')
            return
        #Redis Zscore 命令返回有序集中，成员的分数值。
        # 如果成员元素不是有序集 key 的成员，或 key 不存在，返回 nil
        if not self.db.zscore(REDIS_KEY,proxy):
            #Redis Zadd 命令用于将一个或多个成员元素及其分数值加入到有序集当中。
            #如果某个成员已经是有序集的成员，那么更新这个成员的分数值
            return self.db.zadd(REDIS_KEY,score,proxy)

    def random(self):
        '''
        随机获取有效代理，首先尝试获取最高分数（100）代理，
        如最高分不存在，则按排名获取，否则异常
        :return:得到随机代理
        '''
        #Redis Zrangebyscore 返回有序集合中指定分数区间的成员列表。
        #有序集成员按分数值递增(从小到大)次序排列。
        #具有相同分数值的成员按字典序来排列
        #获取100分的代理
        result=self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        #存在100分代理
        if len(result):
            #则choice随机选取一个
            return choice(result)
        #否则按排名获取前100
        else:
            '''
            Redis Zrange 返回有序集中，指定区间内的成员。
            其中成员的位置按分数值递增(从小到大)来排序。
            具有相同分数值的成员按字典序(lexicographical order )来排列。
            '''
            result=self.db.zrange(REDIS_KEY,0,100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self,proxy):
        '''
        代理分值-1，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分值
        '''
        score=self.db.zscore(REDIS_KEY,proxy)
        if score and score>MIN_SCORE:
            print('代理',proxy,'当前分数',score,'-1')
            '''
            Redis Zincrby 命令对有序集合中指定成员的分数加上增量 increment
            可以通过传递一个负数值 increment ，让分数减去相应的值，比如 ZINCRBY key -5 member ，就是让 member 的 score 值减去 5 。
            当 key 不存在，或分数不是 key 的成员时， ZINCRBY key increment member 等同于 ZADD key increment member 。
            当 key 不是有序集类型时，返回一个错误。
            '''
            return self.db.zincrby(REDIS_KEY,proxy,-1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            #Redis Zrem 命令用于移除有序集中的一个或多个成员，不存在的成员将被忽略。
            # 当 key 存在但不是有序集类型时，返回一个错误。
            return self.db.zrem(REDIS_KEY, proxy)

    def exists(self,proxy):
        '''
        判断是否存在
        :param proxy:
        :return: 是否存在
        '''
        return not self.db.zscore(REDIS_KEY,proxy)==None

    def max(self,proxy):
        '''
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        '''
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        '''
        获取数量
        :return: 数量
        '''
        #Redis Zcard 命令用于计算集合中元素的数量。
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        #Redis Zrevrange 命令返回有序集中，指定区间内的成员。
        # 其中成员的位置按分数值递减(从大到小)来排列。
        # 具有相同分数值的成员按字典序的逆序(reverse lexicographical order)排列。
        # 除了成员按分数值递减的次序排列这一点外，
        # ZREVRANGE 命令的其他方面和 ZRANGE 命令一样。
        return self.db.zrevrange(REDIS_KEY, start, stop - 1)

if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)











