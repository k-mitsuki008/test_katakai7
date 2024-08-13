from typing import Tuple

from common.cerberus.custom_rules import (OPTIONAL_BIRTH_DATE,
                                          OPTIONAL_MAX_HEART_RATE,
                                          OPTIONAL_NICKNAME, OPTIONAL_WEIGHT,
                                          REQUIRED_GIGYA_UID)
from common.decorator.default_api import default_api
from common.logger import Logger
from common.rds.transactional import transactional
from common.response import get_response_element
from service import user_info_service

log = Logger()

PUT_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **OPTIONAL_WEIGHT,
    **OPTIONAL_NICKNAME,
    **OPTIONAL_BIRTH_DATE,
    **OPTIONAL_MAX_HEART_RATE
}


# pylint: disable=unused-argument
@default_api(schema=PUT_SCHEMA, method='PUT')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ユーザ情報登録更新API
    """
    log.info(f'params={params}')
    gigya_uid = params['gigya_uid']
    nickname = params.get('nickname')
    weight = params.get('weight')
    birth_date = params.get('birth_date')
    max_heart_rate = params.get('max_heart_rate')

    _ = user_info_service.upsert_user_info(
        gigya_uid,
        nickname,
        weight,
        birth_date,
        max_heart_rate
    )

    result = {
        "result": True
    }
    return get_response_element(result)
