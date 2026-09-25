import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True)
    
    PROJECT_NAME: str = "Hospital Patient Scheduling System"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./hospital_scheduling.db")
    
    # Scheduling window configuration
    WORK_DAY_START: str = "09:00"  # 9:00 AM
    WORK_DAY_END: str = "13:00"    # 1:00 PM (4 hours = 240 minutes)
    
    # Heuristic Weights
    WEIGHT_WAITING_TIME: float = 5.0
    WEIGHT_CONFLICTS: float = 100.0
    WEIGHT_PRIORITY_PENALTY: float = 20.0
    WEIGHT_UNDER_UTILIZATION: float = 10.0

settings = Settings()
