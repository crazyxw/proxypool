# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import time
from proxypool.config import *
from proxypool import redis_store
from proxypool.user_agents import random_ua


class Tester(object):

    async def parse(self, url, proxy=None, target=None):
        """
        发送一个请求
        :param url:测试代理是否可用的目标站点
        :param proxy: 完整的代理 例如: http://1.1.1.1:8000
        :param target: 目标站点
        """

        headers = {"User-Agent": random_ua()}
        if isinstance(proxy, bytes):
            proxy = proxy.decode("utf-8")
        proxies = "http://" + proxy
        try:
            conn = aiohttp.TCPConnector(verify_ssl=False)
            async with aiohttp.ClientSession(connector=conn) as session:
                async with session.get(url, proxy=proxies, headers=headers, timeout=5) as response:
                    if response.status == 200:
                        # 将ip添加到相应的目标池
                        redis_store.sadd(target, proxy)
        except Exception:
            redis_store.srem(target, proxy)

    def run(self):
        while True:
            ips = redis_store.smembers("ip_pool")
            print("ips: ", ips)
            redis_store.delete("ip_pool")
            if ips:
                for site, url in SITE.items():
                    loop = asyncio.get_event_loop()
                    tasks = [self.parse(url, proxy=ip, target=site) for ip in ips]
                    loop.run_until_complete(asyncio.wait(tasks))
            redis_store.sunionstore("ip_pool", SITE.keys())
            time.sleep(TEST_RATE)


if __name__ == "__main__":
    t = Tester()
    t.run()
