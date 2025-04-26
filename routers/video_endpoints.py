from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload
from fastapi.responses import JSONResponse

from routers.authorization import only_authorized, get_cookie_value
from pydantic_models import VideoSchema, VideoFeedSchema
from database import create_session
from models import Video
from pylogger import logger

from constants import UPLOAD_VIDEO_PATH, MAX_VIDEO_SIZE

import os
import aiofiles
import uuid

router = APIRouter(
    prefix="/video",
    tags=["video"],
)

templates = Jinja2Templates(directory="templates/video")


@router.get("/upload", response_class=HTMLResponse)
@only_authorized
async def upload_index(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/upload", response_class=JSONResponse)
@only_authorized
async def upload_video(
        request: Request,
        title: str = Form(...),
        description: str = Form(...),
        video_file: UploadFile = File(...)
):
    if video_file.size > MAX_VIDEO_SIZE:
        return JSONResponse(status_code=400, content={"message": "File is too large"})

    extension = os.path.splitext(video_file.filename)[1]  # .mp4, .mov и т.д.

    filename = f"{uuid.uuid4().hex}{extension}"
    savepath = f"{UPLOAD_VIDEO_PATH}/{filename}"

    logger.info(f"savepath: {savepath}")
    async with aiofiles.open(savepath, "wb") as out_file:
        while content := await video_file.read(1024 * 1024):
            await out_file.write(content)

    author_id = get_cookie_value(request, value="user_id")
    video_dump = {
        "title": title,
        "description": description,
        "filename": filename,
        "author_id": author_id
    }
    async with create_session() as session:
        video_db = Video(**video_dump)
        session.add(video_db)
        await session.commit()
        await session.refresh(video_db)

    return JSONResponse(status_code=200, content={
        "message": "Видео загружено успешно",
        "video_id": video_db.id
    })


@router.get("/get-feed", response_model=list[VideoFeedSchema])
async def get_feed(request: Request):
    async with create_session() as session:
        videos = await session.scalars(
            select(Video)
            .options(joinedload(Video.author))
            .order_by(desc(Video.id))
            .limit(30)
        )

        return [VideoFeedSchema.model_validate(video) for video in videos]


@router.get("/", response_class=HTMLResponse)
async def show_feed(request: Request):
    return templates.TemplateResponse("feed.html", {"request": request})



@router.get("/{video_id}", response_class=HTMLResponse)
async def get_video(request: Request, video_id: int):
    async with create_session() as session:
        video = await session.scalar(
            select(Video).options(joinedload(Video.author)).filter(Video.id == video_id)
        )

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    video_return = VideoSchema.model_validate(video)
    return templates.TemplateResponse(
        "video.html",
        {
            "request": request,
            "user_id": get_cookie_value(request, "user_id"),
            **video_return.model_dump(),
        }
    )