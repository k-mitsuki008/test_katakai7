import datetime
from importlib import import_module
import pytest
from common.error.db_access_error import DbAccessError
from common.rds.transactional import transactional

import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup


module = import_module('common.rds.core')
execute_statement = getattr(module, 'execute_statement')
execute_select_statement = getattr(module, 'execute_select_statement')
execute_insert_statement = getattr(module, 'execute_insert_statement')
execute_update_statement = getattr(module, 'execute_update_statement')
execute_delete_statement = getattr(module, 'execute_delete_statement')
batch_execute_insert_statement = getattr(module, 'batch_execute_insert_statement')
DbConnection = getattr(module, 'DbConnection')


@transactional
def sample_insert_func():
    """
    トランザクションのためのサンプル関数
    """

    sql1 = '''
    INSERT INTO t_user_shop_regular( 
        gigya_uid
        , shop_name
        , shop_tel
        , shop_location
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    ('test_uid_06','test_shop_03','0312345678','東京都世田谷区玉川3丁目3-3','2022/12/12 12:12:12.610','test_uid_05');
    '''
    sql2 = '''
    INSERT INTO t_user_shop_regular( 
        gigya_uid
        , shop_name
        , shop_tel
        , shop_location
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    ('test_uid_05','test_shop_03','0312345678','東京都世田谷区玉川3丁目3-3','2022/12/12 12:12:12.610','test_uid_05');
    '''

    execute_insert_statement(sql1)
    execute_insert_statement(sql2)


def test_execute_statement_ng_db_access_error():

    """
    準正常系
    execute_statement エラー
    """

    # デタラメなSQLを実行して、DBエラーを発生させる
    sql = '***'

    with pytest.raises(DbAccessError) as e:
        execute_statement(sql)

    assert type(e.value) == DbAccessError


def test_execute_statement(mocker):
    """
    正常系
    execute_statement
    """

    sql = 'SELECT * FROM t_device;'
    execute_statement(sql)
    sample_insert_func()

    assert True


def test_execute_select_statement_ng_db_access_error():

    """
    準正常系
    execute_select_statement エラー
    """

    # デタラメなSQLを実行して、DBエラーを発生させる
    sql = '***'

    with pytest.raises(DbAccessError) as e:
        execute_select_statement(sql)

    assert type(e.value) == DbAccessError


def test_execute_select_statement(mocker):
    """
    正常系
    execute_select_statement
    """

    sql = 'SELECT * FROM t_device;'
    execute_select_statement(sql)

    assert True


def test_execute_insert_statement_ng_db_access_error():

    """
    準正常系
    execute_insert_statement エラー
    """

    # デタラメなSQLを実行して、DBエラーを発生させる
    sql = '***'

    with pytest.raises(DbAccessError) as e:
        execute_insert_statement(sql)

    assert type(e.value) == DbAccessError


def test_execute_insert_statement(mocker):
    """
    正常系
    execute_insert_statement
    """

    sql = 'SELECT * FROM t_device;'
    parameters_dict = {None}
    execute_insert_statement(sql)
    execute_insert_statement(sql, parameters_dict, True)

    assert True


def test_execute_update_statement_ng_db_access_error():

    """
    準正常系
    execute_update_statement エラー
    """

    # デタラメなSQLを実行して、DBエラーを発生させる
    sql = '***'

    with pytest.raises(DbAccessError) as e:
        execute_update_statement(sql)

    assert type(e.value) == DbAccessError


@transactional
def sample_update_func():
    """
    トランザクションのためのサンプル関数
    """

    sql1 = '''
        UPDATE t_user_shop_regular SET shop_name='test_shop_updated' WHERE t_user_shop_regular.gigya_uid='test_uid_01';
    '''
    sql2 = '''
        UPDATE t_user_shop_regular SET shop_name='test_shop_updated-2' WHERE t_user_shop_regular.gigya_uid='test_uid_03';
    '''

    execute_update_statement(sql1)
    execute_update_statement(sql2)


def test_execute_update_statement(mocker):
    """
    正常系
    execute_update_statement
    """

    sql = 'SELECT * FROM t_device;'
    parameters_dict = {None}
    execute_update_statement(sql)
    execute_update_statement(sql, parameters_dict, True)

    sample_update_func()

    assert True


def test_execute_delete_statement_ng_db_access_error():

    """
    準正常系
    execute_delete_statement エラー
    """

    # デタラメなSQLを実行して、DBエラーを発生させる
    sql = '***'

    with pytest.raises(DbAccessError) as e:
        execute_delete_statement(sql)

    assert type(e.value) == DbAccessError


@transactional
def sample_delete_func():
    """
    トランザクションのためのサンプル関数
    """

    sql1 = '''
        DELETE FROM t_user_shop_regular WHERE t_user_shop_regular.gigya_uid='test_uid_01';
    '''
    sql2 = '''
        DELETE FROM t_user_shop_regular WHERE t_user_shop_regular.gigya_uid='test_uid_03';
    '''

    execute_delete_statement(sql1)
    execute_delete_statement(sql2)


def test_execute_delete_statement(mocker):
    """
    正常系
    execute_delete_statement
    """

    sql = 'SELECT * FROM t_device;'
    parameters_dict = {None}
    execute_delete_statement(sql)
    execute_delete_statement(sql, parameters_dict, True)

    sample_delete_func()

    assert True


def test_batch_execute_insert_statement(mocker):
    """
    正常系
    batch_execute_insert_statement
    """

    sql = '''
        INSERT INTO
        t_bicycle_parking(
          route_id,
          bicycle_parking_name,
          bicycle_parking_distance,
          bicycle_parking_location,
          bicycle_parking_place_id,
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(route_id)s,
          %(bicycle_parking_name)s,
          %(bicycle_parking_distance)s,
          ST_GeomFromText('POINT(%(latitude)s %(longitude)s)', 4326),
          %(bicycle_parking_place_id)s,
          %(now_str)s,
          %(gigya_uid)s
        );
    '''
    bicycle_parking = [
        {
            'route_id': 1,
            'bicycle_parking_name': '駐輪場1',
            'bicycle_parking_distance': 123,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0,
            'now_str': datetime.datetime.now(),
            'gigya_uid': 'asdf1234'
        },
        {
            'route_id': 1,
            'bicycle_parking_name': '駐輪場2',
            'bicycle_parking_distance': 124,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0,
            'now_str': datetime.datetime.now(),
            'gigya_uid': 'asdf1234'
        },
        {
            'route_id': 1,
            'bicycle_parking_name': '駐輪場3',
            'bicycle_parking_distance': 125,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0,
            'now_str': datetime.datetime.now(),
            'gigya_uid': 'asdf1234'
        }
    ]

    count = batch_execute_insert_statement(sql, bicycle_parking)

    assert count == 3
