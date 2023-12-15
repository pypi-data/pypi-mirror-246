from typing import Optional
from typing_extensions import Annotated
from pydantic import Field, RedisDsn, UrlConstraints
from pydantic_core import Url
from pydantic_settings import BaseSettings, SettingsConfigDict


S3Dsn = Annotated[
    Url,
    UrlConstraints(
        host_required=True,
        allowed_schemes=[
            's3'
        ],
    )
]


class RedisStorageConf(BaseSettings):
    # redis dsn: 'redis://:password@localhost:6379/0'
    redis_dsn: Optional[RedisDsn] = Field(None, alias='REDIS_DSN')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="allow")


class S3StorageConf(BaseSettings):
    s3_dsn: Optional[S3Dsn] = Field(None, alias='S3_DSN')

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra="allow")

