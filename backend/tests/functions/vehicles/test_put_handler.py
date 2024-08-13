from datetime import datetime
import json
from importlib import import_module, reload
from tests.test_utils.utils import get_event
from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures
from common.error.business_error import BusinessError
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles.put_handler')
put_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系　車両設定更新API
    Mock化あり
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-9999999",
        "vehicle_name": "test_vehicle_nm_01",
        "managed_flag": True,
        "peripheral_identifier": "E3:69:7D:AB:8A:24",
        "complete_local_name": "スイッチ",
        "registered_flag": True,
        "equipment_weight": 5,
        "vehicle_nickname": "test_vehicle_nm_01",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02',  path_parameters={'user_vehicle_id': '1'}, path='/vehicles')
    context = {}

    # service.user_vehicle_service.get_user_vehicle のモック化
    mocker.patch("service.user_vehicle_service.get_user_vehicle", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'equipment_weight': 5,
        "vehicle_nickname": "test_vehicle_nm_01",
    })
    # service.user_vehicle_service.update_vehicle のモック化
    mocker.patch("service.user_vehicle_service.update_vehicle", return_value=1)
    # service.user_vehicle_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.get_vehicles", return_value=[
        {
            "user_vehicle_id": 1,
            "model_code": "abcd",
            "vehicle_id": "abcd-9999999",
            "vehicle_name": "ユーザ車両名_01",
            "managed_flag": True,
            "registered_flag": True,
            "peripheral_identifier": '01504101-8F5C-49B6-BC32-0C2175E07DBF',
            "complete_local_name": "スイッチ",
            'equipment_weight': 5,
            "vehicle_nickname": "test_vehicle_nm_01",
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
                        "maintain_item_code": "00001",
                        "maintain_item_name": "タイヤの空気圧",
                        "maintain_item_alert": True
                    },
                    {
                        "maintain_item_code": "00002",
                        "maintain_item_name": "ブレーキ",
                        "maintain_item_alert": True
                    }
                ]
            }
        }
    ])
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 1,
        "model_code": "abcd",
        "vehicle_id": "abcd-9999999",
        "vehicle_name": "ユーザ車両名_01",
        "managed_flag": True,
        "registered_flag": True,
        "peripheral_identifier": '01504101-8F5C-49B6-BC32-0C2175E07DBF',
        "complete_local_name": "スイッチ",
        'equipment_weight': 5,
        "vehicle_nickname": "test_vehicle_nm_01",
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
                    "maintain_item_code": "00001",
                    "maintain_item_name": "タイヤの空気圧",
                    "maintain_item_alert": True
                },
                {
                    "maintain_item_code": "00002",
                    "maintain_item_name": "ブレーキ",
                    "maintain_item_alert": True
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02():
    """
    正常系　車両設定更新API
    Mock化なし
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-0000003",
        "vehicle_name": "ユーザー指定車両名12345-02-01",# 19文字以上の入力可否確認
        "managed_flag": True,
        "peripheral_identifier": "switch-02-01",
        "complete_local_name": "スイッチ-02-01",
        "registered_flag": True,
        'equipment_weight': 10,
        "vehicle_nickname": "ユーザー指定車両名02-01",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02',  path_parameters={'user_vehicle_id': '1'}, path='/vehicles')
    context = {}

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'result': True,
        'user_vehicle_id': 1,
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000003',
        'vehicle_name': 'ユーザー指定車両名12345-02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'complete_local_name': 'スイッチ-02-01',
        'equipment_weight': 10,
        "vehicle_nickname": "ユーザー指定車両名02-01",
        'purchase_shop': {
            'shop_name': 'test_shop_02-1',
            'shop_tel': '0212345678',
            'shop_location': '東京都世田谷区玉川2丁目2-2'
        },
        'bluetooth': {
            'du_serial_number': '000011',
            'du_odometer': 30
        },
        'contact': {
            'contact_title': '問合せタイトル',
            'contact_text': '問合せ本文',
            'contact_mail_address': 'test@test.com'
        },
        'maintain_setting': {
            'maintain_consciousness': '01',
            'maintain_alerts': [
                {
                    'maintain_item_code': '00002',
                    'maintain_item_name': 'タイヤ空気圧',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00003',
                    'maintain_item_name': 'タイヤ摩耗',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00004',
                    'maintain_item_name': 'チェーン動作',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00005',
                    'maintain_item_name': 'ブレーキ動作、摩耗',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00001',
                    'maintain_item_name': 'ホイール',
                    'maintain_item_alert': True},
                {
                    'maintain_item_code': '00009',
                    'maintain_item_name': '定期点検',
                    'maintain_item_alert': True
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_03(mocker):
    """
    正常系　号機番号の変更でない場合は存在チェックを行わないこと
    Mock化なし
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-0000001",
        "vehicle_name": "車両名変更",
        "managed_flag": True,
        "registered_flag": True,
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'user_vehicle_id': '1'},
                      path='/vehicles')
    context = {}

    # service.user_vehicle_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.vehicle_id_check", side_effect=BusinessError(error_code='E040'))
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'result': True,
        'user_vehicle_id': 1,
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': '車両名変更',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'complete_local_name': 'スイッチ-02-01',
        'equipment_weight': 5,
        "vehicle_nickname": "ユーザー指定車両名02-01",
        'purchase_shop': {
            'shop_name': 'test_shop_02-1',
            'shop_tel': '0212345678',
            'shop_location': '東京都世田谷区玉川2丁目2-2'
        },
        'bluetooth': {
            'du_serial_number': '000011',
            'du_odometer': 30
        },
        'contact': {
            'contact_title': '問合せタイトル',
            'contact_text': '問合せ本文',
            'contact_mail_address': 'test@test.com'
        },
        'maintain_setting': {
            'maintain_consciousness': '01',
            'maintain_alerts': [
                {
                    'maintain_item_code': '00002',
                    'maintain_item_name': 'タイヤ空気圧',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00003',
                    'maintain_item_name': 'タイヤ摩耗',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00004',
                    'maintain_item_name': 'チェーン動作',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00005',
                    'maintain_item_name': 'ブレーキ動作、摩耗',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00001',
                    'maintain_item_name': 'ホイール',
                    'maintain_item_alert': True},
                {
                    'maintain_item_code': '00009',
                    'maintain_item_name': '定期点検',
                    'maintain_item_alert': True
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_04(mocker):
    """
    正常系　車両設定更新API
    Mock化あり
    車種変更
    """
    # 入力データ
    input_body = {
        "model_code": "efgh",
        "vehicle_id": "efgh-9999999",
        "vehicle_name": "test_vehicle_nm_01",
        "managed_flag": True,
        "peripheral_identifier": "E3:69:7D:AB:8A:24",
        "complete_local_name": "スイッチ",
        "registered_flag": True,
        "equipment_weight": 5,
        "vehicle_nickname": "test_vehicle_nm_01",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02',  path_parameters={'user_vehicle_id': '1'}, path='/vehicles')
    context = {}

    # service.user_vehicle_service.get_user_vehicle のモック化
    mocker.patch("service.user_vehicle_service.get_user_vehicle", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'equipment_weight': 5,
        "vehicle_nickname": "test_vehicle_nm_01",
    })
    # service.user_vehicle_service.update_vehicle のモック化
    mocker.patch("service.user_vehicle_service.update_vehicle", return_value=1)
    # service.user_vehicle_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.get_vehicles", return_value=[
        {
            "user_vehicle_id": 1,
            "model_code": "efgh",
            "vehicle_id": "efgh-9999999",
            "vehicle_name": "ユーザ車両名_01",
            "managed_flag": True,
            "registered_flag": True,
            "peripheral_identifier": '01504101-8F5C-49B6-BC32-0C2175E07DBF',
            "complete_local_name": "スイッチ",
            'equipment_weight': 5,
            "vehicle_nickname": "test_vehicle_nm_01",
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
                        "maintain_item_code": "00001",
                        "maintain_item_name": "タイヤの空気圧",
                        "maintain_item_alert": True
                    },
                    {
                        "maintain_item_code": "00002",
                        "maintain_item_name": "ブレーキ",
                        "maintain_item_alert": True
                    }
                ]
            }
        }
    ])
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 1,
        "model_code": "efgh",
        "vehicle_id": "efgh-9999999",
        "vehicle_name": "ユーザ車両名_01",
        "managed_flag": True,
        "registered_flag": True,
        "peripheral_identifier": '01504101-8F5C-49B6-BC32-0C2175E07DBF',
        "complete_local_name": "スイッチ",
        'equipment_weight': 5,
        "vehicle_nickname": "test_vehicle_nm_01",
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
                    "maintain_item_code": "00001",
                    "maintain_item_name": "タイヤの空気圧",
                    "maintain_item_alert": True
                },
                {
                    "maintain_item_code": "00002",
                    "maintain_item_name": "ブレーキ",
                    "maintain_item_alert": True
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_05():
    """
    正常系　車両設定更新API
    Mock化なし
    車種変更あり
    """
    # 入力データ
    input_body = {
        "model_code": "zzzz",
        "vehicle_id": "zzzz-0000003",
        "vehicle_name": "ユーザー指定車両名02-01",
        "managed_flag": True,
        "peripheral_identifier": "switch-02-01",
        "complete_local_name": "スイッチ-02-01",
        "registered_flag": True,
        'equipment_weight': 10,
        "vehicle_nickname": "ユーザー指定車両名02-01",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02',  path_parameters={'user_vehicle_id': '1'}, path='/vehicles')
    context = {}

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'result': True,
        'user_vehicle_id': 1,
        'model_code': 'zzzz',
        'vehicle_id': 'zzzz-0000003',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'complete_local_name': 'スイッチ-02-01',
        'equipment_weight': 10,
        "vehicle_nickname": "ユーザー指定車両名02-01",
        'purchase_shop': {
            'shop_name': 'test_shop_02-1',
            'shop_tel': '0212345678',
            'shop_location': '東京都世田谷区玉川2丁目2-2'
        },
        'bluetooth': {
            'du_serial_number': '000011',
            'du_odometer': 30
        },
        'contact': None,
        'maintain_setting': {
            'maintain_consciousness': '01',
            'maintain_alerts': [
                {
                    'maintain_item_code': '00002',
                    'maintain_item_name': 'タイヤ空気圧',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00003',
                    'maintain_item_name': 'タイヤ摩耗',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00004',
                    'maintain_item_name': 'チェーン動作',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00005',
                    'maintain_item_name': 'ブレーキ動作、摩耗',
                    'maintain_item_alert': True
                },
                {
                    'maintain_item_code': '00001',
                    'maintain_item_name': 'ホイール',
                    'maintain_item_alert': True},
                {
                    'maintain_item_code': '00009',
                    'maintain_item_name': '定期点検',
                    'maintain_item_alert': True
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    異常系 車両設定更新API
    別車両のmanaged_flag更新時にエラー発生 → ユーザ車両TBLが更新前にロールバックされること
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-9999999",
        "vehicle_name": "test_vehicle_nm_01",
        "managed_flag": True,
        "peripheral_identifier": "E3:69:7D:AB:8A:24",
        "registered_flag": True,
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'user_vehicle_id': '2'}, path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E001",
            "message": "システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。",
            "validationErrors": None
        }
    }

    # repository.user_vehicle_repository.update_t_user_vehicle_unmanaged でエラー発生
    mocker.patch("repository.user_vehicle_repository.update_t_user_vehicle_unmanaged", side_effect=Exception)
    reload(module)

    response = put_handler(event, context)

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


def test_handler_ng_02():
    """
    異常系 車両設定更新API
    バリデーションチェック(null更新不可チェック)
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": None,
        "vehicle_id": None,
        "vehicle_name": None,
        "managed_flag": None,
        # "peripheral_identifier": None,
        # "complete_local_name": None,
        "registered_flag": None,
        "equipment_weight": None,
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': ''}, path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "managed_flag",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "registered_flag",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "user_vehicle_id",
                    "message": "validation error"
                },
                {
                    "code": "E010",
                    "field": "vehicle_id",
                    "message": "号機番号は必須入力項目です。"
                },
                {
                    "code": "E010",
                    "field": "vehicle_name",
                    "message": "車両名は必須入力項目です。"
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_03():
    """
    異常系 車両設定更新API
    バリデーションチェック(空文字チェック)
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": "",
        "vehicle_id": "",
        "vehicle_name": "",
        "managed_flag": "",
        "registered_flag": "",
        "vehicle_nickname": "",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': ''}, path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "managed_flag",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "registered_flag",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "user_vehicle_id",
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
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_04():
    """
    異常系 車両設定更新API
    バリデーションチェック
    号機番号：文字数超過エラー
    車両名：文字数超過エラー
    CompleteLocalName：文字数超過エラー
    """
    # 入力データ
    input_body = {
        "vehicle_id": "あいうえお12345123",
        "vehicle_name": "あいうえお1234512345123451234512345123451234512345123451",
        "complete_local_name": f"{'Z'*256}"
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': '123'}, path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "complete_local_name",
                    "message": "validation error"
                },
                {
                    "code": "E017",
                    "field": "vehicle_id",
                    "message": "7文字で入力してください。"
                },
                {
                    "code": "E016",
                    "field": "vehicle_name",
                    "message": "50文字以下で入力してください。"
                },
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_05():
    """
    異常系 車両設定更新API
    バリデーションチェック
    号機番号：文字数不足エラー
    車両名：文字数不足エラー
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-123456",
        "vehicle_name": "",
        "managed_flag": True,
        "peripheral_identifier": "01504101-8F5C-49B6-BC32-0C2175E07DBF",
        "registered_flag": True,
        "vehicle_nickname": "",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': '123'}, path='/vehicles')
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

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_06():
    """
    異常系 車両設定更新API
    バリデーションチェック
    号機番号：指定した形式でない
    管理対象フラグ：boolean型ではない
    スイッチ識別子：指定した形式でない
    接続登録フラグ：boolean型ではない
    装備重量：int型ではない
    """
    # 入力データ
    input_body = {
        "vehicle_id": "1234567890AB",
        "vehicle_name": "ユーザー指定車両名01-01",
        "managed_flag": "test",
        "peripheral_identifier": "漢字",
        "registered_flag": "test",
        "equipment_weight": "test",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': '123'}, path='/vehicles')
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
                    "field": "peripheral_identifier",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "registered_flag",
                    "message": "validation error"
                },
                {
                    "code": "E017",
                    "field": "vehicle_id",
                    "message": "7文字で入力してください。"
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_07():
    """
    異常系 車両設定更新API
    バリデーションチェック(文字列チェック)
    """
    # 入力データ
    input_body = {
        'vehicle_id': 0o00000000001,
        "vehicle_name": 1234,
        "peripheral_identifier": 1234,
        "complete_local_name": 1234,
        "vehicle_nickname": 1234,
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': '1'}, path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "complete_local_name",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "peripheral_identifier",
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
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_08():
    """
    異常系 車両設定更新API
    バリデーションチェック(無効な項目チェック)
    """
    # 入力データ
    input_body = {
        "model_code": "error"
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path_parameters={'user_vehicle_id': '123'}, path='/vehicles')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "model_code",
                    "message": "validation error"
                },
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value


def test_handler_ng_09(mocker):
    """
    異常系 車両設定更新API
    業務エラー(vehicle_id上4ケタ != ユーザ車両TBL.モデルコード)
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-9999999",
        "managed_flag": True,
        "registered_flag": True,
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'user_vehicle_id': '1'},
                      path='/vehicles')
    context = {}

    # service.user_vehicle_service.get_user_vehicle のモック化
    mocker.patch("service.user_vehicle_service.get_user_vehicle", return_value={
        'model_code': 'xxxx'
    })
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E043",
            'message': '型式が異なります。',
            "validationErrors": None
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 400
    assert body == expected_value


