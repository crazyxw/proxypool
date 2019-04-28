# -*- coding: utf-8 -*-
import redis
from proxypool.config import REDIS_HOST, REDIS_PORT


redis_store = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

