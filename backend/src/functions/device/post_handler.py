from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.rds.transactional import transactional

from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_DEVICE_ID, REQUIRED_DEVICE_TOKEN
from service import device_service as device

log = Logger()

POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_DEVICE_ID,
    **REQUIRED_DEVICE_TOKEN
}


@default_api(schema=POST_SCHEMA, method='POST')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    デバイストークン登録更新API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    device_id = params["device_id"]
    device_token = params["device_token"]

    upsert_data = device.upsert_device(gigya_uid, device_id=device_id, device_token=device_token)
    result = {
        'result': True,
        **upsert_data
    }

    return get_response_element(result)
