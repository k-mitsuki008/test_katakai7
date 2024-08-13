from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import (
    REQUIRED_GIGYA_UID,
    REQUIRED_DATA_SOURCE_KIND_CODE,
    REQUIRED_DATA_SOURCE_ID,
    USER_VEHICLE_ID,
    START_TIMESTAMP,
    END_TIMESTAMP,
    REQUIRED_WORKOUT_TIME,
    TRIP_DISTANCE,
    RADAR_TOTAL_CALORIE,
    OPTIONAL_HEARTBEAT_ZONE_1_TIME,
    OPTIONAL_HEARTBEAT_ZONE_2_TIME,
    OPTIONAL_HEARTBEAT_ZONE_3_TIME,
    OPTIONAL_HEARTBEAT_ZONE_4_TIME,
    OPTIONAL_HEARTBEAT_ZONE_5_TIME,
    OPTIONAL_RADAR_AVERAGE_HEART_RATE,
    RADAR_AVERAGE_SPEED,
    RADAR_MAX_SPEED,
    RADAR_REQUIRED_AVERAGE_PEDALING_POWER,
    RADAR_MAX_PEDALING_POWER,
    RADAR_REQUIRED_AVERAGE_CADENCE,
    RADAR_MAX_CADENCE,
    OPTIONAL_WEATHER,
    OPTIONAL_TEMPERATURE,
    OPTIONAL_HUMIDITY,
    REQUIRED_WORKOUT_MODE_CODE
)
from service import workout_service

log = Logger()

# cerberusのvalidation定義を設定
POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_DATA_SOURCE_KIND_CODE,
    **REQUIRED_DATA_SOURCE_ID,
    **USER_VEHICLE_ID,
    **START_TIMESTAMP,
    **END_TIMESTAMP,
    **REQUIRED_WORKOUT_TIME,
    **TRIP_DISTANCE,
    **RADAR_TOTAL_CALORIE,
    **OPTIONAL_HEARTBEAT_ZONE_1_TIME,
    **OPTIONAL_HEARTBEAT_ZONE_2_TIME,
    **OPTIONAL_HEARTBEAT_ZONE_3_TIME,
    **OPTIONAL_HEARTBEAT_ZONE_4_TIME,
    **OPTIONAL_HEARTBEAT_ZONE_5_TIME,
    **OPTIONAL_RADAR_AVERAGE_HEART_RATE,
    **RADAR_AVERAGE_SPEED,
    **RADAR_MAX_SPEED,
    **RADAR_REQUIRED_AVERAGE_PEDALING_POWER,
    **RADAR_MAX_PEDALING_POWER,
    **RADAR_REQUIRED_AVERAGE_CADENCE,
    **RADAR_MAX_CADENCE,
    **OPTIONAL_WEATHER,
    **OPTIONAL_TEMPERATURE,
    **OPTIONAL_HUMIDITY,
    **REQUIRED_WORKOUT_MODE_CODE
}


# pylint: disable=unused-argument
@default_api(schema=POST_SCHEMA, method='POST')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ワークアウト登録更新API
    """
    log.info(f'params={params}')
    gigya_uid = params['gigya_uid']
    data_source_kind_code = params.get('data_source_kind_code')
    data_source_id = params.get('data_source_id')
    user_vehicle_id = params.get('user_vehicle_id')
    start_timestamp = params.get('start_timestamp')
    end_timestamp = params.get('end_timestamp')
    workout_time = params.get('workout_time')
    trip_distance = params.get('trip_distance')
    total_calorie = params.get('total_calorie')
    heartbeat_zone_1_time = params.get('heartbeat_zone_1_time')
    heartbeat_zone_2_time = params.get('heartbeat_zone_2_time')
    heartbeat_zone_3_time = params.get('heartbeat_zone_3_time')
    heartbeat_zone_4_time = params.get('heartbeat_zone_4_time')
    heartbeat_zone_5_time = params.get('heartbeat_zone_5_time')
    average_heart_rate = params.get('average_heart_rate')
    average_speed = params.get('average_speed')
    max_speed = params.get('max_speed')
    average_pedaling_power = params.get('average_pedaling_power')
    max_pedaling_power = params.get('max_pedaling_power')
    average_cadence = params.get('average_cadence')
    max_cadence = params.get('max_cadence')
    weather = params.get('weather')
    temperature = params.get('temperature')
    humidity = params.get('humidity')
    workout_mode_code = params.get('workout_mode_code')

    workout_id = workout_service.upsert_workout(
        gigya_uid,
        data_source_kind_code,
        data_source_id,
        user_vehicle_id,
        start_timestamp,
        end_timestamp,
        workout_time,
        trip_distance,
        total_calorie,
        heartbeat_zone_1_time,
        heartbeat_zone_2_time,
        heartbeat_zone_3_time,
        heartbeat_zone_4_time,
        heartbeat_zone_5_time,
        average_heart_rate,
        average_speed,
        max_speed,
        average_pedaling_power,
        max_pedaling_power,
        average_cadence,
        max_cadence,
        weather,
        temperature,
        humidity,
        workout_mode_code
    )

    result: dict = {
        "result": True,
        "workout_id": workout_id
    }

    return get_response_element(result)
