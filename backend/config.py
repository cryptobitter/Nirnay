import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application configurations managed via Environment Variables.
    Loaded automatically from .env or system env vars.
    """
    APP_NAME: str = "Nirnay Audit Platform Backend"
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "default_secret_key_change_me"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 Hours

    # Database
    DATABASE_URL: str

    # AI & Embeddings
    CHROMA_PERSIST_DIR: str = "./chroma_db"
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # Blockchain (Polygon Amoy Testnet)
    POLYGON_AMOY_RPC_URL: str = "https://rpc-amoy.polygon.technology/"
    CONTRACT_ADDRESS: str = "0x0000000000000000000000000000000000000000"
    PRIVATE_KEY: str = ""
    CONTRACT_ABI_PATH: str = "./contract_abi.json"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()