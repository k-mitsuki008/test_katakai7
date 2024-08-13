from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api

from service import maintain_history_service, user_vehicle_service

from common.cerberus.custom_rules import (
    REQUIRED_GIGYA_UID,
    USER_VEHICLE_ID,
    OPTIONAL_MAINTAIN_ITEM_CODE,
    LIMIT,
    OFFSET,
)

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **USER_VEHICLE_ID,
    **OPTIONAL_MAINTAIN_ITEM_CODE,
    **LIMIT,
    **OFFSET,
}


@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    メンテナンス履歴一覧取得API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    user_vehicle_id = params["user_vehicle_id"]
    limit = params.get("limit", 30)
    offset = params.get("offset", 0)
    maintain_item_code = params.get('maintain_item_code', None)

    # ユーザー車両存在チェック
    user_vehicle_service.user_vehicle_id_is_exist(
        gigya_uid,
        user_vehicle_id,
    )

    ride_data = maintain_history_service.get_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
        maintain_item_code,
    )
    result: dict = {
        "result": True,
        **ride_data,
    }
    return get_response_element(result)
