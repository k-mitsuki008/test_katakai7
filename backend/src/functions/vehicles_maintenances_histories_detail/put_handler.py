from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, USER_VEHICLE_ID, REQUIRED_MAINTAIN_HISTORY_ID,\
    REQUIRED_MAINTAIN_ITEM_CODE, REQUIRED_MAINTAIN_IMPLEMENT_DATE, OPTION_MAINTAIN_LOCATION, OPTION_MAINTAIN_COST,\
    OPTION_MAINTAIN_REQUIRED_TIME, OPTION_MAINTAIN_MEMO, REQUIRED_MAINTAIN_IMAGE_IDS
from service import maintain_history_service, user_vehicle_service

log = Logger()

PUT_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **USER_VEHICLE_ID,
    **REQUIRED_MAINTAIN_HISTORY_ID,
    **REQUIRED_MAINTAIN_ITEM_CODE,
    **REQUIRED_MAINTAIN_IMPLEMENT_DATE,
    **OPTION_MAINTAIN_LOCATION,
    **OPTION_MAINTAIN_COST,
    **OPTION_MAINTAIN_REQUIRED_TIME,
    **OPTION_MAINTAIN_MEMO,
    **REQUIRED_MAINTAIN_IMAGE_IDS,
}


@default_api(schema=PUT_SCHEMA, method='PUT')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    メンテナンス記録更新API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    maintain_history_id = params.pop("maintain_history_id")
    user_vehicle_id = params["user_vehicle_id"]

    # ユーザー車両存在チェック
    user_vehicle_service.user_vehicle_id_is_exist(
        gigya_uid,
        user_vehicle_id,
    )

    # メンテナンス履歴更新
    maintain_history_service.update_maintain_history(maintain_history_id, **params)
    # メンテナンス履歴取得
    maintain_history = maintain_history_service.get_maintain_history(gigya_uid, maintain_history_id, user_vehicle_id)

    result: dict = {
        "result": True,
        **maintain_history
    }
    return get_response_element(result)
