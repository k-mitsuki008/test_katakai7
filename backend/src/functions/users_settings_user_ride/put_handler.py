from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
import common.cerberus.setting.basic_rules as br
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, OPTIONAL_BATTERY_REMIND_CD, OPTIONAL_HOME_ASSIST_MODE_NUMBER
from service import user_setting_service as user_setting

log = Logger()

# cerberusのvalidation定義を設定
PUT_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    "battery_remind_latitude": {**br.OPTIONAL_LATITUDE},
    "battery_remind_longitude": {**br.OPTIONAL_LONGITUDE},
    **OPTIONAL_BATTERY_REMIND_CD,
    "battery_remind_voice_notice": {**br.OPTIONAL_COMMON_BOOLEAN},
    "safety_ride_alert": {**br.OPTIONAL_COMMON_BOOLEAN},
    "long_drive_alert": {**br.OPTIONAL_COMMON_BOOLEAN},
    "speed_over_alert": {**br.OPTIONAL_COMMON_BOOLEAN},
    "no_light_alert": {**br.OPTIONAL_COMMON_BOOLEAN},
    "safety_ride_voice_notice": {**br.OPTIONAL_COMMON_BOOLEAN},
    **OPTIONAL_HOME_ASSIST_MODE_NUMBER,
}


@default_api(schema=PUT_SCHEMA, method='PUT')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ユーザーライド設定登録更新API
    """
    log.info(f'params={params}')
    gigya_uid = params.pop('gigya_uid')
    upsert_data = user_setting.upsert_t_user_setting_ride(gigya_uid, **params)
    # pylint: disable-next=unsupported-delete-operation
    del upsert_data['gigya_uid']

    result = {
        "result": True,
        **upsert_data
    }

    return get_response_element(result)
