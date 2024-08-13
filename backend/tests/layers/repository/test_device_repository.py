from importlib import import_module
from datetime import datetime
import pytest

from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.device_repository')
upsert_t_device = getattr(module, 'upsert_t_device')
update_other_device_token = getattr(module, 'update_other_device_token')
get_t_device = getattr(module, 'get_t_device')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_device_ok_01():
    """
    正常系: デバイスTBL　INSERT
    """
    expected_value = [{
        "gigya_uid": "test_uid_01", "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRRRR", "device_token": "740f4707",
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01", "update_timestamp": None, "update_user_id": None
    }]

    recs = {
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRRRR",
        "device_token": "740f4707"
    }

    upsert_t_device('test_uid_01', **recs)

    sql: str = '''
        SELECT * FROM t_device
        WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_01'}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_device_ok_02():
    """
    正常系: デバイスTBL　UPDATE
    """
    expected_value = [{
        "gigya_uid": "test_uid_02", "device_id": "RRRRRRRR_UPD", "device_token": "XXXXX_UPD",
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01","update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"
    }]

    recs = {
        "device_id": "RRRRRRRR_UPD",
        "device_token": "XXXXX_UPD"
    }

    upsert_t_device('test_uid_02', **recs)

    sql: str = '''
        SELECT * FROM t_device
        WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_02'}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_other_device_token_ok():
    """
    正常系: 同一デバイスIDが登録されている場合はそのレコードのデバイストークンを空文字列にUPDATEする。
    """
    expected_value = [{
        "gigya_uid": "test_uid_03", "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX", "device_token": "",
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01","update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"
    }]

    update_other_device_token('test_uid_02', 'RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX')

    sql: str = '''
      SELECT * FROM t_device
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_03'}
    assert execute_select_statement(sql, parameters_dict) == expected_value
