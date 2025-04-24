from fastapi import APIRouter, HTTPException, UploadFile, File, Depends, Form
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from starlette.responses import JSONResponse

from authorization import only_authorized, get_cookie_value
from pydantic_models import VideoCreate
from database import create_session
from models import Video

from werkzeug.utils import secure_filename
import os
import aiofiles
import logging
import uuid

router = APIRouter(
    prefix="/video",
    tags=["video"],
)

UPLOAD_PATH = "uploads/"
MAX_FILE_SIZE = 20 * 1024 * 1024
templates = Jinja2Templates(directory="templates/video")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/upload", response_class=HTMLResponse)
@only_authorized
async def upload_index(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})


@router.post("/upload", response_class=JSONResponse)
# @only_authorized
async def upload_video(
        request: Request,
        title: str = Form(...),
        description: str = Form(...),
        video_file: UploadFile = File(...)
):
    if video_file.size > MAX_FILE_SIZE:
        return JSONResponse(status_code=400, content={"message": "File is too large"})

    extension = os.path.splitext(video_file.filename)[1]  # .mp4, .mov и т.д.

    filename = f"{uuid.uuid4().hex}{extension}"
    savepath = os.path.join(UPLOAD_PATH, filename)
    logger.info(f"filename: {filename}")

    async with aiofiles.open(savepath, "wb") as out_file:
        while content := await video_file.read(1024 * 1024):
            await out_file.write(content)

    logger.info(f"userid {get_cookie_value(request, value="user_id")}")
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


@router.get("/{video_id}", response_class=HTMLResponse)
async def get_video(request: Request, video_id: int):
    logger.info(f"video id: {video_id}")
    async with create_session() as session:
        video = await session.scalar(
            select(Video).filter(Video.id == video_id)
        )

    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    logger.info(f"path: {os.path.join(UPLOAD_PATH, video.filename)}")
    return templates.TemplateResponse(
        "video.html",
        {
            "request": request,
            "title": video.title,
            # "author_id": video.author_id,
            # "author_name": video.author.username,
            "video_path": f"/uploads/{video.filename}",
            "likes": video.likes,
            "dislikes": video.dislikes,
        }
    )
