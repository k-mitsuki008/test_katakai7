import json

from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.ride_detail.delete_handler')
delete_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ライド詳細削除API
    モック化あり
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )
    # 入力データ
    path_parameters = {
        "ride_history_id": "1212022-10-06T15:30:31.000",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/rides/1212022-10-06T15:30:31.000'
    )

    context = {}

    # device.service.delete_ride_historyのモック化
    mocker.patch(
        "service.ride_history_service.delete_ride_history",
        return_value=None
    )

    # device.service.delete_ride_trackのモック化
    mocker.patch(
        "service.ride_track_service.delete_ride_track",
        return_value=None
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "ride_history_id": "1212022-10-06T15:30:31.000"
    }

    response = delete_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02():
    """
    正常系 ライド詳細削除API
    モック化無し
    """
    # 入力データ
    path_parameters = {
        "ride_history_id": "1232022-10-06T15:30:31.000",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/rides/1232022-10-06T15:30:31.000'
    )

    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "ride_history_id": "1232022-10-06T15:30:31.000",
    }

    response = delete_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    準正常系 ライド詳細削除
    バリデーションチェック
    ライド履歴ID: 型確認
    """
    # 入力データ
    input_body = {
        "ride_history_id": 999999999
    }

    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'ride_history_id': '1'},
                      path='/rides')
    context = {}

    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "ride_history_id",
                    "message": "validation error"
                }
            ]
        }
    }

    response = delete_handler(event, context)
    status_code = response["statusCode"]
    body = json.loads(response["body"])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_02(mocker):
    """
    準正常系 ライド詳細削除
    バリデーションチェック
    ライド履歴ID: 必須項目エラー
    """
    # 入力データ
    input_body = {
        "ride_history_id": ""
    }

    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'ride_history_id': '1'},
                      path='/rides')
    context = {}

    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "ride_history_id",
                    "message": "validation error"
                }
            ]
        }
    }

    response = delete_handler(event, context)
    status_code = response["statusCode"]
    body = json.loads(response["body"])
    assert status_code == 422
    assert body == expected_value
