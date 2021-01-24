from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse

# from tortoise import Tortoise
from models.UrlMap import UrlMap
from utils.base62 import base62_decode

url_router = APIRouter()


async def check_url(id: int) -> UrlMap:
    """
    查询记录是否存在
    """
    result = await UrlMap.get_or_none(id=id, deleted=False)
    if not result:
        raise HTTPException(404, '记录不存在')
    return result


@url_router.get('/{token}')
async def url_redirect(request: Request, token):
    origin_url = await request.app.state.redis.get(token)
    if not origin_url:
        result = await check_url(base62_decode(token))
        await request.app.state.redis.set(result.token, result.origin_url)
        origin_url = result.origin_url
    Response = RedirectResponse(origin_url, status_code=302)
    return Response
