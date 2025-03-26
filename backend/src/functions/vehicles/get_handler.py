from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID
from service import user_vehicle_service as user_vehicle

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
}


# pylint: disable=unused-argument
@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ユーザ車両設定一覧取得API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]

    # ユーザ車両設定一覧取得
    user_vehicles = user_vehicle.get_vehicles(gigya_uid)

    result = {
        "result": True,
        "vehicles": user_vehicles
    }

    return get_response_element(result)
