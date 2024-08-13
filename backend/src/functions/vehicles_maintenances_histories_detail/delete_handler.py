from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.rds.transactional import transactional

from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_MAINTAIN_HISTORY_ID, USER_VEHICLE_ID
from service import maintain_history_service, user_vehicle_service

log = Logger()

DELETE_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_MAINTAIN_HISTORY_ID,
    **USER_VEHICLE_ID,
}


@default_api(schema=DELETE_SCHEMA, method='DELETE')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    メンテナンス記録削除API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    maintain_history_id = params["maintain_history_id"]
    user_vehicle_id = params["user_vehicle_id"]

    # gigya_uidとuser_vehicle_idで正誤性チェック
    user_vehicle_service.user_vehicle_id_is_exist(gigya_uid, user_vehicle_id)

    # メンテナンス履歴TBL削除
    maintain_history_service.delete_maintain_history(gigya_uid, maintain_history_id, user_vehicle_id)

    result: dict = {
        "result": True,
        "maintain_history_id": maintain_history_id
    }
    return get_response_element(result)
