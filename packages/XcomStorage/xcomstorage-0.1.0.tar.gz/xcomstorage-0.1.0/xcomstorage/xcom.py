import json
from typing import Any, Optional
from xcomstorage.storage.xcom import StorageFactory, XcomStorage


def get_xcom_storage(storage_type: str = 'redis') -> XcomStorage:
    factory = StorageFactory()
    storage = XcomStorage(factory.create_storage(storage_type))
    return storage


def xcom_storage_write(key: str, data: Any, decoder: Optional[str] = 'json'):
    xcom = get_xcom_storage()
    if decoder == 'json':
        content = json.dumps(data)
    else:
        content = data
    xcom.write(key, content)


def xcom_storage_read(key: str, decoder: Optional[str] = 'json') -> Any:
    xcom = get_xcom_storage()
    content = xcom.read(key)
    if decoder == 'json':
        return json.loads(content)
    else: 
        return content
