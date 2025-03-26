from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID
from service import session_service as session

log = Logger()

# cerberusのvalidation定義を設定
POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
}


# pylint: disable=unused-argument
@default_api(schema=POST_SCHEMA, method='POST')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ログアウトAPI
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]

    # t_sessionのセッション有効期限を更新
    _ = session.logout_session(gigya_uid)

    result = {
        'result': True
    }

    return get_response_element(result)
