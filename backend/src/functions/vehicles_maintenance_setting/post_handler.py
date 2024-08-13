from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.rds.transactional import transactional
from service import user_setting_maintain_service
from service import user_vehicle_service
from common.cerberus.custom_rules import (
    REQUIRED_GIGYA_UID,
    USER_VEHICLE_ID,
    MAINTAIN_CONSCIOUSNESS,
    MAINTAIN_ALERTS,
)

log = Logger()

# cerberusのvalidation定義を設定
POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **USER_VEHICLE_ID,
    **MAINTAIN_CONSCIOUSNESS,
    **MAINTAIN_ALERTS,
}


@default_api(schema=POST_SCHEMA, method='POST')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    メンテナンス設定登録更新API
    """
    log.info(f'params={params}')
    gigya_uid = params.pop("gigya_uid")
    user_vehicle_id = params.pop("user_vehicle_id")

    user_vehicle_service.user_vehicle_id_is_exist(
        gigya_uid,
        user_vehicle_id,
    )
    # Todo:メンテナンス項目マスタチェックを追加
    maintain_data = user_setting_maintain_service.upsert_setting_maintain(
        gigya_uid,
        user_vehicle_id,
        **params
    )

    result: dict = {
        "result": True,
        **maintain_data,
    }

    return get_response_element(result)
