
from datetime import datetime
from importlib import import_module
import pytest
from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.maintain_history_repository')
insert_t_maintain_history = getattr(module, 'insert_t_maintain_history')
update_t_maintain_history = getattr(module, 'update_t_maintain_history')
get_t_maintain_history = getattr(module, 'get_t_maintain_history')
get_maintain_history_limit = getattr(module, 'get_maintain_history_limit')
get_maintain_history_all_count = getattr(module, 'get_maintain_history_all_count')
delete_t_maintain_history = getattr(module, 'delete_t_maintain_history')
get_maintain_history_detail = getattr(module, 'get_maintain_history_detail')
delete_t_maintain_history_maintain_history_id = getattr(module, 'delete_t_maintain_history_maintain_history_id')
get_t_maintain_history_all = getattr(module, 'get_t_maintain_history_all')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_insert_t_maintain_history_ok():
    """
    正常系: メンテナンス履歴TBL INSERT
    """
    expected_value = [
        {"gigya_uid": "test_uid_01", "user_vehicle_id": 1, "maintain_item_code": "00001", "model_code": "zzzz",
         "maintain_implement_date": datetime(2022, 10, 17, 00, 00, 00, 000), "maintain_location": "代官山モトベロ",
         "maintain_cost": 3980, "maintain_required_time": 120, "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円",
         "maintain_du_serial_number": "16777215",
         "maintain_du_last_timestamp": datetime(2022, 10, 17, 12, 34, 56, 789000), "maintain_du_last_odometer": 123,
         "maintain_image_ids": "XXXXX1, null, XXXXX2",
         "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None,
         "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False,
         "delete_timestamp": None, "delete_user_id": None,
         "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",
         "update_timestamp": None, "update_user_id": None}
    ]

    recs = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "model_code": "zzzz",
        "maintain_implement_date": "2022-10-17",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": "2022-10-17T12:34:56.789",
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXX1, null, XXXXX2"
    }
    inserted_maintain_history_id = insert_t_maintain_history(**recs)

    sql: str = '''
      SELECT * FROM t_maintain_history
      WHERE maintain_history_id = %(maintain_history_id)s;
    '''
    parameters_dict: dict = {'maintain_history_id': inserted_maintain_history_id}
    results = execute_select_statement(sql, parameters_dict)

    expected_value[0]['maintain_history_id'] = inserted_maintain_history_id
    assert results == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_t_maintain_history_ok():
    """
    正常系: メンテナンス履歴TBL UPDATE
    """
    expected_value = [
        {"maintain_history_id": 7, "gigya_uid": "test_uid_02", "user_vehicle_id": 1, "maintain_item_code": "00001",
         "model_code": "abcd", "maintain_implement_date": datetime(2022, 10, 18, 00, 00, 00, 000),
         "maintain_location": "代官山モトベロ_UPDATE", "maintain_cost": 9999, "maintain_required_time": 999,
         "maintain_memo": "メンテナンスメモ", "maintain_du_serial_number": "16777215",
         "maintain_du_last_timestamp": datetime(2022, 10, 18, 12, 34, 56, 789000), "maintain_du_last_odometer": 123,
         "maintain_image_ids": "XXXXX1,null,null",
         "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None,
         "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False,
         "delete_timestamp": None, "delete_user_id": None,
         "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",
         "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"}
    ]

    maintain_history_id = 7
    recs = {
        "maintain_implement_date": "2022-10-18",
        "maintain_location": "代官山モトベロ_UPDATE",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        # "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": "2022-10-18T12:34:56.789",
        # "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXX1,null,null"
    }
    update_t_maintain_history(7, "test_uid_02", "00001", 1, **recs)

    sql: str = '''
      SELECT * FROM t_maintain_history
      WHERE maintain_history_id = %(maintain_history_id)s;
    '''
    parameters_dict: dict = {'maintain_history_id': maintain_history_id}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


def test_update_t_maintain_history_ng_01():
    """
    異常系: メンテナンス履歴TBL UPDATE対象なし
    """
    maintain_history_id = 128

    results = update_t_maintain_history(
        maintain_history_id, "test_uid_02", "0001", 1, **{"maintain_location": "代官山モトベロ_UPDATE"})
    assert results == 0


def test_get_t_maintain_history_ok_01():
    """
    正常系: メンテナンス履歴TBL SELECT
    maintain_item_code、maintain_implement_date指定あり
    """
    expected_value = {
        'gigya_uid': 'test_uid_03',
        'maintain_cost': 9999,
        'maintain_du_last_odometer': 123,
        'maintain_du_last_timestamp': datetime(2022, 10, 11, 12, 34, 56, 789000),
        'maintain_du_serial_number': '16777215',
        'maintain_history_id': 10,
        'maintain_image_ids': 'null,null,null',
        'maintain_implement_date': datetime(2020, 10, 12, 0, 0),
        'maintain_item_code': '00002',
        'maintain_location': 'メンテナンス場所3',
        'maintain_memo': 'メンテナンスメモ',
        'maintain_required_time': 999,
        'model_code': 'abcd',
        'user_vehicle_id': 4,
    }

    gigya_uid = "test_uid_03"
    user_vehicle_id = 4
    maintain_item_code = "00002"
    maintain_implement_date = "2020-10-12"

    result = get_t_maintain_history(
        gigya_uid,
        user_vehicle_id,
        maintain_item_code,
        maintain_implement_date
    )
    assert result == expected_value


