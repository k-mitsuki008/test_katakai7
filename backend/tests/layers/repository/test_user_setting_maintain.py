from datetime import datetime
from importlib import import_module
import pytest
from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.user_setting_maintain_repository')
upsert_t_user_setting_maintain = getattr(module, 'upsert_t_user_setting_maintain')
get_user_setting_maintains = getattr(module, 'get_user_setting_maintains')
delete_t_user_setting_maintain = getattr(module, 'delete_t_user_setting_maintain')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_user_setting_maintain_ok_01():
    """
    正常系: ユーザーメンテナンス設定TBL UPSERT(INSERT)
    """
    expected_value = [
        {
            "user_vehicle_id": 7, "gigya_uid": "test_uid_05", "maintain_consciousness": "02", "fcdyobi1": None,
            "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None,
            "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None,
            "delete_flag": False, "delete_timestamp": None, "delete_user_id": None,
            "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
            "insert_user_id": "test_uid_05", "update_timestamp": None, "update_user_id": None
        }
    ]

    user_vehicle_id = 7
    gigya_uid = 'test_uid_05'
    recs = {
        "maintain_consciousness": "02"
    }

    maintain_consciousness = upsert_t_user_setting_maintain(user_vehicle_id, gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_setting_maintain
      WHERE user_vehicle_id = %(user_vehicle_id)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': 7}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
    assert maintain_consciousness == "02"


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_user_setting_maintain_ok_02():
    """
    正常系: ユーザーメンテナンス設定TBL UPSERT(UPDATE)
    """
    expected_value = [
        {
            "user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "03", "fcdyobi1": None,
            "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None,
            "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": 0,
            "delete_timestamp": None, "delete_user_id": None,
            "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000),
            "insert_user_id": "test_uid_01", "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
            "update_user_id": "test_uid_02"
        }
    ]

    user_vehicle_id = 1
    gigya_uid = 'test_uid_02'
    recs = {
        "maintain_consciousness": "03"
    }

    maintain_consciousness = upsert_t_user_setting_maintain(user_vehicle_id, gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_setting_maintain
      WHERE user_vehicle_id = %(user_vehicle_id)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': 1}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
    assert maintain_consciousness == "03"


def test_get_t_user_setting_ride_ok():
    """
    正常系: ユーザーライドTBL SELECT
    """
    expected_value = [
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01",
         "maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_item_alert": True,
         "maintain_item_alert_status": 0},
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01",
         "maintain_item_code": "00003", "maintain_item_name": "タイヤ摩耗", "maintain_item_alert": True,
         "maintain_item_alert_status": 0},
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01",
         "maintain_item_code": "00004", "maintain_item_name": "チェーン動作", "maintain_item_alert": True,
         "maintain_item_alert_status": 0},
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01",
         "maintain_item_code": "00005", "maintain_item_name": "ブレーキ動作、摩耗", "maintain_item_alert": True,
         "maintain_item_alert_status": 0},
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01",
         "maintain_item_code": "00001", "maintain_item_name": "ホイール", "maintain_item_alert": True,
         "maintain_item_alert_status": 0},
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01",
         "maintain_item_code": "00009", "maintain_item_name": "定期点検", "maintain_item_alert": True,
         "maintain_item_alert_status": 0}
    ]

    result = get_user_setting_maintains(1)
    assert result == expected_value


def test_delete_t_user_setting_maintain_ok():
    """
    正常系: ユーザーセッティングTBL DELETE
    """
    expected_value = []
    gigya_uid = "test_uid_01"
    user_vehicle_id = "1"

    delete_t_user_setting_maintain(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_user_setting_maintain
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_01', 'user_vehicle_id': "1"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_user_setting_maintain_ng():
    """
    異常系: ユーザーセッティングTBL DELETE
    対象データなし
    """
    expected_value = []
    gigya_uid = "test_uid_99"
    user_vehicle_id = "999999999"

    delete_t_user_setting_maintain(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_user_setting_maintain
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_99', 'user_vehicle_id': "999999999"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
