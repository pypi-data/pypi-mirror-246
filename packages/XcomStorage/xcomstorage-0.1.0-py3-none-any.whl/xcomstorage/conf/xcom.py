from typing import Optional
from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisStorageConf(BaseSettings):
    # redis dsn: 'redis://:password@localhost:6379/0'
    redis_dsn: Optional[RedisDsn] = Field(None, alias='REDIS_DSN')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

