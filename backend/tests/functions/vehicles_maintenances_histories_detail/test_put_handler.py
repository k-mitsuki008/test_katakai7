import json
from importlib import import_module, reload
import pytest
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles_maintenances_histories_detail.put_handler')
put_handler = getattr(module, 'handler')


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ok_01(mocker):
    """
    正常系 メンテナンス記録更新API
    Mock化あり
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
                "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
                None,
                "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1', 'maintain_history_id': '123'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
    )
    context = {}

    # device.service.user_vehicle_id_is_existのモック化
    mocker.patch(
        "service.user_vehicle_service.user_vehicle_id_is_exist",
        return_value={}
    )

    # service.maintain_history_service.update_maintain_historyのモック化
    mocker.patch("service.maintain_history_service.update_maintain_history")
    # service.maintain_history_service.get_t_maintain_historyのモック化
    mocker.patch("service.maintain_history_service.get_maintain_history", return_value={
        "maintain_history_id": 123,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            None,
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
        ]
    })
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "maintain_history_id": 123,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            None,
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
        ]
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ok_02():
    """
    正常系 メンテナンス記録更新API
    Mock化なし
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00002",
        "maintain_implement_date": "2023-06-01",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
                "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
                "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
                "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1', 'maintain_history_id': '1'},
        gigya_uid='test_uid_02',
        path='/vehicles/1/maintenances/histories/1'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "maintain_history_id": 1,
        "maintain_item_code": "00002",
        "maintain_implement_date": "2023-06-01",
        "du_serial_number": "000011",
        "du_last_odometer": 5,
        "du_last_timestamp": "2022-05-11T12:00:00.000Z",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        ]
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_01():
    """
    準正常系 メンテナンス記録更新API
    バリデーションチェック 必須入力項目チェック
    　ユーザ車両ID             : None
      メンテナンス履歴ID        : None
    　メンテナンス項目CD        : None
    　実施日                  : None
    　実施場所(任意入力)       : None
    　費用(任意入力)          : None
    　所要時間(分)(任意入力)   : None
    　備考(任意入力)          : None
    　メンテナンス記録画像IDリスト(配列) : None
    """
    # 入力データ
    input_body = {
        "user_vehicle_id": None,
        "maintain_item_code": None,
        "maintain_implement_date": None,
        "maintain_location": None,
        "maintain_cost": None,
        "maintain_required_time": None,
        "maintain_memo": None,
        "maintain_image_ids": None,
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '', 'maintain_history_id': ''},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
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
                    "field": "maintain_image_ids",
                    "message": "validation error"
                },
                {
                    "code": "E010",
                    "field": "maintain_implement_date",
                    "message": "日付は必須入力項目です。"
                },
                {
                    "code": "E007",
                    "field": "maintain_item_code",
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

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_02():
    """
    準正常系 メンテナンス記録更新API
    バリデーションチェック 空文字チェック
    　ユーザ車両ID             : ""
    　メンテナンス履歴ID       : ""
    　メンテナンス項目CD       : ""
    　実施日                   : ""
    　画像id                   : ""
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "",
        "maintain_implement_date": "",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": ""
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '', 'maintain_history_id': ''},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
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
                    "field": "maintain_image_ids",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_implement_date",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_item_code",
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

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_03():
    """
    準正常系 メンテナンス記録更新API
    バリデーションチェック 型チェック
    　ユーザ車両ID            : validation error（整数値以外）
    　メンテナンス履歴ID       : validation error（整数値以外）
    　メンテナンス項目CD       : validation error（半角数字以外）
    　実施日                 : validation error（日付以外）
    　費用(任意入力)          : 半角数字で入力してください。
    　所要時間(分)(任意入力)   : 半角数字で入力してください。
    　画像id                 : validation error（リスト以外）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "NG",
        "maintain_implement_date": "2023/06/01",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": "NG",
        "maintain_required_time": "NG",
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": "test"
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': 'NG', 'maintain_history_id': 'NG'},
        gigya_uid='test_uid_01',
        path='/vehicles/NG/maintenances/histories/NG'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E019",
                    "field": "maintain_cost",
                    "message": "半角数字で入力してください。"
                },
                {
                    "code": "E007",
                    "field": "maintain_history_id",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_image_ids",
                    "message": "validation error"
                },
                {
                    "code": "E009",
                    "field": "maintain_implement_date",
                    "message": "日付の形式が無効です。"
                },
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E019",
                    "field": "maintain_required_time",
                    "message": "半角数字で入力してください。"
                },
                {
                    "code": "E007",
                    "field": "user_vehicle_id",
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


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_04():
    """
    準正常系 メンテナンス記録更新API
    バリデーションチェック 型チェック
    　画像id : validation error（リスト内要素の入力形式が不正）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            12345678-1234-1234-1234-123456789012,
            12345678-1234-1234-1234-123456789012,
            12345678-1234-1234-1234-123456789012
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1', 'maintain_history_id': '123'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
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
                    "field": "maintain_image_ids",
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


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_05():
    """
    準正常系 メンテナンス記録更新API
    バリデーションチェック サイズ超過
    　メンテナンス項目CD       : validation error（半角数字6文字以上）
    　メンテナンス場所         : 30文字以下で入力してください。
    　費用                   : 10000000以下で入力してください。
    　所要時間(分)            : 100000以下で入力してください。
    　備考                   : 2000文字以下で入力してください。
    　画像id                 : validation error（リストが4以上）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "123456",
        "maintain_implement_date": "2023-06-01",
        "maintain_location": f"{'Z'*31}",
        "maintain_cost": 10000001,
        "maintain_required_time": 100001,
        "maintain_memo": f"{'あ'*1000}{'a'*1001}",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX4"
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1', 'maintain_history_id': '123'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E032",
                    "field": "maintain_cost",
                    "message": "10000000以下で入力してください。"
                },
                {
                    "code": "E007",
                    "field": "maintain_image_ids",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E016",
                    "field": "maintain_location",
                    "message": "30文字以下で入力してください。"
                },
                {
                    "code": "E016",
                    "field": "maintain_memo",
                    "message": "2000文字以下で入力してください。"
                },
                {
                    "code": "E032",
                    "field": "maintain_required_time",
                    "message": "100000以下で入力してください。"
                },
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_06():
    """
    準正常系 メンテナンス記録更新API
    バリデーションチェック サイズ超過
    　画像id : validation error（リスト内要素の文字数が37以上）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXNG1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXNG2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXNG3"
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1', 'maintain_history_id': '123'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
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
                    "field": "maintain_image_ids",
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


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_07():
    """
    準正常系 メンテナンス記録更新API
    バリデーションチェック サイズ不足
    　メンテナンス項目CD       : validation error（半角数字4文字以下）
    　費用                   : 0以上で入力してください。
    　所要時間(分)            : 0以上で入力してください。
    　画像id                 : validation error（リストが2以下）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "1234",
        "maintain_implement_date": "2023-06-01",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": -1,
        "maintain_required_time": -1,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2"
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1', 'maintain_history_id': '123'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E033",
                    "field": "maintain_cost",
                    "message": "0以上で入力してください。"
                },
                {
                    "code": "E007",
                    "field": "maintain_image_ids",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E033",
                    "field": "maintain_required_time",
                    "message": "0以上で入力してください。"
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_08():
    """
    準正常系 メンテナンス記録更新API
    バリデーションチェック サイズ不足
    　画像id : validation error（リスト内要素の文字数が35以下）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXNG1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXNG2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXNG3"
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1', 'maintain_history_id': '123'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
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
                    "field": "maintain_image_ids",
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


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_09():
    """
    準正常系 メンテナンス記録更新API
    バリデーションチェック 文字列チェック
    """
    # 入力データ
    input_body = {
        "maintain_item_code": 1234,
        "maintain_implement_date": 1234,
        "maintain_location": 1234,
        "maintain_memo": 1234,
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1', 'maintain_history_id': '123'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
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
                    "field": "maintain_implement_date",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_location",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "maintain_memo",
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


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_10():
    """
    異常系: ユーザ車両ID存在チェックNG
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
                "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
                None,
                "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '999', 'maintain_history_id': '123'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories/123'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E042",
            "message": "ユーザ車両IDが存在しません。",
            "validationErrors": None
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 400
    assert body == expected_value
