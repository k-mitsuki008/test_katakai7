
from importlib import import_module
import pytest

from common.error.db_access_error import DbAccessError

module = import_module('common.rds.connect')
DbConnection = getattr(module, 'DbConnection')


def test_db_access_error(mocker):
    """
    準正常系
    DB アクセス失敗時のエラーハンドリング
    """
    # DB接続に必要な情報を書き換えて接続エラーを発生させる
    mocker.patch(
        'common.rds.connect.get_secret',
        return_value={
            'username': 'admin',
            'password': 'spvc_admin',
            'host': 'localhost',
            'port': '15432',
            'dbClusterIdentifier': 'dummy'
        }
    )

    with pytest.raises(DbAccessError) as e:
        dc = DbConnection()
        dc.connect()

    assert type(e.value) == DbAccessError


def test_db_not_connected():
    """
    正常系
    ※DB接続してない場合の考慮
    """
    dc = DbConnection()
    dc.close()

    # 例外などが発生しなければ問題なし
    assert True


def test_db_connect(mocker):
    """
    正常系
    DBアクセス
    """

    mocker.patch(
        'common.rds.connect.get_secret',
        return_value={
            'username': 'admin',
            'password': 'spvc_admin',
            'host': 'localhost',
            'port': '15432',
            'dbClusterIdentifier': 'spvc_local'
        }
    )

    dc = DbConnection()
    dc.connect()

    # 例外などが発生しなければ問題なし
    assert True


def test_db_already_connected(mocker):
    """
    正常系
    コネクションが確立済みの場合はそのまま返す
    """

    mocker.patch(
        'common.rds.connect.get_secret',
        return_value={
            'username': 'admin',
            'password': 'spvc_admin',
            'host': 'localhost',
            'port': '15432',
            'dbClusterIdentifier': 'spvc_local'
        }
    )

    dc = DbConnection()
    dc.connect()
    dc.connect()

    # 例外などが発生しなければ問題なし
    assert True


def test_db_delete_connection(mocker):
    """
    正常系
    コネクション削除処理
    """

    mocker.patch(
        'common.rds.connect.get_secret',
        return_value={
            'username': 'admin',
            'password': 'spvc_admin',
            'host': 'localhost',
            'port': '15432',
            'dbClusterIdentifier': 'spvc_local'
        }
    )

    dc = DbConnection()
    dc.connect()
    # pylint: disable-next=unnecessary-dunder-call
    dc.__del__()

    # 例外などが発生しなければ問題なし
    assert True


def test_db_commit(mocker):
    """
    正常系
    DB コミット関数呼び出し
    """

    mocker.patch(
        'common.rds.connect.get_secret',
        return_value={
            'username': 'admin',
            'password': 'spvc_admin',
            'host': 'localhost',
            'port': '15432',
            'dbClusterIdentifier': 'spvc_local'
        }
    )

    dc = DbConnection()
    dc.connect()
    dc.commit()

    # 例外などが発生しなければ問題なし
    assert True


def test_db_rollback(mocker):
    """
    正常系
    ロールバック関数呼び出し
    """

    mocker.patch(
        'common.rds.connect.get_secret',
        return_value={
            'username': 'admin',
            'password': 'spvc_admin',
            'host': 'localhost',
            'port': '15432',
            'dbClusterIdentifier': 'spvc_local'
        }
    )

    dc = DbConnection()
    dc.connect()
    dc.rollback()

    # 例外などが発生しなければ問題なし
    assert True


def test_db_is_transaction(mocker):
    """
    正常系
    トランザクション存在確認
    """

    mocker.patch(
        'common.rds.connect.get_secret',
        return_value={
            'username': 'admin',
            'password': 'spvc_admin',
            'host': 'localhost',
            'port': '15432',
            'dbClusterIdentifier': 'spvc_local'
        }
    )

    dc = DbConnection()
    dc.connect()
    # pylint: disable-next=pointless-statement
    dc.is_transactional

    # 例外などが発生しなければ問題なし
    assert True


def test_db_start_transaction(mocker):
    """
    正常系
    トランザクション開始
    """

    mocker.patch(
        'common.rds.connect.get_secret',
        return_value={
            'username': 'admin',
            'password': 'spvc_admin',
            'host': 'localhost',
            'port': '15432',
            'dbClusterIdentifier': 'spvc_local'
        }
    )

    dc = DbConnection()
    dc.connect()
    dc.start_transaction()

    # 例外などが発生しなければ問題なし
    assert True


def test_db_stop_transaction(mocker):
    """
    正常系
    トランザクション停止
    """

    mocker.patch(
        'common.rds.connect.get_secret',
        return_value={
            'username': 'admin',
            'password': 'spvc_admin',
            'host': 'localhost',
            'port': '15432',
            'dbClusterIdentifier': 'spvc_local'
        }
    )

    dc = DbConnection()
    dc.connect()
    dc.stop_transaction()

    # 例外などが発生しなければ問題なし
    assert True
