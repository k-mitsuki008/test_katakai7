from datetime import datetime
from importlib import import_module
import pytest
from common.rds import execute_select_statement
from tests.test_utils.fixtures import db_setup

module = import_module('repository.user_setting_maintain_item_repository')
upsert_t_user_setting_maintain_item = getattr(module, 'upsert_t_user_setting_maintain_item')
get_t_user_setting_maintain_item = getattr(module, 'get_t_user_setting_maintain_item')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_user_setting_maintain_item_ok_01():
    """
    正常系: ユーザーメンテナンス項目設定TBL UPSERT(INSERT)
    """
    expected_value = [
        {"user_vehicle_id": 1, "maintain_item_code": "10001", "maintain_item_alert": True,
         "maintain_item_alert_status": 0
            , "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None,
         "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": 0,
         "delete_timestamp": None, "delete_user_id": None,
         "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",
         "update_timestamp": None, "update_user_id": None}
    ]

    user_vehicle_id = 1
    maintain_item_code = '10001'
    gigya_uid = 'test_uid_01'
    recs = {
        "maintain_item_alert": True,
        "maintain_item_alert_status": 0
    }

    maintain_item_alert = upsert_t_user_setting_maintain_item(user_vehicle_id, maintain_item_code, gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_setting_maintain_item
      WHERE user_vehicle_id = %(user_vehicle_id)s AND maintain_item_code = %(maintain_item_code)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': 1, 'maintain_item_code': '10001'}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
    assert maintain_item_alert is True


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_user_setting_maintain_item_ok_02():
    """
    正常系: ユーザーメンテナンス項目設定TBL UPSERT(UPDATE)
    """
    expected_value = [
        {"user_vehicle_id": 1, "maintain_item_code": "00001", "maintain_item_alert": False,
         "maintain_item_alert_status": 0
            , "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None,
         "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": 0,
         "delete_timestamp": None, "delete_user_id": None,
         "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",
         "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"}
    ]

    user_vehicle_id = 1
    maintain_item_code = '00001'
    gigya_uid = 'test_uid_02'
    recs = {
        "maintain_item_alert": False,
        # "maintain_item_alert_status": 0 # 未更新確認項目
    }

    maintain_item_alert = upsert_t_user_setting_maintain_item(user_vehicle_id, maintain_item_code, gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_setting_maintain_item
      WHERE user_vehicle_id = %(user_vehicle_id)s AND maintain_item_code = %(maintain_item_code)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': 1, 'maintain_item_code': '00001'}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
    assert maintain_item_alert is False


def test_get_t_user_setting_maintain_item_ok_01():
    """
    正常系: メンテナンス指示一覧取得
    """
    # 期待しているレスポンスボディの値
    expected_value = [
        {
            "device_token": "XXXXX",
            "gigya_uid": "test_uid_02",
            "maintain_item_code": "00001",
            "user_vehicle_id": 1,
            "vehicle_name": "ユーザー指定車両名02-01"
        },
        {
            "device_token": "XXXXX",
            "gigya_uid": "test_uid_02",
            "maintain_item_code": "00002",
            "user_vehicle_id": 1,
            "vehicle_name": "ユーザー指定車両名02-01"
        },
        {
            "device_token": "XXXXX",
            "gigya_uid": "test_uid_02",
            "maintain_item_code": "00003",
            "user_vehicle_id": 1,
            "vehicle_name": "ユーザー指定車両名02-01"
        },
        {
            "device_token": "XXXXX",
            "gigya_uid": "test_uid_02",
            "maintain_item_code": "00004",
            "user_vehicle_id": 1,
            "vehicle_name": "ユーザー指定車両名02-01"
        },
        {
            "device_token": "XXXXX",
            "gigya_uid": "test_uid_02",
            "maintain_item_code": "00005",
            "user_vehicle_id": 1,
            "vehicle_name": "ユーザー指定車両名02-01"
        },
        {
            "device_token": "XXXXX",
            "gigya_uid": "test_uid_02",
            "maintain_item_code": "00009",
            "user_vehicle_id": 1,
            "vehicle_name": "ユーザー指定車両名02-01"
        }
    ]

    result = get_t_user_setting_maintain_item()
    assert result == expected_value
