from typing import Dict
import json
from typing import Any, Optional
from xcomstorage.storage.xcom import StorageFactory, XcomStorage


def get_xcom_storage(storage_type: str = 'redis', extra_info: Dict[str, Any] = {}) -> XcomStorage:
    """
    storage_type: redis, s3
    """
    factory = StorageFactory()
    storage = XcomStorage(factory.create_storage(storage_type, extra_info=extra_info))
    return storage


def xcom_storage_write(key: str, data: Any, storage_type: str = 'redis', decoder: Optional[str] = 'json'):
    xcom = get_xcom_storage(storage_type=storage_type)
    if decoder == 'json':
        content = json.dumps(data)
    else:
        content = data
    xcom.write(key, content)


def xcom_storage_read(key: str, storage_type: str = 'redis', decoder: Optional[str] = 'json') -> Any:
    xcom = get_xcom_storage(storage_type=storage_type)
    content = xcom.read(key)
    if decoder == 'json':
        return json.loads(content)
    else: 
        return content
