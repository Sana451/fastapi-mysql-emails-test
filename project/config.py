import os
import pathlib
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    DATABASE_CONNECT_DICT: dict = {}


class DevelopmentConfig(BaseConfig):
    DATABASE_URL: str = os.environ.get("LOCAL_DATABASE_URL")


class ProductionConfig(BaseConfig):
    DATABASE_URL: str = os.environ.get("DOCKER_DATABASE_URL")


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }

    config_name = os.environ.get("FASTAPI_CONFIG")
    config_cls = config_cls_dict[config_name]
    print(f"config_name={config_name}  (.env)")
    return config_cls()


settings = get_settings()
