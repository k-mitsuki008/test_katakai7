from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import (
    REQUIRED_GIGYA_UID,
    REQUIRED_UNEXPECTED_DATA,
    REQUIRED_CCU_ID,
)

from service import bluetooth_unexpected_data_service

log = Logger()

POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_UNEXPECTED_DATA,
    **REQUIRED_CCU_ID,
}


@default_api(schema=POST_SCHEMA, method='POST')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    Bluetooth異常データ送信API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    json_data = params["unexpected_data"]
    ccu_id = params["ccu_id"]

    bluetooth_unexpected_data_service.upload_file(gigya_uid, ccu_id, **json_data)

    result = {
        "result": True,
    }
    return get_response_element(result)
