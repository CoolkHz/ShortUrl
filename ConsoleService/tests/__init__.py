# @Time    : 2020-05-18 15:01
# @Author  : Seven
# @File    : __init__.py.py
# @Desc    : 测试用例
import asyncio

from utils.base62 import base62_encode
from utils.DAO import set_value

urlkey = base62_encode(9931321)
print(urlkey)
asyncio.run(set_value(urlkey, "https://www.qq.com"))
