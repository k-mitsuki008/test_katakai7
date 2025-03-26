from datetime import datetime
import json
from importlib import import_module, reload
from tests.test_utils.utils import get_event
from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles_bluetooth.post_handler')
post_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系　bluetooth接続切断API
    Mock化あり
    """
    # 入力データ
    input_body = {
        "du_serial_number": "16777215",
        "timestamp": "2022-10-06T15:30:31.000Z",
        "du_odometer": 120
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'user_vehicle_id': '1'}, path='/vehicles/1/bluetooth')
    context = {}

    # service.drive_unit_history_service.registration_drive_unit_history のモック化
    mocker.patch("service.drive_unit_history_service.registration_drive_unit_history", return_value=None)
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 1,
        "du_serial_number": "16777215",
        "du_odometer": 120
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02():
    """
    正常系　bluetooth接続切断API
    Mock化なし
    """
    # 入力データ
    input_body = {
        "du_serial_number": "16777215",
        "timestamp": "2022-10-06T15:30:31.000Z",
        "du_odometer": 120
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'user_vehicle_id': '1'}, path='/vehicles/1/bluetooth')
    context = {}
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 1,
        "du_serial_number": "16777215",
        "du_odometer": 120
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    異常系 bluetooth接続切断API
    ドライブユニット変更時のドライブユニット履歴追加時にエラー発生 → ドライブユニット履歴が更新前にロールバックされること
    """
    # 入力データ
    input_body = {
        "du_serial_number": "16777215",
        "timestamp": "2022-10-06T15:30:31.000Z",
        "du_odometer": 120
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'user_vehicle_id': '1'}, path='/vehicles/1/bluetooth')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E001",
            "message": "システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。",
            "validationErrors": None
        }
    }

    # repository.drive_unit_history_repository.insert_t_drive_unit_history でエラー発生
    mocker.patch("repository.drive_unit_history_repository.insert_t_drive_unit_history", side_effect=Exception)
    reload(module)

    response = post_handler(event, context)

    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 500
    assert body == expected_value

    # ユーザ車両TBLが更新前にロールバックされることを確認。
    expected_value = [
        {"user_vehicle_id": 1, "du_first_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "du_last_timestamp": datetime(9999, 12, 31, 23, 59, 59, 999000), "gigya_uid": "test_uid_02", "du_serial_number": "000011", "du_first_odometer": 30, "du_last_odometer": 30,
         "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01", "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_01"}
    ]
    sql: str = '''
      SELECT * FROM t_drive_unit_history
      WHERE 
        user_vehicle_id = %(user_vehicle_id)s 
        AND du_last_timestamp = to_timestamp('9999/12/31 23:59:59.999', 'YYYY/MM/DD HH24:MI:SS.MS');
    '''
    parameters_dict: dict = {'user_vehicle_id': 1}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


def test_handler_ng_02():
    """
    異常系 bluetooth接続切断API
    バリデーションチェック(必須項目チェック)
    """
    # 入力データ
    input_body = {
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={}, path='/vehicles//bluetooth')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E006",
                    "field": "du_odometer",
                    "message": "missing field"
                },
                {
                    "code": "E006",
                    "field": "du_serial_number",
                    "message": "missing field"
                },
                {
                    "code": "E006",
                    "field": "timestamp",
                    "message": "missing field"
                },
                {
                    "code": "E006",
                    "field": "user_vehicle_id",
                    "message": "missing field"
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_03():
    """
    異常系 bluetooth接続切断API
    バリデーションチェック
    ユーザ車両ID：整数値チェック
    DU識別子：半角英数字チェック
    タイムスタンプ	：日時チェック
    DU接続Odometer：整数値チェック
    """
    # 入力データ
    input_body = {
        "du_serial_number": "テスト",
        "timestamp": "2022-10-06 15:30:31.000",
        "du_odometer": "NG"
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': 'NG'}, path='/vehicles/123/bluetooth')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "du_odometer",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "du_serial_number",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "user_vehicle_id",
                    "message": "validation error"
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_04():
    """
    異常系 bluetooth接続切断API
    バリデーションチェック(文字数不足)
    """
    # 入力データ
    input_body = {
        "du_serial_number": "",
        "timestamp": "2022-10-06T15:30:31.000Z",
        "du_odometer": 120,
        "user_vehicle_id": 1234
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={}, path='/vehicles//bluetooth')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "du_serial_number",
                    "message": "validation error"
                }
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_05():
    """
    異常系 bluetooth接続切断API
    バリデーションチェック(文字数超過)
    """
    # 入力データ
    input_body = {
        "du_serial_number": "111111111122222222223333333333444444444455555555551",
        "timestamp": "2022-10-06T15:30:31.000Z",
        "du_odometer": 120,
        "user_vehicle_id": 1234
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={}, path='/vehicles//bluetooth')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "du_serial_number",
                    "message": "validation error"
                }
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_06():
    """
    異常系 bluetooth接続切断API
    バリデーションチェック(空文字チェック)
    """
    # 入力データ
    input_body = {
        "du_serial_number": "",
        "timestamp": "",
        "du_odometer": ""
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': ''}, path='/vehicles/123/bluetooth')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "du_odometer",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "du_serial_number",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "user_vehicle_id",
                    "message": "validation error"
                }
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_07():
    """
    異常系 bluetooth接続切断API
    バリデーションチェック(文字列チェック)
    """
    # 入力データ
    input_body = {
        "du_serial_number": 1,
        "timestamp": 20221010151031000,
        "du_odometer": 120
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': '123'}, path='/vehicles/123/bluetooth')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "du_serial_number",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "timestamp",
                    "message": "validation error"
                }
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
