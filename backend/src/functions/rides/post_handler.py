from typing import Tuple

import datetime
from common.rds.transactional import transactional
from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from service import user_vehicle_service
from service import ride_history_service

from common.cerberus.custom_rules import (
    REQUIRED_GIGYA_UID,
    USER_VEHICLE_ID,
    START_TIMESTAMP,
    END_TIMESTAMP,
    TRIP_DISTANCE,
    TRIP_TIME,
    TOTAL_CALORIE,
    BATTERY_CONSUMPTION,
    AVERAGE_SPEED,
    MAX_SPEED,
    MAX_PEDALING_POWER,
    MAX_CADENCE,
    RIDE_TRACKS,
)


log = Logger()

# cerberusのvalidation定義を設定
POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **USER_VEHICLE_ID,
    **START_TIMESTAMP,
    **END_TIMESTAMP,
    **TRIP_DISTANCE,
    **TRIP_TIME,
    **TOTAL_CALORIE,
    **BATTERY_CONSUMPTION,
    **AVERAGE_SPEED,
    **MAX_SPEED,
    **MAX_PEDALING_POWER,
    **MAX_CADENCE,
    **RIDE_TRACKS,
}


@default_api(schema=POST_SCHEMA, method='POST')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ユーザーライドデータ送信API
    """
    log.info(f'params={params}')
    gigya_uid = params.pop("gigya_uid")
    user_vehicle_id = params["user_vehicle_id"]
    start_time = params["start_timestamp"]

    # ユーザー車両存在チェック、車両名取得
    vehicle_data = user_vehicle_service.get_user_vehicle(
        gigya_uid,
        user_vehicle_id,
    )
    vehicle_name = vehicle_data.get("vehicle_name")
    # ライド名称取得{車両名}のライド
    ride_name = vehicle_name + "のライド"

    # ライド履歴ID取得
    # ユーザー車両ID＋開始日時
    ride_history_id = str(user_vehicle_id) + start_time

    params["ride_name"] = ride_name
    params["bookmark_flg"] = False

    ride_data = ride_history_service.upsert_ride_history(
        gigya_uid,
        ride_history_id,
        **params
    )

    result: dict = {
        "result": True,
        **ride_data
    }

    return get_response_element(result)
