from common.decorator.service import service
from common.logger import Logger
from repository import workout_repository

log = Logger()


@service
def upsert_workout(gigya_uid, data_source_kind_code, data_source_id, user_vehicle_id, start_timestamp, end_timestamp,
                   workout_time, trip_distance, total_calorie, heartbeat_zone_1_time, heartbeat_zone_2_time,
                   heartbeat_zone_3_time, heartbeat_zone_4_time, heartbeat_zone_5_time, average_heart_rate,
                   average_speed, max_speed, average_pedaling_power, max_pedaling_power, average_cadence, max_cadence,
                   weather, temperature, humidity, workout_mode_code) -> int:

    # 登録/更新値設定
    params = {
        'data_source_kind_code': data_source_kind_code,
        'data_source_id': data_source_id,
        'user_vehicle_id': user_vehicle_id,
        'start_timestamp': start_timestamp,
        'end_timestamp': end_timestamp,
        'workout_time': workout_time,
        'trip_distance': trip_distance,
        'total_calorie': total_calorie,
        'heartbeat_zone_1_time': heartbeat_zone_1_time,
        'heartbeat_zone_2_time': heartbeat_zone_2_time,
        'heartbeat_zone_3_time': heartbeat_zone_3_time,
        'heartbeat_zone_4_time': heartbeat_zone_4_time,
        'heartbeat_zone_5_time': heartbeat_zone_5_time,
        'average_heart_rate': average_heart_rate,
        'average_speed': average_speed,
        'max_speed': max_speed,
        'average_pedaling_power': average_pedaling_power,
        'max_pedaling_power': max_pedaling_power,
        'average_cadence': average_cadence,
        'max_cadence': max_cadence,
        'weather': weather,
        'temperature': temperature,
        'humidity': humidity,
        'workout_mode_code': workout_mode_code,
    }
    convert_params = {key: value for key, value in params.items() if value is not None}

    inserted_workout_id = workout_repository.upsert_workout(gigya_uid, **convert_params)

    # INSERTしたワークアウトIDを返却
    return inserted_workout_id
