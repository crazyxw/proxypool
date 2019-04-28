# -*- coding: utf-8 -*-

import requests
import time
from lxml import etree
from proxypool.config import CRAWL_RATE
from proxypool.user_agents import random_ua
import re
from threading import Thread
from proxypool import redis_store
from proxypool.utils import check_ip


def parse(url):
    headers = {"User-Agent": random_ua()}
    r = requests.get(url, headers=headers)
    return r


def add_proxy(proxy):
    if not check_ip(proxy):  # 如果ip检测不合格，说明这个网站的规则已变
        return False
    redis_store.sadd("ip_pool", proxy)


def xici():
    url = "http://www.xicidaili.com/wn/"
    r = parse(url)
    html = etree.HTML(r.content)
    ip_list = html.xpath("//table[@id='ip_list']/tr[@class]")
    for ip in ip_list:
        data = ":".join(ip.xpath("./td/text()")[:2])
        add_proxy(data)


def qydaili():
    url = "http://www.qydaili.com/free/?action=china&page=1"
    r = parse(url)
    ip_list = re.findall(r'(\d+\.\d+\.\d+\.\d+).*?"PORT">(\d+)', r.text, re.S)
    for ip in ip_list:
        proxy = ":".join(ip)
        add_proxy(proxy)


def ip3366():
    url = "http://www.ip3366.net/free/"
    r = parse(url)
    ip_list = re.findall('(\d+\.\d+\.\d+\.\d+)</td>.*?<td>(\d+)</td>', r.text, re.S)
    for ip in ip_list:
        proxy = ":".join(ip)
        add_proxy(proxy)


def ip66():
    """有问题，待修复"""
    url = "http://www.66ip.cn/nmtq.php?getnum=300&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=1&api=66ip"
    r = parse(url)
    print(r.text)
    ip_list = re.findall(r"(\d+\.\d+\.\d+\.\d+:\d+)", r.text)
    print(ip_list)


def run():
    while True:
        task_list = [xici, qydaili, ip3366]
        for i in task_list:
            t = Thread(target=i)
            t.start()
        print("获取代理完毕")
        time.sleep(CRAWL_RATE)


if __name__ == "__main__":
    run()
