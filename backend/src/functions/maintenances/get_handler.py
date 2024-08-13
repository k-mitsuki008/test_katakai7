from typing import Tuple

from common.logger import Logger
from common.response import get_response_element
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_MODEL_CD, REQUIRED_MAINTAIN_ITEM_CODE
from service import maintain_item_service

log = Logger()

GET_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_MODEL_CD,
    **REQUIRED_MAINTAIN_ITEM_CODE
}


@default_api(schema=GET_SCHEMA, method='GET')
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    メンテナンス指示詳細取得API
    """
    log.info(f'params={params}')
    model_code = params["model_code"]
    maintain_item_code = params["maintain_item_code"]

    maintain_explanation = maintain_item_service.get_maintain_explanation(model_code, maintain_item_code)

    result = {
        "result": True,
        ** maintain_explanation
    }

    return get_response_element(result)
