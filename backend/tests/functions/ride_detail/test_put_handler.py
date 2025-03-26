import json

from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.ride_detail.put_handler')
put_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ライド詳細更新API
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )
    # 入力データ
    input_data = {
        "ride_name": "YYYYYYY",
        "bookmark_flg": True
    }
    path_parameters = {
        "ride_history_id": "1212022-10-06T15:30:31.000",
    }
    event = get_event(
        body=input_data,
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/rides/1212022-10-06T15:30:31.000'
    )

    context = {}

    # device.service.update_ride_historyのモック化
    mocker.patch(
        "service.ride_history_service.update_ride_history",
        return_value={
            "ride_history_id": "1212022-10-06T15:30:31.000",
            "ride_name": "YYYYYYY",
            "bookmark_flg": True,
        }
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "ride_history_id": "1212022-10-06T15:30:31.000",
        "ride_name": "YYYYYYY",
        "bookmark_flg": True,
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02():
    """
    正常系 ライド詳細更新API
    Mock化なし
    """
    # 入力データ
    input_data = {
        "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": True
    }
    path_parameters = {
        "ride_history_id": "1202022-10-06T15:30:31.000",
    }
    event = get_event(
        body=input_data,
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/rides/1202022-10-06T15:30:31.000'
    )

    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "ride_history_id": "1202022-10-06T15:30:31.000",
        "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": True,
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_03():
    """
    正常系 ライド詳細更新API
    Mock化なし
    inputデータなし
    """
    # 入力データ
    path_parameters = {
        "ride_history_id": "1202022-10-06T15:30:31.000",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/rides/1202022-10-06T15:30:31.000'
    )

    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "ride_history_id": "1202022-10-06T15:30:31.000",
        "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": False,
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    準正常系 ライド詳細更新API
    バリデーションチェック
    ライド履歴ID：必須項目エラー
    お気に入りフラグ：Boolean型以外の場合
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )
    # 入力データ
    input_data = {
        "bookmark_flg": "あいうえお",
    }
    event = get_event(
        body=input_data,
        gigya_uid='test_uid_01',
        path='/rides/1222023-01-22T15:30:31.000'
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
                    "field": "bookmark_flg",
                    "message": "validation error"
                },
                {
                    "code": "E006",
                    "field": "ride_history_id",
                    "message": "missing field"
                },
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value
