from passlib.context import CryptContext

from models import BaseModelMixin
from utils.tools.fields import LocalDatetimeField
from tortoise import fields

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModelMixin):
    """
    用户表
    """
    account = fields.CharField(max_length=32, unique=True, null=True, description='用户名')
    password = fields.CharField(max_length=128, null=True, description='密码')
    avatar_url = fields.CharField(max_length=255, null=True, description='头像URL')
    # wechat_id = fields.CharField(max_length=32, null=True, description='微信号')
    # real_name = fields.CharField(max_length=32, null=True, description='真实姓名')
    email = fields.CharField(max_length=32, null=True, description='邮箱')
    # mobile = fields.CharField(max_length=30, null=True, description='手机号码')

    enabled = fields.BooleanField(default=True, description="启用")
    type = fields.IntField(default=1, description='管理员类型0:超级管理员1:管理员')
    last_at = LocalDatetimeField(null=True, description='最后登录时间')
    remark = fields.CharField(max_length=255, null=True, description='备注')

    class Meta:
        exclude = ('password',)

    def set_password(self, password: str):
        """ 设置加密密码
        :param password: 明文密码
        """
        self.password = pwd_context.hash(password)

    def check_password(self, raw_password: str) -> bool:
        """ 检查密码是否正确
        :param raw_password: 明文密码
        :return: bool
        """
        return pwd_context.verify(raw_password, self.password)

    def get_created_at(self) -> str or None:
        if not self.created_at:
            return self.created_at
        return self.created_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_updated_at(self) -> str or None:
        if not self.updated_at:
            return self.updated_at
        return self.updated_at.strftime('%Y-%m-%d %H:%M:%S')

    def get_avatar_url(self) -> str:
        if self.avatar_url:
            return self.avatar_url
        return 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'


class UrlMapType(BaseModelMixin):
    """
    短链分类-分组
    """
    user_id = fields.IntField(description='用户id')
    title = fields.CharField(max_length=128, description='标题')
