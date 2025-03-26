from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from service import maintain_item_service, user_vehicle_service
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, USER_VEHICLE_ID

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **USER_VEHICLE_ID
}


@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    メンテナンス指示一覧取得API
    """
    log.info(f'params={params}')
    gigya_uid = params['gigya_uid']
    user_vehicle_id = params['user_vehicle_id']

    # ユーザー車両存在チェック
    user_vehicle_service.user_vehicle_id_is_exist(
        gigya_uid,
        user_vehicle_id,
    )

    user_vehicle_maintain_items = maintain_item_service.get_maintain_items(gigya_uid, user_vehicle_id)

    result = {
        "result": True,
        "maintain_items": user_vehicle_maintain_items
    }

    return get_response_element(result)
