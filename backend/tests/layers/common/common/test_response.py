import os

from common.error.custom_error import CustomError
from common.response import get_response_element, get_response, get_validation_error_response_element

API_CORS_ORIGIN = os.environ.get('API_CORS_ORIGIN')


class TestResponse:

    def test_get_response_element_ok_01(self):
        """
        正常系
        result
        """
        res = {
            'key': 'value'
        }
        result, status_code = get_response_element(res)
        assert res == result
        assert 200 == status_code

    def test_get_response_element_ok_02(self):
        """
        正常系
        result、status_code
        """

        res = {
            'key': 'value'
        }
        st_code = 400
        result, status_code = get_response_element(res, st_code)
        assert res == result
        assert st_code == status_code

    def test_get_response_element_ng_01(self):
        """
        準正常系
        result、status_code、params
        """

        err_code = 'E001'
        st_code = 500
        params = ('テスト', 1)
        res = {
            'key': 'value'
        }
        expect = {
            'errors': {
                'code': err_code,
                'message': 'システムエラーが発生しました。\n'
                           '時間をあけて再度操作をお願いいたします。',
                'validationErrors': None
            }
        }
        error = CustomError(err_code, st_code, params)
        result, status_code = get_response_element(res, st_code, error)
        assert expect == result
        assert st_code == status_code

    def test_get_response_element_ng_02(self):
        """
        準正常系
        result、status_code、err_code
        """

        err_code = Exception('E001')
        st_code = 500
        res = {
            'key': 'value'
        }
        expect = {
            'errors': {
                'code': 'E001',
                'message': 'システムエラーが発生しました。\n'
                           '時間をあけて再度操作をお願いいたします。',
                'validationErrors': None
            }
        }
        result, status_code = get_response_element(res, st_code, err_code)
        assert expect == result
        assert st_code == status_code

    def test_get_validation_error_response_element(self):
        """
        正常系
        err_code
        """

        err_code = ['E005']
        expect = {
            'errors': {
                'code': "E005",
                'message': 'validation error',
                'validationErrors': err_code
            }
        }
        result, status_code = get_validation_error_response_element(err_code)
        assert expect == result
        assert 422 == status_code

    def test_get_response_ok_01(self):
        """
        正常系
        デフォルト
        """

        body = {
            'key': 'テスト'
        }
        expect = {
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token', 
                'Access-Control-Allow-Origin': API_CORS_ORIGIN, 
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Content-Type': 'application/json; charset=utf-8',
                'X-Content-Type-Options': 'nosniff',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Content-Security-Policy': 'reflected-xss block',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                'Referrer-Policy': 'same-origin'
            },
            'statusCode': 200,
            'body': '{"key": "テスト"}',
            'isBase64Encoded': False
        }
        actual = get_response(body)
        assert expect == actual

    def test_get_response_ok_02(self):
        """
        正常系
        値更新
        """

        status_code = 400
        body = {
            'key': 'テスト'
        }
        method = 'GET, POST'
        expect = {
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token', 
                'Access-Control-Allow-Origin': API_CORS_ORIGIN, 
                'Access-Control-Allow-Methods': "{}, OPTIONS".format(method),
                'Content-Type': 'application/json; charset=utf-8',
                'X-Content-Type-Options': 'nosniff',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache',
                'Content-Security-Policy': 'reflected-xss block',
                'X-Frame-Options': 'DENY',
                'X-XSS-Protection': '1; mode=block',
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                'Referrer-Policy': 'same-origin'
            },
            'statusCode': status_code,
            'body': '{"key": "テスト"}',
            'isBase64Encoded': False
        }
        actual = get_response(body, status_code, method)
        assert expect == actual
