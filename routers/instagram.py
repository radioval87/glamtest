from typing import Annotated

from dependencies import scrape_pic_urls
from fastapi import APIRouter, Query

instagram_router = APIRouter(prefix="", tags=["instagram"])


@instagram_router.get("/getPhotos/")
async def get_photos_urls(username: str, max_count: Annotated[int, Query(ge=0)]):
    urls = await scrape_pic_urls(username, max_count)
    return {"urls": urls}
