import json
from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.upload_urls.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 画像アップロードURL取得API
    """
    event = get_event(query_string_parameters={'upload_file_counts': '3'}, gigya_uid='test_uid_02', path='/upload_urls')
    context = {}

    # upload_file_service.get_upload_urlsのモック化
    mocker.patch(
        "service.upload_file_service.get_upload_urls",
        return_value=[
            {
                "file_id": "XXXXX",
                "s3_url": "https://spvc-dev-upload-items.s3.amazonaws.com/spvc-dev-upload-items/cd tetest_uid_02/XXXXX?AWSAccessKeyId=foobar_key&Signature=9NP%2Bo5BG1fGSMgKmThDtV8crmtI%3D&Expires=1652446196"
            }
        ]
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "upload_urls": [
            {
                "file_id": "XXXXX",
                "s3_url": "https://spvc-dev-upload-items.s3.amazonaws.com/spvc-dev-upload-items/cd tetest_uid_02/XXXXX?AWSAccessKeyId=foobar_key&Signature=9NP%2Bo5BG1fGSMgKmThDtV8crmtI%3D&Expires=1652446196"
            }
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    準正常系 画像アップロードURL取得API
    バリデーションチェック gigya_uid = null、upload_file_counts = null
    """
    # 入力データ
    event = get_event(path='/upload_urls')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "gigya_uid",
                    "message": "validation error"
                },
                {
                    "code": "E006",
                    "field": "upload_file_counts",
                    "message": "missing field"
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
    準正常系 画像アップロードURL取得API
    バリデーションチェック upload_file_counts > 3
    """
    # 入力データ
    event = get_event(query_string_parameters={'upload_file_counts': '4'}, gigya_uid='test_uid_02', path='/upload_urls')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "upload_file_counts",
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


def test_handler_ng_03(mocker):
    """
    準正常系 画像アップロードURL取得API
    バリデーションチェック upload_file_counts <= 0
    """
    # 入力データ
    event = get_event(query_string_parameters={'upload_file_counts': '0'}, gigya_uid='test_uid_02', path='/upload_urls')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "upload_file_counts",
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
