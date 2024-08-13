import json

from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.bluetooth_unexpected_data.post_handler')
post_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 Bluetooth異常データ送信API
    """
    # 入力データ
    input_body = {
        "ccu_id": "0019XXXXXXXXXX",
        "unexpected_data": {
            "timestamp": "2020-11-27T12:34:56.789Z",
            "GIGYA-UUID": "0123456789abcdef01234567890abcde",
            "Serial-number": "X123-1234567",
            "Frame-number": "1234567890",
            "RIDE-DATA-1": [
                {"timestamp": "2020-01-07T14:05:08.707Z",
                 "Contents": "1000000000000000000000000000000000000000000000000000FF"},
                {"timestamp": "2020-01-07T14:05:09.707Z",
                 "Contents": "1000000000000000000000000000000000000000000000000000FF"}
            ],
            "DU-SYNCHRONIZATION-DATA-1": [
                {"timestamp": "2020-01-07T14:05:08.707Z",
                 "Contents": "2000000000000000000000000000000000000000000000000000FF"},
                {"timestamp": "2020-01-07T14:05:09.707Z",
                 "Contents": "2000000000000000000000000000000000000000000000000000FF"}
            ],
        }
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/bluetooth_unexpected_data'
    )
    context = {}

    # service.bluetooth_unexpected_data_service upload_file のモック化
    mocker.patch("service.bluetooth_unexpected_data_service.upload_file", return_value={None})
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02(mocker):
    """
    正常系 Bluetooth異常データ送信API
    Mock化なし
    """
    # 入力データ
    input_body = {
        "ccu_id": "0019XXXXXXXXXX",
        "unexpected_data": {
            "timestamp": "2020-11-27T12:34:56.789Z",
            "GIGYA-UUID": "0123456789abcdef01234567890abcde",
            "Serial-number": "X123-1234567",
            "Frame-number": "1234567890",
            "RIDE-DATA-1": [
                {"timestamp": "2020-01-07T14:05:08.707Z",
                 "Contents": "1000000000000000000000000000000000000000000000000000FF"},
                {"timestamp": "2020-01-07T14:05:09.707Z",
                 "Contents": "1000000000000000000000000000000000000000000000000000FF"}
            ],
            "DU-SYNCHRONIZATION-DATA-1": [
                {"timestamp": "2020-01-07T14:05:08.707Z",
                 "Contents": "2000000000000000000000000000000000000000000000000000FF"},
                {"timestamp": "2020-01-07T14:05:09.707Z",
                 "Contents": "2000000000000000000000000000000000000000000000000000FF"}
            ],
        }
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/bluetooth_unexpected_data'
    )
    context = {}

    # service.bluetooth_unexpected_data_service create_s3_objects のモック化
    mocker.patch(
        "service.bluetooth_unexpected_data_service.create_s3_objects",
        side_effect=lambda *args, **kwargs: args
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    異常系 Bluetooth異常データ送信API
    timestampが日付型以外の場合
    """
    # 入力データ
    input_body = {
        "ccu_id": "0019XXXXXXXXXX",
        "unexpected_data": {
            "timestamp": "123456789",
            "GIGYA-UUID": "0123456789abcdef01234567890abcde",
            "Serial-number": "X123-1234567",
            "Frame-number": "1234567890",
            "RIDE-DATA-1": [
                {"timestamp": "2020-01-07T14:05:08.707+0800",
                 "Contents": "1000000000000000000000000000000000000000000000000000FF"},
                {"timestamp": "2020-01-07T14:05:09.707+0800",
                 "Contents": "1000000000000000000000000000000000000000000000000000FF"}
            ],
            "DU-SYNCHRONIZATION-DATA-1": [
                {"timestamp": "2020-01-07T14:05:08.707+0800",
                 "Contents": "2000000000000000000000000000000000000000000000000000FF"},
                {"timestamp": "2020-01-07T14:05:09.707+0800",
                 "Contents": "2000000000000000000000000000000000000000000000000000FF"}
            ],
        }
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/bluetooth_unexpected_data'
    )
    context = {}

    # service.bluetooth_unexpected_data_service create_s3_objects のモック化
    mocker.patch(
        "service.bluetooth_unexpected_data_service.create_s3_objects",
        side_effect=lambda *args, **kwargs: args
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E001',
            'message': 'システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。', 'validationErrors': None
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 400
    assert body == expected_value


def test_handler_ng_02(mocker):
    """
    異常系 Bluetooth異常データ送信API
    ccu_id:文字型以外の場合
    unexpected_data:辞書型以外の場合
    """
    # 入力データ
    input_body = {
        "ccu_id": int('00195678901234'),
        "unexpected_data": "あいうえお"
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/bluetooth_unexpected_data'
    )
    context = {}

    # service.bluetooth_unexpected_data_service create_s3_objects のモック化
    mocker.patch(
        "service.bluetooth_unexpected_data_service.create_s3_objects",
        side_effect=lambda *args, **kwargs: args
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005',
            'message': 'validation error',
            'validationErrors': [
                {
                    'code': 'E007',
                    'field': 'ccu_id',
                    'message': 'validation error'
                },
                {
                    'code': 'E007',
                    'field': 'unexpected_data',
                    'message': 'validation error'
                }
            ]
        },
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_03(mocker):
    """
    異常系 Bluetooth異常データ送信API
    ccu_id:空欄の場合
    unexpected_data:空欄の場合
    """
    # 入力データ
    input_body = {
        "ccu_id": "",
        "unexpected_data": ""
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/bluetooth_unexpected_data'
    )
    context = {}

    # service.bluetooth_unexpected_data_service create_s3_objects のモック化
    mocker.patch(
        "service.bluetooth_unexpected_data_service.create_s3_objects",
        side_effect=lambda *args, **kwargs: args
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005',
            'message': 'validation error',
            'validationErrors': [
                {
                    'code': 'E007',
                    'field': 'ccu_id',
                    'message': 'validation error'
                },
                {
                    'code': 'E007',
                    'field': 'unexpected_data',
                    'message': 'validation error'
                }
            ]
        },
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_04(mocker):
    """
    異常系 Bluetooth異常データ送信API
    ccu_id:文字不足の場合
    """
    # 入力データ
    input_body = {
        "ccu_id": "0019567890123",
        "unexpected_data": {"timestamp": "123456789"},
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/bluetooth_unexpected_data'
    )
    context = {}

    # service.bluetooth_unexpected_data_service create_s3_objects のモック化
    mocker.patch(
        "service.bluetooth_unexpected_data_service.create_s3_objects",
        side_effect=lambda *args, **kwargs: args
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005',
            'message': 'validation error',
            'validationErrors': [
                {
                    'code': 'E007',
                    'field': 'ccu_id',
                    'message': 'validation error'
                }
            ]
        },
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_05(mocker):
    """
    異常系 Bluetooth異常データ送信API
    ccu_id:文字超過の場合
    """
    # 入力データ
    input_body = {
        "ccu_id": "001956789012345",
        "unexpected_data": {"timestamp": "123456789"},
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/bluetooth_unexpected_data'
    )
    context = {}

    # service.bluetooth_unexpected_data_service create_s3_objects のモック化
    mocker.patch(
        "service.bluetooth_unexpected_data_service.create_s3_objects",
        side_effect=lambda *args, **kwargs: args
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005',
            'message': 'validation error',
            'validationErrors': [
                {
                    'code': 'E007',
                    'field': 'ccu_id',
                    'message': 'validation error'
                }
            ]
        },
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_06(mocker):
    """
    異常系 Bluetooth異常データ送信API
    ccu_id:0019XXXXXXXXXXでは無い場合
    """
    # 入力データ
    input_body = {
        "ccu_id": "12345678901234",
        "unexpected_data": {"timestamp": "123456789"},
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/bluetooth_unexpected_data'
    )
    context = {}

    # service.bluetooth_unexpected_data_service create_s3_objects のモック化
    mocker.patch(
        "service.bluetooth_unexpected_data_service.create_s3_objects",
        side_effect=lambda *args, **kwargs: args
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005',
            'message': 'validation error',
            'validationErrors': [
                {
                    'code': 'E007',
                    'field': 'ccu_id',
                    'message': 'validation error'
                }
            ]
        },
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
