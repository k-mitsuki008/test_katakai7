import json
from importlib import import_module, reload
import pytest
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
from common.rds import execute_insert_statement
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles_maintenances_histories_detail.post_handler')
post_handler = getattr(module, 'handler')


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ok_01(mocker):
    """
    正常系 メンテナンス記録登録API
    Mock化あり
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-02",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
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
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories'
    )
    context = {}

    # device.service.user_vehicle_id_is_existのモック化
    mocker.patch(
        "service.user_vehicle_service.user_vehicle_id_is_exist",
        return_value={}
    )

    # service.maintain_history_service.insert_maintain_historyのモック化
    mocker.patch("service.maintain_history_service.insert_maintain_history", return_value=123)

    # service.maintain_history_service.get_t_maintain_historyのモック化
    mocker.patch("service.maintain_history_service.get_maintain_history", return_value={
        "maintain_history_id": 123,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            None,
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2"
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
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            None,
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2"
        ]
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    # assert status_code == 200
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ok_02():
    """
    正常系 メンテナンス記録登録API
    Mock化なし
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00002",
        "maintain_implement_date": "2023-02-01",
        "du_serial_number": "000011",
        "du_last_odometer": 5,
        "du_last_timestamp": "2023-02-01T12:00:00.000Z",
        "maintain_location": "メンテナンス場所_01",
        "maintain_cost": 1000,
        "maintain_required_time": 10,
        "maintain_memo": "memo_タイヤ空気圧",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_02',
        path='/vehicles/1/maintenances/histories'
    )
    context = {}
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "maintain_history_id": 13,
        "maintain_item_code": "00002",
        "maintain_implement_date": "2023-02-01",
        "du_serial_number": "000011",
        "du_last_odometer": 5,
        "du_last_timestamp": "2023-02-01T12:00:00.000Z",
        "maintain_location": "メンテナンス場所_01",
        "maintain_cost": 1000,
        "maintain_required_time": 10,
        "maintain_memo": "memo_タイヤ空気圧",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        ]
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_01():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック 必須入力項目チェック
    　ユーザ車両ID             : None
    　メンテナンス項目CD        : None
    　実施日                  : None
    　DU_serial_number       : None
    　DU最終接続Odometer      : None
    　DU最終接続タイムスタンプ  : None
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
        "du_serial_number": None,
        "du_last_odometer": None,
        "du_last_timestamp": None,
        "maintain_location": None,
        "maintain_cost": None,
        "maintain_required_time": None,
        "maintain_memo": None,
        "maintain_image_ids": None,
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': ''},
        gigya_uid='test_uid_01',
        path='/vehicles//maintenances/histories'
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
                    "field": "du_last_odometer",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "du_last_timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "du_serial_number",
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
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_02():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック 空文字チェック
    　ユーザ車両ID             : ""
    　メンテナンス項目CD       : ""
    　実施日                   : ""
    　DU_serial_number         : ""
    　DU最終接続Odometer       : ""
    　DU最終接続タイムスタンプ : ""
    　画像id                   : ""
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "",
        "maintain_implement_date": "",
        "du_serial_number": "",
        "du_last_odometer": "",
        "du_last_timestamp": "",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": ""
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': ''},
        gigya_uid='test_uid_01',
        path='/vehicles//maintenances/histories'
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
                    "field": "du_last_odometer",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "du_last_timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "du_serial_number",
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

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_03():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック 型チェック
    　ユーザ車両ID            : validation error（整数値以外）
    　メンテナンス項目CD       : validation error（半角数字以外）
    　実施日                 : validation error（日付以外）
    　DU_serial_number      : validation error（半角英数字以外）
    　DU最終接続Odometer     : validation error（整数値以外）
    　DU最終接続タイムスタンプ  : validation error（日時以外）
    　費用(任意入力)          : 半角数字で入力してください。
    　所要時間(分)(任意入力)   : 半角数字で入力してください。
    　画像id                 : validation error（リスト以外）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "NG",
        "maintain_implement_date": "2023/06/01",
        "du_serial_number": "あいうえお",
        "du_last_odometer": "NG",
        "du_last_timestamp": "NG",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": "NG",
        "maintain_required_time": "NG",
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": "test"
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': 'NG'},
        gigya_uid='test_uid_01',
        path='/vehicles/NG/maintenances/histories'
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
                    "field": "du_last_odometer",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "du_last_timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "du_serial_number",
                    "message": "validation error"
                },
                {
                    "code": "E019",
                    "field": "maintain_cost",
                    "message": "半角数字で入力してください。"
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

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_04():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック 型チェック
    　画像id : validation error（リスト内要素の入力形式が不正）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
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
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories'
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

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_05():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック サイズ超過
    　メンテナンス項目CD       : validation error（半角数字6文字以上）
    　DU_serial_number       : validation error（半角数字51文字以上）
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
        "du_serial_number": "111111111122222222223333333333444444444455555555556",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
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
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories'
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
                    "field": "du_serial_number",
                    "message": "validation error"
                },
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

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_06():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック サイズ超過
    　画像id : validation error（リスト内要素の文字数が37以上）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
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
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories'
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

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_07():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック サイズ不足
    　メンテナンス項目CD       : validation error（半角数字4文字以下）
    　DU_serial_number      : validation error（半角数字0文字以下）
    　費用                   : 0以上で入力してください。
    　所要時間(分)            : 0以上で入力してください。
    　画像id                 : validation error（リストが2以下）
    """
    input_body = {
        "maintain_item_code": "1234",
        "maintain_implement_date": "2023-06-01",
        "du_serial_number": "",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
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
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories'
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
                    "field": "du_serial_number",
                    "message": "validation error"
                },
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

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_08():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック サイズ不足
    　画像id : validation error（リスト内要素の文字数が35以下）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-01",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
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
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories'
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

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_09():
    """
    業務エラーチェック: メンテナンス実施日が重複
    """
    sql = '''
    INSERT INTO t_maintain_history(
        maintain_history_id
        , gigya_uid
        , user_vehicle_id
        , maintain_item_code
        , model_code
        , maintain_implement_date
        , maintain_location
        , maintain_cost
        , maintain_required_time
        , maintain_memo
        , maintain_du_serial_number
        , maintain_du_last_timestamp
        , maintain_du_last_odometer
        , maintain_image_ids
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    (13,'test_uid_02',1,'00002', 'abcd','2023/06/01','メンテナンス場所_01',1000,10,'memo_タイヤ空気圧', '000011','2022/06/01 12:00:00.000', 5,'test1,test2,test3', '2020/05/13 12:34:56.789','test_uid_01');
    '''
    execute_insert_statement(sql)
    # 入力データ
    input_body = {
        "maintain_item_code": "00002",
        "maintain_implement_date": "2023-06-01",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            None,
            "",
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_02',
        path='/vehicles/1/maintenances/histories'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E044",
            "message": "1回目のメンテナンス記録を編集してください。",
            "validationErrors": None
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 400
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_10():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック 文字列チェック
    """
    # 入力データ
    input_body = {
        "maintain_item_code": 1234,
        "maintain_implement_date": 1234,
        "du_serial_number": 1234,
        "du_last_timestamp": 1234,
        "maintain_location": 1234,
        "maintain_memo": 1234,
        "du_last_odometer": 1,
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            None,
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
        ]
    }
    event = get_event(
        body=input_body,
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories'
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
                    "field": "du_last_timestamp",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "du_serial_number",
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

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_11():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック メンテナンス実施日（未来日入力）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2023-06-03",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
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
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E051",
                    "field": "maintain_implement_date",
                    "message": "メンテナンス実施日には本日以前の日付を入力してください。"
                }
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_handler_ng_12():
    """
    準正常系 メンテナンス記録登録API
    バリデーションチェック メンテナンス実施日（2023/01/01より前の日付入力）
    """
    # 入力データ
    input_body = {
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-12-31",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2023-06-01T12:34:56.789Z",
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
        path_parameters={'user_vehicle_id': '1'},
        gigya_uid='test_uid_01',
        path='/vehicles/1/maintenances/histories'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E052",
                    "field": "maintain_implement_date",
                    "message": "入力できない日付です。"
                }
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value
