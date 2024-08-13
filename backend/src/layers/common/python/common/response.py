import os
import json

from common.utils.aws_utils import get_message
from common.error.custom_error import CustomError

API_CORS_ORIGIN: str = os.environ.get('API_CORS_ORIGIN')


def get_response_element(result: dict, status_code: int = 200, exception: Exception = None) -> tuple:
    if exception:
        if isinstance(exception, CustomError):
            return get_error_response_body(exception.error_code, exception.params), exception.status_code
        else:
            return get_error_response_body('E001'), 500

    return result, status_code


def get_validation_error_response_element(errors: list) -> tuple:
    return get_error_response_body('E005', errors=errors), 422


def get_error_response_body(code: str, params: tuple = (), errors: list = None) -> dict:
    print(f'PARAMS:{params} {code} {errors}')
    return {
        'errors': {
            'code': code,
            'message': get_message(code, '不明なエラーです。').format(*params),
            'validationErrors': errors,
        }
    }


def get_response(response_body: dict, status_code: int = 200, method: str = 'GET, POST, PUT, DELETE') -> dict:
    headers: dict = {
        'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
        'Access-Control-Allow-Origin': API_CORS_ORIGIN,
        'Access-Control-Allow-Methods': '{}, OPTIONS'.format(method),
        'Content-Type': 'application/json; charset=utf-8',
        'X-Content-Type-Options': 'nosniff',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Content-Security-Policy': 'reflected-xss block',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Referrer-Policy': 'same-origin'
    }

    response: dict = {
        'headers': headers,
        'statusCode': status_code,
        'body': json.dumps(response_body, ensure_ascii=False),
        'isBase64Encoded': False
    }

    return response
