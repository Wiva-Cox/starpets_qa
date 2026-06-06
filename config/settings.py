from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    base_api_url: str = "https://jsonplaceholder.typicode.com"
    base_ui_url: str = "https://starpets.gg"
    headless: bool = False
    slow_mo: int = 0
    browser: str = "chromium"


settings = Settings()
