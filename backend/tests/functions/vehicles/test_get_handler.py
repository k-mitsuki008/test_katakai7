import json
from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok(mocker):
    """
    正常系　ユーザ車両設定一覧取得API
    """
    # 入力データ
    input_body = {}
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/vehicles')
    context = {}

    # service.user_vehicles_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.get_vehicles", return_value=[
        {
            "user_vehicle_id": 123,
            "model_code": "abcd",
            "vehicle_id": "abcd-1111111",
            "vehicle_name": "test_behicle_name_01",
            "managed_flag": True,
            "registered_flag": True,
            "peripheral_identifier": "xxxxxx",
            "complete_local_name": "スイッチ",
            "equipment_weight": 10,
            "vehicle_nickname": "test_vehicle_name_01",
            "purchase_shop": {
                "shop_name": "モトベロ二子玉川",
                "shop_tel": "03-6277-1234",
                "shop_location": "東京都世田谷区玉川1丁目１４－１　二子玉川　ライズS．C．テラスマーケット１Ｆ"
            },
            "bluetooth": {
                "du_serial_number": "16777215",
                "du_odometer": 123
            },
            "maintain_setting": {
                "maintain_consciousness": "01",
                "maintain_alerts": [
                    {
                        "maintain_item_code": "00001",
                        "maintain_item_name": "タイヤの空気圧",
                        "maintain_item_alert": True
                    },
                    {
                        "maintain_item_code": "00002",
                        "maintain_item_name": "ブレーキ",
                        "maintain_item_alert": False
                    }
                ]
            }
        },
        {
            "user_vehicle_id": 456,
            "model_code": "efgh",
            "vehicle_id": "efgh-1111111",
            "vehicle_name": "test_behicle_name_02",
            "managed_flag": False,
            "registered_flag": True,
            "peripheral_identifier": "yyyyyy"
        }
    ])
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "vehicles": [
            {
                "user_vehicle_id": 123,
                "model_code": "abcd",
                "vehicle_id": "abcd-1111111",
                "vehicle_name": "test_behicle_name_01",
                "managed_flag": True,
                "registered_flag": True,
                "peripheral_identifier": "xxxxxx",
                "complete_local_name": "スイッチ",
                "equipment_weight": 10,
                "vehicle_nickname": "test_vehicle_name_01",
                "purchase_shop": {
                    "shop_name": "モトベロ二子玉川",
                    "shop_tel": "03-6277-1234",
                    "shop_location": "東京都世田谷区玉川1丁目１４－１　二子玉川　ライズS．C．テラスマーケット１Ｆ"
                },
                "bluetooth": {
                    "du_serial_number": "16777215",
                    "du_odometer": 123
                },
                "maintain_setting": {
                    "maintain_consciousness": "01",
                    "maintain_alerts": [
                        {
                            "maintain_item_code": "00001",
                            "maintain_item_name": "タイヤの空気圧",
                            "maintain_item_alert": True
                        },
                        {
                            "maintain_item_code": "00002",
                            "maintain_item_name": "ブレーキ",
                            "maintain_item_alert": False
                        }
                    ]
                }
            },
            {
                "user_vehicle_id": 456,
                "model_code": "efgh",
                "vehicle_id": "efgh-1111111",
                "vehicle_name": "test_behicle_name_02",
                "managed_flag": False,
                "registered_flag": True,
                "peripheral_identifier": "yyyyyy"
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
    異常系 ユーザ車両設定一覧取得API
    バリデーションチェック(GIGYA_UID 型NGチェック)
    """
    # 入力データ
    input_body = {}
    event = get_event(body=input_body, gigya_uid=None, path='/vehicles')
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
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
