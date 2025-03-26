from typing import Tuple

from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_ROUTE_ID
from common.decorator.default_api import default_api
from common.logger import Logger
from common.rds.transactional import transactional
from common.response import get_response_element
from service import route_service

log = Logger()

DELETE_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_ROUTE_ID
}


# pylint: disable=unused-argument
@default_api(schema=DELETE_SCHEMA, method='DELETE')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ルート削除API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    route_id = params["route_id"]

    _ = route_service.delete_route(gigya_uid, route_id)

    result: dict = {
        "result": True,
    }

    return get_response_element(result)
