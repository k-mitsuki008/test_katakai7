import json

from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles_maintenances_histories_detail.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 メンテナンス履歴詳細取得API
    Mock化あり
    """
    # 入力データ
    event = get_event(
        path_parameters={'user_vehicle_id': '1'},
        query_string_parameters={'maintain_history_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories?maintain_history_id=1'
    )
    context = {}

    mocker.patch(
        "service.user_vehicle_service.user_vehicle_id_is_exist",
        return_value={}
    )

    # device.service.get_maintain_history_detailのモック化
    mocker.patch(
        "service.maintain_history_service.get_maintain_history_detail",
        return_value={
            "maintain_history_id": 1,
            "maintain_item_code": "00001",
            "maintain_item_name": "タイヤの空気圧",
            "maintain_implement_date": "2022-06-23",
            "maintain_location": "ル・サイクル仙台店",
            "maintain_item_file_id": "00001",
            "maintain_cost": 3980,
            "maintain_required_time": 120,
            "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
            "maintain_image_urls": [
                {
                    "file_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
                    "s3_url": "/uid/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1?AWSAccessKeyId=xxx&Signature=yyy&Expires=XXX"
                },
                {
                    "file_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
                    "s3_url": "/uid/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2?AWSAccessKeyId=xxx&Signature=yyy&Expires=XXX"
                },
                {
                    "file_id": None,
                    "s3_url": None
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
        "maintain_history_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "タイヤの空気圧",
        "maintain_implement_date": "2022-06-23",
        "maintain_location": "ル・サイクル仙台店",
        "maintain_item_file_id": "00001",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_urls": [
            {
                "file_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
                "s3_url": "/uid/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1?AWSAccessKeyId=xxx&Signature=yyy&Expires=XXX"
            },
            {
                "file_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
                "s3_url": "/uid/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2?AWSAccessKeyId=xxx&Signature=yyy&Expires=XXX"
            },
            {
                "file_id": None,
                "s3_url": None
            }
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02(mocker):
    """
    正常系 メンテナンス履歴詳細取得API
    Mock化なし
    """
    # 入力データ
    path_parameters = {
        'user_vehicle_id': '4',
        'maintain_history_id': '9'
    }
    event = get_event(
        path_parameters={'user_vehicle_id': '4'},
        query_string_parameters={'maintain_history_id': '9'},
        gigya_uid='test_uid_03',
        path='/vehicles/4/maintenances/histories?maintain_history_id=9'
    )
    context = {}

    # common.utils.aws_utils import get_s3_url のモック化
    mocker.patch("service.maintain_history_service.get_s3_url", side_effect=lambda *args, **kwargs: args)
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "maintain_history_id": 9,
        "maintain_item_code": "00002",
        "maintain_item_name": "タイヤ空気圧",
        "maintain_implement_date": "2020-10-11",
        "maintain_location": "メンテナンス場所2",
        "maintain_item_file_id": "00002",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_image_urls": [
            {
                "file_id": 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1',
                "s3_url": ['spvc-dev-upload-items', 'test_uid_03/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1']
            },
            {
                "file_id": 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2',
                "s3_url": ['spvc-dev-upload-items', 'test_uid_03/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2']
            },
            {
                "file_id": None,
                "s3_url": None
            }
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01():
    """
    準正常系 メンテナンス履歴詳細API
    バリデーションチェック 必須項目
      ユーザー車両ID     : None
      メンテナンス履歴ID  : None
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": None,
        "maintain_history_id": None
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/vehicles/None/maintenances/histories?maintain_history_id=None'
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

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_02():
    """
    準正常系 メンテナンス履歴詳細API
    バリデーションチェック 空文字入力
      ユーザー車両ID      : 空文字入力のチェック
      メンテナンス履歴ID   : 空文字入力のチェック
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": "",
        "maintain_history_id": ""
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/vehicles//maintenances/histories?maintain_history_id='
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

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_03():
    """
    準正常系 メンテナンス履歴詳細API
    バリデーションチェック 型確認
      ユーザー車両ID     : int型以外の入力値
      メンテナンス履歴ID  : int型以外の入力値
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": "test",
        "maintain_history_id": "test"
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/vehicles/test/maintenances/histories?maintain_history_id=test'
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

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value
