from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.rds.transactional import transactional
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, USER_VEHICLE_ID
from service import user_vehicle_service, user_setting_ride_service

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **USER_VEHICLE_ID,
}


# pylint: disable=unused-argument
@default_api(schema=GET_SCHEMA, method='GET')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    車両設定削除API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    user_vehicle_id = params["user_vehicle_id"]

    # ユーザ車両IDが存在しなければ削除完了とみなす
    if user_vehicle_service.get_user_vehicle(gigya_uid, user_vehicle_id, is_check=False):
        # gigya_uidとuser_vehicle_idで正誤性チェック
        user_vehicle_service.user_vehicle_id_is_exist(gigya_uid, user_vehicle_id)

        # ユーザー車両削除
        count = user_vehicle_service.delete_vehicle(gigya_uid, user_vehicle_id)

        if count <= 0:
            # ユーザー情報削除
            user_setting_ride_service.delete_t_user_setting_ride(gigya_uid)

    result: dict = {
        "result": True,
        "user_vehicle_id": user_vehicle_id
    }
    return get_response_element(result)
