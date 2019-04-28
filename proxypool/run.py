# -*- coding: utf-8 -*-
from proxypool.config import web_host, web_port, generate_proxies, test_proxies, Web_Api
from proxypool.tester.async_tester import Tester
from proxypool.crawl.crawl import run as c_run
from multiprocessing import Process
from proxypool.web.Api import app


def web():
    app.run(host=web_host, port=web_port)


def tester():
    t = Tester()
    t.run()


def main():
    if generate_proxies:
        g = Process(target=c_run)
        g.start()
    if test_proxies:
        t = Process(target=tester)
        t.start()
    if Web_Api:
        api = Process(target=web)
        api.start()


if __name__ == "__main__":
    main()
