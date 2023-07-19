from fastapi import APIRouter

from app.api.endpoints import like_router, post_router, user_router

main_router = APIRouter()
main_router.include_router(user_router)
main_router.include_router(post_router, prefix="/posts", tags=["Post"])
main_router.include_router(like_router, prefix="/likes", tags=["Like"])
