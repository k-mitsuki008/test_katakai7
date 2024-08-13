from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
import common.cerberus.setting.basic_rules as br
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_VEHICLE_ID, REQUIRED_MODEL_CD, \
    REQUIRED_VEHICLE_NAME, OPTIONAL_EQUIPMENT_WEIGHT, OPTIONAL_VEHICLE_NICKNAME
from common.rds.transactional import transactional
from service import user_vehicle_service
from service import user_setting_maintain_service

log = Logger()

POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_VEHICLE_ID,
    **REQUIRED_MODEL_CD,
    **REQUIRED_VEHICLE_NAME,
    'managed_flag': {**br.REQUIRED_COMMON_BOOLEAN},
    **OPTIONAL_EQUIPMENT_WEIGHT,
    **OPTIONAL_VEHICLE_NICKNAME
}


# pylint: disable=unused-argument
@default_api(schema=POST_SCHEMA, method='POST')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    車両設定登録API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    vehicle_id = params["vehicle_id"]
    # 同一車両存在チェック
    user_vehicle_service.vehicle_id_check(gigya_uid, vehicle_id)

    # ユーザ車両設定登録
    user_vehicle_id = user_vehicle_service.insert_vehicle(**params)

    # ユーザメンテナンス設定情報を登録
    _ = user_setting_maintain_service.initialize_maintenance_setting(user_vehicle_id, gigya_uid)

    # ユーザ車両設定一覧取得
    user_vehicles = user_vehicle_service.get_vehicles(gigya_uid, user_vehicle_id)[0]

    result = {
        "result": True,
        **user_vehicles
    }
    return get_response_element(result)
