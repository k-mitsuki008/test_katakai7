from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID,REGULAR_SHOP_NAME,REGULAR_SHOP_TEL,REGULAR_SHOP_LOCATION

from service import user_shop_regular_service

log = Logger()

POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REGULAR_SHOP_NAME,
    **REGULAR_SHOP_TEL,
    **REGULAR_SHOP_LOCATION
}


@default_api(schema=POST_SCHEMA, method='POST')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ユーザー普段利用店舗登録更新API
    """
    log.info(f'params={params}')

    upsert_data = user_shop_regular_service.upsert_t_user_shop_regular(
        **params
    )

    result = {
        "result": True,
        **upsert_data
    }
    return get_response_element(result)
