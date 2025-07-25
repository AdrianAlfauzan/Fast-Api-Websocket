from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.chat import router as chat_router
from app.api.v1.chat import router as chat_rooms_router
from app.api.v1.call import router as call_router
# from app.api.v1.user_mgt import router as user_router
# from app.api.v1.position_mgt import router as position_router
# from app.api.v1.company_mgt import router as company_router
# from app.api.v1.employee_mgt import router as employee_router
# from app.api.v1.dailySalary_mgt import router as dailySalary_router
# from app.api.v1.employee_daily_salary_mgt import router as employee_daily_salary_router
# from app.api.v1.employee_monthly_salary_mgt import router as employee_monthly_salary_router
# from app.api.v1.application_mgt import router as application_router
# from app.api.v1.attendance_mgt import router as attendance_router
# from app.api.v1.faceapi_mgt import router as faceapi_router
# from app.api.v1.face_mgt import router as face_router
# from app.api.v1.dashboard_mgt import router as dashboard_router
# from app.api.v1.shift_schedule_mgt import router as shift_schedule_router
# from app.api.v1.employee_shift_mgt import router as employee_shift_router

router = APIRouter(prefix="/v1")
router.include_router(auth_router)
router.include_router(chat_router)
router.include_router(chat_rooms_router)
router.include_router(call_router)
# router.include_router(user_router)
# router.include_router(position_router)
# router.include_router(company_router)
# router.include_router(employee_router)
# router.include_router(dailySalary_router)
# router.include_router(employee_daily_salary_router)
# router.include_router(employee_monthly_salary_router)
# router.include_router(application_router)
# router.include_router(faceapi_router)
# router.include_router(face_router)
# router.include_router(attendance_router)
# router.include_router(dashboard_router)
# router.include_router(shift_schedule_router)
# router.include_router(employee_shift_router)
