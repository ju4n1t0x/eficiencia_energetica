from pydantic_settings import BaseSettings
 
 
class Settings(BaseSettings):
    # Base de datos
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_NAME: str = "energia_db"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
 
    # FastAPI
    DEBUG: bool = True
    API_PREFIX: str = "/api"
 
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
 
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
 
 
settings = Settings()