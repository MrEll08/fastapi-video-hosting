import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routers import video_endpoints, authorization, subscriptions

app = FastAPI()
app.include_router(authorization.router)
app.include_router(video_endpoints.router)
app.include_router(subscriptions.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
