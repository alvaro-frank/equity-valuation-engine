from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    # Required API Keys
    alpha_vantage_api_key: str = Field(..., validation_alias="ALPHA_VANTAGE_API_KEY")
    gemini_api_key: str = Field(..., validation_alias="GEMINI_API_KEY")
    
    # Optional Server Configs
    host: str = Field("0.0.0.0", validation_alias="HOST")
    port: int = Field(8000, validation_alias="PORT")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
