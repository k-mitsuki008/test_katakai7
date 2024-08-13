from typing import Tuple

from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, OPTIONAL_BIKE_RADAR_FLAG
from common.decorator.default_api import default_api
from common.logger import Logger
from common.response import get_response_element
from service import model_service

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **OPTIONAL_BIKE_RADAR_FLAG
}


# pylint: disable=unused-argument
@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    車種マスタ取得API
    """
    log.info(f'params={params}')

    bike_radar_flag = params.get('bike_radar_flag', False)
    model_code_data = model_service.get_m_model(bike_radar_flag)

    result = {
        "result": True,
        "model_codes": model_code_data
    }

    return get_response_element(result)
