from datetime import date, datetime
from importlib import import_module

import pytest
from common.rds import execute_select_statement

import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.radar_user_info_setting_repository')
get_user_info_setting = getattr(module, 'get_user_info_setting')
upsert_user_info_setting = getattr(module, 'upsert_user_info_setting')


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_get_user_info_setting_ok_01():
    """
    正常系: 個人設定TBL SELECT
    レコードあり
    """
    expected_value = {
        'gigya_uid': 'test_uid_02',
        'nickname': 'test_user_02',
        'weight': 60,
        'birth_date': date(2000, 1, 1),
        'max_heart_rate': 150
    }

    result = get_user_info_setting('test_uid_02')
    assert result == expected_value


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_get_user_info_setting_ok_02():
    """
    正常系: 個人設定TBL SELECT
    レコードなし
    """
    expected_value = {}

    result = get_user_info_setting('test_uid_99')
    assert result == expected_value


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_upsert_user_info_setting_ok_01():
    """
    正常系: 個人設定TBL UPSERT
    登録 全項目
    """
    expected_value = [{
        'gigya_uid': 'new_user_1',
        'nickname': 'new_user_1',
        'weight': 100,
        'birth_date': date(2001, 1, 1),
        'max_heart_rate': 140,
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
        'nickname': 'new_user_1',
        'weight': 100,
        'birth_date': '2001-01-01',
        'max_heart_rate': 140
    }

    upsert_user_info_setting('new_user_1', **params)

    sql: str = '''
        SELECT
            *
        FROM t_user_setting
        WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'new_user_1'}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_upsert_user_info_setting_ok_02():
    """
    正常系: 個人設定TBL UPSERT
    登録 項目不足
    """
    expected_value = [{
        'gigya_uid': 'new_user_2',
        'nickname': 'new_user_2',
        'weight': 102,
        'birth_date': None,
        'max_heart_rate': None,
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
        'nickname': 'new_user_2',
        'weight': 102,
    }

    upsert_user_info_setting('new_user_2', **params)

    sql: str = '''
        SELECT
            *
        FROM t_user_setting
        WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'new_user_2'}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_upsert_user_info_setting_ok_03():
    """
    正常系: 個人設定TBL UPSERT
    更新 全項目
    """
    expected_value = [{
        'gigya_uid': 'test_uid_02',
        'nickname': 'test_uid_02',
        'weight': 101,
        'birth_date': date(2001, 1, 2),
        'max_heart_rate': 141,
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
        'insert_timestamp': datetime(2022, 12, 12, 12, 12, 12, 610000),
        'insert_user_id': 'test_uid_05',
        'update_timestamp': datetime(2023, 5, 13, 12, 34, 56, 789000),
        'update_user_id': 'test_uid_02',
    }]

    params = {
        'nickname': 'test_uid_02',
        'weight': 101,
        'birth_date': '2001-01-02',
        'max_heart_rate': 141
    }

    upsert_user_info_setting('test_uid_02', **params)

    sql: str = '''
        SELECT
            *
        FROM t_user_setting
        WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_02'}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time('2023-05-14 12:34:56.789101')
def test_upsert_user_info_setting_ok_04():
    """
    正常系: 個人設定TBL UPSERT
    更新 項目不足
    """
    expected_value = [{
        'gigya_uid': 'test_uid_02',
        'nickname': 'test_uid_04',
        'weight': 104,
        'birth_date': date(2000, 1, 1),
        'max_heart_rate': 150,
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
        'insert_timestamp': datetime(2022, 12, 12, 12, 12, 12, 610000),
        'insert_user_id': 'test_uid_05',
        'update_timestamp': datetime(2023, 5, 14, 12, 34, 56, 789000),
        'update_user_id': 'test_uid_02',
    }]

    params = {
        'nickname': 'test_uid_04',
        'weight': 104,
    }

    upsert_user_info_setting('test_uid_02', **params)

    sql: str = '''
        SELECT
            *
        FROM t_user_setting
        WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_02'}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value
