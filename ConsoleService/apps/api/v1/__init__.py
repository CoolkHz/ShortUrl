# @Time    : 2020-05-18 16:19
# @Author  : Seven
# @File    : __init__.py.py
# @Desc    : Api Router

from fastapi import APIRouter, Depends

from utils.depends.authentication import user_jwt_authentication
from . import User as router_user

api_router = APIRouter()

api_router.include_router(router_user.login_router, prefix='/v1', tags=['v1'])
# api_router.include_router(cbv_router.router, prefix='/v1', tags=['v1-cbv'])

# jwt认证/rbac权限
api_router.include_router(
    router_user.router,
    prefix='/v1',
    tags=['v1'],
    dependencies=[Depends(user_jwt_authentication), ],
)
