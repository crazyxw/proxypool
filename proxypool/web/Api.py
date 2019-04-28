# -*- coding: utf-8 -*-

from flask import Flask
from proxypool import redis_store
from proxypool.config import SITE, web_host, web_port

app = Flask(__name__)


@app.route("/")
def index():
    data = "<h1 style='text-align:center;'>Welcome to Flask Proxy System</h1>"
    return data


@app.route("/count/")
def count():
    """
    等待验证的代理数量
    :return:
    """
    ip_num = redis_store.scard("ip_pool")
    return "<p style='text-align:center;'>一共还有<strong>%s</strong>个代理等待验证...</p>" % ip_num


@app.route("/<path:platform>/count/")
def proxy_count(platform):
    if platform in SITE:
        html = "<h1 style='text-align:center;'><strong>{platform}</strong>还有<strong>{num}</strong>个代理ip可用<h1>"
        num = redis_store.scard(platform)
        return html.format(platform=platform, num=num)
    else:
        return "<h1 style='text-align:center;'>老铁,没有<strong>{}</strong>平台的代理ip噢</h1>".format(platform)


@app.route("/<path:platform>/<int:num>/")
def get_proxy(platform, num):
    if platform in SITE:
        data = redis_store.srandmember(platform, num)
        if data:
            data = ",".join(data)
            return data
        else:
            return "<h1 style='text-align:center;'><strong>{}</strong>还没有代理ip可用<h1>".format(platform)
    else:
        return "<h1 style='text-align:center;'>老铁,没有<strong>{}</strong>平台的代理ip噢</h1>".format(platform)


if __name__ == "__main__":
    app.run(host=web_host, port=web_port)
