from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_ROUTE_ID
from service import route_service

log = Logger()

# cerberusのvalidation定義を設定
GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_ROUTE_ID
}


# pylint: disable=unused-argument
@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ルート取得API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    route_id = params["route_id"]

    route_data = route_service.get_route(gigya_uid, route_id)
    result: dict = {
        "result": True,
        **route_data
    }

    return get_response_element(result)
