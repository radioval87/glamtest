from fastapi import FastAPI

from routers.instagram import instagram_router


app = FastAPI(debug=True)


app.include_router(instagram_router)
