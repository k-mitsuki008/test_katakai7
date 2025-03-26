import json
from importlib import import_module, reload
import pytest

from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.login.post_handler')
handler = getattr(module, 'handler')


class RequestResponse:
    text = '{"keys": [{"kid": "test_kid"}]}'


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_handler_ok(mocker):
    """
    正常系 ログインAPI
    Mock化なし
    """
    # 入力データ
    input_body = {
        "device_id": "BCCAC812-7A94-5F41-DCAA-2599D8C4C1DA"
    }
    event = get_event(body=input_body, gigya_uid=None, path='/login')
    context = {}

    # service.session_service.create_session_id のモック化
    mocker.patch("service.session_service.create_session_id",
                 return_value="1111111111222222222233333333334444444444555555555566666666667777")

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "session_id": "1111111111222222222233333333334444444444555555555566666666667777"
    }

    response = handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_1():
    """
    異常系 ログインAPI
    バリデーションチェック
    デバイスID：文字数超過エラー
    """
    # 入力データ
    input_body = {
        "device_id": "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJ"
    }
    event = get_event(body=input_body, path='/login')
    context = {}
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "device_id",
                    "message": "validation error"
                },
            ]
        }
    }

    response = handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_2():
    """
    異常系 ログインAPI
    バリデーションチェック
    デバイスID：文字数不足エラー
    """
    # 入力データ
    input_body = {
        "device_id": "AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIII"
    }
    event = get_event(body=input_body, path='/login')
    context = {}
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "device_id",
                    "message": "validation error"
                },
            ]
        }
    }

    response = handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_3():
    """
    異常系 ログインAPI
    バリデーションチェック
    デバイスID：null更新不可チェック
    """
    # 入力データ
    input_body = {
        "device_id": None
    }
    event = get_event(body=input_body, path='/login')
    context = {}
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "device_id",
                    "message": "validation error"
                }
            ]
        }
    }

    response = handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_4():
    """
    異常系 ログインAPI
    バリデーションチェック
    デバイスID：空文字不可チェック
    """
    # 入力データ
    input_body = {
        "device_id": ""
    }
    event = get_event(body=input_body, path='/login')
    context = {}
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "device_id",
                    "message": "validation error"
                }
            ]
        }
    }

    response = handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_5():
    """
    異常系 ログインAPI
    バリデーションチェック
    デバイスID：型チェック
    """
    # 入力データ
    input_body = {
        "device_id": 123456789012345678901234567890123456
    }
    event = get_event(body=input_body, path='/login')
    context = {}
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "device_id",
                    "message": "validation error"
                }
            ]
        }
    }

    response = handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
