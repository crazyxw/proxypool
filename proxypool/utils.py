# -*- coding: utf-8 -*-
import re


def check_ip(proxy) -> bool:
    result = re.match(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}:\d{2,5}", proxy)
    if result:
        print(result.group())
        return True
    else:
        print("代理不合法")
        return False


if __name__ == "__main__":

    check_ip("192.168.112.11:8000")
