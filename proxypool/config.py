# -*- coding: utf-8 -*-

# 抓取频率 10分钟抓一次
CRAWL_RATE = 600

# 验证频率  每分钟验证一次代理池里的ip是否可用
TEST_RATE = 60

# REDIS配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

# 哪些网站需要使用代理, key是redis中队列的名字，value是检测ip是否可用的站点
SITE = {
    "baidu": "https://www.baidu.com",
}

# 是否开启抓取模块
generate_proxies = True

# 是否开启测试模块
test_proxies = True

# 是否开启WEB接口
Web_Api = True
# 接口
web_host = "0.0.0.0"
web_port = 5000
