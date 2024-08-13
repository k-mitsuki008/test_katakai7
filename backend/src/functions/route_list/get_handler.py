from typing import Tuple

from common.cerberus.custom_rules import REQUIRED_GIGYA_UID
from common.decorator.default_api import default_api
from common.logger import Logger
from common.response import get_response_element
from service import route_service

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
}


# pylint: disable=unused-argument
@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ルート一覧取得API
    """
    log.info(f'params={params}')
    gigya_uid = params.get('gigya_uid')

    route_list = route_service.get_route_list(gigya_uid)

    result: dict = {
        'result': True,
        'routes': route_list
    }

    return get_response_element(result)
