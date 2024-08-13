import json
import re
from functools import wraps
from typing import Tuple

from common.response import get_validation_error_response_element
from common.response import get_response_element
from common.response import get_response
from common.cerberus import validate
from common.stack_trace import get_stack_trace
from common.logger import Logger
from common.rds.connect import DbConnection
from common.aws.dynamodb import DynamoDb

log: any = Logger()

# 型変換対象パラメータ
CAST_PARAMS = {
    "user_vehicle_id",
    "maintain_history_id",
    "upload_file_counts",
    "limit",
    "offset",
    "bookmark_flg",
    "latitude",
    "longitude",
    "radius",
    "route_id",
    "bike_radar_flag"
}


def default_api(schema: dict, method: str = 'POST') -> Tuple[dict, int]:
    def decorator(func: any) -> any:
        @wraps(func)
        def decorated(*args: any) -> any:

            # daynamoDb定数クラスの初期化
            dynm_db = DynamoDb()
            dynm_db.set_data()

            log.info('event => ')
            log.info(args[0])

            # リクエストのパース処理
            params, headers = parse_request(args[0])
            log.info('parameter => ')
            log.info(params)

            # バリデーションチェック
            is_validated, validate_response, status_code = validate_params(schema, params)
            if not is_validated:
                log.info('response => ')
                log.info(validate_response)
                return get_response(validate_response, status_code=status_code, method=method)
            dc = DbConnection()
            try:

                # DBに接続する
                dc.connect()
                # handler関数を実行
                handler_response, status_code = func(params, headers)

            except Exception as e:  # pylint: disable=broad-except
                log.error(get_stack_trace())
                handler_response, status_code = get_response_element({}, exception=e)

            finally:
                # DBとの接続を切る
                dc.close()

            log.info('response => ')
            log.info(handler_response)

            return get_response(handler_response, status_code=status_code, method=method)

        return decorated

    return decorator


def parse_request(event: any) -> Tuple[dict, dict]:
    # リクエストに設定された、クエリ文字列を取得する
    query_dict: dict = event.get('queryStringParameters') if event.get('queryStringParameters') else {}
    # リクエストに設定された、パスパラメータを取得する
    query_dict.update(event.get('pathParameters') if event.get('pathParameters') else {})
    # クエリパラメータの型を変換する
    for k, v in query_dict.items():
        if re.fullmatch(r'\d+\.\d+', v) is not None and k in CAST_PARAMS:
            query_dict[k] = float(v)
        if re.fullmatch(r'\d+', v) is not None and k in CAST_PARAMS:
            query_dict[k] = int(v)
        if v.lower() in ["true", "false"] and k in CAST_PARAMS:
            query_dict[k] = v.lower() in ["true"]

    # リクエストに設定された、リクエストボディを取得する
    request_body_dict: dict = json.loads(event.get("body")) if event.get("body") else {}

    # authorizerで取得したgigya_uidを取得する
    gigya_uid = event.get('requestContext', {}).get('authorizer', {}).get('gigya_uid')
    log.info(f'gigya_uid = {gigya_uid}')
    gigya_uid_dict: dict = {'gigya_uid': gigya_uid}

    # headerからuser_agentを取得して、dictにパースする
    headers = event.get('headers', {})
#    user_agent = _parse_user_agent(event.get('headers', {}).get('User-Agent', ''))

    return {**query_dict, **request_body_dict, **gigya_uid_dict}, headers


def validate_params(schema: dict, params: dict) -> tuple:
    errors: list = validate(schema, params)

    if errors:
        log.info('バリデーションチェックNG')
        response_body, status_code = get_validation_error_response_element(errors)
        return False, response_body, status_code

    return True, {}, 200
