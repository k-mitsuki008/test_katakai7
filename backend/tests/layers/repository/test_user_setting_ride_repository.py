from importlib import import_module
from datetime import datetime
import pytest

from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.user_setting_ride_repository')
get_t_user_setting_ride = getattr(module, 'get_t_user_setting_ride')
insert_t_user_setting_ride = getattr(module, 'insert_t_user_setting_ride')
delete_t_user_setting_ride = getattr(module, 'delete_t_user_setting_ride')


def test_get_t_user_setting_ride_ok(mocker):
    """
    正常系: ユーザーライド設定TBL SELECT
    """
    expected_value = {
        "gigya_uid": "test_uid_02",
        'battery_remind_latitude': 35.123456,
        'battery_remind_longitude': 139.123456,
        'battery_remind_cd': '02',
        'battery_remind_voice_notice': True,
        'safety_ride_alert': True,
        'long_drive_alert': True,
        'speed_over_alert': True,
        'no_light_alert': True,
        'safety_ride_voice_notice': True,
        'home_assist_mode_number': '02'
    }

    result = get_t_user_setting_ride('test_uid_02')
    assert result == expected_value


def test_get_t_user_setting_ride_ng():
    """
    異常系: ユーザーライド設定TBL 対象0件
    """
    expected_value = None

    result = get_t_user_setting_ride('test_uid_99')
    assert result == expected_value


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_insert_t_user_setting_ride_ok_01(mocker):
    """
    正常系: ユーザーライド設定TBL INSERT
    データなし
    """
    expected_value = [{
        "gigya_uid": "test_uid_05",
        "battery_remind_latitude": 153.9807,
        "battery_remind_longitude": 24.2867,
        "battery_remind_cd": '00',
        "battery_remind_voice_notice": False,
        "safety_ride_alert": False,
        "long_drive_alert": False,
        "speed_over_alert": False,
        "no_light_alert": False,
        "safety_ride_voice_notice": False,
        "home_assist_mode_number": '02',
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None,
        "etxyobi4": None, "etxyobi5": None, "delete_flag": False,
        "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 3, 13, 13, 13, 13, 610000),
        "insert_user_id": "test_uid_05",
        "update_timestamp": None, "update_user_id": None
    }]

    gigya_uid = "test_uid_05"
    recs = {
        "battery_remind_latitude": 153.9807,
        "battery_remind_longitude": 24.2867,
        "battery_remind_cd": '00',
        "battery_remind_voice_notice": False,
        "safety_ride_alert": False,
        "long_drive_alert": False,
        "speed_over_alert": False,
        "no_light_alert": False,
        "safety_ride_voice_notice": False,
        "home_assist_mode_number": '02',
    }

    insert_t_user_setting_ride(gigya_uid, **recs)
    sql: str = '''
      SELECT * FROM t_user_setting_ride
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_05'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


def test_insert_t_user_setting_ride_ok_02(mocker):
    """
    正常系: ユーザーライド設定TBL INSERT
    データあり
    """
    expected_value = [{
        "gigya_uid": "test_uid_02",
        'battery_remind_latitude': 35.123456,
        'battery_remind_longitude': 139.123456,
        'battery_remind_cd': '02',
        'battery_remind_voice_notice': True,
        'safety_ride_alert': True,
        'long_drive_alert': True,
        'speed_over_alert': True,
        'no_light_alert': True,
        'safety_ride_voice_notice': True,
        'home_assist_mode_number': '02',
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None,
        "etxyobi4": None, "etxyobi5": None, "delete_flag": False,
        "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000),
        "insert_user_id": "test_uid_01",
        "update_timestamp": None, "update_user_id": None
    }]

    gigya_uid = "test_uid_02"
    recs = {
        "battery_remind_latitude": 153.9807,
        "battery_remind_longitude": 24.2867,
        "battery_remind_cd": '00',
        "battery_remind_voice_notice": False,
        "safety_ride_alert": False,
        "long_drive_alert": False,
        "speed_over_alert": False,
        "no_light_alert": False,
        "safety_ride_voice_notice": False,
        "home_assist_mode_number": '02',
    }

    insert_t_user_setting_ride(gigya_uid, **recs)
    sql: str = '''
      SELECT * FROM t_user_setting_ride
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_02'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


def test_delete_t_user_setting_maintain_ok_01():
    """
    正常系: ユーザーライド設定TBL delete
    """
    expected_value = []
    gigya_uid = "test_uid_02"

    delete_t_user_setting_ride(gigya_uid)

    sql: str = '''
         SELECT * FROM t_user_setting_ride
         WHERE gigya_uid = %(gigya_uid)s;
       '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_02'}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_user_setting_maintain_ng_01():
    """
    異常系: ユーザーライド設定TBL delete
    対象データなし
    """
    expected_value = []
    gigya_uid = "test_uid_99"

    delete_t_user_setting_ride(gigya_uid)

    sql: str = '''
         SELECT * FROM t_user_setting_ride
         WHERE gigya_uid = %(gigya_uid)s;
       '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_99'}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
