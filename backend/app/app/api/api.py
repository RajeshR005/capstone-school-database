from fastapi import APIRouter

from app.api.endpoints import login
from app.crud import add_user,update_user,bulkupdate

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(add_user.router,tags=["Add User"])
api_router.include_router(update_user.router,tags=["Update User"])
# api_router.include_router(bulkupdate.router,tags=["Bulk ADD"])