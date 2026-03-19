from fastapi import APIRouter
from app.controllers import post, user, auth

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(post.router)
api_router.include_router(user.router)
