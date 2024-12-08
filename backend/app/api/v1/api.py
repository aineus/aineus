from fastapi import APIRouter
from app.api.v1.endpoints import news, users, prompts, auth

api_router = APIRouter()

api_router.include_router(news.router, prefix="/news", tags=["news"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(auth.router, tags=["auth"])