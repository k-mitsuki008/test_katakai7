import json
import pytest

from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.rides.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ライド一覧取得API
    Mock化あり
    """
    # 入力データ
    input_body = {}
    query_string_parameters = {
        "begin": "2022-09-01T09:00:00.000Z",
        "end": "2022-09-30T09:00:00.000Z",
        "bookmark_flg": 'True',
        "limit": '30',
        "offset": '0'
    }
    event = get_event(
        query_string_parameters=query_string_parameters,
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
    )
    context = {}

    # device.service.get_history_limitのモック化
    mocker.patch(
        "service.ride_history_service.get_history_limit",
        return_value={
            "end_of_data": False,
            "ride_histories": [
                {
                    "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                    "start_timestamp": "2022-09-01T05:18:30.000Z",
                    "end_timestamp": "2022-09-01T15:30:31.000Z",
                    "ride_name": "XXXXXXX",
                    "trip_distance": 1234.5,
                    "trip_time": 3600,
                    "bookmark_flg": True
                },
                {
                    "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                    "start_timestamp": "2022-10-01T14:18:30.000Z",
                    "end_timestamp": "2022-10-01T15:30:31.000Z",
                    "ride_name": "YYYYYYY",
                    "trip_distance": 999.9,
                    "trip_time": 72000,
                    "bookmark_flg": False
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

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "end_of_data": False,
        "ride_histories": [
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": "2022-09-01T05:18:30.000Z",
                "end_timestamp": "2022-09-01T15:30:31.000Z",
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": True
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": "2022-10-01T14:18:30.000Z",
                "end_timestamp": "2022-10-01T15:30:31.000Z",
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": False
            }
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


@pytest.mark.freeze_time("2022-10-1 12:34:56.789101")
def test_handler_ok_02(mocker):
    """
    正常系 ライド一覧取得API
    Mock化あり
    begin,end,bookmark_flg指定なし
    """
    # 入力データ
    input_body = {}
    query_string_parameters = {
        "limit": '30',
        "offset": '0'
    }
    event = get_event(
        query_string_parameters=query_string_parameters,
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
    )
    context = {}

    # device.service.get_history_limitのモック化
    mocker.patch(
        "service.ride_history_service.get_history_limit",
        return_value={
            "end_of_data": False,
            "ride_histories": [
                {
                    "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                    "start_timestamp": "2022-09-01T05:18:30.000",
                    "end_timestamp": "2022-09-01T15:30:31.000",
                    "ride_name": "XXXXXXX",
                    "trip_distance": 1234.5,
                    "trip_time": 3600,
                    "bookmark_flg": True
                },
                {
                    "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                    "start_timestamp": "2022-10-01T14:18:30.000",
                    "end_timestamp": "2022-10-01T15:30:31.000",
                    "ride_name": "YYYYYYY",
                    "trip_distance": 999.9,
                    "trip_time": 72000,
                    "bookmark_flg": False
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

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "end_of_data": False,
        "ride_histories": [
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": "2022-09-01T05:18:30.000",
                "end_timestamp": "2022-09-01T15:30:31.000",
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": True
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": "2022-10-01T14:18:30.000",
                "end_timestamp": "2022-10-01T15:30:31.000",
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": False
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
    正常系 ライド一覧取得API
    Mock化なし
    """
    # 入力データ
    input_body = {}
    query_string_parameters = {
        "begin": "2022-12-05T09:00:00.000Z",
        "end": "2022-12-10T09:00:00.000Z",
        "bookmark_flg": 'False',
        "limit": '2',
        "offset": '3'
    }
    event = get_event(
        query_string_parameters=query_string_parameters,
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
    )
    context = {}

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "end_of_data": True,
        "ride_histories": [
            {
                "ride_history_id": "1262022-10-06T15:30:31.000",
                "start_timestamp": "2022-12-06T12:12:12.610Z",
                "end_timestamp": "2022-12-06T12:12:12.610Z",
                "ride_name": "ユーザー車両名のライド",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": False
            },
            {
                "ride_history_id": "1252022-10-06T15:30:31.000",
                "start_timestamp": "2022-12-05T12:12:12.610Z",
                "end_timestamp": "2022-12-05T12:12:12.610Z",
                "ride_name": "ユーザー車両名のライド",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": False
            },
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


@pytest.mark.freeze_time("2022-12-19 12:34:56.789101")
def test_handler_ok_04():
    """
    正常系 ライド一覧取得API
    Mock化なし
    begin,end,bookmark_flg指定なし
    """
    # 入力データ
    input_body = {}
    query_string_parameters = {
        "limit": '2',
        "offset": '3'
    }
    event = get_event(
        query_string_parameters=query_string_parameters,
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
    )
    context = {}

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "end_of_data": False,
        "ride_histories": [
            {
                "ride_history_id": "1362022-10-06T15:30:31.000",
                "start_timestamp": "2022-12-16T12:12:12.610Z",
                "end_timestamp": "2022-12-16T12:12:12.610Z",
                "ride_name": "ユーザー車両名のライド",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": False
            },
            {
                "ride_history_id": "1352022-10-06T15:30:31.000",
                "start_timestamp": "2022-12-15T12:12:12.610Z",
                "end_timestamp": "2022-12-15T12:12:12.610Z",
                "ride_name": "ユーザー車両名のライド",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": False
            },
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    準正常系 ライド一覧取得API
    バリデーションチェック
    検索開始日：日付型以外が入力された場合
    検索終了日：日付型以外が入力された場合
    お気に入りフラグ：Boolean以外が入力された場合
    limit：半角数字以外が入力された場合
    offset：半角数字以外が入力された場合
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 入力データ
    query_string_parameters = {
        "begin": "1234",
        "end": "1234",
        "bookmark_flg": "あいうえお",
        "limit": "あいうえお",
        "offset": "あいうえお",
    }
    event = get_event(
        gigya_uid='test_uid_01',
        query_string_parameters=query_string_parameters,
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
                    "field": "begin",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "bookmark_flg",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "end",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "limit",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "offset",
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


def test_handler_ng_02(mocker):
    """
    準正常系 ライド一覧取得API
    バリデーションチェック
    文字列チェック
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    input_body = {
        "begin": 9999,
        "end": 9999
    }
    # 入力データ
    query_string_parameters = {
        "begin": "2022-12-17T12:12:12.610Z",
        "end": "2022-12-17T12:12:12.610Z"
    }
    event = get_event(
        gigya_uid='test_uid_01',
        body=input_body,
        query_string_parameters=query_string_parameters,
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
                    "field": "begin",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "end",
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


def test_handler_ng_03(mocker):
    """
    準正常系 ライド一覧取得API
    バリデーションチェック
    検索開始日 > 検索終了日の場合
    """
    # 入力データ
    input_body = {}
    query_string_parameters = {
        "begin": "2022-09-01T09:00:00.000Z",
        "end": "2022-09-01T08:00:00.000Z",
        "bookmark_flg": 'True',
        "limit": '30',
        "offset": '0'
    }
    event = get_event(
        query_string_parameters=query_string_parameters,
        body=input_body,
        gigya_uid='test_uid_01',
        path='/rides'
    )
    context = {}

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E014",
                    "field": "end",
                    "message": "期間設定終了日には期間設定開始日以降の日付を入力してください。"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
