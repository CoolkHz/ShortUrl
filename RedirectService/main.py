import redis
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from apps.Redirect import url_router
from conf.config import config
from models import init_db
from utils import http_error_handler, validation_error_handler
from utils.tools.redis import init_redis


def add_event_handler(application: FastAPI) -> None:
    init_db(application)

    init_redis(application)


def get_application() -> FastAPI:
    logger.debug(f"CONF:{config.__dict__}")

    # 初始化 FastAPI app
    application = FastAPI(
        title=config.PROJECT_NAME,
        debug=config.DEBUG,
        version=config.VERSION,
    )

    # CORS 中间件配置
    application.add_middleware(
        CORSMiddleware,
        allow_origins=config.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=config.ALLOWED_METHODS,
        allow_headers=config.ALLOWED_HEADERS,
    )
    # 载入数据库
    add_event_handler(application)

    # 异常处理
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, validation_error_handler)
    # 路由处理
    application.include_router(url_router, prefix="")
    return application


app = get_application()
if __name__ == '__main__':
    uvicorn.run(app, **{'host': '0.0.0.0', 'port': 8000})
