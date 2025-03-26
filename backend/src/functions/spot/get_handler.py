from typing import Tuple

from common.cerberus.custom_rules import (OPTIONAL_RADIUS, REQUIRED_GIGYA_UID,
                                          REQUIRED_LATITUDE,
                                          REQUIRED_LONGITUDE)
from common.decorator.default_api import default_api
from common.logger import Logger
from common.response import get_response_element
from service import spot_service

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_LATITUDE,
    **REQUIRED_LONGITUDE,
    **OPTIONAL_RADIUS
}

DEFAULT_RADIUS: int = 1000


# pylint: disable=unused-argument
@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    スポット取得API
    """
    log.info(f'params={params}')
    latitude = params.get('latitude')
    longitude = params.get('longitude')
    radius = params.get('radius') if params.get('radius') is not None else DEFAULT_RADIUS

    spot_list = spot_service.get_spot(latitude, longitude, radius)

    result: dict = {
        "result": True,
        "spots": spot_list
    }

    return get_response_element(result)
