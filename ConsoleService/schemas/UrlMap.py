from pydantic import BaseModel, Field


class UrlMapModel(BaseModel):
    user_id: int = Field(None, description='user_id')
    title: str = Field(max_length=128, description='标题')
    token: str = Field(None, max_length=32, null=True, description='token')
    # short_url: str = Field(None, max_length=64, null=True, description='短链接')
    origin_url: str = Field(max_length=255, description='原链接')
    status: int = Field(None, null=True, description='status')


class UrlMapUpdateModel(BaseModel):
    title: str = Field(None, max_length=128, description='标题')
    origin_url: str = Field(None, max_length=255, description='原链接')
    status: int = Field(None, null=True, description='status')


class UrlMapUpdateRecordModel(BaseModel):
    user_id: int = Field(description='用户id')
    urlmap_id: int = Field(description='url_id')
    title: str = Field(None, null=True, max_length=128, description='标题')
    token: str = Field(None, null=True, max_length=255, description='原链接')
    status: int = Field(None, null=True, description='status')
