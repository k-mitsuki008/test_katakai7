import json
from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles_maintenances_histories_detail.delete_handler')
put_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 メンテナンス記録削除API
    Mock化あり
    """
    # 入力データ
    path_parameters = {
        "maintain_history_id": "1",
        "user_vehicle_id": "123",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/vehicles/123/maintenances/histories/1'
    )
    context = {}

    # service.user_vehicle_service.user_vehicle_id_is_existのモック化
    mocker.patch("service.user_vehicle_service.user_vehicle_id_is_exist", return_value={})
    # service.maintain_history_service.delete_maintain_historyのモック化
    mocker.patch("service.maintain_history_service.delete_maintain_history", return_value=1)
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "maintain_history_id": 1,
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02():
    """
    正常系 メンテナンス記録削除API
    Mock化なし
    """
    # 入力データ
    path_parameters = {
        "maintain_history_id": "12",
        "user_vehicle_id": "4",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_03',
        path='/vehicles/12/maintenances/histories/4'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "maintain_history_id": 12,
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01():
    """
    準正常系 メンテナンス記録削除API
    バリデーションチェック 必須入力項目チェック
    """
    # 入力データ
    input_body = {
        "maintain_history_id": None,
        "user_vehicle_id": None
    }
    path_parameters = {
        "maintain_history_id": "",
        "user_vehicle_id": ""
    }
    event = get_event(
        body=input_body,
        path_parameters=path_parameters,
        gigya_uid='test_uid_03',
        path='/vehicles/1/maintenances/histories/1'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_history_id",
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

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_02():
    """
    準正常系 メンテナンス記録削除API
    バリデーションチェック 空文字チェック
    """
    # 入力データ
    input_body = {
        "maintain_history_id": "",
        "user_vehicle_id": ""
    }
    path_parameters = {
        "maintain_history_id": "",
        "user_vehicle_id": ""
    }
    event = get_event(
        body=input_body,
        path_parameters=path_parameters,
        gigya_uid='test_uid_03',
        path='/vehicles/1/maintenances/histories/1'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_history_id",
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

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_03():
    """
    準正常系 メンテナンス記録削除API
    バリデーションチェック 型チェック
    """
    # 入力データ
    path_parameters = {
        "maintain_history_id": "NG",
        "user_vehicle_id": "NG"
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_03',
        path='/vehicles/1/maintenances/histories/1'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_history_id",
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

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_04():
    """
    異常系 メンテナンス記録削除API
    ユーザ車両ID存在チェックNG
    """
    # 入力データ
    path_parameters = {
        "maintain_history_id": "123",
        "user_vehicle_id": "999"
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_03',
        path='/vehicles/999/maintenances/histories/123'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E042",
            "message": "ユーザ車両IDが存在しません。",
            "validationErrors": None
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 400
    assert body == expected_value
