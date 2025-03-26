from common.logger import Logger
from common.decorator.service import service
from common.error.not_expected_error import NotExpectedError
from repository import user_setting_repository as repository

log = Logger()


@service
def upsert_t_user_setting_ride(gigya_uid, **kwargs) -> dict:
    _ = repository.upsert_t_user_setting_ride(gigya_uid, **kwargs)

    upsert_result = repository.get_t_user_setting_ride(gigya_uid)
    if not upsert_result:
        raise NotExpectedError()

    return upsert_result
