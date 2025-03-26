import json

from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.ride_detail.get_handler')
post_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ライド詳細取得
    Mock化あり
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

    # device.service.get_ride_historyのモック化
    mocker.patch(
        "service.ride_history_service.get_ride_history",
        return_value={
            "ride_history_id": "1212022-10-06T15:30:31.000",
            "start_timestamp": "2022-09-01T05:30:31.000",
            "end_timestamp": "2022-09-01T15:30:31.000",
            "ride_name": "XXXXXXX",
            "trip_distance": 1234.5,
            "trip_time": 3600,
            "total_calorie": 535,
            "battery_consumption": 72,
            "average_speed": 15,
            "max_speed": 20,
            "max_pedaling_power": 6,
            "max_cadence": 126,
            "bookmark_flg": False,
        }
    )

    # device.service.upsert_ride_historyのモック化
    mocker.patch(
        "service.ride_track_service.get_ride_track",
        return_value=[
            {
                "track_id": 1,
                "latitude": 35.675069,
                "longitude": 139.763328
            },
            {
                "track_id": 2,
                "latitude": 35.665498,
                "longitude": 139.75964
            }
        ]
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "ride_history_id": "1212022-10-06T15:30:31.000",
        "start_timestamp": "2022-09-01T05:30:31.000",
        "end_timestamp": "2022-09-01T15:30:31.000",
        "ride_name": "XXXXXXX",
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max_speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "bookmark_flg": False,
        "ride_tracks": [
            {
                "track_id": 1,
                "latitude": 35.675069,
                "longitude": 139.763328
            },
            {
                "track_id": 2,
                "latitude": 35.665498,
                "longitude": 139.75964
            }
        ]
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02():
    """
    正常系 ライド詳細取得
    Mock化なし
    """
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

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "ride_history_id": "1212022-10-06T15:30:31.000",
        "start_timestamp": "2022-12-12T12:12:12.610Z",
        "end_timestamp": "2022-12-12T12:12:12.610Z",
        "ride_name": "ユーザー車両名のライド",
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max_speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "bookmark_flg": False,
        "ride_tracks": [
            {
                "track_id": 1,
                "latitude": 35.67506,
                "longitude": 139.763328
            },
            {
                "track_id": 2,
                "latitude": 36.67506,
                "longitude": 138.763328
            },
            {
                "track_id": 3,
                "latitude": 37.67506,
                "longitude": 137.763328
            }
        ]
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    準正常系 ライド詳細取得
    バリデーションチェック
    ライド履歴ID：必須項目エラー
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )
    # 入力データ
    input_body = {
        "ride_history_id": None
    }
    path_parameters = {
        "ride_history_id": "123",
    }
    event = get_event(
        body=input_body,
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/rides/1212022-10-06T15:30:31.000'
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
                    "field": "ride_history_id",
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


def test_handler_ng_02(mocker):
    """
    準正常系 ライド詳細取得
    バリデーションチェック
    ライド履歴ID：空文字チェック
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )
    # 入力データ
    input_body = {
        "ride_history_id": ""
    }
    path_parameters = {
        "ride_history_id": "",
    }
    event = get_event(
        body=input_body,
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/rides/1212022-10-06T15:30:31.000'
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
                    "field": "ride_history_id",
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


def test_handler_ng_03(mocker):
    """
    準正常系 ライド詳細取得
    バリデーションチェック
    ライド履歴ID：文字列チェック
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )
    # 入力データ
    input_body = {
        "ride_history_id": 123
    }
    path_parameters = {
        "ride_history_id": "123",
    }
    event = get_event(
        body=input_body,
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/rides/1212022-10-06T15:30:31.000'
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
                    "field": "ride_history_id",
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


def test_handler_ng_04(mocker):
    """
    準正常系 ライド詳細取得
    バリデーションチェック
    ライド履歴ID：型確認エラー
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )
    # 入力データ
    input_body = {
        "ride_history_id": 999999999
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path_parameters={'ride_history_id': '1'},
        path='/rides/1212022-10-06T15:30:31.000'
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
                    "field": "ride_history_id",
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