def test_get_t_maintain_history_ok_02():
    """
    正常系: メンテナンス履歴TBL SELECT
    maintain_item_code、maintain_implement_date指定なし
    """
    expected_value = {
        'gigya_uid': 'test_uid_03',
        'maintain_cost': 9999,
        'maintain_du_last_odometer': 123,
        'maintain_du_last_timestamp': datetime(2022, 10, 11, 12, 34, 56, 789000),
        'maintain_du_serial_number': '16777215',
        'maintain_history_id': 8,
        'maintain_image_ids': 'null,null,null',
        'maintain_implement_date': datetime(2020, 10, 10, 0, 0),
        'maintain_item_code': '00002',
        'maintain_location': 'メンテナンス場所',
        'maintain_memo': 'メンテナンスメモ',
        'maintain_required_time': 999,
        'model_code': 'abcd',
        'user_vehicle_id': 4,
    }

    gigya_uid = "test_uid_03"
    user_vehicle_id = 4

    result = get_t_maintain_history(
        gigya_uid,
        user_vehicle_id
    )
    assert result == expected_value


def test_get_t_maintain_history_ng():
    """
    正常系: メンテナンス履歴TBL 対象データなし
    """
    expected_value = None

    gigya_uid = "test_uid_9999"
    user_vehicle_id = 9999
    maintain_item_code = "99999"
    maintain_implement_date = "9999-09-09"

    result = get_t_maintain_history(
        gigya_uid,
        user_vehicle_id,
        maintain_item_code,
        maintain_implement_date
    )
    assert result == expected_value


def test_get_maintain_history_limit_ok_01():
    """
    正常系: メンテナンス履歴TBL SELECT
    maintain_item_code指定あり
    offset 1
    """
    expected_value = [
        {
            "maintain_history_id": 10,
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_implement_date": datetime(2020, 10, 12, 0, 0),
            "maintain_location": "メンテナンス場所3"
        },
        {
            "maintain_history_id": 9,
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_implement_date": datetime(2020, 10, 11, 0, 0),
            "maintain_location": "メンテナンス場所2"
        }
    ]

    gigya_uid = "test_uid_03"
    user_vehicle_id = 4
    maintain_item_code = "00002"
    limit = 2
    offset = 1

    result = get_maintain_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
        maintain_item_code,
    )
    assert result == expected_value


def test_get_maintain_history_limit_ok_02():
    """
    正常系: メンテナンス履歴TBL SELECT
    maintain_item_code指定なし
    """
    expected_value = [
        {
            "maintain_history_id": 12,
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_implement_date": datetime(2020, 10, 14, 0, 0),
            "maintain_location": "メンテナンス場所5"
        },
        {
            "maintain_history_id": 11,
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_implement_date": datetime(2020, 10, 13, 0, 0),
            "maintain_location": "メンテナンス場所4"
        }
    ]

    gigya_uid = "test_uid_03"
    user_vehicle_id = 4
    limit = 2
    offset = 0

    result = get_maintain_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
    )
    assert result == expected_value


def test_get_maintain_history_limit_ok_03():
    """
    正常系: メンテナンス履歴TBL SELECT
    limit:1
    """
    expected_value = [
        {
            "maintain_history_id": 12,
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_implement_date": datetime(2020, 10, 14, 0, 0),
            "maintain_location": "メンテナンス場所5"
        }
    ]

    gigya_uid = "test_uid_03"
    user_vehicle_id = 4
    limit = 1
    offset = 0

    result = get_maintain_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
    )
    assert result == expected_value


def test_get_maintain_history_limit_ng():
    """
    異常系: メンテナンス履歴TBL 対象0件
    """
    expected_value = []

    gigya_uid = "test_uid_02"
    user_vehicle_id = 4
    maintain_item_code = "0"
    limit = 3
    offset = 2

    result = get_maintain_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
        maintain_item_code,
    )
    assert result == expected_value


def test_get_maintain_history_all_count_ok_01():
    """
    正常系: メンテナンス履歴TBL全件取得
    maintain_item_code指定あり
    """
    expected_value = {'count': 4}

    gigya_uid = "test_uid_03"
    user_vehicle_id = 4
    maintain_item_code = "00002"

    result = get_maintain_history_all_count(
        gigya_uid,
        user_vehicle_id,
        maintain_item_code,
    )
    assert result == expected_value


