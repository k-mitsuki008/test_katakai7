from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.error.business_error import BusinessError
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, USER_VEHICLE_ID, OPTIONAL_VEHICLE_ID, \
    OPTIONAL_VEHICLE_NAME, OPTIONAL_MANAGED_FLAG, OPTIONAL_PERIPHERAL_IDENTIFIER, OPTIONAL_COMPLETE_LOCAL_NAME,\
    OPTIONAL_REGISTERED_FLAG, OPTIONAL_EQUIPMENT_WEIGHT, OPTIONAL_VEHICLE_NICKNAME, OPTIONAL_MODEL_CD
from common.rds.transactional import transactional
from service import user_vehicle_service

log = Logger()

PUT_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **USER_VEHICLE_ID,
    **OPTIONAL_VEHICLE_ID,
    **OPTIONAL_VEHICLE_NAME,
    **OPTIONAL_MANAGED_FLAG,
    **OPTIONAL_PERIPHERAL_IDENTIFIER,
    **OPTIONAL_COMPLETE_LOCAL_NAME,
    **OPTIONAL_REGISTERED_FLAG,
    **OPTIONAL_EQUIPMENT_WEIGHT,
    **OPTIONAL_VEHICLE_NICKNAME,
    **OPTIONAL_MODEL_CD
}


# pylint: disable=unused-argument
@default_api(schema=PUT_SCHEMA, method='PUT')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    車両設定更新API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    user_vehicle_id = params["user_vehicle_id"]
    vehicle_id = params.get('vehicle_id', None)

    vehicle_info = user_vehicle_service.get_user_vehicle(gigya_uid, user_vehicle_id)

    # 号機番号が変更されている場合のみチェック
    if vehicle_id != vehicle_info.get("vehicle_id"):
        # 同一車両存在チェック
        user_vehicle_service.vehicle_id_check(gigya_uid, vehicle_id)

    if not vehicle_id:
        vehicle_id = vehicle_info.get("vehicle_id")

    # gigya_uidとuser_vehicle_idで正誤性チェック
    # model_codeがパラメータに含まれていたらそれを使用、そうでなければDB保存済みの値を使用
    model_code = params.get("model_code")
    if not model_code:
        model_code = vehicle_info.get("model_code")

    # vehicle_id上4ケタ = ユーザ車両TBL.モデルコードのチェック
    if vehicle_id and model_code != vehicle_id[:4]:
        raise BusinessError(error_code='E043')

    # ユーザ車両設定更新
    user_vehicle_service.update_vehicle(**params)
    # ユーザ車両設定一覧取得
    user_vehicles = user_vehicle_service.get_vehicles(gigya_uid, user_vehicle_id)[0]

    if not user_vehicles["maintain_setting"]:
        raise BusinessError(error_code='E042', params=('ユーザメンテナンス設定情報',))

    result = {
        "result": True,
        **user_vehicles
    }
    return get_response_element(result)
