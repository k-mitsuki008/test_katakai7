from common.decorator.service import service
from common.error.not_expected_error import NotExpectedError
from repository import user_setting_ride_repository as repository
from repository import user_shop_regular_repository
from common.utils.aws_utils import get_constant


@service
def insert_t_user_setting_ride(gigya_uid: str, **kwargs) -> int:
    _ = repository.insert_t_user_setting_ride(gigya_uid, **kwargs)

    insert_result = repository.get_t_user_setting_ride(gigya_uid)
    if not insert_result:
        raise NotExpectedError()

    return insert_result


@service
def get_t_user_setting_ride(gigya_uid: str) -> dict:

    result = repository.get_t_user_setting_ride(gigya_uid)
    if not result:

        battery_remind_latitude = None
        battery_remind_longitude = None
        battery_remind_cd = get_constant('INIT_VALUE', code='BATTERY_REMIND_CD')
        battery_remind_voice_notice = get_constant('INIT_VALUE', code='BATTERY_REMIND_VOICE_NOTICE')
        safety_ride_alert = get_constant('INIT_VALUE', code='SAFETY_RIDE_ALERT')
        long_drive_alert = get_constant('INIT_VALUE', code='LONG_DRIVE_ALERT')
        speed_over_alert = get_constant('INIT_VALUE', code='SPEED_OVER_ALERT')
        no_light_alert = get_constant('INIT_VALUE', code='NO_LIGHT_ALERT')
        safety_ride_voice_notice = get_constant('INIT_VALUE', code='SAFETY_RIDE_VOICE_NOTICE')
        home_assist_mode_number = get_constant('INIT_VALUE', code='HOME_ASSIST_MODE_NUMBER')

        result = {
            'battery_remind_latitude': battery_remind_latitude,
            'battery_remind_longitude': battery_remind_longitude,
            'battery_remind_cd': battery_remind_cd,
            'battery_remind_voice_notice': battery_remind_voice_notice,
            'safety_ride_alert': safety_ride_alert,
            'long_drive_alert': long_drive_alert,
            'speed_over_alert': speed_over_alert,
            'no_light_alert': no_light_alert,
            'safety_ride_voice_notice': safety_ride_voice_notice,
            'home_assist_mode_number': home_assist_mode_number,
        }
        repository.insert_t_user_setting_ride(gigya_uid, **result)
    return result


@service
def delete_t_user_setting_ride(gigya_uid: str) -> None:
    # ユーザライド設定テーブル削除処理
    _ = repository.delete_t_user_setting_ride(gigya_uid)

    # ユーザ普段利用店舗テーブル削除処理
    _ = user_shop_regular_repository.delete_t_user_shop_regular(gigya_uid)

    return
