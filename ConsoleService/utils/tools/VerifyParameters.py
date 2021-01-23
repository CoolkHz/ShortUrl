import re

from fastapi import HTTPException

from conf.config import config


async def verify_url(url: str):
    if re.match(r'^https?:/{2}\w.+$', url):
        return
    else:
        raise HTTPException(403, 'url不合法')


def generate_url(data):
    data['short_url'] = config.DOMAIN + data['token']
    return data


def generate_urls(data):
    for item in data:
        item['short_url'] = config.DOMAIN + str(item['token'])
    return data
