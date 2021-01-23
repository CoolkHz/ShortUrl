from pydantic import BaseModel, Field


class UserModel(BaseModel):
    account: str = Field(max_length=32, description='用户名')
    password: str = Field(max_length=128, description='密码')
    # nickname: str = Field(None, max_length=32, null=True, description='管理员昵称')
    # avatar_url: str = Field(None, max_length=255, null=True, description='头像URL')
    # phone: str = Field(None, max_length=30, null=True, description='手机号码')
    email: str = Field(None, max_length=32, null=True, description='邮箱')
    # wechat_id: str = Field(None, max_length=32, null=True, description='微信号')


class UserUpdateModel(BaseModel):
    password: str = Field(None, max_length=128, null=True, description='密码')
    # nickname: str = Field(None, max_length=32, null=True, description='管理员昵称')
    avatar_url: str = Field(None, max_length=255, null=True, description='头像URL')
    remark: str = Field(None, max_length=255, null=True, description='备注')
    email: str = Field(None, max_length=32, null=True, description='邮箱')

    # wechat_id: str = Field(None, max_length=32, null=True, description='微信号')


class UrlMapTypeModel(BaseModel):
    user_id: int = Field(description='用户id')
    title: str = Field(max_length=128, description='标题')


class UrlMapTypeUpdateModel(BaseModel):
    title: str = Field(max_length=128, description='标题')
