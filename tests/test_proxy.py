# -*- coding: utf-8 -*-
import aiohttp
import asyncio


async def fetch(url, proxy):
    conn = aiohttp.TCPConnector(verify_ssl=False)
    async with aiohttp.ClientSession(connector=conn) as session:
        async with session.get(url, proxy=proxy, timeout=3) as response:
            html = await response.text()
            print(html)


def run(url, proxy):
    loop = asyncio.get_event_loop()
    tasks = [fetch(url, proxy)]
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == "__main__":
    url = "https://httpbin.org/get"

    proxy = "http://" + "61.128.208.94:3128"

    run(url, proxy)
