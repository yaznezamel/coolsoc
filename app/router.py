from fastapi import APIRouter
from app.controllers import post, user

api_router = APIRouter()

api_router.include_router(post.router)
api_router.include_router(user.router)
