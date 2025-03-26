from datetime import datetime, timedelta
from importlib import import_module
import pytest
from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup

module = import_module('repository.drive_unit_history_repository')
insert_t_drive_unit_history = getattr(module, 'insert_t_drive_unit_history')
update_latest_drive_unit_history = getattr(module, 'update_latest_drive_unit_history')
get_latest_drive_unit_history = getattr(module, 'get_latest_drive_unit_history')
get_last_maintain_archive = getattr(module, 'get_last_maintain_archive')
get_after_last_maintain_archive_list = getattr(module, 'get_after_last_maintain_archive_list')
get_oldest_drive_unit_history = getattr(module, 'get_oldest_drive_unit_history')
delete_t_drive_unit_history = getattr(module, 'delete_t_drive_unit_history')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_insert_t_drive_unit_history_ok_01():
    """
    正常系: ドライブユニット履歴TBL INSERT
    """
    expected_value = [

        {"user_vehicle_id": 123, "du_first_timestamp": datetime(2022, 10, 6, 15, 30, 31, 000), "du_last_timestamp": datetime(9999, 12, 31, 23, 59, 59, 999000), "gigya_uid": "test_uid_01", "du_serial_number": "16777215", "du_first_odometer": 120, "du_last_odometer": 120,
         "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01", "update_timestamp": None, "update_user_id": None}
    ]

    recs = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
        "du_serial_number": "16777215",
        "timestamp": "2022-10-06T15:30:31.000",
        "du_odometer": 120,
    }
    insert_t_drive_unit_history(**recs)

    sql: str = '''
      SELECT * FROM t_drive_unit_history
      WHERE 
        user_vehicle_id = %(user_vehicle_id)s 
        AND du_last_timestamp = to_timestamp('9999/12/31 23:59:59.999', 'YYYY/MM/DD HH24:MI:SS.US');
    '''
    parameters_dict: dict = {'user_vehicle_id': 123}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_latest_drive_unit_history_ok_01():
    """
    正常系: ドライブユニット履歴テーブル UPDATE
    """
    expected_value = [
        {"user_vehicle_id": 1, "du_first_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "du_last_timestamp": datetime(2022, 10, 6, 15, 30, 31, 000000), "gigya_uid": "test_uid_02", "du_serial_number": "000011", "du_first_odometer": 30, "du_last_odometer": 999,
         "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01", "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"}
    ]

    recs = {
        "du_last_timestamp": "2022-10-06T15:30:31.000",
        "du_last_odometer": 999,
    }
    update_count = update_latest_drive_unit_history("test_uid_02", 1, **recs)

    assert update_count == 1

    sql: str = '''
      SELECT * FROM t_drive_unit_history
      WHERE 
        user_vehicle_id = %(user_vehicle_id)s 
        AND du_last_timestamp = to_timestamp(%(du_last_timestamp)s, 'YYYY/MM/DD HH24:MI:SS.US');
    '''
    parameters_dict: dict = {'user_vehicle_id': 1, 'du_last_timestamp': '2022-10-06 15:30:31.000'}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_latest_drive_unit_history_ok():
    """
    正常系: 最新Du識別子取得
    """
    expected_value = {
        "du_serial_number": "000011",
        "du_first_odometer": 30,
        "du_last_odometer": 30,
        "du_first_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
        "du_last_timestamp": datetime(2022, 5, 14, 12, 34, 56, 789101),
        "odometer": 0,
    }
    result = get_latest_drive_unit_history('test_uid_02', 1)

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_get_latest_drive_unit_history_ng():
    """
    異常系: ドライブユニット履歴なし
    """
    expected_value = None
    result = get_latest_drive_unit_history(None, None)

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.999999")
def test_get_oldest_drive_unit_history_ok_01():
    """
    正常系: 初回接続時のドライブユニット履歴を取得
    du最終接続タイムスタンプが最新の場合の取得
    """
    expected_value = {
        "du_serial_number": "000099",
        "du_first_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
        "du_last_timestamp": datetime(2022, 5, 14, 12, 34, 56, 999999),
        "odometer": 30,
        "du_first_odometer": 0,
        "du_last_odometer": 30,
    }

    result = get_oldest_drive_unit_history('test_uid_99', 99)

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_oldest_drive_unit_history_ok_02():
    """
    正常系: 初回接続時のドライブユニット履歴を取得
    du最終接続タイムスタンプがではない場合
    """
    expected_value = {
        "du_serial_number": "000011",
        "du_first_timestamp": datetime(2022, 5, 10, 12, 34, 56, 789000),
        "du_last_timestamp": datetime(2022, 5, 11, 12, 34, 56, 789000),
        "odometer": 10,
        "du_first_odometer": 0,
        "du_last_odometer": 10,
    }

    result = get_oldest_drive_unit_history('test_uid_02', 1)

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_oldest_drive_unit_history_ok_03():
    """
    正常系: 初回接続時のドライブユニット履歴を取得
    取得対象なし
    """
    expected_value = None

    result = get_oldest_drive_unit_history('test_uid_9999', 1)

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_last_maintain_archive_ok_1():
    """
    正常系: 前回メンテナンス日時時点のDUの走行距離、走行時間を取得（切断済Duの場合)
    """
    expected_value = {
        "du_serial_number": "000011",
        "du_first_timestamp": datetime(2022, 5, 10, 12, 34, 56, 789000),
        "du_last_timestamp": datetime(2022, 5, 11, 12, 34, 56, 789000),
        "odometer": 10,
        "du_first_odometer": 0,
        "du_last_odometer": 10,
    }
    result = get_last_maintain_archive('test_uid_02', 1, '000011', '2022/05/11 00:00:00.000')

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_last_maintain_archive_ok_2():
    """
    正常系: 前回メンテナンス日時時点のDUの走行距離、走行時間を取得（接続中Duの場合)
    """
    expected_value = {
        "du_serial_number": "000011",
        "du_first_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
        "du_last_timestamp": datetime(2022, 5, 14, 12, 34, 56, 789101),
        "odometer": 0,
        "du_first_odometer": 30,
        "du_last_odometer": 30,
    }
    result = get_last_maintain_archive('test_uid_02', 1, '000011', '2022/05/13 00:00:00.000')

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.999999")
def test_get_last_maintain_archive_ok_3():
    """
    正常系: du最終接続タイムスタンプが最新の場合の取得
    """
    expected_value = {
        "du_serial_number": "000099",
        "du_first_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
        "du_last_timestamp": datetime(2022, 5, 14, 12, 34, 56, 999999),
        "odometer": 30,
        "du_first_odometer": 0,
        "du_last_odometer": 30,
    }
    result = get_last_maintain_archive('test_uid_99', 99, '000099', '2022/05/13 00:00:00.000')

    assert result == expected_value


