import os
import json
from importlib import import_module, reload
import pytest
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles_maintenances.get_handler')
get_handler = getattr(module, 'handler')
cloud_front_domain_name = os.environ['CLOUD_FRONT_DOMAIN_NAME']


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_handler_ok(mocker):
    """
    正常系 メンテナンス指示一覧取得API
    Mock化なし
    """
    # 入力データ
    event = get_event(path_parameters={'user_vehicle_id': '1'}, gigya_uid='test_uid_02', path='/vehicles/1/maintenances')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "maintain_items": [
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "タイヤ空気圧",
                "maintain_type_code": "01",
                "maintain_interval": 10,
                "priority": 1,
                "maintain_archive": 3,
                "maintain_item_icon_url": cloud_front_domain_name + 'icons/abcde00002.png'
            },
            {
                "maintain_item_code": "00003",
                "maintain_item_name": "タイヤ摩耗",
                "maintain_type_code": "02",
                "maintain_interval": 100,
                "priority": 2,
                "maintain_archive": 25,
                "maintain_item_icon_url": cloud_front_domain_name + 'icons/abcde00003.png'
            },
            {
                "maintain_item_code": "00004",
                "maintain_item_name": "チェーン動作",
                "maintain_type_code": "02",
                "maintain_interval": 101,
                "priority": 3,
                "maintain_archive": 26,
                "maintain_item_icon_url": cloud_front_domain_name + 'icons/abcde00004.png'
            },
            {
                "maintain_item_code": "00005",
                "maintain_item_name": "ブレーキ動作、摩耗",
                "maintain_type_code": "02",
                "maintain_interval": 102,
                "priority": 4,
                "maintain_archive": 30,
                "maintain_item_icon_url": cloud_front_domain_name + 'icons/abcde00005.png'
            },
            {
                "maintain_item_code": "00001",
                "maintain_item_name": "ホイール",
                "maintain_type_code": "02",
                "maintain_interval": 103,
                "priority": 5,
                "maintain_archive": 30,
                "maintain_item_icon_url": cloud_front_domain_name + 'icons/abcde00001.png'
            },
            {
                "maintain_item_code": "00009",
                "maintain_item_name": "定期点検",
                "maintain_type_code": "01",
                "maintain_interval": 120,
                "priority": 9,
                "maintain_archive": 3,
                "maintain_item_icon_url": cloud_front_domain_name + 'icons/abcde00009.png'
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
    異常系 メンテナンス指示一覧取得API
    バリデーションチェック(USER_VEHICLE_ID 型NGチェック)
    """
    # 入力データ
    input_body = {"user_vehicle_id": "1"}
    event = get_event(body=input_body, gigya_uid="test_uid2", path='/vehicles/1/maintenances')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
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


def test_handler_ng_02(mocker):
    """
    異常系 メンテナンス指示一覧取得API
    バリデーションチェック(USER_VEHICLE_ID 必須項目)
    """
    # 入力データ
    input_body = {"user_vehicle_id": None}
    event = get_event(body=input_body, gigya_uid="test_uid2", path='/vehicles/1/maintenances')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
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
