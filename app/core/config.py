from pydantic_settings import BaseSettings
from pydantic import ConfigDict
 
 
class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")
 
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
 
 
settings = Settings()
  