def test_handler_ng_10(mocker):
    """
    異常系 車両設定更新API
    業務エラー(ユーザメンテナンス設定 == None)
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-9999999",
        "managed_flag": True,
        "registered_flag": True,
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'user_vehicle_id': '1'},
                      path='/vehicles')
    context = {}

    # service.user_vehicle_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.get_vehicles", return_value=[
        {
            "maintain_setting": None
        }
    ])
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E042",
            'message': 'ユーザメンテナンス設定情報が存在しません。',
            "validationErrors": None
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 400
    assert body == expected_value


def test_handler_ng_11(mocker):
    """
    異常系 車両設定更新API
    業務エラー(号機番号重複登録)
    """
    # 入力データ
    input_body = {
        "vehicle_id": "abcd-9999999",
        "managed_flag": True,
        "registered_flag": True,
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02', path_parameters={'user_vehicle_id': '1'},
                      path='/vehicles')
    context = {}

    # service.user_vehicle_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.vehicle_id_check", side_effect=BusinessError(error_code='E040'))
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E040",
            'message': '入力された号機番号の車両はすでに登録されています。',
            "validationErrors": None
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 400
    assert body == expected_value


def test_handler_ng_12(mocker):
    """
    異常系　車両設定更新API
    Mock化あり
    車種コードと号機番号の不一致
    """
    # 入力データ
    input_body = {
        "model_code": "efgh",
        "vehicle_id": "abcd-9999999",
        "vehicle_name": "test_vehicle_nm_01",
        "managed_flag": True,
        "peripheral_identifier": "E3:69:7D:AB:8A:24",
        "complete_local_name": "スイッチ",
        "registered_flag": True,
        "equipment_weight": 5,
        "vehicle_nickname": "test_vehicle_nm_01",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02',  path_parameters={'user_vehicle_id': '1'}, path='/vehicles')
    context = {}

    # service.user_vehicle_service.get_user_vehicle のモック化
    mocker.patch("service.user_vehicle_service.get_user_vehicle", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'equipment_weight': 5,
        "vehicle_nickname": "test_vehicle_nm_01",
    })
    # service.user_vehicle_service.update_vehicle のモック化
    mocker.patch("service.user_vehicle_service.update_vehicle", return_value=1)
    # service.user_vehicle_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.get_vehicles", return_value=[
        {
            "user_vehicle_id": 1,
            "model_code": "efgh",
            "vehicle_id": "efgh-9999999",
            "vehicle_name": "ユーザ車両名_01",
            "managed_flag": True,
            "registered_flag": True,
            "peripheral_identifier": '01504101-8F5C-49B6-BC32-0C2175E07DBF',
            "complete_local_name": "スイッチ",
            'equipment_weight': 5,
            "vehicle_nickname": "test_vehicle_nm_01",
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
                        "maintain_item_code": "00001",
                        "maintain_item_name": "タイヤの空気圧",
                        "maintain_item_alert": True
                    },
                    {
                        "maintain_item_code": "00002",
                        "maintain_item_name": "ブレーキ",
                        "maintain_item_alert": True
                    }
                ]
            }
        }
    ])
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E043",
            'message': '型式が異なります。',
            "validationErrors": None
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 400
    assert body == expected_value


def test_handler_ng_13(mocker):
    """
    異常系　車両設定更新API
    Mock化あり
    車種コードのみを変更
    """
    # 入力データ
    input_body = {
        "model_code": "efgh",
        "vehicle_name": "test_vehicle_nm_01",
        "managed_flag": True,
        "peripheral_identifier": "E3:69:7D:AB:8A:24",
        "complete_local_name": "スイッチ",
        "registered_flag": True,
        "equipment_weight": 5,
        "vehicle_nickname": "test_vehicle_nm_01",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_02',  path_parameters={'user_vehicle_id': '1'}, path='/vehicles')
    context = {}

    # service.user_vehicle_service.get_user_vehicle のモック化
    mocker.patch("service.user_vehicle_service.get_user_vehicle", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'equipment_weight': 5,
        "vehicle_nickname": "test_vehicle_nm_01",
    })
    # service.user_vehicle_service.update_vehicle のモック化
    mocker.patch("service.user_vehicle_service.update_vehicle", return_value=1)
    # service.user_vehicle_service.get_vehicles のモック化
    mocker.patch("service.user_vehicle_service.get_vehicles", return_value=[
        {
            "user_vehicle_id": 1,
            "model_code": "efgh",
            "vehicle_id": "efgh-9999999",
            "vehicle_name": "ユーザ車両名_01",
            "managed_flag": True,
            "registered_flag": True,
            "peripheral_identifier": '01504101-8F5C-49B6-BC32-0C2175E07DBF',
            "complete_local_name": "スイッチ",
            'equipment_weight': 5,
            "vehicle_nickname": "test_vehicle_nm_01",
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
                        "maintain_item_code": "00001",
                        "maintain_item_name": "タイヤの空気圧",
                        "maintain_item_alert": True
                    },
                    {
                        "maintain_item_code": "00002",
                        "maintain_item_name": "ブレーキ",
                        "maintain_item_alert": True
                    }
                ]
            }
        }
    ])
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E043",
            'message': '型式が異なります。',
            "validationErrors": None
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 400
    assert body == expected_value
