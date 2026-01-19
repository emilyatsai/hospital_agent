from fastapi import APIRouter

from app.api.endpoints import users, auth, appointments, doctors, patients, ai_insights, medical_records

api_router = APIRouter()

# Include all API endpoints
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
api_router.include_router(medical_records.router, prefix="/medical-records", tags=["medical-records"])
api_router.include_router(ai_insights.router, prefix="/ai-insights", tags=["ai-insights"])