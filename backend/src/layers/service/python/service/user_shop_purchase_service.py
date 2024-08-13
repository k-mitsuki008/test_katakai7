from common.logger import Logger

from repository import user_shop_purchase_repository as repository
from common.decorator.service import service
from common.error.not_expected_error import NotExpectedError

log = Logger()


@service
def upsert_t_user_shop_purchase(user_vehicle_id: int, **kwargs) -> dict:
    _ = repository.upsert_t_user_shop_purchase(user_vehicle_id, **kwargs)

    upsert_result = repository.get_t_user_shop_purchase(user_vehicle_id)
    if not upsert_result:
        raise NotExpectedError()

    return upsert_result
