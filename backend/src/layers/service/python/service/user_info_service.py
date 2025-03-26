from common.decorator.service import service
from common.logger import Logger
from repository import radar_user_info_setting_repository

log = Logger()


@service
def get_user_info(gigya_uid) -> dict:
    user_setting_info = radar_user_info_setting_repository.get_user_info_setting(gigya_uid)

    result = {
        'nickname': user_setting_info.get('nickname'),
        'weight': user_setting_info.get('weight'),
        'birth_date': (str(user_setting_info.get('birth_date'))
                       if user_setting_info.get('birth_date') is not None else None),
        'max_heart_rate': user_setting_info.get('max_heart_rate')
    }

    return result


@service
def upsert_user_info(gigya_uid, nickname, weight, birth_date, max_heart_rate):

    # 登録/更新値設定
    params = {
        'nickname': nickname,
        'weight': weight,
        'birth_date': birth_date,
        'max_heart_rate': max_heart_rate
    }
    convert_params = {key: value for key, value in params.items() if value is not None}

    _ = radar_user_info_setting_repository.upsert_user_info_setting(gigya_uid, **convert_params)

    return {}
