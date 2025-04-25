import uvicorn
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import logging

from routers import video_endpoints, authorization, subscriptions

app = FastAPI()
app.include_router(authorization.router)
app.include_router(video_endpoints.router)
app.include_router(subscriptions.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
