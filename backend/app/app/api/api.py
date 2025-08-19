from fastapi import APIRouter

from app.api.endpoints import login,attendance,staff,masters,master_association,question_crud,leave_crud,forgot_passwrod,mark_crud,projects
from app.crud import add_user,update_user,bulkupdate

api_router = APIRouter()

api_router.include_router(login.router, tags=["Authentication"])
api_router.include_router(add_user.router,tags=["User"])
# api_router.include_router(update_user.router,tags=["Update User"])

api_router.include_router(attendance.router,tags=["Attendance"])
api_router.include_router(leave_crud.router,tags=["Leave Requests"])

api_router.include_router(staff.router,tags=["Staff"])
api_router.include_router(mark_crud.router,tags=["Marks"])
api_router.include_router(question_crud.router,tags=["Questions"])
# api_router.include_router(bulkupdate.router,tags=["Bulk ADD"])
api_router.include_router(masters.api_router)
api_router.include_router(master_association.api_router)
api_router.include_router(forgot_passwrod.router,tags=["Authentication"])
api_router.include_router(projects.router,tags=["Project Submission"])
