from typing import Tuple
from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.utils.time_utils import get_current_datetime, replace_time
from datetime import timedelta

from service import ride_history_service

from common.cerberus.custom_rules import (
    REQUIRED_GIGYA_UID,
    BEGIN,
    END,
    BOOKMARK_FLG,
    LIMIT,
    OFFSET,
)

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **BEGIN,
    **END,
    **BOOKMARK_FLG,
    **LIMIT,
    **OFFSET,
}


@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ライド一覧取得API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    limit = params.get("limit", 30)
    offset = params.get("offset", 0)
    begin = params.get('begin', None)
    end = params.get('end', None)
    bookmark_flg = params.get('bookmark_flg', None)

    if not begin:
        # 本日から30日前の日付を代入
        begin = (get_current_datetime() - timedelta(days=30)).isoformat(timespec="milliseconds") + "Z"

    if not end:
        # 本日の日付を代入
        end = get_current_datetime().isoformat(timespec="milliseconds") + "Z"

    ride_data = ride_history_service.get_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end,
        bookmark_flg,
    )
    result: dict = {
        "result": True,
        **ride_data,
    }
    return get_response_element(result)
