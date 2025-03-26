from importlib import import_module, reload

module = import_module('service.workout_service')
upsert_workout = getattr(module, 'upsert_workout')


def test_upsert_workout_ok_01(mocker):
    """
    正常系 ワークアウト登録更新
    全項目設定
    """
    # repository.workout_repository.upsert_workout のモック化
    m = mocker.patch('repository.workout_repository.upsert_workout', return_value=123)
    reload(module)

    # 期待している返却値
    expected_value = 123

    upsert_data = upsert_workout('test_uid', '01', 'abcd-1234', 1, '2022-10-10 15:00:00', '2022-10-10 18:00:00', 3600,
                                 1000.0, 1000, 100, 100, 100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001',
                                 30, 60, '01')

    assert upsert_data == expected_value

    test_input = {
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234',
        'user_vehicle_id': 1,
        'start_timestamp': '2022-10-10 15:00:00',
        'end_timestamp': '2022-10-10 18:00:00',
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
        'workout_mode_code': '01',
    }
    # ユーザー情報登録がinsertされることを確認
    m.assert_called_with('test_uid', **test_input)


def test_upsert_workout_ok_02(mocker):
    """
    正常系 ワークアウト登録更新
    項目不足
    """
    # repository.workout_repository.upsert_workout のモック化
    m = mocker.patch('repository.workout_repository.upsert_workout', return_value=123)
    reload(module)

    # 期待している返却値
    expected_value = 123

    upsert_data = upsert_workout('test_uid', '01', 'abcd-1234', 1, None, None, None,
                                 None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                                 None, None, None, None)

    assert upsert_data == expected_value

    test_input = {
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234',
        'user_vehicle_id': 1,
    }
    # ユーザー情報登録がinsertされることを確認
    m.assert_called_with('test_uid', **test_input)
