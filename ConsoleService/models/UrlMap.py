from passlib.context import CryptContext
from tortoise import fields

from models import BaseModelMixin
from utils.tools.fields import LocalDatetimeField

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UrlMap(BaseModelMixin):
    """
    短链接-原链接
    """
    user_id = fields.IntField(description='用户id')
    title = fields.CharField(max_length=128, description='标题')
    token = fields.CharField(max_length=32, unique=True, null=True, description='token')
    # short_url = fields.CharField(max_length=64, unique=True, null=True, description='短链接')
    origin_url = fields.CharField(max_length=256, description='原链接')

    enabled = fields.BooleanField(default=True, description="启用")
    status = fields.IntField(description='状态')

    def get_created_at(self) -> str or None:
        if not self.created_at:
            return self.created_at
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')


class ExpiredUrlMap(BaseModelMixin):
    """
    过期或逻辑删除
    """
    user_id = fields.IntField(description='用户id')
    title = fields.CharField(max_length=128, description='标题')
    token = fields.CharField(max_length=32, unique=True, null=True, description='token')
    # short_url = fields.CharField(max_length=32, unique=True, null=True, description='短链接')
    origin_url = fields.CharField(max_length=256, description='原链接')
    created_time = LocalDatetimeField(null=True, description='创建时间')


class UrlMapToType(BaseModelMixin):
    """
    短链分类-分组映射
    """
    type_id = fields.IntField(description='分类id')
    urlmap_id = fields.IntField(description='urlmap_id')


class UrlMapUpdateRecord(BaseModelMixin):
    """
    活链更新记录
    """
    user_id = fields.IntField(description='用户id')
    urlmap_id = fields.IntField(description='用户id')
    title = fields.CharField(null=True, max_length=128, description='标题')
    origin_url = fields.CharField(null=True, max_length=255, description='更改前原链接')
    updated_time = LocalDatetimeField(null=True, description='更新时间')
