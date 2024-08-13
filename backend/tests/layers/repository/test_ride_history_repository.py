from datetime import datetime

from importlib import import_module
import pytest

from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.ride_history_repository')
upsert_t_ride_history = getattr(module, 'upsert_t_ride_history')
get_ride_history = getattr(module, 'get_ride_history')
get_ride_history_limit = getattr(module, 'get_ride_history_limit')
get_ride_history_all_count = getattr(module, 'get_ride_history_all_count')
update_t_ride_history = getattr(module, 'update_t_ride_history')
delete_t_ride_history = getattr(module, 'delete_t_ride_history')
delete_t_ride_history_user_vehicle_id = getattr(module, 'delete_t_ride_history_user_vehicle_id')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_ride_history_ok_01():
    """
    正常系: ライド履歴TBL UPSERT(INSERT)
    """
    expected_value = [{
        "ride_history_id": "3332022-10-06T15:30:31.000",
        "gigya_uid": "test_uid_01",
        "start_timestamp": datetime(2022, 10, 6, 15, 30, 31),
        "end_timestamp": datetime(2022, 9, 1, 15, 30, 31),
        "user_vehicle_id": 123, "trip_distance": 1234.5,
        "trip_time": 3600, "total_calorie": 535, "battery_consumption": 72,
        "average_speed": 15, "max_speed": 20, "max_pedaling_power": 6,
        "max_cadence": 126, "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": False,
        "fcdyobi1": None,
        "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None,
        "etxyobi3": None, "etxyobi4": None, "etxyobi5": None,
        "delete_flag": False, "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
        "insert_user_id": "test_uid_01", "update_timestamp": None,
        "update_user_id": None
    }]

    ride_history_id = "3332022-10-06T15:30:31.000"
    gigya_uid = "test_uid_01"
    recs = {
        "start_timestamp": "2022-10-06T15:30:31.000",
        "end_timestamp": "2022-09-01T15:30:31.000",
        "user_vehicle_id": 123,
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max_speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": False,
    }

    upsert_t_ride_history(gigya_uid, ride_history_id, **recs)

    sql: str = '''
      SELECT * FROM t_ride_history
      WHERE ride_history_id = %(ride_history_id)s;
    '''
    parameters_dict: dict = {'ride_history_id': "3332022-10-06T15:30:31.000"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_ride_history_ok_02():
    """
    正常系: ユーザーメンテナンス設定TBL UPSERT(UPDATE)
    """
    expected_value = [{
        "ride_history_id": "1212022-10-06T15:30:31.000",
        "gigya_uid": "test_uid_01",
        "start_timestamp": datetime(2022, 10, 6, 15, 30, 31),
        "end_timestamp": datetime(2022, 9, 1, 15, 30, 31),
        "user_vehicle_id": 121, "trip_distance": 1234.5,
        "trip_time": 3600, "total_calorie": 535, "battery_consumption": 72,
        "average_speed": 15, "max_speed": 20, "max_pedaling_power": 6,
        "max_cadence": 126, "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": False,
        "fcdyobi1": None,
        "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None,
        "etxyobi3": None, "etxyobi4": None, "etxyobi5": None,
        "delete_flag": False, "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 11, 17, 17, 17, 17, 610000),
        "insert_user_id": "test_uid_05",
        "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
        "update_user_id": "test_uid_01",
    }]

    ride_history_id = '1212022-10-06T15:30:31.000'
    gigya_uid = 'test_uid_01'
    recs = {
        "start_timestamp": "2022-10-06T15:30:31.000",
        "end_timestamp": "2022-09-01T15:30:31.000",
        "user_vehicle_id": 121,
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max_speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": False,
    }

    upsert_t_ride_history(gigya_uid, ride_history_id, **recs)

    sql: str = '''
      SELECT * FROM t_ride_history
      WHERE ride_history_id = %(ride_history_id)s;
    '''
    parameters_dict: dict = {'ride_history_id': "1212022-10-06T15:30:31.000"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_get_ride_history_ok():
    """
    正常系: ライド履歴TBL SELECT
    """
    expected_value = {
        "ride_history_id": "1202022-10-06T15:30:31.000",
        "start_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
        "end_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
        "trip_distance": 1234.5,
        "trip_time": 3600, "total_calorie": 535, "battery_consumption": 72,
        "average_speed": 15, "max_speed": 20, "max_pedaling_power": 6,
        "max_cadence": 126, "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": False,
    }

    ride_history_id = "1202022-10-06T15:30:31.000"
    gigya_uid = "test_uid_01"

    result = get_ride_history(gigya_uid, ride_history_id)
    assert result == expected_value


def test_get_ride_history_ng():
    """
    異常系: ライド履歴TBL 対象0件
    """
    expected_value = None

    ride_history_id = "99999"
    gigya_uid = "9999"

    result = get_ride_history(gigya_uid, ride_history_id)
    assert result == expected_value


def test_get_ride_history_limit_ok_01():
    """
    正常系: ライド履歴TBL SELECT
    begin,end,bookmark_flg指定あり
    """
    expected_value = [
        {
            "ride_history_id": "1332022-10-06T15:30:31.000",
            "start_timestamp": datetime(2022, 12, 13, 12, 12, 12, 611000),
            "end_timestamp": datetime(2022, 12, 13, 12, 12, 12, 611000),
            "ride_name": "ユーザー車両名のライド",
            "trip_distance": 1234.5,
            "trip_time": 3600,
            "bookmark_flg": False,
        },
        {
            "ride_history_id": "2222022-10-06T15:30:31.000",
            "start_timestamp": datetime(2022, 12, 13, 12, 12, 12, 610000),
            "end_timestamp": datetime(2022, 12, 13, 12, 12, 12, 610000),
            "ride_name": "ユーザー車両名のライド",
            "trip_distance": 1234.5,
            "trip_time": 3600,
            "bookmark_flg": False,
        },
        {
            "ride_history_id": "1322022-10-06T15:30:31.000",
            "start_timestamp": datetime(2022, 12, 12, 12, 12, 12, 611000),
            "end_timestamp": datetime(2022, 12, 12, 12, 12, 12, 611000),
            "ride_name": "ユーザー車両名のライド",
            "trip_distance": 1234.5,
            "trip_time": 3600,
            "bookmark_flg": False,
        },
    ]

    gigya_uid = "test_uid_01"
    begin = "2022/12/5 12:12:12.610"
    end = "2022/12/15 12:12:12.610"
    bookmark_flg = False
    limit = 3
    offset = 2

    result = get_ride_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end,
        bookmark_flg,
    )
    assert result == expected_value


def test_get_ride_history_limit_ok_02():
    """
    正常系: ライド履歴TBL SELECT
    bookmark_flg指定なし
    """
    expected_value = [
        {
            "ride_history_id": "1402022-10-06T15:30:31.000",
            "start_timestamp": datetime(2022, 12, 20, 12, 12, 12, 610000),
            "end_timestamp": datetime(2022, 12, 20, 12, 12, 12, 610000),
            "ride_name": "ユーザー車両名のライド",
            "trip_distance": 1234.5,
            "trip_time": 3600,
            "bookmark_flg": True,
        },
        {
            "ride_history_id": "1392022-10-06T15:30:31.000",
            "start_timestamp": datetime(2022, 12, 19, 12, 12, 12, 610000),
            "end_timestamp": datetime(2022, 12, 19, 12, 12, 12, 610000),
            "ride_name": "ユーザー車両名のライド",
            "trip_distance": 1234.5,
            "trip_time": 3600,
            "bookmark_flg": False,
        },
        {
            "ride_history_id": "1382022-10-06T15:30:31.000",
            "start_timestamp": datetime(2022, 12, 18, 12, 12, 12, 610000),
            "end_timestamp": datetime(2022, 12, 18, 12, 12, 12, 610000),
            "ride_name": "ユーザー車両名のライド",
            "trip_distance": 1234.5,
            "trip_time": 3600,
            "bookmark_flg": False,
        },
    ]

    gigya_uid = "test_uid_01"
    limit = 3
    offset = 0
    begin = "2022/12/1 12:12:12.610"
    end = "2022/12/21 12:12:12.610"

    result = get_ride_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end
    )
    assert result == expected_value


