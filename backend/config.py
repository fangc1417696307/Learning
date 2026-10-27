from pydantic_settings import BaseSettings, SettingsConfigDict


class setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",  # 自动读这个文件
        env_file_encoding="utf-8",  # 中文值不乱码
        extra="ignore",  # .env 里多出来的变量不报错
    )

    db_path: str = "student.db"
    llm_api_key: str = ""
    llm_base_url: str = "https://api.example.com/v1"
    llm_model: str = "some-model"


# 全局配置对象
setting = setting()
