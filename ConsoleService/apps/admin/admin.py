# @Desc    : 管理员相关操作
from datetime import datetime

from fastapi import APIRouter, Request
from fastapi import HTTPException
from fastapi.params import Query, Body
from loguru import logger
from tortoise.queryset import Q

from models.User import User, UrlMapType
from models.admin import Admin
from schemas.User import UserModel, UserUpdateModel
from utils import success_response, parameter_error_response
from utils.depends.authentication import get_token
from utils.tools.paginator import paginator

router = APIRouter()
login_router = APIRouter()


async def check_user(user_id: int) -> User:
    """
    检查用户是否存在
    """
    result = await User.get_or_none(id=user_id, deleted=False)
    if not result:
        raise HTTPException(200, '账号不存在')
    if not result.enabled:
        raise HTTPException(200, '账号已被禁用，请联系管理员')
    return result


@router.get('/allUser', summary='获取user列表')
async def allUser(
        user_info: str = Query(None, description='account or nickname 模糊查询'),
        page: int = Query(1, description='page'),
        page_size: int = Query(15, description='page_size'),
):
    result = User.filter(deleted=False).order_by('id')
    data = await paginator(result, page, page_size)
    count = await result.count()
    return success_response([item.excludes(('password',)).data for item in data], {'count': count})


@router.post('/newUser', summary='创建用户')
async def newUser(request: Request, user: UserModel = Body(..., )):
    if request.user.type != 0:
        return parameter_error_response('权限不够，无法创建用户账号')
    result = await User.get_or_none(account=user.account, enabled=True, deleted=False)
    if result:
        raise HTTPException(403, '账号已存在')
    data = user.dict(exclude_unset=True)
    r = await User.create(**data)
    r.set_password(user.password)
    r.last_at = datetime.now()
    await r.save(update_fields=['password', 'last_at', 'type'])
    await UrlMapType.create(user_id=r.pk, title="默认分组")
    return success_response(r.data)


@router.get('/{user_id}', summary='获取admin详情')
async def retrieve(user_id: int):
    result = await check_user(user_id)
    result.excludes(('password', 'updated_at'))
    return success_response(result.data)


@router.put('/{user_id}/enabled', summary='用户禁用')
async def enabled(user_id: int):
    result = await User.get_or_none(id=user_id, deleted=False)
    if not result:
        raise HTTPException(200, '账号不存在')
    if result.enabled:
        result.enabled = False
    else:
        result.enabled = True
    await result.save()
    return success_response()


@router.put('/{user_id}/update', summary='更新用户信息')
async def update(request: Request, user_id: int, user: UserUpdateModel = Body(..., )):
    result = await check_user(user_id)
    # 不是超级管理员 不是自己的账号不能修改
    if request.user.type != 0:
        if request.user.pk != result.pk:
            return parameter_error_response('权限不够，不能修改他人账号信息')
    # 使用 dict update 更新
    result.__dict__.update(**user.dict(exclude_unset=True))
    # 密码修改
    data = user.dict(exclude_unset=True)
    if data.get('password'):
        result.set_password(data.get('password'))
        data.pop('password')

    await result.save()
    result.excludes(('password',))
    return success_response(result.data)


@router.delete('/{user_id}/del', summary='删除admin信息')
async def delete(request: Request, admin_id: int):
    if request.user.type != 0:
        return parameter_error_response('权限不够，无法删除管理员账号')
    instance = await check_user(admin_id)
    if instance.type == 0:
        return parameter_error_response('无法删除超级管理员')

    instance.deleted = True
    await instance.save(update_fields=['deleted'])
    return success_response('删除成功')


@login_router.post('/login', summary='管理员登录')
async def login(account: str = Body(..., title='账号'), password: str = Body(..., title='密码')):
    try:
        result = await Admin.get_or_none(account=account, deleted=False)
    except Exception as e:
        print(e)
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
    data.setdefault('token', get_token(result.pk, "admin"))
    print(data['token'])
    return success_response(data)