def test_get_maintain_history_all_count_ok_02():
    """
    正常系: メンテナンス履歴TBL 全件取得
    maintain_item_code指定なし
    """
    expected_value = {'count': 5}

    gigya_uid = "test_uid_03"
    user_vehicle_id = 4

    result = get_maintain_history_all_count(
        gigya_uid,
        user_vehicle_id
    )
    assert result == expected_value


def test_get_maintain_history_all_count_ng_01():
    """
    正常系: メンテナンス履歴TBL 対象データ0件
    """
    expected_value = {'count': 0}

    gigya_uid = "test_uid_02"
    user_vehicle_id = 4
    maintain_item_code = "99999"

    result = get_maintain_history_all_count(
        gigya_uid,
        user_vehicle_id,
        maintain_item_code,
    )
    assert result == expected_value


def test_delete_t_user_setting_maintain_ok_01():
    """
    正常系: メンテナンス履歴TBL delete
    """
    expected_value = []
    gigya_uid = "test_uid_03"
    user_vehicle_id = 4

    delete_t_maintain_history(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_maintain_history
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_user_setting_maintain_ng_01():
    """
    異常系: メンテナンス履歴TBL delete
    対象データなし
    """
    expected_value = []
    gigya_uid = "test_uid_99"
    user_vehicle_id = "999999999"

    delete_t_maintain_history(gigya_uid, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_maintain_history
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
      '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_99', 'user_vehicle_id': "999999999"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_get_maintain_history_detail_ok():
    """
    正常系: メンテナンス履歴TBL SELECT
    """
    expected_value = {
        "maintain_history_id": 9,
        "user_vehicle_id": 4,
        "maintain_item_code": "00002",
        "model_code": "abcd",
        "maintain_item_name": "タイヤ空気圧",
        "maintain_implement_date": datetime(2020, 10, 11, 0, 0),
        "maintain_location": "メンテナンス場所2",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": datetime(2022, 10, 11, 12, 34, 56, 789000),
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,null"
    }
    result = get_maintain_history_detail('test_uid_03', 9, 4)
    assert result == expected_value


def test_get_maintain_history_detail_ng():
    """
    異常系: メンテナンス履歴TBL SELECT対象なし
    """
    result = get_maintain_history_detail('test_uid_03', 1, 9)
    assert result is None


def test_delete_t_maintain_history_maintain_history_id_ok_01():
    """
    正常系: メンテナンス履歴TBL delete
    """
    expected_value = []
    gigya_uid = "test_uid_02"
    user_vehicle_id = 1
    maintain_history_id = 1

    delete_t_maintain_history_maintain_history_id(gigya_uid, maintain_history_id, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_maintain_history
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s
        AND maintain_history_id = %(maintain_history_id)s;
      '''
    parameters_dict: dict = {'gigya_uid': gigya_uid, 'maintain_history_id': maintain_history_id, 'user_vehicle_id': user_vehicle_id}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_maintain_history_maintain_history_id_ng_01():
    """
    異常系: メンテナンス履歴TBL delete
    対象データなし
    """
    expected_value = []
    gigya_uid = "test_uid_99"
    user_vehicle_id = 999999999
    maintain_history_id = 99

    delete_t_maintain_history_maintain_history_id(gigya_uid, maintain_history_id, user_vehicle_id)

    sql: str = '''
        SELECT * FROM t_maintain_history
        WHERE user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s
        AND maintain_history_id = %(maintain_history_id)s;
      '''
    parameters_dict: dict = {'gigya_uid': gigya_uid, 'maintain_history_id': maintain_history_id, 'user_vehicle_id': user_vehicle_id}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_get_t_maintain_history_all_ok():
    """
    正常系: メンテナンス履歴TBL SELECT
    """
    expected_value = [
        {
            "gigya_uid": "test_uid_02",
            "maintain_image_ids": "test1,test2,test3",
        },
        {
            "gigya_uid": "test_uid_02",
            "maintain_image_ids": "test1,test2,test3",
        },
        {
            "gigya_uid": "test_uid_02",
            "maintain_image_ids": "test1,test2,test3",
        },
        {
            "gigya_uid": "test_uid_02",
            "maintain_image_ids": "test1,test2,test3",
        },
        {
            "gigya_uid": "test_uid_02",
            "maintain_image_ids": "test1,test2,test3",
        },
        {
            "gigya_uid": "test_uid_02",
            "maintain_image_ids": "test1,test2,test3",
        },
        {
            "gigya_uid": "test_uid_02",
            "maintain_image_ids": "null,null,null",
        },
        {
            "gigya_uid": "test_uid_03",
            "maintain_image_ids": "null,null,null",
        },
        {
            "gigya_uid": "test_uid_03",
            "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,null",
        },
        {
            "gigya_uid": "test_uid_03",
            "maintain_image_ids": "null,null,null",
        },
        {
            "gigya_uid": "test_uid_03",
            "maintain_image_ids": "null,null,null",
        },
        {
            "gigya_uid": "test_uid_03",
            "maintain_image_ids": "null,null,null",
        }
    ]
    result = get_t_maintain_history_all()
    assert result == expected_value
