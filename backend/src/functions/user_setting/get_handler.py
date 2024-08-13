from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api

from common.cerberus.custom_rules import REQUIRED_GIGYA_UID
from service import user_setting_ride_service
from service import user_shop_regular_service

log = Logger()

# cerberusのvalidation定義を設定
GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
}


@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ユーザー設定情報取得API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]

    ride_data = user_setting_ride_service.get_t_user_setting_ride(
        gigya_uid
    )
    shop_data = user_shop_regular_service.get_t_user_shop_regular(
        gigya_uid
    )
    result = {
        "result": True,
        "user_ride": ride_data,
        "regular_shop": shop_data,
    }
    return get_response_element(result)
