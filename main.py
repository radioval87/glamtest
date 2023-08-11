import logging

from fastapi import FastAPI

from routers.instagram import instagram_router


app = FastAPI()


app.include_router(instagram_router)


logging.basicConfig(
    format=(
        '%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s] '
        '%(message)s'
    ),
    level=logging.INFO
)
