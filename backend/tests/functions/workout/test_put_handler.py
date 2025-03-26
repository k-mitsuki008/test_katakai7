import json
from importlib import import_module, reload

import pytest

from tests.test_utils.utils import get_event

module = import_module('src.functions.workout.put_handler')
put_handler = getattr(module, 'handler')


def test_handler_ok1(mocker):
    """
    正常系 ワークアウト登録更新API
    """
    # 入力データ
    input_body = {
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234',
        'user_vehicle_id': 1,
        'start_timestamp': '2022-10-10T15:00:00.000Z',
        'end_timestamp': '2022-10-10T18:00:00.000Z',
        'workout_time': 3600,
        'trip_distance': 1000.0,
        'total_calorie': 1000,
        'heartbeat_zone_1_time': 100,
        'heartbeat_zone_2_time': 100,
        'heartbeat_zone_3_time': 100,
        'heartbeat_zone_4_time': 100,
        'heartbeat_zone_5_time': 100,
        'average_heart_rate': 160,
        'average_speed': 20,
        'max_speed': 40,
        'average_pedaling_power': 40,
        'max_pedaling_power': 100,
        'average_cadence': 40,
        'max_cadence': 100,
        'weather': '001',
        'temperature': 30,
        'humidity': 60,
        'workout_mode_code': '10'
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/user')
    context = {}

    # service.user_info_service.upsert_user_info のモック化
    mocker.patch("service.workout_service.upsert_workout", return_value=123)

    reload(module)

    # common.rds.connect.DbConnection.connect, commit のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})
    mocker.patch('common.rds.connect.DbConnection.commit', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "workout_id": 123
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok2(mocker):
    """
    正常系 ワークアウト登録更新API
    Optional項目省略
    """
    # 入力データ
    input_body = {
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234',
        'user_vehicle_id': 1,
        'start_timestamp': '2022-10-10T15:00:00.000Z',
        'end_timestamp': '2022-10-10T18:00:00.000Z',
        'workout_time': 3600,
        'trip_distance': 1000.0,
        'total_calorie': 1000,
        'average_speed': 20,
        'max_speed': 40,
        'average_pedaling_power': 40,
        'max_pedaling_power': 100,
        'average_cadence': 40,
        'max_cadence': 100,
        'workout_mode_code': '20'
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/user')
    context = {}

    # service.user_info_service.upsert_user_info のモック化
    mocker.patch("service.workout_service.upsert_workout", return_value=123)

    reload(module)

    # common.rds.connect.DbConnection.connect, commit のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})
    mocker.patch('common.rds.connect.DbConnection.commit', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "workout_id": 123
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


@pytest.mark.parametrize(
    ['data_source_kind_code', 'data_source_id', 'user_vehicle_id', 'start_timestamp', 'end_timestamp', 'workout_time',
     'trip_distance', 'total_calorie', 'heartbeat_zone_1_time', 'heartbeat_zone_2_time', 'heartbeat_zone_3_time',
     'heartbeat_zone_4_time', 'heartbeat_zone_5_time', 'average_heart_rate', 'average_speed', 'max_speed',
     'average_pedaling_power', 'max_pedaling_power', 'average_cadence', 'max_cadence', 'weather', 'temperature',
     'humidity', 'workout_mode_code', 'error_value_name', 'error_code', 'error_message'],
    [
        (None, 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'data_source_kind_code', 'E007', 'validation error'),
        ('01', None, 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'data_source_id', 'E007', 'validation error'),
        ('01', 'abcd-1234', None, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'user_vehicle_id', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, None, '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'start_timestamp', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', 123, 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'end_timestamp', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', None, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'workout_time', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, None, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'trip_distance', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, None, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'total_calorie', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, '100', 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'heartbeat_zone_1_time', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, '100',
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'heartbeat_zone_2_time', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         '100', 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'heartbeat_zone_3_time', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, '100', 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'heartbeat_zone_4_time', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, '100', 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'heartbeat_zone_5_time', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, '100', 20, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'average_heart_rate', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, None, 40, 40, 100, 40, 100, '001', 30, 60, '10',
         'average_speed', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, None, 40, 100, 40, 100, '001', 30, 60, '10',
         'max_speed', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, None, 100, 40, 100, '001', 30, 60, '10',
         'average_pedaling_power', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, None, 40, 100, '001', 30, 60, '10',
         'max_pedaling_power', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, None, 100, '001', 30, 60, '10',
         'average_cadence', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, None, '001', 30, 60, '10',
         'max_cadence', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, 123, 30, 60, '10',
         'weather', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', '100', 60, '10',
         'temperature', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, '123', '10',
         'humidity', 'E007', 'validation error'),
        ('01', 'abcd-1234', 1, '2022-10-10T15:00:00.000Z', '2022-10-10T18:00:00.000Z', 3600, 1000.0, 1000, 100, 100,
         100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, None,
         'workout_mode_code', 'E007', 'validation error'),
    ]
)
def test_handler_ng_01(mocker, data_source_kind_code, data_source_id, user_vehicle_id, start_timestamp, end_timestamp,
                       workout_time, trip_distance, total_calorie, heartbeat_zone_1_time, heartbeat_zone_2_time,
                       heartbeat_zone_3_time, heartbeat_zone_4_time, heartbeat_zone_5_time, average_heart_rate,
                       average_speed, max_speed, average_pedaling_power, max_pedaling_power, average_cadence,
                       max_cadence, weather, temperature, humidity, workout_mode_code,
                       error_value_name, error_code, error_message):
    """
    異常系 ワークアウト登録更新API
    バリデーションチェック(画面入力項目:nickname, weight, birth_date, max_heart_rate の型エラー)
    """
    # 入力データ
    input_body = {
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

    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/workout')
    context = {}

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005', 'message': 'validation error',
            'validationErrors': [
                {
                    'code': error_code,
                    'field': error_value_name,
                    'message': error_message
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
