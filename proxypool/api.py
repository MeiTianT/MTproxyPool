from flask import Flask,g

from proxypool.db import RedisClient

__all__ = ['app']

#声明Flask对象
app=Flask(__name__)

def get_conn():
    if not hasattr(g,'redis'):
        g.redis=RedisClient()
    return g.redis

#http://127.0.0.1:5000/
@app.route('/')
def index():
    return '<h2>Welcome to MitaProxy Pool System</h2>'

#http://127.0.0.1:5000/random
@app.route('/random')
def get_proxy():
    '''
    获取随机可用代理
    :return:
    '''
    conn=get_conn()
    return conn.random()

##http://127.0.0.1:5000/cocunt
@app.route('/count')
def get_counts():
    '''
    代理池总数
    :return:
    '''
    conn=get_conn()
    return str(conn.count())

if __name__ == '__main__':
    app.run()