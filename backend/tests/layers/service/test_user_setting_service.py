from importlib import import_module, reload
import pytest
from common.error.not_expected_error import NotExpectedError

module = import_module('service.user_setting_service')
upsert_t_user_setting_ride = getattr(module, 'upsert_t_user_setting_ride')


def test_upsert_t_user_setting_ride_ok(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    """
    # repository.user_setting_repository.upsert_t_user_setting_ride のモック化
    mocker.patch("repository.user_setting_repository.upsert_t_user_setting_ride", return_value=0)
    # repository.user_setting_repository.get_t_user_setting_ride のモック化
    mocker.patch("repository.user_setting_repository.get_t_user_setting_ride", return_value={
        'gigya_uid': 'test_uid_02',
        'battery_remind_latitude': 35.123456,
        'battery_remind_longitude': 139.123456,
        'battery_remind_cd': '02',
        'battery_remind_voice_notice': True,
        "safety_ride_alert": True,
        'long_drive_alert': True,
        'speed_over_alert': False,
        'no_light_alert': False,
        'safety_ride_voice_notice': False,
        'home_assist_mode_number': '02'
    })
    reload(module)

    # 期待している返却値
    expected_value = {
        'gigya_uid': 'test_uid_02',
        'battery_remind_latitude': 35.123456,
        'battery_remind_longitude': 139.123456,
        'battery_remind_cd': '02',
        'battery_remind_voice_notice': True,
        "safety_ride_alert": True,
        'long_drive_alert': True,
        'speed_over_alert': False,
        'no_light_alert': False,
        'safety_ride_voice_notice': False,
        'home_assist_mode_number': '02'
    }

    gigya_uid = 'test_uid_01'
    recs = {
        'battery_remind_latitude': 35.123456,
        'battery_remind_longitude': 139.123456,
        'battery_remind_cd': '02',
        'battery_remind_voice_notice': True,
        "safety_ride_alert": True,
        'long_drive_alert': True,
        'speed_over_alert': False,
        'no_light_alert': False,
        'safety_ride_voice_notice': False,
        'home_assist_mode_number': '02'
    }
    updated_data = upsert_t_user_setting_ride(gigya_uid, **recs)

    assert updated_data == expected_value


def test_get_tasks_ng_not_expected_error_01(mocker):
    """
    準正常系: upsert_t_user_setting_rideでエラー
    ※ @serviceでException → NotExpectedError に変換されること
    """
    # repository.user_setting_repository.upsert_t_user_setting_ride のモック化
    mocker.patch("repository.user_setting_repository.upsert_t_user_setting_ride", side_effect=Exception)
    reload(module)

    with pytest.raises(NotExpectedError) as e:
        ret = upsert_t_user_setting_ride('test_uid_01', **{})
        assert ret is None


def test_get_tasks_ng_not_expected_error_02(mocker):
    """
    準正常系: get_t_user_setting_rideでNoneが返却
    ※ @serviceでException → NotExpectedError に変換されること
    """
    # repository.user_setting_repository.upsert_t_user_setting_ride のモック化
    mocker.patch("repository.user_setting_repository.upsert_t_user_setting_ride", return_value=0)
    # repository.user_setting_repository.get_t_user_setting_ride のモック化
    mocker.patch("repository.user_setting_repository.get_t_user_setting_ride", return_value=None)
    reload(module)

    with pytest.raises(NotExpectedError) as e:
        ret = upsert_t_user_setting_ride('test_uid_01', **{})
        assert ret is None
