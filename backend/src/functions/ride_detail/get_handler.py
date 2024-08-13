from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_RIDE_HISTORY_ID
from service import ride_history_service
from service import ride_track_service

log = Logger()

# cerberusのvalidation定義を設定
GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_RIDE_HISTORY_ID,
}


@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ライド詳細取得API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    ride_history_id = params["ride_history_id"]

    ride_data = ride_history_service.get_ride_history(gigya_uid, ride_history_id)
    ride_tracks = ride_track_service.get_ride_track(ride_history_id)
    result: dict = {
        "result": True,
        **ride_data,
        "ride_tracks": ride_tracks
    }
    return get_response_element(result)
