from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api

from common.cerberus.custom_rules import REQUIRED_GIGYA_UID
from service import user_info_service

log = Logger()

# cerberusのvalidation定義を設定
GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID
}


# pylint: disable=unused-argument
@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ユーザー設定情報取得API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]

    user_info = user_info_service.get_user_info(
        gigya_uid
    )
    result = {
        "result": True,
        **user_info
    }
    return get_response_element(result)
