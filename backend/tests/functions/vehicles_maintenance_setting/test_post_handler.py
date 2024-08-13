import json
from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module("src.functions.vehicles_maintenance_setting.post_handler")
post_handler = getattr(module, "handler")


def test_handler_ok_01(mocker):
    """
    正常系 メンテナンス設定登録更新API
    Mock化あり
    """
    # 入力データ
    input_body = {
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00001",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00002",
                "maintain_item_alert": False
            }
        ]
    }
    user_vehicle_id = {
        "user_vehicle_id": '1',
    }
    event = get_event(
        body=input_body,
        path_parameters=user_vehicle_id,
        gigya_uid="test_uid_02",
        path="/vehicles/111/shop"
    )

    context = {}

    # device.service.upsert_setting_maintainのモック化
    mocker.patch(
        "service.user_setting_maintain_service.upsert_setting_maintain",
        return_value={
            "user_vehicle_id": 111,
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
    )

    # device.service.user_vehicle_id_is_existのモック化
    mocker.patch(
        "service.user_vehicle_service.user_vehicle_id_is_exist",
        return_value=True
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 111,
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

    response = post_handler(event, context)
    status_code = response["statusCode"]
    body = json.loads(response["body"])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02():
    """
    正常系 メンテナンス設定登録更新API
    Mock化なし
    """
    # 入力データ
    input_body = {
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00001",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00002",
                "maintain_item_alert": False
            },
            {
                "maintain_item_code": "00003",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00004",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00005",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00009",
                "maintain_item_alert": True
            }
        ]
    }
    user_vehicle_id = {
        "user_vehicle_id": '1',
    }
    event = get_event(
        body=input_body,
        path_parameters=user_vehicle_id,
        gigya_uid="test_uid_02",
        path="/vehicles/111/shop"
    )

    context = {}
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 1,
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "タイヤ空気圧",
                "maintain_item_alert": False
            },
            {
                "maintain_item_code": "00003",
                "maintain_item_name": "タイヤ摩耗",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00004",
                "maintain_item_name": "チェーン動作",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00005",
                "maintain_item_name": "ブレーキ動作、摩耗",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00001",
                "maintain_item_name": "ホイール",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00009",
                "maintain_item_name": "定期点検",
                "maintain_item_alert": True
            }
        ]
    }

    response = post_handler(event, context)
    status_code = response["statusCode"]
    body = json.loads(response["body"])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    準正常系 メンテナンス設定登録更新API
    バリデーションチェック
    メンテナンス意識設定CD：必須項目エラー
    user_vehicle_id：必須項目エラー
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 入力データ
    input_body = {
        "maintain_consciousness": None,
        "maintain_alerts": None
    }
    user_vehicle_id = {
        "user_vehicle_id": '',
    }
    event = get_event(
        body=input_body,
        path_parameters=user_vehicle_id,
        gigya_uid="test_uid_01",
        path="/vehicles/123/maintenance-setting"
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
                    "field": "maintain_consciousness",
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
    status_code = response["statusCode"]
    body = json.loads(response["body"])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_02(mocker):
    """
    準正常系 メンテナンス設定登録更新API
    バリデーションチェック
    メンテナンス意識設定CD：文字型以外が入力された場合
    メンテナンス通知フラグ：リスト以外が入力された場合
    user_vehicle_id：半角数字以外が入力された場合
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 入力データ
    input_body = {
        "maintain_consciousness": 12345,
        "maintain_alerts": "あいうえお"
    }
    user_vehicle_id = {
        "user_vehicle_id": "AAA",
    }
    event = get_event(
        body=input_body,
        path_parameters=user_vehicle_id,
        gigya_uid="test_uid_01",
        path="/vehicles/123/maintenance-setting"
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
                    "field": "maintain_alerts",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_consciousness",
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
    status_code = response["statusCode"]
    body = json.loads(response["body"])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_03():
    """
    準正常系 メンテナンス設定登録更新API
    バリデーションチェック
    メンテナンス意識設定CD：定数マスタ以外の値が入力された場合
    """
    # 入力データ
    input_body = {
        "maintain_consciousness": "04",
        "maintain_alerts": []
    }
    user_vehicle_id = {
        "user_vehicle_id": "1",
    }
    event = get_event(
        body=input_body,
        path_parameters=user_vehicle_id,
        gigya_uid="test_uid_01",
        path="/vehicles/123/maintenance-setting"
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
                    "field": "maintain_consciousness",
                    "message": "validation error"
                }
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response["statusCode"]
    body = json.loads(response["body"])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_04(mocker):
    """
    準正常系 メンテナンス設定登録更新API
    バリデーションチェック
    メンテナンス意識設定CD：空文字チェック
    user_vehicle_id：空文字チェック
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 入力データ
    input_body = {
        "maintain_consciousness": "",
        "maintain_alerts": []
    }
    user_vehicle_id = {
        "user_vehicle_id": "",
    }
    event = get_event(
        body=input_body,
        path_parameters=user_vehicle_id,
        gigya_uid="test_uid_01",
        path="/vehicles/123/maintenance-setting"
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
                    "field": "maintain_consciousness",
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
    status_code = response["statusCode"]
    body = json.loads(response["body"])
    assert status_code == 422
    assert body == expected_value
