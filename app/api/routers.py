from fastapi import APIRouter

from app.api.endpoints import (charity_project_router, donation_router,
                               google_api_router, user_router)

main_router = APIRouter()
main_router.include_router(
    charity_project_router,
    tags=['Charity projects'],
)

main_router.include_router(
    donation_router,
    tags=['Donations']
)

main_router.include_router(
    google_api_router,
    tags=['Google']
)
main_router.include_router(user_router)
