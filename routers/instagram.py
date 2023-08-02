from typing import Annotated

from fastapi import APIRouter, Query

from dependencies import scrape_pic_urls


instagram_router = APIRouter(prefix="", tags=["instagram"])


@instagram_router.get("/getPhotos/")
def get_photos_urls(username: str, max_count: Annotated[int, Query(ge=0)]):
    urls = scrape_pic_urls(username, max_count)
    return {"urls": urls}
