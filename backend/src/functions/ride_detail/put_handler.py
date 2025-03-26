from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.rds.transactional import transactional
from service import ride_history_service

from common.cerberus.custom_rules import (
    REQUIRED_GIGYA_UID,
    REQUIRED_RIDE_HISTORY_ID,
    OPTIONAL_RIDE_NAME,
    OPTIONAL_BOOKMARK_FLG
)

log = Logger()

# cerberusのvalidation定義を設定
PUT_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_RIDE_HISTORY_ID,
    **OPTIONAL_RIDE_NAME,
    **OPTIONAL_BOOKMARK_FLG,
}


@default_api(schema=PUT_SCHEMA, method='PUT')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ライド詳細更新API
    """
    log.info(f'params={params}')
    gigya_uid = params.pop("gigya_uid")
    ride_history_id = params.pop("ride_history_id")

    ride_history_data = ride_history_service.update_ride_history(
        gigya_uid,
        ride_history_id,
        **params
    )
    result: dict = {
        "result": True,
        **ride_history_data
    }

    return get_response_element(result)
