import uvicorn
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from routers import video_endpoints, authorization, subscriptions, comments

app = FastAPI()
app.include_router(authorization.router)
app.include_router(video_endpoints.router)
app.include_router(subscriptions.router)
app.include_router(comments.router)

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home_index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
