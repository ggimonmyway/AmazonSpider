import json
import random
import redis
import time
import sys
from  AmazonCrapy import xici

#下载中间键

class ProxyMiddleware(object):
    def __init__(self):
        print("当前路径为")
        print(sys.path[0])
        # with open('proxy.json', 'r') as f:
        #     self.proxies = json.load(f)
        #     self.r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB,
        #                         )

    def process_request(self, request, spider):
        # while True:
        #     proxy = random.choice(self.proxies)
        #     # print("当前代理ip"+proxy)
        #     if self.proxyReady(proxy):
        #         request.meta['proxy'] = 'http://{}'.format(proxy)
        #         break
        # xc1=xici.xiciip()
        # proxy = xc1.readip()
        # if proxy!="":
        #     print("当前代理ip"+proxy)
        #     request.meta['proxy'] = 'https://{}'.format(proxy)

    # def proxyReady(self, proxy):
    #     key = proxy + settings.BOT_NAME
    #     retult = self.r.exists(key)
    #     if retult:
    #         return False
    #     else:
    #         self.r.setex(key, 1, 15)
    #         #Redis Setex 命令为指定的 key 设置值及其过期时间。如果 key 已经存在， SETEX 命令将会替换旧的值。
    #         return True
