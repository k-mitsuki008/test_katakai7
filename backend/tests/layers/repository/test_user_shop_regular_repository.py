from datetime import datetime

from importlib import import_module
import pytest

from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.user_shop_regular_repository')
upsert_t_user_shop_regular = getattr(module, 'upsert_t_user_shop_regular')
update_t_user_shop_regular = getattr(module, 'update_t_user_shop_regular')
get_t_user_shop_regular = getattr(module, 'get_t_user_shop_regular')
insert_t_user_shop_regular = getattr(module, 'insert_t_user_shop_regular')
delete_t_user_shop_regular = getattr(module, 'delete_t_user_shop_regular')


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_upsert_t_user_shop_regular_ok_01():
    """
    正常系:  ユーザ普段利用する店舗TBL UPSERT(INSERT)
    """
    expected_value = [{
        "gigya_uid": "test_uid_04", "shop_name": "test_shop_04",
        "shop_tel": "0412345678", "shop_location": "東京都世田谷区玉川4丁目4-4",
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None,
        "etxyobi4": None, "etxyobi5": None, "delete_flag": False,
        "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 3, 13, 13, 13, 13, 610000),
        "insert_user_id": "test_uid_04",
        "update_timestamp": None, "update_user_id": None
    }]

    gigya_uid = "test_uid_04"
    recs = {
        'shop_name': 'test_shop_04',
        'shop_tel': '0412345678',
        'shop_location': '東京都世田谷区玉川4丁目4-4',
    }

    upsert_t_user_shop_regular(gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_shop_regular
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_04'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_upsert_t_user_shop_regular_ok_02():
    """
    正常系:  ユーザ普段利用する店舗TBL UPSERT(update)
    """
    expected_value = [{
        "gigya_uid": "test_uid_07", "shop_name": "test_shop_07",
        "shop_tel": "0712345678", "shop_location": "東京都世田谷区玉川7丁目7-7",
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None,
        "etxyobi4": None, "etxyobi5": None, "delete_flag": False,
        "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 7, 17, 17, 17, 17, 610000),
        "insert_user_id": "test_uid_05",
        "update_timestamp": datetime(2022, 3, 13, 13, 13, 13, 610000),
        "update_user_id": "test_uid_07"
    }]

    gigya_uid = "test_uid_07"
    recs = {
        'shop_name': 'test_shop_07',
        'shop_tel': '0712345678',
        'shop_location': '東京都世田谷区玉川7丁目7-7',
    }

    upsert_t_user_shop_regular(gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_shop_regular
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_07'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_upsert_t_user_shop_regular_ok_03():
    """
    正常系:  ユーザ普段利用する店舗TBL UPDATE
    """
    expected_value = [{
        "gigya_uid": "test_uid_07", "shop_name": "test_shop_08",
        "shop_tel": "0812345678", "shop_location": "東京都世田谷区玉川8丁目8-8",
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None,
        "etxyobi4": None, "etxyobi5": None, "delete_flag": False,
        "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 7, 17, 17, 17, 17, 610000),
        "insert_user_id": "test_uid_05",
        "update_timestamp": datetime(2022, 3, 13, 13, 13, 13, 610000),
        "update_user_id": "test_uid_07"
    }]

    gigya_uid = "test_uid_07"
    recs = {
        'shop_name': 'test_shop_08',
        'shop_tel': '0812345678',
        'shop_location': '東京都世田谷区玉川8丁目8-8',
    }

    update_t_user_shop_regular(gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_shop_regular
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_07'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


def test_get_t_use_shop_regular_ok():
    """
    正常系: ユーザ普段利用する店舗TBL SELECT
    """
    expected_value = {
        'shop_name': 'test_shop_03',
        'shop_tel': '0312345678',
        'shop_location': '東京都世田谷区玉川3丁目3-3',
    }

    result = get_t_user_shop_regular('test_uid_03')
    assert result == expected_value


def test_get_t_user_shop_regular_ng():
    """
    異常系: ユーザ普段利用する店舗TBL 対象0件
    """
    expected_value = None

    result = get_t_user_shop_regular('test_uid_99')
    assert result == expected_value


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_upsert_t_user_shop_regular_ok_04():
    """
    正常系:  ユーザ普段利用する店舗TBL INSERT
    """
    expected_value = [{
        "gigya_uid": "test_uid_04", "shop_name": "test_shop_04",
        "shop_tel": "0412345678", "shop_location": "東京都世田谷区玉川4丁目4-4",
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None,
        "etxyobi4": None, "etxyobi5": None, "delete_flag": False,
        "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 3, 13, 13, 13, 13, 610000),
        "insert_user_id": "test_uid_04",
        "update_timestamp": None, "update_user_id": None
    }]

    gigya_uid = "test_uid_04"
    recs = {
        'shop_name': 'test_shop_04',
        'shop_tel': '0412345678',
        'shop_location': '東京都世田谷区玉川4丁目4-4',
    }

    insert_t_user_shop_regular(gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_shop_regular
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_04'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


@pytest.mark.freeze_time("2022-3-13 13:13:13.610101")
def test_upsert_t_user_shop_regular_ok_05():
    """
    正常系:  ユーザ普段利用する店舗TBL 登録済み
    """
    expected_value = [{
        "gigya_uid": "test_uid_03", "shop_name": "test_shop_03",
        "shop_tel": "0312345678", "shop_location": "東京都世田谷区玉川3丁目3-3",
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None,
        "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None,
        "etxyobi2": None, "etxyobi3": None, "etxyobi4": None,
        "etxyobi5": None, "delete_flag": False, "delete_timestamp": None,
        "delete_user_id": None,
        "insert_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
        "insert_user_id": "test_uid_05",
        "update_timestamp": None, "update_user_id": None
    }]

    gigya_uid = "test_uid_03"
    recs = {
        'shop_name': 'test_shop_08',
        'shop_tel': '0812348888',
        'shop_location': '東京都世田谷区玉川8丁目8-8',
    }

    insert_t_user_shop_regular(gigya_uid, **recs)

    sql: str = '''
      SELECT * FROM t_user_shop_regular
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_03'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


def test_delete_t_user_setting_maintain_ok_01():
    """
    正常系: ユーザ普段利用する店舗TBL delete
    """
    expected_value = []
    gigya_uid = "test_uid_01"

    delete_t_user_shop_regular(gigya_uid)

    sql: str = '''
         SELECT * FROM t_user_shop_regular
         WHERE gigya_uid = %(gigya_uid)s;
       '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_01'}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_user_setting_maintain_ng_01():
    """
    異常系: ユーザ普段利用する店舗TBL delete
    対象データなし
    """
    expected_value = []
    gigya_uid = "test_uid_99"

    delete_t_user_shop_regular(gigya_uid)

    sql: str = '''
         SELECT * FROM t_user_shop_regular
         WHERE gigya_uid = %(gigya_uid)s;
       '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_99'}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
