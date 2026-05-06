from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    
    DB_PASS: str = Field(default='')
    DB_HOST: str = Field(default='')
    DB_PORT: int = Field(default=0)
    DB_NAME: str = Field(default='')
    DB_USER: str = Field(default='')
    
    COINGECKO_API_KEY: str = Field(default='')
    
    model_config = SettingsConfigDict(env_file='.env')
    
    @property
    def async_db_url(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        
        
@lru_cache
def get_setting():
    return Settings()
    
settings = get_setting()