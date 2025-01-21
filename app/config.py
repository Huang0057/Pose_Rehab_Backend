from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:mudowl@localhost/pose_rehab_db"
    
    class Config:
        env_file = ".env"

settings = Settings()