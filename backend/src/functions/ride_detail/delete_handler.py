from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.rds.transactional import transactional
from service import ride_history_service
from service import ride_track_service

from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_RIDE_HISTORY_ID

log = Logger()

DELETE_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_RIDE_HISTORY_ID,
}


@default_api(schema=DELETE_SCHEMA, method='DELETE')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ライド詳細削除API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    ride_history_id = params["ride_history_id"]

    ride_history_service.delete_ride_history(gigya_uid, ride_history_id)
    result: dict = {
        "result": True,
        "ride_history_id": ride_history_id
    }

    return get_response_element(result)
