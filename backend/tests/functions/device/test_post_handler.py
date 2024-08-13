
import json
from importlib import import_module, reload
from common.rds import execute_select_statement
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.device.post_handler')
post_handler = getattr(module, 'handler')


def test_post_handler_ok_01(mocker):
    """
    正常系 デバイストークン登録更新API
    """
    # 入力データ
    body = {
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX",
        "device_token": "740f4707 bebcf74f 9b7c25d4 8e335894 5f6aa01d a5ddb387 462c7eaf 61bb78aa"
    }
    event = get_event(body=body, gigya_uid='test_uid_01', path='/device-token')
    context = {}

    # service.device_service.upsert_t_device のモック化
    mocker.patch("service.device_service.upsert_device", return_value={
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX",
        "device_token": "740f4707 bebcf74f 9b7c25d4 8e335894 5f6aa01d a5ddb387 462c7eaf 61bb78aa"
    })
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX",
        "device_token": "740f4707 bebcf74f 9b7c25d4 8e335894 5f6aa01d a5ddb387 462c7eaf 61bb78aa"
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_post_handler_ok_02(mocker):
    """
    正常系: 同一デバイスIDが登録されている場合はそのレコードのデバイストークンを空文字列にUPDATEする。
    モック無し
    """
    # 入力データ
    body = {
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX",
        "device_token": "77777777"
    }
    event = get_event(body=body, gigya_uid='test_uid_02', path='/device-token')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX",
        "device_token": "77777777"
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value

    expected_value = [{
        "gigya_uid": "test_uid_03", "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX", "device_token": "",
    }]

    sql: str = '''
      SELECT gigya_uid, device_id, device_token FROM t_device
      WHERE gigya_uid = %(gigya_uid)s;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_03'}
    assert execute_select_statement(sql, parameters_dict) == expected_value


def test_post_handler_ng_01(mocker):
    """
    準正常系 デバイストークン登録更新API
    バリデーションチェック device_id
    """
    # 入力データ
    body = {
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXX",
        "device_token": None
    }
    event = get_event(body=body, gigya_uid='test_uid_01', path='/device-token')
    context = {}

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
                {
                    "code": "E007",
                    "field": "device_token",
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
