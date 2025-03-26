from datetime import datetime
from importlib import import_module

import pytest
from common.rds import execute_select_statement

import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.workout_repository')
upsert_workout = getattr(module, 'upsert_workout')


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_upsert_workout_ok_01():
    """
    正常系: ワークアウトTBL UPSERT
    登録 全項目
    """
    expected_value = [{
        'workout_id': 2,
        'data_source_kind_code': '01',
        'data_source_id': 'test-123123',
        'gigya_uid': 'new_user_1',
        'user_vehicle_id': 1,
        'start_timestamp': datetime(2022, 10, 6, 15, 30, 31),
        'end_timestamp': datetime(2022, 10, 16, 15, 30, 31),
        'workout_time': 10000,
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
        'fcdyobi1': None,
        'fcdyobi2': None,
        'fcdyobi3': None,
        'fcdyobi4': None,
        'fcdyobi5': None,
        'etxyobi1': None,
        'etxyobi2': None,
        'etxyobi3': None,
        'etxyobi4': None,
        'etxyobi5': None,
        'delete_flag': False,
        'delete_timestamp': None,
        'delete_user_id': None,
        'insert_timestamp': datetime(2023, 5, 13, 12, 34, 56, 789000),
        'insert_user_id': 'new_user_1',
        'update_timestamp': None,
        'update_user_id': None
    }]

    params = {
        'data_source_kind_code': '01',
        'data_source_id': 'test-123123',
        'user_vehicle_id': 1,
        'start_timestamp': datetime(2022, 10, 6, 15, 30, 31),
        'end_timestamp': datetime(2022, 10, 16, 15, 30, 31),
        'workout_time': 10000,
        'trip_distance': 1000,
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

    upsert_workout('new_user_1', **params)

    sql: str = '''
        SELECT
            *
        FROM t_workout
        WHERE gigya_uid = %(gigya_uid)s
        AND data_source_kind_code = %(data_source_kind_code)s
        AND data_source_id = %(data_source_id)s;
    '''
    parameters_dict: dict = {
        'gigya_uid': 'new_user_1',
        'data_source_kind_code': '01',
        'data_source_id': 'test-123123'
    }
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_upsert_workout_ok_02():
    """
    正常系: ワークアウトTBL UPSERT
    登録 項目不足
    """
    expected_value = [{
        'workout_id': 2,
        'data_source_kind_code': '01',
        'data_source_id': 'test-123123',
        'gigya_uid': 'new_user_2',
        'user_vehicle_id': 1,
        'start_timestamp': None,
        'end_timestamp': None,
        'workout_time': None,
        'trip_distance': None,
        'total_calorie': None,
        'heartbeat_zone_1_time': None,
        'heartbeat_zone_2_time': None,
        'heartbeat_zone_3_time': None,
        'heartbeat_zone_4_time': None,
        'heartbeat_zone_5_time': None,
        'average_heart_rate': None,
        'average_speed': None,
        'max_speed': None,
        'average_pedaling_power': None,
        'max_pedaling_power': None,
        'average_cadence': None,
        'max_cadence': None,
        'weather': None,
        'temperature': None,
        'humidity': None,
        'workout_mode_code': None,
        'fcdyobi1': None,
        'fcdyobi2': None,
        'fcdyobi3': None,
        'fcdyobi4': None,
        'fcdyobi5': None,
        'etxyobi1': None,
        'etxyobi2': None,
        'etxyobi3': None,
        'etxyobi4': None,
        'etxyobi5': None,
        'delete_flag': False,
        'delete_timestamp': None,
        'delete_user_id': None,
        'insert_timestamp': datetime(2023, 5, 13, 12, 34, 56, 789000),
        'insert_user_id': 'new_user_2',
        'update_timestamp': None,
        'update_user_id': None
    }]

    params = {
        'data_source_kind_code': '01',
        'data_source_id': 'test-123123',
        'user_vehicle_id': 1,
    }

    upsert_workout('new_user_2', **params)

    sql: str = '''
        SELECT
            *
        FROM t_workout
        WHERE gigya_uid = %(gigya_uid)s
        AND data_source_kind_code = %(data_source_kind_code)s
        AND data_source_id = %(data_source_id)s;
    '''
    parameters_dict: dict = {
        'gigya_uid': 'new_user_2',
        'data_source_kind_code': '01',
        'data_source_id': 'test-123123'
    }
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_upsert_workout_ok_03():
    """
    正常系: ワークアウトTBL UPSERT
    更新 全項目
    """
    expected_value = [{
        'workout_id': 1,
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234567',
        'gigya_uid': 'test_uid',
        'user_vehicle_id': 1,
        'start_timestamp': datetime(2022, 10, 6, 15, 30, 31),
        'end_timestamp': datetime(2022, 10, 16, 15, 30, 31),
        'workout_time': 10000,
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
        'fcdyobi1': None,
        'fcdyobi2': None,
        'fcdyobi3': None,
        'fcdyobi4': None,
        'fcdyobi5': None,
        'etxyobi1': None,
        'etxyobi2': None,
        'etxyobi3': None,
        'etxyobi4': None,
        'etxyobi5': None,
        'delete_flag': False,
        'delete_timestamp': None,
        'delete_user_id': None,
        'insert_timestamp': None,
        'insert_user_id': None,
        'update_timestamp': datetime(2023, 5, 13, 12, 34, 56, 789000),
        'update_user_id': 'test_uid'
    }]

    params = {
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234567',
        'user_vehicle_id': 1,
        'start_timestamp': '2022-10-06T15:30:31.000',
        'end_timestamp': '2022-10-16T15:30:31.000',
        'workout_time': 10000,
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

    upsert_workout('test_uid', **params)

    sql: str = '''
        SELECT
            *
        FROM t_workout
        WHERE gigya_uid = %(gigya_uid)s
        AND data_source_kind_code = %(data_source_kind_code)s
        AND data_source_id = %(data_source_id)s;
    '''
    parameters_dict: dict = {
        'gigya_uid': 'test_uid',
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234567'
    }
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time('2023-05-14 12:34:56.789101')
def test_upsert_workout_ok_04():
    """
    正常系: ワークアウトTBL UPSERT
    更新 項目不足
    """
    expected_value = [{
        'workout_id': 1,
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234567',
        'gigya_uid': 'test_uid',
        'user_vehicle_id': 1,
        'start_timestamp': datetime(2022, 10, 6, 15, 30, 31),
        'end_timestamp': datetime(2022, 10, 16, 15, 30, 31),
        'workout_time': 10000,
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
        'fcdyobi1': None,
        'fcdyobi2': None,
        'fcdyobi3': None,
        'fcdyobi4': None,
        'fcdyobi5': None,
        'etxyobi1': None,
        'etxyobi2': None,
        'etxyobi3': None,
        'etxyobi4': None,
        'etxyobi5': None,
        'delete_flag': False,
        'delete_timestamp': None,
        'delete_user_id': None,
        'insert_timestamp': None,
        'insert_user_id': None,
        'update_timestamp': datetime(2023, 5, 14, 12, 34, 56, 789000),
        'update_user_id': 'test_uid_02'
    }]

    params = {
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234567',
        'user_vehicle_id': 1,
        'start_timestamp': '2022-10-06T15:30:31.000',
        'end_timestamp': '2022-10-16T15:30:31.000',
    }

    upsert_workout('test_uid_02', **params)

    sql: str = '''
        SELECT
            *
        FROM t_workout
        WHERE gigya_uid = %(gigya_uid)s
        AND data_source_kind_code = %(data_source_kind_code)s
        AND data_source_id = %(data_source_id)s;
    '''
    parameters_dict: dict = {
        'gigya_uid': 'test_uid',
        'data_source_kind_code': '01',
        'data_source_id': 'abcd-1234567'
    }
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value
