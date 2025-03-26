import json
from importlib import import_module, reload

from tests.test_utils.fixtures import dynamodb_setup
from tests.test_utils.fixtures import db_setup
from tests.test_utils.utils import get_event

module = import_module('src.functions.user_setting.get_handler')
post_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ユーザー設定情報取得API
    """
    event = get_event(gigya_uid='test_uid_01', path='/users/settings')

    context = {}

    # device.service.get_t_user_settingのモック化
    mocker.patch(
        "service.user_setting_ride_service.get_t_user_setting_ride",
        return_value={
            "battery_remind_latitude": 35.675069,
            "battery_remind_longitude": 139.763328,
            "battery_remind_cd": "123",
            "battery_remind_voice_notice": True,
            "safety_ride_alert": True,
            "long_drive_alert": True,
            "speed_over_alert": True,
            "no_light_alert": True,
            "safety_ride_voice_notice": True,
            "home_assist_mode_number": "01"
        }
    )

    # device.service.get_t_user_shop_regularのモック化
    mocker.patch(
        "service.user_shop_regular_service.get_t_user_shop_regular",
        return_value={
            "regular_shop_name": "test_shop_01",
            "regular_shop_tel": "0312345678",
            "regular_shop_location": "東京都世田谷区玉川1丁目1-1",
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_ride": {
                "battery_remind_latitude": 35.675069,
                "battery_remind_longitude": 139.763328,
                "battery_remind_cd": "123",
                "battery_remind_voice_notice": True,
                "safety_ride_alert": True,
                "long_drive_alert": True,
                "speed_over_alert": True,
                "no_light_alert": True,
                "safety_ride_voice_notice": True,
                "home_assist_mode_number": "01"
        },
        "regular_shop": {
                "regular_shop_name": "test_shop_01",
                "regular_shop_tel": "0312345678",
                "regular_shop_location": "東京都世田谷区玉川1丁目1-1"
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02(mocker):
    """
    正常系 ユーザー設定情報取得API
    ユーザライド設定TBLにデータなし
    """
    event = get_event(gigya_uid='test_uid_01', path='/users/settings')

    context = {}

    # device.service.get_t_user_setting_rideのモック化
    mocker.patch(
        "service.user_setting_ride_service.get_t_user_setting_ride",
        return_value={
            "battery_remind_latitude": 153.9807,
            "battery_remind_longitude": 24.2867,
            "battery_remind_cd": '00',
            "battery_remind_voice_notice": False,
            "safety_ride_alert": False,
            "long_drive_alert": False,
            "speed_over_alert": False,
            "no_light_alert": False,
            "safety_ride_voice_notice": False,
            "home_assist_mode_number": '02',
        }
    )

    # device.service.get_t_user_shop_regularのモック化
    mocker.patch(
        "service.user_shop_regular_service.get_t_user_shop_regular",
        return_value={
            "regular_shop_name": "test_shop_01",
            "regular_shop_tel": "0312345678",
            "regular_shop_location": "東京都世田谷区玉川1丁目1-1",
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_ride": {
                "battery_remind_latitude": 153.9807,
                "battery_remind_longitude": 24.2867,
                "battery_remind_cd": '00',
                "battery_remind_voice_notice": False,
                "safety_ride_alert": False,
                "long_drive_alert": False,
                "speed_over_alert": False,
                "no_light_alert": False,
                "safety_ride_voice_notice": False,
                "home_assist_mode_number": '02',
        },
        "regular_shop": {
                "regular_shop_name": "test_shop_01",
                "regular_shop_tel": "0312345678",
                "regular_shop_location": "東京都世田谷区玉川1丁目1-1"
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_03():
    """
    正常系 ユーザー設定情報取得API
    ユーザライド設定TBLにデータなし
    """
    event = get_event(gigya_uid='test_uid_01', path='/users/settings')

    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_ride": {
                "battery_remind_latitude": None,
                "battery_remind_longitude": None,
                "battery_remind_cd": '00',
                "battery_remind_voice_notice": False,
                "safety_ride_alert": False,
                "long_drive_alert": False,
                "speed_over_alert": False,
                "no_light_alert": False,
                "safety_ride_voice_notice": False,
                "home_assist_mode_number": '02',
        },
        "regular_shop": {
                "regular_shop_name": "test_shop_01",
                "regular_shop_tel": "0312345678",
                "regular_shop_location": "東京都世田谷区玉川1丁目1-1"
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value
