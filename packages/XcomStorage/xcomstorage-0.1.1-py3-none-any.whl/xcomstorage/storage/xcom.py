"""
策略模式来实现数据存储和读取的功能
"""
from abc import abstractmethod
from datetime import timedelta
from pathlib import Path
from urllib.parse import parse_qs
from typing import Any, Dict, Optional, Protocol
from pydantic import HttpUrl
import redis
from minio import Minio
from minio.error import S3Error

from xcomstorage.conf.xcom import RedisStorageConf, S3StorageConf

from xcomstorage.conf.xcom import S3Dsn

class XcomException(Exception):
    pass


# 定义一个接口，包含写入和读取的方法
class StorageStrategy(Protocol):
    @abstractmethod
    def write(self, key: str, data: Any, expires: Optional[timedelta] = None) -> None:
        pass

    @abstractmethod
    def read(self, key: str) -> Any:
        pass
    
    @abstractmethod
    def upload_local_file(self, local_file: Path, target: Any = None, expires: Any = None) -> Any:
        pass

# Redis存储策略
class RedisStorageStrategy:
    def __init__(self, redis_client):
        self.client = redis_client

    def write(self, key: str, data: Any, expires: Optional[timedelta] = None) -> None:
        self.client.set(key, data)

    def read(self, key: str) -> Any:
        return self.client.get(key)
    
    def upload_local_file(self, local_file: Path, target: Any = None, expires: Any = None) -> Any:
        raise NotImplementedError('redis not support upload')



def s3_cleint(conf: S3Dsn) -> Minio:
    """ref: https://min.io/docs/minio/linux/developers/python/API.html
    """
    if conf.query:
        query_params_dict = parse_qs(conf.query)
        secure = query_params_dict.get('secure', [])
        secure = True if 'true' in  secure else False
    else:
        secure = False

    endpoint = f'{conf.host}:{conf.port}' if conf.port else f'{conf.host}:80'
    return Minio(endpoint, access_key=conf.username, secret_key=conf.password, secure=secure)



# S3存储策略
class S3StorageStrategy:
    def __init__(self, s3_client, bucket_name: str):
        self.client = s3_client
        self.bucket_name = bucket_name

    def write(self, key: str, data: Any) -> None:
        self.client.put_object(Bucket=self.bucket_name, Key=key, Body=data)

    def read(self, key: str) -> Any:
        return self.client.get_object(Bucket=self.bucket_name, Key=key)['Body'].read()
    
    def upload_local_file(self, local_file: Path, target: Any, expires: Optional[timedelta] = None)  -> Any:
        try:
            self.client.fput_object(self.bucket_name, target, str(local_file))
        except S3Error as err:
            raise XcomException(err)
        
        download_url = self.client.presigned_get_object(
                self.bucket_name, target, expires=expires)
            # 使用 Pydantic HttpUrl 类型验证下载链接
        try:
            url = HttpUrl(download_url)
        except ValueError as err:
            raise ValueError(err)
        return url


# 使用策略模式的数据存储类
class XcomStorage:
    def __init__(self, strategy: StorageStrategy):
        self.strategy = strategy

    def write(self, key: str, data: Any) -> None:
        self.strategy.write(key, data)

    def read(self, key: str) -> Any:
        return self.strategy.read(key)
    
    def upload_local_file(self, local_file: Path, target: Any = None, expires: Any = None) -> Any:
        return self.strategy.upload_local_file(local_file, target=target, expires=expires)


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
            conf = S3StorageConf()
            bucket_name = extra_info['bucket_name']
            return S3StorageStrategy(s3_cleint(conf.s3_dsn), bucket_name)
        else:
            raise ValueError('Unsupported storage type')
