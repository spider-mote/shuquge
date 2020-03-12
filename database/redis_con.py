import redis
import random

class Redis_database(object):

    def __init__(self):
        self.db = redis.Redis(host='127.0.0.1', port=6379, password='abc123456',db=0)

    # 获取代理ip
    def get_proxis(self):
        proxy_list = self.db.lrange('proxies',0,-1)
        # print(proxy_list)
        proxy_b = random.choice(proxy_list)
        # bytes转换成str
        proxy = proxy_b.decode(encoding='utf-8')
        return proxy

    def sava_urls(self,url):
        self.db.lpush('shuquge:start_urls',url)


if __name__ == '__main__':
    c = Redis_database()
    # c.get_proxis()
    c.sava_urls('http://www.shuquge.com/txt/5809/index.html')
