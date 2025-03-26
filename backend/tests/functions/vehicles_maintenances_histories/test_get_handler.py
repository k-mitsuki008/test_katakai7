import json

from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles_maintenances_histories.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 メンテナンス履歴一覧取得API
    Mock化あり
    """
    # 入力データ
    input_body = {}
    query_string_parameters = {
        "maintain_item_code": "00001",
        "limit": '2',
        "offset": '0'
    }
    path_parameters = {
        'user_vehicle_id': '1'
    }
    event = get_event(
        query_string_parameters=query_string_parameters,
        path_parameters=path_parameters,
        body=input_body,
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories?maintenance_item_code=00001&limit=2&offset=0'
    )
    context = {}

    # device.service.get_history_limitのモック化
    mocker.patch(
        "service.maintain_history_service.get_history_limit",
        return_value={
            "end_of_data": False,
            "maintain_histories": [
                {
                    "maintain_history_id": 1,
                    "maintain_item_code": "00001",
                    "maintain_item_name": "タイヤの空気圧",
                    "maintain_implement_date": "2022-06-23",
                    "maintain_location": "ル・サイクル仙台店"
                },
                {
                    "maintain_history_id": 2,
                    "maintain_item_code": "00001",
                    "maintain_item_name": "タイヤの空気圧",
                    "maintain_implement_date": "2022-06-15",
                    "maintain_location": "ル・サイクル仙台店"
                },
            ]
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # device.service.user_vehicle_id_is_existのモック化
    mocker.patch(
        "service.user_vehicle_service.user_vehicle_id_is_exist",
        return_value=True
    )

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "end_of_data": False,
        "maintain_histories": [
            {
                "maintain_history_id": 1,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-23",
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 2,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-15",
                "maintain_location": "ル・サイクル仙台店"
            },
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02(mocker):
    """
    正常系 メンテナンス履歴一覧取得API
    Mock化あり
    maintain_item_code指定なし
    """
    # 入力データ
    input_body = {}
    query_string_parameters = {
        "limit": '2',
        "offset": '0'
    }
    path_parameters = {
        'user_vehicle_id': '1'
    }
    event = get_event(
        query_string_parameters=query_string_parameters,
        path_parameters=path_parameters,
        body=input_body,
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories?limit=2&offset=0'
    )
    context = {}

    # device.service.get_history_limitのモック化
    mocker.patch(
        "service.maintain_history_service.get_history_limit",
        return_value={
            "end_of_data": False,
            "maintain_histories": [
                {
                    "maintain_history_id": 1,
                    "maintain_item_code": "00001",
                    "maintain_item_name": "タイヤの空気圧",
                    "maintain_implement_date": "2022-06-23",
                    "maintain_location": "ル・サイクル仙台店"
                },
                {
                    "maintain_history_id": 2,
                    "maintain_item_code": "00001",
                    "maintain_item_name": "タイヤの空気圧",
                    "maintain_implement_date": "2022-06-15",
                    "maintain_location": "ル・サイクル仙台店"
                }
            ]
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # device.service.user_vehicle_id_is_existのモック化
    mocker.patch(
        "service.user_vehicle_service.user_vehicle_id_is_exist",
        return_value=True
    )

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "end_of_data": False,
        "maintain_histories": [
            {
                "maintain_history_id": 1,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-23",
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 2,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-15",
                "maintain_location": "ル・サイクル仙台店"
            }
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_03():
    """
    正常系 メンテナンス履歴一覧取得API
    Mock化なし
    """
    # 入力データ
    input_body = {}
    query_string_parameters = {
        "maintain_item_code": "00002",
        "limit": '2',
        "offset": '2'
    }
    path_parameters = {
        'user_vehicle_id': '4'
    }
    event = get_event(
        query_string_parameters=query_string_parameters,
        path_parameters=path_parameters,
        body=input_body,
        gigya_uid='test_uid_03',
        path='/vehicles/1/maintenances/histories?maintenance_item_code=00002&limit=2&offset=0'
    )
    context = {}

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "end_of_data": True,
        "maintain_histories": [
            {
                "maintain_history_id": 9,
                "maintain_item_code": "00002",
                "maintain_item_name": "タイヤ空気圧",
                "maintain_implement_date": "2020-10-11",
                "maintain_location": "メンテナンス場所2"
            },
            {
                "maintain_history_id": 8,
                "maintain_item_code": "00002",
                "maintain_item_name": "タイヤ空気圧",
                "maintain_implement_date": "2020-10-10",
                "maintain_location": "メンテナンス場所"
            },
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_04():
    """
    正常系 メンテナンス履歴一覧取得API
    Mock化なし
    maintain_item_code指定なし
    """
    # 入力データ
    input_body = {}
    query_string_parameters = {
        "limit": '2',
        "offset": '0'
    }
    path_parameters = {
        'user_vehicle_id': '4'
    }
    event = get_event(
        query_string_parameters=query_string_parameters,
        path_parameters=path_parameters,
        body=input_body,
        gigya_uid='test_uid_03',
        path='/vehicles/1/maintenances/histories?limit=2&offset=3'
    )
    context = {}

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "end_of_data": False,
        "maintain_histories": [
            {
                "maintain_history_id": 12,
                "maintain_item_code": "00003",
                "maintain_item_name": "タイヤ摩耗",
                "maintain_implement_date": "2020-10-14",
                "maintain_location": "メンテナンス場所5"
            },
            {
                "maintain_history_id": 11,
                "maintain_item_code": "00002",
                "maintain_item_name": "タイヤ空気圧",
                "maintain_implement_date": "2020-10-13",
                "maintain_location": "メンテナンス場所4"
            },
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01():
    """
    準正常系 メンテナンス履歴一覧取得API
    バリデーションチェック 必須項目
    ユーザー車両ID : 必須項目エラー
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": None
    }
    event = get_event(body=input_body, gigya_uid="test_uid2", path='/vehicles/1/maintenances/histories')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "user_vehicle_id",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_02():
    """
    準正常系 メンテナンス履歴一覧取得API
    バリデーションチェック 型確認
    ユーザー車両ID : int型以外が入力された場合
    メンテナンスアイテムCD : string型以外が入力された場合
    上限 : int型以外が入力された場合
    開始位置: int型以外が入力された場合
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": "test",
        "maintain_item_code": int("00005"),
        "limit": "test",
        "offset": "test"
                  }
    event = get_event(body=input_body, gigya_uid="test_uid2", path='/vehicles/1/maintenances/histories')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "limit",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "offset",
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

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_03():
    """
    準正常系 メンテナンス履歴一覧取得API
    バリデーションチェック 空文字チェック
    ユーザー車両ID : 空文字入力エラー
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": "",
        "maintain_item_code": "",
        "limit": "",
        "offset": ""
    }
    event = get_event(body=input_body, gigya_uid="test_uid2",
                      path='/vehicles/1/maintenances/histories')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "user_vehicle_id",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_04():
    """
    準正常系 メンテナンス履歴一覧取得API
    バリデーションチェック 文字数超過
    メンテナンスアイテムCD : 文字数が6文字以上の場合
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": 5,
        "maintain_item_code": "000005"
    }
    event = get_event(body=input_body, gigya_uid="test_uid2",
                      path='/vehicles/1/maintenances/histories')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_05():
    """
    準正常系 メンテナンス履歴一覧取得API
    バリデーションチェック 文字数不足
    メンテナンスアイテムCD : 文字数が4文字以下の場合
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": 5,
        "maintain_item_code": "0005"
    }
    event = get_event(body=input_body, gigya_uid="test_uid2",
                      path='/vehicles/1/maintenances/histories')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_06():
    """
    準正常系 メンテナンス履歴一覧取得API
    バリデーションチェック 半角数字チェック
    メンテナンスアイテムCD : 半角数字以外が入力された場合
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": 5,
        "maintain_item_code": "００００５"
    }
    event = get_event(body=input_body, gigya_uid="test_uid2",
                      path='/vehicles/1/maintenances/histories')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
