from functools import wraps

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy import select

from database import create_session
from pydantic_models import SubscriptionCreate
from models import Subscription

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"],
)


async def check_subscription(subsc: SubscriptionCreate):
    async with create_session() as session:
        subscription = await session.scalar(
            select(Subscription).filter_by(follower_id=subsc.follower_id, followed_id=subsc.followed_id)
        )
        return subscription is not None


@router.get("/check", response_class=JSONResponse)
async def check_subscribed(subsc: SubscriptionCreate = Depends()):
    status = await check_subscription(subsc)
    return JSONResponse({"status": status})


def subscription_status(flag: bool):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            subsc = kwargs.get("subsc")
            if not subsc or await check_subscription(subsc) != flag:
                raise HTTPException(status_code=404, detail="Subscription not found")

            return await func(*args, **kwargs)

        return wrapper

    return decorator


@router.post("/subscribe")
@subscription_status(False)
async def subscribe(request: Request, subsc: SubscriptionCreate = Depends()):
    async with create_session() as session:
        subscription = Subscription(**subsc.model_dump())
        session.add(subscription)
        await session.commit()
        await session.refresh(subscription)
        return JSONResponse(status_code=200, content={"subscribed": True})


@router.post("/unsubscribe")
@subscription_status(True)
async def subscribe(request: Request, subsc: SubscriptionCreate = Depends()):
    async with create_session() as session:
        subscription = await session.scalar(
            select(Subscription).filter_by(follower_id=subsc.follower_id, followed_id=subsc.followed_id)
        )
        await session.delete(subscription)
        await session.commit()
        return JSONResponse(status_code=200, content={"subscribed": False})
