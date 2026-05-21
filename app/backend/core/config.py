from pydantic_settings import BaseSettings
 
 
class Settings(BaseSettings):
    # Base de datos
    DB_HOST: str 
    DB_PORT: int 
    DB_NAME: str 
    DB_USER: str 
    DB_PASS: str 
 
    # FastAPI
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"

    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8   # 8 horas

    # CORS - orígenes permitidos (frontend React)
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    # Seed del admin inicial
    ADMIN_MAIL: str
    ADMIN_PASSWORD: str

    # ML - rutas a los archivos del modelo
    BASE_DATASET_PATH: str = "ml/base_dataset/demanda_limpia.csv"
    MODEL_PATH: str = "ml/trained/gradient_boosting.joblib"
    ENCODERS_PATH: str = "ml/trained/encoders.joblib"
 
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
 
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
 
 
settings = Settings()