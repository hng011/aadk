from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # APP
    PROJECT_NAME: str = Field(default="AADK")
    GITHUB_TOKEN: str = Field(default=...)
    HUGGING_FACE_TOKEN: str = Field(default=...)
    NOTION_TOKEN: str = Field(default=...)
    CONTEXT7_TOKEN: str = Field(default=...)
    
    # GCP
    GOOGLE_GENAI_USE_VERTEXAI: str = Field(default="FALSE")
    GOOGLE_CLOUD_PROJECT: str = Field(default=...)
    GOOGLE_CLOUD_LOCATION: str = Field(default=...)
    
    ## GCS
    GCS_BUCKET_NAME: str = Field(default=...)
    GCS_BLOB_NAME: str = Field(default=...)
    
    ## BQ
    BQ_DATASET_NAME: str = Field(default=...)
    BQ_DATASET_LOCATION: str = Field(default=...)
    BQ_TABLE: str = Field(default=...)
    BQ_TUKERINAJA_TABLE: str = Field(default=...)
    
    ## AI
    MODEL_ID: str = Field(default="gemini-2.0-flash-001")
    MODEL_TEMPERATURE: float = Field(default=0.2)
    MAXIMUM_PAPER: int = Field(default=7)
    
        
    @property
    def BQ_TABLE(self) -> str:
        return f"{self.GOOGLE_CLOUD_PROJECT}.{self.BQ_DATASET_NAME}.{self.BQ_TABLE}"
    
    @property
    def BQ_TUKERINAJA_KNOWLEDGE(self) -> str:
        return f"{self.GOOGLE_CLOUD_PROJECT}.{self.BQ_TUKERINAJA_TABLE}"
    
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"
    )
    
@lru_cache
def get_settings() -> Settings:
    return Settings()