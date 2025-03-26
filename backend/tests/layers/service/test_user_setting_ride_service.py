from importlib import import_module, reload
import pytest

from decimal import Decimal
from common.error.not_expected_error import NotExpectedError
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.user_setting_ride_service')
get_t_user_setting_ride = getattr(module, 'get_t_user_setting_ride')
insert_t_user_setting_ride = getattr(module, 'insert_t_user_setting_ride')
delete_t_user_setting_ride = getattr(module, 'delete_t_user_setting_ride')


def test_get_t_user_setting_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    """
    # tasks.repository.get_t_user_setting_ride のモック化
    mocker.patch(
        "repository.user_setting_ride_repository.get_t_user_setting_ride",
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
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = {
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

    gigya_uid = 'test01'
    data = get_t_user_setting_ride(gigya_uid)

    assert data == expected_value


def test_insert_t_user_setting_ride_ok(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    """
    # tasks.repository.insert_t_user_setting_ride のモック化
    mocker.patch(
        "repository.user_setting_ride_repository.insert_t_user_setting_ride",
        return_value=0
    )
    # tasks.repository.get_t_user_shop_purchase のモック化
    mocker.patch(
        "repository.user_setting_ride_repository.get_t_user_setting_ride",
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
    reload(module)

    # 期待している返却値
    expected_value = {
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

    gigya_uid = 'test01'
    recs = {
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
    updated_data = insert_t_user_setting_ride(gigya_uid, **recs)

    assert updated_data == expected_value


def test_insert_tasks_ng_not_expected_error_01(mocker):
    """
    準正常系: insert_t_user_setting_rideでエラー
    ※ Exception → NotExpectedError に変換されること
    """

    # tasks.repository.insert_t_user_setting_ride のモック化
    mocker.patch(
        "repository.user_setting_ride_repository.insert_t_user_setting_ride",
        side_effect=Exception
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        insert_t_user_setting_ride(9999, **{})


def test_get_t_user_setting_ride_ok_01(mocker):
    """
    正常系
    get_t_user_setting_rideでデータ取得出来ない場合
    ※ repository関数からの取得値をそのまま返す
    """
    # tasks.repository.insert_t_user_setting_ride のモック化
    mocker.patch(
        "repository.user_setting_ride_repository.insert_t_user_setting_ride",
        return_value=0
    )
    # tasks.repository.get_t_user_shop_purchase のモック化
    mocker.patch(
        "repository.user_setting_ride_repository.get_t_user_setting_ride",
        return_value=None
    )
    reload(module)

    # 期待している返却値
    expected_value = {
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
    }

    gigya_uid = 'test01'
    get_data = get_t_user_setting_ride(gigya_uid)

    assert get_data == expected_value


def test_get_t_user_setting_ride_ng_01(mocker):
    """
    異常系　ユーザーデータの更新が出来なかった場合
    NotExpectedError
    """
    # tasks.repository.insert_t_user_setting_ride のモック化
    mocker.patch(
        "repository.user_setting_ride_repository.insert_t_user_setting_ride",
        return_value=0
    )
    # tasks.repository.get_t_user_shop_purchase のモック化
    mocker.patch(
        "repository.user_setting_ride_repository.get_t_user_setting_ride",
        return_value=None
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        insert_t_user_setting_ride(9999, **{})


def test_delete_t_user_setting_ride_ok_01(mocker):
    """
    正常系: ユーザデータ DELETE
    """
    # repository.user_setting_ride_repository.delete_t_user_setting_ride のモック化
    mocker.patch("repository.user_setting_ride_repository.delete_t_user_setting_ride", return_value=1)
    # repository.user_shop_regular_repository.delete_t_user_shop_regular のモック化
    mocker.patch("repository.user_shop_regular_repository.delete_t_user_shop_regular", return_value=1)
    reload(module)

    # 期待している返却値
    expected_value = None
    gigya_uid = 'test_uid_01'

    result = delete_t_user_setting_ride(gigya_uid)

    assert result == expected_value


def test_delete_t_user_setting_ride_ok_02(mocker):
    """
    正常系: ユーザデータ DELETE
    """
    # repository.user_setting_ride_repository.delete_t_user_setting_ride のモック化
    mocker.patch("repository.user_setting_ride_repository.delete_t_user_setting_ride", return_value=None)
    # repository.user_shop_regular_repository.delete_t_user_shop_regular のモック化
    mocker.patch("repository.user_shop_regular_repository.delete_t_user_shop_regular", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = None
    gigya_uid = 'test_uid_01'

    result = delete_t_user_setting_ride(gigya_uid)

    assert result == expected_value
