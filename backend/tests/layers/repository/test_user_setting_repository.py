
from datetime import datetime
from importlib import import_module
import pytest
from common.rds import execute_select_statement
from tests.test_utils.fixtures import db_setup

module = import_module('repository.user_setting_repository')
upsert_t_user_setting_ride = getattr(module, 'upsert_t_user_setting_ride')
update_t_user_setting_ride = getattr(module, 'update_t_user_setting_ride')
get_t_user_setting_ride = getattr(module, 'get_t_user_setting_ride')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_user_setting_ride_ok_01():
    """
    正常系: ユーザーライドTBL UPSERT(INSERT)
    """
    expected_value = [
        {"gigya_uid": "test_uid_01", "battery_remind_latitude": 35.675069, "battery_remind_longitude": 139.763328, "battery_remind_cd": "01", "battery_remind_voice_notice": 0, "safety_ride_alert": 1, "long_drive_alert": 1,  "speed_over_alert": 1,  "no_light_alert": 1, "safety_ride_voice_notice": 1, "home_assist_mode_number":  "01"
        , "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": 0, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01", "update_timestamp": None, "update_user_id": None}
    ]

    gigya_uid = 'test_uid_01'
    recs = {
        "battery_remind_latitude": 35.675069,
        "battery_remind_longitude": 139.763328,
        "battery_remind_cd": "01",
        "battery_remind_voice_notice": False,
        "safety_ride_alert": True,
        "long_drive_alert": True,
        "speed_over_alert": True,
        "no_light_alert": True,
        "safety_ride_voice_notice": True,
        "home_assist_mode_number": "01"
    }

    upsert_t_user_setting_ride(gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_setting_ride
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_01'}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_user_setting_ride_ok_02():
    """
    正常系: ユーザーライドTBL UPSERT(UPDATE)
    """
    expected_value = [
        {"gigya_uid": "test_uid_02", "battery_remind_latitude": 35.675069, "battery_remind_longitude": 139.763328, "battery_remind_cd": None, "battery_remind_voice_notice": 0, "safety_ride_alert": 1, "long_drive_alert": 1, "speed_over_alert": 1, "no_light_alert": 1, "safety_ride_voice_notice": 1, "home_assist_mode_number": "02"
        , "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": 0, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01", "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"}
    ]

    gigya_uid = 'test_uid_02'
    recs = {
        "battery_remind_latitude": 35.675069,
        "battery_remind_longitude": 139.763328,
        "battery_remind_cd": None,              # null値更新確認項目
        "battery_remind_voice_notice": False,
        "safety_ride_alert": True,
        "long_drive_alert": True,
        "speed_over_alert": True,
        "no_light_alert": True,
        "safety_ride_voice_notice": True,
        # "home_assist_mode_number": "01"       # 未更新確認項目
    }

    upsert_t_user_setting_ride(gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_setting_ride
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_02'}
    assert execute_select_statement(sql, parameters_dict) == expected_value

@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_t_user_setting_ride_ok():
    """
    正常系: ユーザーライドTBL UPDATE
    """
    expected_value = [
        {"gigya_uid": "test_uid_02", "battery_remind_latitude": None, "battery_remind_longitude": None, "battery_remind_cd": "02", "battery_remind_voice_notice": 0, "safety_ride_alert": 0, "long_drive_alert": 0, "speed_over_alert": 0, "no_light_alert": 0, "safety_ride_voice_notice": 0, "home_assist_mode_number": "02"
        , "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": 0, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01", "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"}
    ]

    gigya_uid = 'test_uid_02'
    recs = {
        "battery_remind_latitude": None,
        "battery_remind_longitude": None,
        # "battery_remind_cd": "01",  # 未更新確認項目
        "battery_remind_voice_notice": False,
        "safety_ride_alert": False,
        "long_drive_alert": False,
        "speed_over_alert": False,
        "no_light_alert": False,
        "safety_ride_voice_notice": False,
        "home_assist_mode_number": "02"
    }

    update_t_user_setting_ride(gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_setting_ride
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_02'}
    assert execute_select_statement(sql, parameters_dict) == expected_value

@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_get_t_user_setting_ride_ok():
    """
    正常系: ユーザーライドTBL SELECT
    """
    expected_value = {
        'gigya_uid': 'test_uid_02',
        'battery_remind_latitude': 35.123456,
        'battery_remind_longitude': 139.123456,
        'battery_remind_cd': '02',
        'battery_remind_voice_notice': True,
        "safety_ride_alert": True,
        'long_drive_alert': True,
        'speed_over_alert': True,
        'no_light_alert': True,
        'safety_ride_voice_notice': True,
        'home_assist_mode_number': '02'
    }

    result = get_t_user_setting_ride("test_uid_02")
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_get_t_user_setting_ride_ng_01():
    """
    異常系: ユーザーライドTBL 対象0件
    """
    expected_value = None

    result = get_t_user_setting_ride("test_uid_err")
    assert result == expected_value
