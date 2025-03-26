
from datetime import datetime

from importlib import import_module
import pytest

from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.user_shop_purchase_repository')
upsert_t_user_shop_purchase = getattr(module, 'upsert_t_user_shop_purchase')
update_t_user_shop_purchase = getattr(module, 'update_t_user_shop_purchase')
get_t_user_shop_purchase = getattr(module, 'get_t_user_shop_purchase')
delete_t_user_shop_purchase = getattr(module, 'delete_t_user_shop_purchase')


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_upsert_t_user_shop_purchase_ok_01():
    """
    正常系: ユーザー購入店舗TBL UPSERT(INSERT)
    """
    expected_value = [{
        "user_vehicle_id": 6, "gigya_uid": "test_uid_05",
        "shop_name": "test_shop_03", "shop_tel": "0312345678",
        "shop_location": "東京都世田谷区玉川3丁目3-3", "fcdyobi1": None,
        "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None,
        "etxyobi3": None, "etxyobi4": None, "etxyobi5": None,
        "delete_flag": False, "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 3, 13, 13, 13, 13, 610000),
        "insert_user_id": "test_uid_05", "update_timestamp": None,
        "update_user_id": None
    }]

    user_vehicle_id = 6
    recs = {
        'gigya_uid': 'test_uid_05',
        'shop_name': 'test_shop_03',
        'shop_tel': '0312345678',
        'shop_location': '東京都世田谷区玉川3丁目3-3',
    }

    upsert_t_user_shop_purchase(user_vehicle_id, **recs)

    sql: str = '''
      SELECT * FROM t_user_shop_purchase
      WHERE user_vehicle_id = %(user_vehicle_id)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': '6'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_upsert_t_user_shop_purchase_ok_02():
    """
    正常系: ユーザー購入店舗TBL UPSERT(UPDATE)
    """
    expected_value = [{
        "user_vehicle_id": 140, "gigya_uid": "test_uid_02",
        "shop_name": "test_shop_02", "shop_tel": "0212345678",
        "shop_location": "東京都世田谷区玉川2丁目2-2", "fcdyobi1": None,
        "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None,
        "etxyobi3": None, "etxyobi4": None, "etxyobi5": None,
        "delete_flag": False, "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
        "insert_user_id": "test_uid_05",
        "update_timestamp":  datetime(2022, 3, 13, 13, 13, 13, 610000),
        "update_user_id": 'test_uid_02'
    }]

    user_vehicle_id = 140
    recs = {
        'gigya_uid': 'test_uid_02',
        'shop_name': 'test_shop_02',
        'shop_tel': '0212345678',
        'shop_location': '東京都世田谷区玉川2丁目2-2',
    }

    upsert_t_user_shop_purchase(user_vehicle_id, **recs)

    sql: str = '''
      SELECT * FROM t_user_shop_purchase
      WHERE user_vehicle_id = %(user_vehicle_id)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': '140'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_update_t_user_shop_purchase_ok_03():
    """
    正常系: ユーザー購入店舗TBL UPDATE
    """
    expected_value = [{
        "user_vehicle_id": 140, "gigya_uid": "test_uid_02",
        "shop_name": "test_shop_02", "shop_tel": "0212345678",
        "shop_location": "東京都世田谷区玉川2丁目2-2", "fcdyobi1": None, "fcdyobi2": None,
        "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None,
        "etxyobi1": None, "etxyobi2": None, "etxyobi3": None,
        "etxyobi4": None, "etxyobi5": None, "delete_flag": False,
        "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
        "insert_user_id": "test_uid_05",
        "update_timestamp":  datetime(2022, 3, 13, 13, 13, 13, 610000),
        "update_user_id": 'test_uid_02'
    }]

    user_vehicle_id = 140
    recs = {
        'gigya_uid': 'test_uid_02',
        'shop_name': 'test_shop_02',
        'shop_tel': '0212345678',
        'shop_location': '東京都世田谷区玉川2丁目2-2',
    }

    update_t_user_shop_purchase(user_vehicle_id, **recs)

    sql: str = '''
      SELECT * FROM t_user_shop_purchase
      WHERE user_vehicle_id = %(user_vehicle_id)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': '140'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_get_t_use_shop_purchase_ok():
    """
    正常系: ユーザー購入店舗TBL SELECT
    """
    expected_value = {
        'user_vehicle_id': 140,
        'gigya_uid': 'test_uid_02',
        'shop_name': 'test_shop_02',
        'shop_tel': '0212345678',
        'shop_location': '東京都世田谷区玉川2丁目2-2',
    }

    result = get_t_user_shop_purchase(140)
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_get_t_user_shop_purchase_ng():
    """
    異常系: ユーザー購入店舗TBL 対象0件
    """
    expected_value = None

    result = get_t_user_shop_purchase(99999)
    assert result == expected_value


def test_delete_t_user_shop_purchase_ok_01():
    """
    正常系: ユーザー購入店舗TBL delete
    """
    expected_value = []
    gigya_uid = "test_uid_01"
    user_vehicle_id = "1"

    delete_t_user_shop_purchase(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_user_shop_purchase
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_01', 'user_vehicle_id': "1"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_user_shop_purchase_ng_01():
    """
    異常系: ユーザー購入店舗TBL delete
    対象データなし
    """
    expected_value = []
    gigya_uid = "test_uid_99"
    user_vehicle_id = "999999999"

    delete_t_user_shop_purchase(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_user_shop_purchase
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_99', 'user_vehicle_id': "999999999"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
