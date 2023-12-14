"""
策略模式来实现数据存储和读取的功能
"""
from abc import abstractmethod
from typing import Any, Protocol, Dict
import json
import redis
from xcomstorage.conf.xcom import RedisStorageConf


# 定义一个接口，包含写入和读取的方法
class StorageStrategy(Protocol):
    @abstractmethod
    def write(self, key: str, data: Any) -> None:
        pass

    @abstractmethod
    def read(self, key: str) -> Any:
        pass

# Redis存储策略
class RedisStorageStrategy:
    def __init__(self, redis_client):
        self.redis_client = redis_client

    def write(self, key: str, data: Any) -> None:
        self.redis_client.set(key, data)

    def read(self, key: str) -> Any:
        return self.redis_client.get(key)

# S3存储策略
class S3StorageStrategy:
    def __init__(self, s3_client, bucket_name: str):
        self.s3_client = s3_client
        self.bucket_name = bucket_name

    def write(self, key: str, data: Any) -> None:
        self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=data)

    def read(self, key: str) -> Any:
        return self.s3_client.get_object(Bucket=self.bucket_name, Key=key)['Body'].read()

# 使用策略模式的数据存储类
class XcomStorage:
    def __init__(self, strategy: StorageStrategy):
        self.strategy = strategy

    def write(self, key: str, data: Any) -> None:
        self.strategy.write(key, data)

    def read(self, key: str) -> Any:
        return self.strategy.read(key)


class StorageFactory:
    def create_storage(self, storage_type: str, extra_info: Dict[str, Any] = {}) -> StorageStrategy:
        """
        storage_type: redis, s3
        """
        if storage_type == 'redis':
            conf = RedisStorageConf()
            client = redis.Redis.from_url(str(conf.redis_dsn))
            return RedisStorageStrategy(client)
        elif storage_type == 's3':
            raise NotImplementedError('s3 not impelemnted')
        else:
            raise ValueError('Unsupported storage type')
