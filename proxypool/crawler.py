#获取模块,从各个网站获取代理

import json,re
from proxypool.utils import get_page
from pyquery import PyQuery as pq


class ProxyMetaclass(type):
    '''
    元类，cls, name, bases为固定参数，attrs包含
    类的一些属性，遍历attrs可获取类的所有属性，
    键名对应方法的名称
    作用：方便扩展，不用关心其他部分的实现逻辑
    扩展时只需添加crawl_开头的方法

    '''
    def __new__(cls, name, bases,attrs):
        count=0
        attrs['__CrawlFunc__'] = []
        for k,v in attrs.items():
            #判断方法是否以crawl_开头
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__']=count
        return type.__new__(cls, name, bases,attrs)

class Crawler(object,metaclass=ProxyMetaclass):
    #将所有crawl_开头的方法调用一遍
    #动态获取所有以crawl_开头的方法列表
    def get_proxies(self,callback):
        proxies=[]
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取到代理',proxy)
            proxies.append(proxy)
        return proxies

    def crawl_daili66(self,page_count=21):
        '''
        获取66代理
        :param page_count: 页码
        :return: 代理
        '''
        start_url='http://www.66ip.cn/{}.html'
        urls=[start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            print('Crawling:',url)
            html=get_page(url)
            if html:
                doc=pq(html)
                #:gt() 选择器选取 index 值大于指定数字的元素。
                # index 值从 0 开始。
                trs=doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    #:nth-child(n)选择器匹配父元素中的第n个子元素。
                    ip=tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip,port])

    def crawl_ip3366(self):
        '''
        获取ip3366代理
        :return:
        '''
        for page in range(1, 21):
            start_url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)
            html = get_page(start_url)
            ip_address=re.compile('<tr>\s*<td>(.*?)</td>\s*<td>(.*?)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_address=ip_address.findall(html)
            for address,port in re_ip_address:
                result=address+':'+ port
                yield result.replace(' ', '')

    def crawl_kuaidaili(self):
        for i in range(1, 4):
            start_url = 'http://www.kuaidaili.com/free/inha/{}/'.format(i)
            html = get_page(start_url)
            if html:
                ip_address = re.compile('<td data-title="IP">(.*?)</td>')
                re_ip_address = ip_address.findall(html)
                port = re.compile('<td data-title="PORT">(.*?)</td>')
                re_port = port.findall(html)
                for address,port in zip(re_ip_address, re_port):
                    address_port = address+':'+port
                    yield address_port.replace(' ','')

    def crawl_xicidaili(self):
        for i in range(1,21):
            start_url='http://www.xicidaili.com/nn/{}'.format(i)
            headers = {
                'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Cookie':'_free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJWRjYzc5MmM1MTBiMDMzYTUzNTZjNzA4NjBhNWRjZjliBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUp6S2tXT3g5a0FCT01ndzlmWWZqRVJNek1WanRuUDBCbTJUN21GMTBKd3M9BjsARg%3D%3D--2a69429cb2115c6a0cc9a86e0ebe2800c0d471b3',
                'Host':'www.xicidaili.com',
                'Referer':'http://www.xicidaili.com/nn/3',
                'Upgrade-Insecure-Requests':'1',
            }
            html=get_page(start_url,options=headers)
            if html:
                find_trs = re.compile('<tr class.*?>(.*?)</tr>', re.S)
                trs = find_trs.findall(html)
                for tr in trs:
                    find_ip = re.compile('<td>(\d+\.\d+\.\d+\.\d+)</td>')
                    re_ip_address = find_ip.findall(tr)
                    find_port = re.compile('<td>(\d+)</td>')
                    re_port = find_port.findall(tr)
                    for address,port in zip(re_ip_address, re_port):
                        address_port = address+':'+port
                        yield address_port.replace(' ','')

    def crawl_89ip(self):
        start_url = 'http://www.89ip.cn/apijk/?&tqsl=1000&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
        html = get_page(start_url)
        if html:
            find_ips = re.compile('(\d+\.\d+\.\d+\.\d+:\d+)', re.S)
            ip_ports = find_ips.findall(html)
            for address_port in ip_ports:
                yield address_port
