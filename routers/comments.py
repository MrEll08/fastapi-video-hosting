from fastapi import APIRouter, Request, Depends, Body, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from starlette.responses import JSONResponse

from models import Video
from pydantic_models import UserCreate
from routers.authorization import only_authorized, get_cookie_value
from pylogger import logger
from pydantic_models import CommentCreate, CommentResponse
from models import VideoComment

from database import create_session

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


@router.get("/video/{video_id}", response_model=list[CommentResponse])
async def get_comments(video_id: int):
    async with create_session() as session:
        video = await session.scalar(
            select(Video).options(
                selectinload(Video.comments).selectinload(VideoComment.user)
            ).filter(Video.id == video_id)
        )
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")
        return [CommentResponse.model_validate(com) for com in video.comments]


@router.post("/video/{video_id}")
@only_authorized
async def comment_video(request: Request, video_id: int, new_comment: CommentCreate = Body(...)):
    user_id = get_cookie_value(request, "user_id")
    async with create_session() as session:
        video = await session.scalar(
            select(Video).filter(Video.id == video_id)
        )
        if not video:
            raise HTTPException(status_code=404, detail="Video not found")

        comment = VideoComment(user_id=user_id, video_id=video_id, content=new_comment.content)
        session.add(comment)
        await session.commit()
        return JSONResponse(status_code=200, content={"message": "Comment created"})
