from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from functools import wraps
from pylogger import logger
import jwt
import bcrypt

from sqlalchemy import select

from database import create_session
from pydantic_models import UserCreate, UserLogin
from models import User

SECRET_KEY = "96619882ee1058b33d61ac7ec4b5f295da8814f9ce773a5c6e11b5b7"
ALGORITHM = "HS256"

router = APIRouter(
    prefix="",
    tags=["authorization"]
)
templates = Jinja2Templates(directory="templates/authorization")


def get_cookie(request: Request):
    token = request.cookies.get("jwt-token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        return None


def get_cookie_value(request: Request, value: str = "user"):
    payload = get_cookie(request)
    if not payload:
        return None
    return payload[value]


async def create_token(user: UserCreate | UserLogin):
    user_id = -1
    if isinstance(user, UserCreate):
        user_id = user.id
    else:
        async with create_session() as session:
            user_id = await session.scalar(select(User.id).where(User.login == user.login))
    payload = {
        "user": user.login,
        "user_id": user_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def only_authorized(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = kwargs.get("request")
        if not request:
            return ValueError("Request not found")
        user = get_cookie_value(request, value="user")
        if not user:
            return RedirectResponse("/login")
        return await func(*args, **kwargs)
    return wrapper

@router.get("/", response_class=HTMLResponse)
async def home_index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/welcome", response_class=HTMLResponse)
@only_authorized
async def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_index(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_logic(user: UserCreate):
    async with create_session() as session:
        session_user = await session.scalar(
            select(User).where(User.login == user.login)
        )
        if session_user is not None:
            return JSONResponse(status_code=400, content={"success": False, "message": "User already exists"})

        dump = user.model_dump()
        dump["password_hash"] = bcrypt.hashpw(dump["password"].encode("utf-8"), bcrypt.gensalt())
        dump.pop("password")
        new_user = User(**dump)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return JSONResponse(status_code=200, content={"success": True})


@router.get("/login", response_class=HTMLResponse)
async def login_index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_logic(request: Request, login_user: UserLogin):
    async with create_session() as session:
        db_user = await session.scalar(
            select(User).where(User.login == login_user.login)
        )
        if not db_user:
            return JSONResponse(status_code=404, content={"success": False, "message": "User not found"})

        if not bcrypt.checkpw(login_user.password.encode("utf-8"), db_user.password_hash):
            return JSONResponse(status_code=401, content={"success": False, "message": "Incorrect password"})

        token = await create_token(db_user)
        logger.info(f"Logged in as {login_user.login}")
        response = JSONResponse(content={
            "success": True,
            "login": login_user.login,
        })
        response.set_cookie(key="jwt-token", value=token, httponly=True, secure=True)
        return response
