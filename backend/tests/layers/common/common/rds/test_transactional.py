from importlib import import_module
import pytest
from common.error.db_access_error import DbAccessError
from common.rds.transactional import transactional

import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup


module = import_module('common.rds.core')
execute_insert_statement = getattr(module, 'execute_insert_statement')


def test_transactional_ok():

    """
    正常系
    """
    sample_insert_func()

    assert True


def test_transactional_ok_rollback():

    """
    正常系
    ※ロールバック関数
    """

    with pytest.raises(DbAccessError) as e:
        sample_transaction_rollback()

    # テストの前後でデータの内容が変わっていないこと
    assert True


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


@transactional
def sample_transaction_rollback():
    """
    ロールバックのためのサンプル関数
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
    raise DbAccessError()