def test_get_last_maintain_archive_ok_4():
    """
    正常系: 対象データが存在しない場合
    """
    expected_value = None
    result = get_last_maintain_archive('test_uid_9999', 99, '999999', '2022/05/13 00:00:00.000')

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_after_last_maintain_archive_list_ok_01():
    """
    正常系: 指定日時より後のDU最終接続Odometer、DU最終接続タイムスタンプを取得
    """
    expected_value = [
        {
            "user_vehicle_id": 1,
            "gigya_uid": "test_uid_02",
            "du_serial_number": "000022",
            "days": timedelta(days=1),
            "odometer": 10
        },
        {
            "user_vehicle_id": 1,
            "gigya_uid": "test_uid_02",
            "du_serial_number": "000011",
            "days": timedelta(days=1, microseconds=101),
            "odometer": 0
        },
    ]
    result = get_after_last_maintain_archive_list('test_uid_02', 1, '2022/05/11 12:34:56.789')

    assert result == expected_value


@pytest.mark.freeze_time("2022/05/15 12:34:56.790")
def test_get_after_last_maintain_archive_list_ok_02():
    """
    正常系: du最終接続タイムスタンプが最新の場合の取得
    """
    expected_value = [
        {
            "user_vehicle_id": 99,
            "gigya_uid": "test_uid_99",
            "du_serial_number": "000099",
            "days": timedelta(days=2, microseconds=1000),
            "odometer": 30
        }
    ]
    result = get_after_last_maintain_archive_list('test_uid_99', 99, '2022/05/11 12:34:56.789')

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_after_last_maintain_archive_list_ng():
    """
    異常系: 対象0件
    """
    expected_value = []
    result = get_after_last_maintain_archive_list('test_uid_02', 2, '2022/05/11 12:34:56.789')

    assert result == expected_value


def test_delete_t_user_setting_maintain_ok_01():
    """
    正常系: ドライブユニット履歴TBL delete
    """
    expected_value = []
    gigya_uid = "test_uid_01"
    user_vehicle_id = "1"

    delete_t_drive_unit_history(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_drive_unit_history
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_01', 'user_vehicle_id': "1"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_user_setting_maintain_ng_01():
    """
    異常系: ドライブユニット履歴TBL delete
    対象データなし
    """
    expected_value = []
    gigya_uid = "test_uid_99"
    user_vehicle_id = "999999999"

    delete_t_drive_unit_history(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_drive_unit_history
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_99', 'user_vehicle_id': "999999999"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
