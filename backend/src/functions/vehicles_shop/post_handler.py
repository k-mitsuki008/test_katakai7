from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, SHOP_NAME, SHOP_TEL, SHOP_LOCATION, USER_VEHICLE_ID
from service import user_shop_purchase_service, user_shop_regular_service, user_vehicle_service

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **SHOP_NAME,
    **SHOP_TEL,
    **SHOP_LOCATION,
    **USER_VEHICLE_ID,
}


@default_api(schema=GET_SCHEMA, method='POST')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ユーザー購入店舗登録更新API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    user_vehicle_id = params["user_vehicle_id"]
    # gigya_uidとuser_vehicle_idで正誤性チェック
    user_vehicle_service.user_vehicle_id_is_exist(gigya_uid, user_vehicle_id)

    upsert_data = user_shop_purchase_service.upsert_t_user_shop_purchase(
        **params
    )

    params.pop("user_vehicle_id")
    user_shop_regular_service.insert_t_user_shop_regular(
        **params
    )

    result = {
        "result": True,
        **upsert_data
    }
    return get_response_element(result)
