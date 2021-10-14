import os
from typing import List, Dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 项目名称
PROJECT_NAME: str = os.environ.get('PROJECT_NAME') or 'console_service'
# 是否开启debug模式
DEBUG: bool = os.environ.get('DEBUG') or True
# 项目版本
VERSION: str = os.environ.get('VERSION') or '0.0.1'

REDIS_URI: str = os.environ.get('REDIS_URI') or 'redis://:@127.0.0.1:6379/3'

# CORS 配置
ALLOWED_HOSTS: List[str] = ['*']
ALLOWED_METHODS: List[str] = ['*']
ALLOWED_HEADERS: List[str] = ['*']

# 短链域名
DOMAIN = 'https://tcpan.cn/'

# 数据库链接配置
DATABASE_URL: str = os.environ.get('DATABASE_URL') or 'mysql://root:xxxxxx/ShortUrl'

# 数据库使用那些model配置
MODELS: Dict[str, List[str]] = {'models': ['models.admin', ], 'user': ['models.User', ], 'urlmap': ['models.UrlMap', ]}

# jwt token 设置
SECRET_KEY: str = '09d25q3e094faa6ca2w556c818wqy313f7099f6f0f4caa6cf63b88e8r53d3e7'
ALGORITHM: str = "HS256"
