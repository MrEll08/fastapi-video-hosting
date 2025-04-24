from sqlalchemy import ForeignKey, JSON, text, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary(60), nullable=False)

    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    post_comments: Mapped[list["PostComment"]] = relationship(back_populates="user")

    videos: Mapped[list["Video"]] = relationship(back_populates="author")
    video_comments: Mapped[list["VideoComment"]] = relationship(back_populates="user")


class Post(Base):
    __tablename__ = "posts"

    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")

    comments: Mapped[list["PostComment"]] = relationship(
        back_populates="post",
        cascade="all, delete-orphan"
    )


class Video(Base):
    __tablename__ = "videos"

    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    filename: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    likes: Mapped[int] = mapped_column(default=0, nullable=False)
    dislikes: Mapped[int] = mapped_column(default=0, nullable=False)

    author: Mapped["User"] = relationship(back_populates="videos")
    comments: Mapped[list["VideoComment"]] = relationship(
        back_populates="video",
        cascade="all, delete-orphan"
    )


class Comment(Base):
    __abstract__ = True

    body: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    likes: Mapped[int] = mapped_column(default=0, nullable=False)
    dislikes: Mapped[int] = mapped_column(default=0, nullable=False)


class PostComment(Comment):
    __tablename__ = "post_comments"

    user: Mapped["User"] = relationship(back_populates="post_comments")
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
    post: Mapped["Post"] = relationship(back_populates="comments")


class VideoComment(Comment):
    __tablename__ = "video_comments"

    user: Mapped["User"] = relationship(back_populates="video_comments")
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"), nullable=False)
    video: Mapped["Video"] = relationship(back_populates="comments")
