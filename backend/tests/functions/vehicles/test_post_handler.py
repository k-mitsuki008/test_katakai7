from datetime import datetime
import json
from importlib import import_module, reload
from tests.test_utils.utils import get_event
from common.error.business_error import BusinessError
from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles.post_handler')
post_handler = getattr(module, 'handler')


def test_handler_ok(mocker):
    """
    正常系　車両設定登録API
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-1234567",
        "model_code": "abcd",
        "vehicle_name": "ユーザ車両名_01",
        "managed_flag": True
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/vehicles')
    context = {}

    # service.user_vehicle_service.insert_t_user_vehicle のモック化
    mocker.patch("service.user_vehicle_service.insert_vehicle", return_value=1234)
    # service.user_vehicle_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.get_vehicles", return_value=[
        {
            "user_vehicle_id": 1234,
            "model_code": "abcd",
            "vehicle_id": "abcd-1234567",
            "vehicle_name": "ユーザ車両名_01",
            "managed_flag": True,
            "registered_flag": None,
            "peripheral_identifier": None,
            "complete_local_name": None,
            "purchase_shop": {
                "shop_name": "モトベロ二子玉川",
                "shop_tel": "03-6277-1234",
                "shop_location": "東京都世田谷区玉川1丁目１４－１　二子玉川　ライズS．C．テラスマーケット１Ｆ"
            },
            "bluetooth": None,
            "maintain_setting": {
                "maintain_consciousness": "01",
                "maintain_alerts": [
                    {
                        "maintain_item_code": "00002",
                        "maintain_item_name": "タイヤ空気圧",
                        "maintain_item_alert": True
                    },
                    {
                        "maintain_item_code": "00003",
                        "maintain_item_name": "タイヤ摩耗",
                        "maintain_item_alert": True
                    },
                ]
            }
        }
    ])
    # service.user_setting_maintain_service.initialize_maintenance_setting のモック化
    mocker.patch("service.user_setting_maintain_service.initialize_maintenance_setting", return_value={
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "タイヤ空気圧",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00003",
                "maintain_item_name": "タイヤ摩耗",
                "maintain_item_alert": True
            }
        ]
    })
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 1234,
        "model_code": "abcd",
        "vehicle_id": "abcd-1234567",
        "vehicle_name": "ユーザ車両名_01",
        "managed_flag": True,
        "registered_flag": None,
        "peripheral_identifier": None,
        "complete_local_name": None,
        "purchase_shop": {
            "shop_name": "モトベロ二子玉川",
            "shop_tel": "03-6277-1234",
            "shop_location": "東京都世田谷区玉川1丁目１４－１　二子玉川　ライズS．C．テラスマーケット１Ｆ"
        },
        "bluetooth": None,
        "maintain_setting": {
            "maintain_consciousness": "01",
            "maintain_alerts": [
                {
                    "maintain_item_code": "00002",
                    "maintain_item_name": "タイヤ空気圧",
                    "maintain_item_alert": True
                },
                {
                    "maintain_item_code": "00003",
                    "maintain_item_name": "タイヤ摩耗",
                    "maintain_item_alert": True
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok2(mocker):
    """
    正常系　車両設定登録API
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-1234567",
        "model_code": "abcd",
        "vehicle_name": "ユーザ車両名1234512345_01",# 19文字以上の入力可否確認
        "managed_flag": True,
        "equipment_weight": 10,
        "vehicle_nickname": "愛車名_01",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/vehicles')
    context = {}

    # service.user_vehicle_service.insert_t_user_vehicle のモック化
    mocker.patch("service.user_vehicle_service.insert_vehicle", return_value=1234)
    # service.user_vehicle_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.get_vehicles", return_value=[
        {
            "user_vehicle_id": 1234,
            "model_code": "abcd",
            "vehicle_id": "abcd-1234567",
            "vehicle_name": "ユーザ車両名1234512345_01",
            "managed_flag": True,
            "registered_flag": None,
            "peripheral_identifier": None,
            "complete_local_name": None,
            "equipment_weight": 10,
            "vehicle_nickname": "愛車名_01",
            "purchase_shop": {
                "shop_name": "モトベロ二子玉川",
                "shop_tel": "03-6277-1234",
                "shop_location": "東京都世田谷区玉川1丁目１４－１　二子玉川　ライズS．C．テラスマーケット１Ｆ"
            },
            "bluetooth": None,
            "maintain_setting": {
                "maintain_consciousness": "01",
                "maintain_alerts": [
                    {
                        "maintain_item_code": "00002",
                        "maintain_item_name": "タイヤ空気圧",
                        "maintain_item_alert": True
                    },
                    {
                        "maintain_item_code": "00003",
                        "maintain_item_name": "タイヤ摩耗",
                        "maintain_item_alert": True
                    },
                ]
            }
        }
    ])
    # service.user_setting_maintain_service.initialize_maintenance_setting のモック化
    mocker.patch("service.user_setting_maintain_service.initialize_maintenance_setting", return_value={
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "タイヤ空気圧",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00003",
                "maintain_item_name": "タイヤ摩耗",
                "maintain_item_alert": True
            }
        ]
    })
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 1234,
        "model_code": "abcd",
        "vehicle_id": "abcd-1234567",
        "vehicle_name": "ユーザ車両名1234512345_01",
        "managed_flag": True,
        "registered_flag": None,
        "peripheral_identifier": None,
        "complete_local_name": None,
        "equipment_weight": 10,
        "vehicle_nickname": "愛車名_01",
        "purchase_shop": {
            "shop_name": "モトベロ二子玉川",
            "shop_tel": "03-6277-1234",
            "shop_location": "東京都世田谷区玉川1丁目１４－１　二子玉川　ライズS．C．テラスマーケット１Ｆ"
        },
        "bluetooth": None,
        "maintain_setting": {
            "maintain_consciousness": "01",
            "maintain_alerts": [
                {
                    "maintain_item_code": "00002",
                    "maintain_item_name": "タイヤ空気圧",
                    "maintain_item_alert": True
                },
                {
                    "maintain_item_code": "00003",
                    "maintain_item_name": "タイヤ摩耗",
                    "maintain_item_alert": True
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    異常系 車両設定登録API
    ユーザメンテナンス設定項目初期登録途中にエラー発生 → ユーザ車両TBL、ユーザメンテナンス設定TBL、ユーザメンテナンス設定項目TBLが更新前にロールバックされること
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-1234567",
        "model_code": "abcd",
        "vehicle_name": "ユーザ車両名_01",
        "managed_flag": True
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E001",
            "message": "システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。",
            "validationErrors": None
        }
    }

    # repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain でエラー発生
    mocker.patch("repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item", side_effect=Exception)
    reload(module)

    response = post_handler(event, context)

    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 500
    assert body == expected_value

    # ユーザ車両TBLが更新前にロールバックされることを確認。
    expected_value_2 = [
        {"user_vehicle_id": 1, "gigya_uid": 'test_uid_02', "managed_flag": True, "registered_flag": True, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",  "update_timestamp": None, "update_user_id": None},
        {"user_vehicle_id": 2, "gigya_uid": "test_uid_02", "managed_flag": False, "registered_flag": False, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",  "update_timestamp": None, "update_user_id": None},
        {"user_vehicle_id": 3, "gigya_uid": "test_uid_02", "managed_flag": False, "registered_flag": False, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",  "update_timestamp": None, "update_user_id": None},
    ]
    sql: str = '''
      SELECT user_vehicle_id, gigya_uid, managed_flag, registered_flag, insert_timestamp, insert_user_id, update_timestamp, update_user_id FROM t_user_vehicle
      WHERE gigya_uid = %(gigya_uid)s
      ORDER BY user_vehicle_id;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_02'}
    results = execute_select_statement(sql, parameters_dict)
    assert results == expected_value_2

    # ユーザメンテナンス設定TBLが更新前にロールバックされることを確認。
    expected_value_3 = [
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01", "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",  "update_timestamp": None, "update_user_id": None},
        {"user_vehicle_id": 2, "gigya_uid": "test_uid_02", "maintain_consciousness": "01", "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",  "update_timestamp": None, "update_user_id": None},
        {"user_vehicle_id": 3, "gigya_uid": "test_uid_02", "maintain_consciousness": "02", "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01", "update_timestamp": None, "update_user_id": None}
    ]
    sql: str = '''
      SELECT user_vehicle_id, gigya_uid, maintain_consciousness, insert_timestamp, insert_user_id, update_timestamp, update_user_id FROM t_user_setting_maintain
      WHERE gigya_uid = %(gigya_uid)s
      ORDER BY user_vehicle_id;
    '''
    parameters_dict: dict = {'gigya_uid': 'test_uid_02'}
    results = execute_select_statement(sql, parameters_dict)
    assert results == expected_value_3


def test_handler_ng_02():
    """
    異常系 車両設定登録API
    バリデーションチェック(システムバリデーションチェック)
    """
    # 入力データ
    input_body = {
        "vehicle_id": 1,
        "model_code": 2,
        "vehicle_name": 3,
        "managed_flag": 4,
        "equipment_weight": "aaa",
        "vehicle_nickname": 5,
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "equipment_weight",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "managed_flag",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "model_code",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "vehicle_id",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "vehicle_name",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "vehicle_nickname",
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


def test_handler_ng_03():
    """
    異常系 車両設定登録API
    バリデーションチェック(画面入力項目:車両名 必須項目エラー)
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-1234567",
        "model_code": "abcd",
        "vehicle_name": None,
        "managed_flag": True,
        "equipment_weight": None,
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E010",
                    "field": "vehicle_name",
                    "message": "車両名は必須入力項目です。"
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_04():
    """
    異常系 車両設定登録API
    バリデーションチェック(画面入力項目:車両名 文字数超過エラー)
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-1234567",
        "model_code": "abcd",
        "vehicle_name": "あいうえお1234512345123451234512345123451234512345123451",
        "managed_flag": True,
        "vehicle_nickname": "あいうえお12345123451234",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E016",
                    "field": "vehicle_name",
                    "message": "50文字以下で入力してください。"
                },
                {
                    "code": "E016",
                    "field": "vehicle_nickname",
                    "message": "18文字以下で入力してください。"
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_05():
    """
    異常系 車両設定登録API
    バリデーションチェック(画面入力項目:号機番号 桁過不足エラー)
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-123456",
        "model_code": "abcd",
        "vehicle_name": "ユーザー指定車両名01-01",
        "managed_flag": True
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E017",
                    "field": "vehicle_id",
                    "message": "7文字で入力してください。"
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_06(mocker):
    """
    異常系 車両設定登録API
    業務エラー(登録車両数超過)
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-1234567",
        "model_code": "abcd",
        "vehicle_name": "ユーザー指定車両名01-01",
        "managed_flag": True
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/vehicles')
    context = {}

    # user_vehicles.service.insert_vehicle のモック化
    mocker.patch("service.user_vehicle_service.insert_vehicle", side_effect=BusinessError('E038', params=(5,)))
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E038",
            'message': '車両は5件まで登録できます。',
            "validationErrors": None
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 400
    assert body == expected_value
