import json

from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.rides.post_handler')
post_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ユーザーライドデータ送信API
    Mock化あり
    """
    # 入力データ
    input_body = {
        "start_timestamp": "2022-10-06T15:30:31.000Z",
        "end_timestamp": "2022-09-01T15:30:31.000Z",
        "user_vehicle_id": 123,
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max_speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "ride_tracks": [
            {
                "track_id": 1,
                "latitude": 35.67506,
                "longitude": 139.763328
            },
            {
                "track_id": 2,
                "latitude": 35.665498,
                "longitude": 139.759649
            }
        ]
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
    )

    context = {}

    # device.service.get_user_vehicleのモック化
    mocker.patch(
        "service.user_vehicle_service.get_user_vehicle",
        return_value={
            'user_vehicle_id': 123,
            'gigya_uid': 'test_uid_01',
            'model_code': 'abcd',
            'vehicle_id': 'abcd-0000001',
            'vehicle_name': 'ユーザー指定車両名02-01',
            'managed_flag': True,
            'registered_flag': True,
            'peripheral_identifier': 'switch-02-01'
        }
    )

    # device.service.upsert_ride_historyのモック化
    mocker.patch(
        "service.ride_history_service.upsert_ride_history",
        return_value={
            "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02():
    """
    正常系 ユーザーライドデータ送信API
    Mock化なし
    """
    # 入力データ
    input_body = {
        "start_timestamp": "2022-12-25T12:12:12.610Z",
        "end_timestamp": "2022-12-25T12:12:12.610Z",
        "user_vehicle_id": 121,
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max_speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "ride_tracks": [
            {
                "track_id": 1,
                "latitude": 35.67506,
                "longitude": 139.763328
            },
            {
                "track_id": 2,
                "latitude": 35.665498,
                "longitude": 139.759649
            }
        ]
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
    )
    context = {}
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "ride_history_id": "1212022-12-25T12:12:12.610Z",
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    準正常系 ユーザーライドデータ送信API
    バリデーションチェック
    ライド開始タイムスタンプ：必須項目エラー
    ユーザ車両ID：必須項目エラー
    ライド距離：必須項目エラー
    ライド時間：必須項目エラー
    消費カロリー：必須項目エラー
    バッテリー消費量：必須項目エラー
    平均車速 ：必須項目エラー
    最大車速 ：必須項目エラー
    最大ペダリングパワー：必須項目エラー
    最大ケイデンス：必須項目エラー
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 入力データ
    input_body = {
        "start_timestamp": None,
        "end_timestamp": None,
        "user_vehicle_id": None,
        "trip_distance": None,
        "trip_time": None,
        "total_calorie": None,
        "battery_consumption": None,
        "average_speed": None,
        "max_speed": None,
        "max_pedaling_power": None,
        "max_cadence":  None,
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
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
                    "field": "average_speed",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "battery_consumption",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "max_cadence",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "max_pedaling_power",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "max_speed",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "start_timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "total_calorie",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "trip_distance",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "trip_time",
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


def test_handler_ng_02(mocker):
    """
    準正常系 ユーザーライドデータ送信API
    バリデーションチェック
    ライド開始タイムスタンプ：timestamp型以外が入力された場合
    ライド終了タイムスタンプ：timestamp型以外が入力された場合
    ユーザ車両ID：半角数字以外が入力された場合
    ライド距離：半角数字以外が入力された場合
    ライド時間：半角数字以外が入力された場合
    消費カロリー：半角数字以外が入力された場合
    バッテリー消費量：半角数字以外が入力された場合
    平均車速 ：半角数字以外が入力された場合
    最大車速 ：半角数字以外が入力された場合
    最大ペダリングパワー：半角数字以外が入力された場合
    最大ケイデンス：半角数字以外が入力された場合
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 入力データ
    input_body = {
        "start_timestamp": "あいうえお",
        "end_timestamp": "あいうえお",
        "user_vehicle_id": "あいうえお",
        "trip_distance": "あいうえお",
        "trip_time": "あいうえお",
        "total_calorie": "あいうえお",
        "battery_consumption": "あいうえお",
        "average_speed": "あいうえお",
        "max_speed": "あいうえお",
        "max_pedaling_power": "あいうえお",
        "max_cadence":  "あいうえお",
        "ride_tracks": "あいうえお",
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
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
                    "field": "average_speed",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "battery_consumption",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "end_timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "max_cadence",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "max_pedaling_power",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "max_speed",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "ride_tracks",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "start_timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "total_calorie",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "trip_distance",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "trip_time",
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


def test_handler_ng_03(mocker):
    """
    準正常系 ユーザーライドデータ送信API
    バリデーションチェック
    ライド開始タイムスタンプ：空文字エラー
    ユーザ車両ID：空文字エラー
    ライド距離：空文字エラー
    ライド時間：空文字エラー
    消費カロリー：空文字エラー
    バッテリー消費量：空文字エラー
    平均車速 ：空文字エラー
    最大車速 ：空文字エラー
    最大ペダリングパワー：空文字エラー
    最大ケイデンス：空文字エラー
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 入力データ
    input_body = {
        "start_timestamp": "",
        "end_timestamp": "",
        "user_vehicle_id": "",
        "trip_distance": "",
        "trip_time": "",
        "total_calorie": "",
        "battery_consumption": "",
        "average_speed": "",
        "max_speed": "",
        "max_pedaling_power": "",
        "max_cadence":  "",
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
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
                    "field": "average_speed",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "battery_consumption",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "max_cadence",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "max_pedaling_power",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "max_speed",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "start_timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "total_calorie",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "trip_distance",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "trip_time",
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


def test_handler_ng_04(mocker):
    """
    準正常系 ユーザーライドデータ送信API
    バリデーションチェック
    ライド開始タイムスタンプ：文字列チェック
    ライド終了タイムスタンプ：文字列チェック
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 入力データ
    input_body = {
        "start_timestamp": 1234,
        "end_timestamp": 1234,
        "user_vehicle_id": 123,
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max_speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "ride_tracks": [
            {
                "track_id": 1,
                "latitude": 35.67506,
                "longitude": 139.763328
            },
            {
                "track_id": 2,
                "latitude": 35.665498,
                "longitude": 139.759649
            }
        ]
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
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
                    "field": "end_timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "start_timestamp",
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
