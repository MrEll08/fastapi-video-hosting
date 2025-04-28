from sqlalchemy import ForeignKey, JSON, text, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    login: Mapped[str] = mapped_column(unique=True, nullable=False)
    nickname: Mapped[str] = mapped_column(unique=True, nullable=False)
    password_hash: Mapped[bytes] = mapped_column(LargeBinary(60), nullable=False)

    # posts: Mapped[list["Post"]] = relationship(back_populates="author")
    # post_comments: Mapped[list["PostComment"]] = relationship(back_populates="user")

    videos: Mapped[list["Video"]] = relationship(back_populates="author")
    video_comments: Mapped[list["VideoComment"]] = relationship(
        back_populates="user",
        foreign_keys="VideoComment.user_id",
    )
    followers: Mapped[list["Subscription"]] = relationship(
        back_populates="followed",
        foreign_keys="Subscription.followed_id",
        cascade="all, delete-orphan",
    )
    subscriptions: Mapped[list["Subscription"]] = relationship(
        back_populates="follower",
        foreign_keys="Subscription.follower_id",
        cascade="all, delete-orphan",
    )
    video_likes: Mapped[list["VideoLike"]] = relationship(
        back_populates="user",
        foreign_keys="VideoLike.user_id",
        cascade="all, delete-orphan",
    )


class Subscription(Base):
    __tablename__ = "subscriptions"

    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    followed_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)

    follower: Mapped["User"] = relationship(
        back_populates="subscriptions",
        foreign_keys=follower_id,
    )
    followed: Mapped["User"] = relationship(
        back_populates="followers",
        foreign_keys=followed_id,
    )


# class Post(Base):
#     __tablename__ = "posts"
#
#     title: Mapped[str] = mapped_column(nullable=False)
#     content: Mapped[str] = mapped_column(nullable=False)
#     author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
#
#     author: Mapped["User"] = relationship(back_populates="posts")
#
#     comments: Mapped[list["PostComment"]] = relationship(
#         back_populates="post",
#         cascade="all, delete-orphan"
#     )


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
        foreign_keys="VideoComment.video_id",
        order_by="desc(VideoComment.id)",
        lazy="selectin",
        cascade="all, delete-orphan"
    )
    video_likes: Mapped[list["VideoLike"]] = relationship(
        back_populates="video",
        foreign_keys="VideoLike.video_id",
        cascade="all, delete-orphan"
    )


class VideoLike(Base):
    __tablename__ = "video_likes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"), index=True, nullable=False)
    value: Mapped[int] = mapped_column(default=0, nullable=False)

    user: Mapped["User"] = relationship(
        back_populates="video_likes",
        foreign_keys=user_id,
    )
    video: Mapped["Video"] = relationship(
        back_populates="video_likes",
        foreign_keys=video_id,
    )

# class Comment(Base):
#     __abstract__ = True
#
#     body: Mapped[str] = mapped_column(nullable=False)
#     user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
#
#     likes: Mapped[int] = mapped_column(default=0, nullable=False)
#     dislikes: Mapped[int] = mapped_column(default=0, nullable=False)
#
#
# class PostComment(Comment):
#     __tablename__ = "post_comments"
#
#     user: Mapped["User"] = relationship(back_populates="post_comments")
#     post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=False)
#     post: Mapped["Post"] = relationship(back_populates="comments")


class VideoComment(Base):
    __tablename__ = "video_comments"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    video_id: Mapped[int] = mapped_column(ForeignKey("videos.id"), index=True, nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)

    likes: Mapped[int] = mapped_column(default=0, nullable=False)
    dislikes: Mapped[int] = mapped_column(default=0, nullable=False)

    user: Mapped["User"] = relationship(back_populates="video_comments")
    video: Mapped["Video"] = relationship(back_populates="comments")