def test_get_ride_history_limit_ng():
    """
    異常系: ライド履歴TBL 対象0件
    begin,end,bookmark_flg指定あり
    """
    expected_value = []

    gigya_uid = "99999"
    begin = "2022/12/5 9:9:9.990"
    end = "2022/12/15 9:9:9.990"
    bookmark_flg = False
    limit = 3
    offset = 2

    result = get_ride_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end,
        bookmark_flg,
    )
    assert result == expected_value


def test_get_ride_history_all_count_ok_01():
    """
    正常系: ライド履歴TBL 対象0件
    begin,end,bookmark_flg指定あり
    """
    expected_value = {'count': 14}

    gigya_uid = "test_uid_01"
    begin = "2022/12/5 12:12:12.610"
    end = "2022/12/15 12:12:12.610"
    bookmark_flg = False

    result = get_ride_history_all_count(
        gigya_uid,
        begin,
        end,
        bookmark_flg,
    )
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_t_ride_history_ok_01():
    """
    正常系: ライド履歴TBL UPDATE
    """
    expected_value = [{
        "ride_history_id": "1212022-10-06T15:30:31.000",
        "gigya_uid": "test_uid_01",
        "start_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
        "end_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
        "user_vehicle_id": 121, "trip_distance": 1234.5,
        "trip_time": 3600, "total_calorie": 535, "battery_consumption": 72,
        "average_speed": 15, "max_speed": 20, "max_pedaling_power": 6,
        "max_cadence": 126, "ride_name": "あああああ",
        "bookmark_flg": True,
        "fcdyobi1": None,
        "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None,
        "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None,
        "etxyobi3": None, "etxyobi4": None, "etxyobi5": None,
        "delete_flag": False, "delete_timestamp": None, "delete_user_id": None,
        "insert_timestamp": datetime(2022, 11, 17, 17, 17, 17, 610000),
        "insert_user_id": "test_uid_05",
        "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
        "update_user_id": "test_uid_01",
    }]

    ride_history_id = "1212022-10-06T15:30:31.000"
    gigya_uid = "test_uid_01"
    recs = {
        "ride_name": "あああああ",
        "bookmark_flg": True,
    }

    update_t_ride_history(gigya_uid, ride_history_id, **recs)

    sql: str = '''
       SELECT * FROM t_ride_history
       WHERE ride_history_id = %(ride_history_id)s;
     '''
    parameters_dict: dict = {'ride_history_id': "1212022-10-06T15:30:31.000"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_t_ride_history_ng_01():
    """
    異常系: ライド履歴TBL UPDATE
    対象データなし
    """
    expected_value = []

    ride_history_id = "999999999"
    gigya_uid = "test_uid_01"
    recs = {
        "ride_name": "あああああ",
        "bookmark_flg": True,
    }

    update_t_ride_history(gigya_uid, ride_history_id, **recs)

    sql: str = '''
       SELECT * FROM t_ride_history
       WHERE ride_history_id = %(ride_history_id)s;
     '''
    parameters_dict: dict = {'ride_history_id': "999999999"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_get_ride_history_all_count_ok_02():
    """
    正常系: ライド履歴TBL 対象0件
    begin,end,bookmark_flg指定なし
    """
    expected_value = {'count': 14}

    gigya_uid = "test_uid_01"
    begin = "2022/12/5 12:12:12.610"
    end = "2022/12/15 12:12:12.610"

    result = get_ride_history_all_count(
        gigya_uid,
        begin,
        end
    )
    assert result == expected_value


def test_delete_t_ride_history_ok_01():
    """
    正常系: ライド履歴TBL delete
    対象データあり
    """
    expected_value = []

    ride_history_id = "1202022-10-06T15:30:31.000"
    gigya_uid = "test_uid_01"

    delete_t_ride_history(gigya_uid, ride_history_id)

    sql: str = '''
       SELECT * FROM t_ride_history
       WHERE ride_history_id = %(ride_history_id)s;
     '''
    parameters_dict: dict = {'ride_history_id': "1202022-10-06T15:30:31.000"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_ride_history_ng_01():
    """
    異常系: ライド履歴TBL delete
    対象データなし
    """
    expected_value = []

    ride_history_id = "999999999"
    gigya_uid = "test_uid_01"

    delete_t_ride_history(gigya_uid, ride_history_id)

    sql: str = '''
       SELECT * FROM t_ride_history
       WHERE ride_history_id = %(ride_history_id)s;
     '''
    parameters_dict: dict = {'ride_history_id': "999999999"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_ride_history_user_vehicle_id_ok_01():
    """
    正常系: ライド履歴TBL delete
    """
    expected_value = []

    gigya_uid = "test_uid_01"
    user_vehicle_id = "121"

    delete_t_ride_history_user_vehicle_id(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_ride_history
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_01', 'user_vehicle_id': "121"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_ride_history_user_vehicle_id_ng_01():
    """
    異常系: ライド履歴TBL delete
    対象データなし
    """
    expected_value = []

    gigya_uid = "test_uid_99"
    user_vehicle_id = "999999999"

    delete_t_ride_history_user_vehicle_id(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_ride_history
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_01', 'user_vehicle_id': "999999999"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
