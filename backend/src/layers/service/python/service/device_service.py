from common.logger import Logger
from common.decorator.service import service
from repository import device_repository as repository

log = Logger()


@service
def upsert_device(gigya_uid, **kwargs) -> dict:
    _ = repository.upsert_t_device(gigya_uid, **kwargs)

    # 重複デバイスIDのデバイストークンを無効化
    repository.update_other_device_token(gigya_uid, kwargs['device_id'])

    upsert_result = repository.get_t_device(gigya_uid)

    return upsert_result
