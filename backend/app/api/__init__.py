from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.patients import router as patients_router
from app.api.doctors import router as doctors_router
from app.api.rooms import router as rooms_router
from app.api.seed_routes import router as seed_router
from app.api.schedules import router as schedules_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(patients_router)
api_router.include_router(doctors_router)
api_router.include_router(rooms_router)
api_router.include_router(seed_router)
api_router.include_router(schedules_router)

