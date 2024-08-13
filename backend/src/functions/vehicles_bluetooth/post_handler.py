from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.rds.transactional import transactional
from service import drive_unit_history_service, user_vehicle_service
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, USER_VEHICLE_ID, REQUIRED_DU_SERIAL_NUMBER,\
    REQUIRED_TIMESTAMP, REQUIRED_DU_ODOMETER

log = Logger()

POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **USER_VEHICLE_ID,
    **REQUIRED_DU_SERIAL_NUMBER,
    **REQUIRED_TIMESTAMP,
    **REQUIRED_DU_ODOMETER
}


@default_api(schema=POST_SCHEMA, method='POST')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    Bluetooth接続切断API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    user_vehicle_id = params.get('user_vehicle_id')

    # ユーザー車両存在チェック
    user_vehicle_service.user_vehicle_id_is_exist(
        gigya_uid,
        user_vehicle_id
    )

    drive_unit_history_service.registration_drive_unit_history(**params)

    result = {
        "result": True,
        "user_vehicle_id": user_vehicle_id,
        "du_serial_number": params["du_serial_number"],
        "du_odometer": params["du_odometer"],
    }
    return get_response_element(result)
