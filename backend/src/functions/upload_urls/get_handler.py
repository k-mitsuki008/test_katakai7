from typing import Tuple

from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_UPLOAD_FILE_COUNTS
from service import upload_file_service

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_UPLOAD_FILE_COUNTS,
}


@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    画像アップロードURL取得API
    """
    log.info(f'params={params}')
    gigya_uid = params["gigya_uid"]
    upload_file_counts = params["upload_file_counts"]

    upload_urls = upload_file_service.get_upload_urls(gigya_uid, upload_file_counts)
    result: dict = {
        "result": True,
        "upload_urls": upload_urls
    }

    return get_response_element(result)
