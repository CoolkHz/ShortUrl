import asyncio
from datetime import datetime

from fastapi import APIRouter, HTTPException, Request, FastAPI
from fastapi.params import Query, Body
from loguru import logger

from models.UrlMap import UrlMap
from models.User import User
from schemas.UrlMap import UrlMapModel, UrlMapUpdateModel
from utils import success_response, parameter_error_response
from utils.base62 import base62_encode
from utils.depends.authentication import get_token
from utils.tools import paginator, redis
from utils.tools.VerifyParameters import verify_url, generate_url, generate_urls
from utils.tools.set_urlmap_update import set_urlmap_update

router = APIRouter()
login_router = APIRouter()


async def check_urlmap(urlmap_id: int) -> UrlMap:
    """
    检查urlmap是否存在
    """
    result = await UrlMap.get_or_none(id=urlmap_id, deleted=False)
    if not result:
        raise HTTPException(404, 'url不存在')
    if not result.enabled:
        raise HTTPException(403, '该url已停用')
    return result

#
# @router.get('/user/', summary='user')
# async def monitor():
#     return 'ok'


@router.get('/allUrl', summary='获取url列表')
async def all_url(
        page: int = Query(1, description='page'),
        page_size: int = Query(15, description='page_size'),
):
    result = UrlMap.filter(deleted=False).order_by('id')
    data = await paginator(result, page, page_size)
    count = await result.count()
    return success_response(
        generate_urls([item.excludes(('enabled', 'status', 'deleted')).data for item in data]),
        {'count': count})


@router.post('/newUrl', summary='创建url')
async def new_url(request: Request, url: UrlMapModel = Body(..., )):
    data = url.dict(exclude_unset=True)
    await verify_url(data['origin_url'])
    data['user_id'] = request.user.pk
    print(data)
    r = await UrlMap.create(**data)
    r.token = base62_encode(r.pk)
    await r.save(update_fields=['token', ])
    await request.app.state.redis.set(r.token, data['origin_url'])
    return success_response(generate_url(r.data))


@router.put('/{urlmap_id}/update', summary='更新url信息')
async def update_urlmap(request: Request, urlmap_id: int, urlmap: UrlMapUpdateModel = Body(..., )):
    result = await check_urlmap(urlmap_id)
    if request.user.type != 0:
        if request.user.pk != result.user_id:
            return parameter_error_response('权限不够，不能修改他人账号信息')
    await set_urlmap_update(request.user.pk, result.pk)
    # 使用 dict update 更新
    result.__dict__.update(**urlmap.dict(exclude_unset=True))
    # data = urlmap.dict(exclude_unset=True)
    await result.save()
    await request.app.state.redis.set(result.token, result.data['origin_url'])
    result.excludes(('enabled', 'status', 'deleted'))
    return success_response(generate_url(result.data))


@router.put('/{urlmap_id}/enabled', summary='url禁用')
async def url_enabled(request: Request, urlmap_id: int):
    result = await UrlMap.get_or_none(id=urlmap_id, deleted=False)
    if request.user.type != 0:
        if request.user.pk != result.user_id:
            return parameter_error_response('权限不够，不能修改他人账号信息')
    if not result:
        raise HTTPException(404, 'url不存在')
    if result.enabled:
        result.enabled = False
        await request.app.state.redis.delete(result.token)
    else:
        result.enabled = True
        await request.app.state.redis.set(result.token, result.origin_url)
    await result.save()
    return success_response()


@router.delete('/{urlmap_id}/del', summary='逻辑删除url信息')
async def delete_url(request: Request, urlmap_id: int):
    instance = await check_urlmap(urlmap_id)
    if request.user.type != 0:
        if request.user.pk != instance.user_id:
            return parameter_error_response('权限不够，不能修改他人账号信息')

    instance.deleted = True
    await instance.save(update_fields=['deleted'])
    await request.app.state.redis.delete(instance.token)
    return success_response('删除成功')


@login_router.post('/login', summary='用户登录')
async def login(account: str = Body(..., title='用户名'), password: str = Body(..., title='密码')):
    result = await User.get_or_none(account=account, deleted=False)
    if not result:
        raise HTTPException(200, '账号不存在')
    if result.enabled is not True:
        raise HTTPException(200, '账号已经被禁用，请联系超级管理员')
    try:
        if not result.check_password(password):
            raise HTTPException(200, '密码错误，请检查')
    except Exception as e:
        logger.error(e)
        raise HTTPException(200, '密码错误，请检查')
    result.last_at = datetime.now()
    await result.save(update_fields=['last_at'])
    data = result.excludes(('password', 'deleted')).data
    data.setdefault('token', get_token(result.pk, "user"))
    return success_response(data)
