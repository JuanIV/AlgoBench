from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Sube 3 niveles desde src/algobench/core/config.py hasta la raíz
ROOT_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    app_name: str = "AlgoBench"
    debug: bool = False
    max_input_size: int = 10000

    model_config = SettingsConfigDict(
        env_file=ROOT_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
