from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api

from service import maintain_history_service, user_vehicle_service

from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, USER_VEHICLE_ID, REQUIRED_MAINTAIN_HISTORY_ID

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **USER_VEHICLE_ID,
    **REQUIRED_MAINTAIN_HISTORY_ID,
}


@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    メンテナンス履歴詳細取得API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    user_vehicle_id = params["user_vehicle_id"]
    maintain_history_id = params["maintain_history_id"]

    # ユーザー車両存在チェック
    user_vehicle_service.user_vehicle_id_is_exist(
        gigya_uid,
        user_vehicle_id,
    )

    maintain_history: dict = maintain_history_service.get_maintain_history_detail(gigya_uid, maintain_history_id, user_vehicle_id)

    result: dict = {
        "result": True,
        **maintain_history
    }

    return get_response_element(result)
