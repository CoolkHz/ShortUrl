from passlib.context import CryptContext
from tortoise import fields

from models import BaseModelMixin
from utils.tools.fields import LocalDatetimeField

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UrlMap(BaseModelMixin):
    """
    短链接-原链接
    """
    short_url = fields.CharField(max_length=32, unique=True, null=True, description='短链接')
    origin_url = fields.CharField(max_length=256, description='原链接')
    token = fields.CharField(max_length=32, unique=True, null=True, description='token')
