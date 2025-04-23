import uvicorn
from fastapi import Depends, FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
import logging
import jwt
import bcrypt

from sqlalchemy import select

from database import create_session
from users.user_models import UserCreate, UserLogin
from models import User

SECRET_KEY = "96619882ee1058b33d61ac7ec4b5f295da8814f9ce773a5c6e11b5b7"
ALGORITHM = "HS256"

app = FastAPI()
templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.get("/", response_class=HTMLResponse)
async def home_index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/welcome", response_class=HTMLResponse)
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
async def register_index(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register")
async def register_logic(user: UserCreate):
    async with create_session() as session:
        session_user = await session.scalar(
            select(User).where(User.login == user.login)
        )
        if session_user is not None:
            return JSONResponse(status_code=400, content={"success": False, "message": "User already exists"})

        dump = user.model_dump()
        logger.info(dump)
        dump["password_hash"] = bcrypt.hashpw(dump["password"].encode("utf-8"), bcrypt.gensalt())
        dump.pop("password")
        new_user = User(**dump)

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return JSONResponse(status_code=200, content={"success": True})


@app.get("/login", response_class=HTMLResponse)
async def login_index(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


def create_token(user: UserCreate | UserLogin):
    payload = {
        "login": user.login,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/login", response_class=HTMLResponse)
async def login_logic(request: Request, login_user: UserLogin):
    async with create_session() as session:
        db_user = await session.scalar(
            select(User).where(User.login == login_user.login)
        )
        if not db_user:
            return JSONResponse(status_code=404, content={"success": False, "message": "User not found"})

        if not bcrypt.checkpw(login_user.password.encode("utf-8"), db_user.password_hash):
            return JSONResponse(status_code=401, content={"success": False, "message": "Incorrect password"})

        token = create_token(db_user)
        response = JSONResponse(content={
            "success": True,
            "login": login_user.login,
            "token": token,
        })
        response.set_cookie(key="jwt-token", value=token, httponly=True, secure=True)
        return response


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
