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
