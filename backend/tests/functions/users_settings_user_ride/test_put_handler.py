
import json
from importlib import import_module, reload
from tests.test_utils.fixtures import db_setup
from tests.test_utils.fixtures import dynamodb_setup
from tests.test_utils.utils import get_event
from common.error.not_expected_error import NotExpectedError

module = import_module('src.functions.users_settings_user_ride.put_handler')
put_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ユーザーライド設定登録更新API
    """
    # 入力データ
    input_body = {
        "battery_remind_latitude": 35.675069,
        "battery_remind_longitude": 139.763328,
        "battery_remind_cd": "02",
        "battery_remind_voice_notice": True,
        "safety_ride_alert": True,
        "long_drive_alert": True,
        "speed_over_alert": True,
        "no_light_alert": True,
        "safety_ride_voice_notice": True,
        "home_assist_mode_number": "01"
    }
    event = get_event(body=input_body, gigya_uid='test_uid_03', path='/users/settings/user-ride')
    context = {}

    # service.users_settings_service.upsert_t_user_setting_ride のモック化
    mocker.patch("service.user_setting_service.upsert_t_user_setting_ride", return_value={
        "gigya_uid": "test_uid_03",
        "battery_remind_latitude": 35.675069,
        "battery_remind_longitude": 139.763328,
        "battery_remind_cd": "01",
        "battery_remind_voice_notice": 1,
        "safety_ride_alert": 1,
        "long_drive_alert": 1,
        "speed_over_alert": 1,
        "no_light_alert": 1,
        "safety_ride_voice_notice": 1,
        "home_assist_mode_number": "01"
    })
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "battery_remind_latitude": 35.675069,
        "battery_remind_longitude": 139.763328,
        "battery_remind_cd": "01",
        "battery_remind_voice_notice": True,
        "safety_ride_alert": True,
        "long_drive_alert": True,
        "speed_over_alert": True,
        "no_light_alert": True,
        "safety_ride_voice_notice": True,
        "home_assist_mode_number": "01"
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02():
    """
    正常系 ユーザーライド設定登録更新API
    Mock化なし
    """
    # 入力データ
    input_body = {
        "battery_remind_latitude": 35.675069,
        "battery_remind_longitude": 139.763328,
        "battery_remind_cd": "02",
        "battery_remind_voice_notice": True,
        "safety_ride_alert": True,
        "long_drive_alert": True,
        "speed_over_alert": True,
        "no_light_alert": True,
        "safety_ride_voice_notice": True,
        "home_assist_mode_number": "01"
    }
    event = get_event(body=input_body, gigya_uid='test_uid_03', path='/users/settings/user-ride')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "battery_remind_latitude": 35.675069,
        "battery_remind_longitude": 139.763328,
        "battery_remind_cd": "02",
        "battery_remind_voice_notice": True,
        "safety_ride_alert": True,
        "long_drive_alert": True,
        "speed_over_alert": True,
        "no_light_alert": True,
        "safety_ride_voice_notice": True,
        "home_assist_mode_number": "01"
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01():
    """
    準正常系 ユーザーライド設定登録更新API
    バリデーションチェック
    型チェック
    """
    # 入力データ
    input_body = {
        "battery_remind_latitude": "NG",
        "battery_remind_longitude": "NG",
        "battery_remind_cd": 0o1,
        "battery_remind_voice_notice": "NG",
        "safety_ride_alert": "NG",
        "long_drive_alert": "NG",
        "speed_over_alert": "NG",
        "no_light_alert": "NG",
        "safety_ride_voice_notice": "NG",
        "home_assist_mode_number": 99
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/users/settings/user-ride')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "battery_remind_cd",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "battery_remind_latitude",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "battery_remind_longitude",
                    "message": "validation error"
                },

                {
                    "code": "E007",
                    "field": "battery_remind_voice_notice",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "home_assist_mode_number",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "long_drive_alert",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "no_light_alert",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "safety_ride_alert",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "safety_ride_voice_notice",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "speed_over_alert",
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


def test_handler_ng_02():
    """
    準正常系 ユーザーライド設定登録更新API
    バリデーションチェック
    バッテリーリマインドコード: 半角数字以外が入力された場合
    """
    # 入力データ
    input_body = {
        "battery_remind_cd": "テスト",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_03', path='/users/settings/user-ride')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "battery_remind_cd",
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


def test_handler_ng_03(mocker):
    """
    異常系 ユーザーライド設定登録更新API
    NotExpectedError発生時
    """
    # 入力データ
    input_body = {
      "battery_remind_cd": "00",
    }
    event = get_event(body=input_body, gigya_uid='test_uid_03', path='/users/settings/user-ride')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E001",
            "message": "システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。",
            "validationErrors": None
        }
    }

    # service.users_settings_service.upsert_t_user_setting_ride のモック化
    mock = mocker.patch("service.user_setting_service.upsert_t_user_setting_ride")
    mock.side_effect = NotExpectedError()
    reload(module)

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 500
    assert body == expected_value


def test_handler_ng_04():
    """
    準正常系 ユーザーライド設定登録更新API
    バリデーションチェック
    バッテリーリマインドコード: 定数マスタ以外の値が入力された場合
    ホームアシストモード: 定数マスタ以外の値が入力された場合
    """
    # 入力データ
    input_body = {
        "battery_remind_cd": "03",
        "home_assist_mode_number": "06"
    }
    event = get_event(body=input_body, gigya_uid='test_uid_03', path='/users/settings/user-ride')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "battery_remind_cd",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "home_assist_mode_number",
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
