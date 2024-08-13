import json
from importlib import import_module, reload

from common.error.not_expected_error import NotExpectedError

from tests.test_utils.utils import get_event

module = import_module('src.functions.model_codes.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 車種マスタ取得API
    """
    # 入力データ
    input_body = {}
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/model_codes')
    context = {}

    # service.model_service.get_m_modelのモック化
    mocker.patch(
        "service.model_service.get_m_model",
        return_value=[
            {
                "model_code": "abcd",
                "model_name": "CROSSCORE RC",
                'weight': 15,
                'charging_rated_output': 100.0
            }
        ]
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "model_codes": [
            {
                "model_code": "abcd",
                "model_name": "CROSSCORE RC",
                'weight': 15,
                'charging_rated_output': 100.0
            }
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02(mocker):
    """
    正常系 車種マスタ取得API
    """
    # 入力データ
    input_body = {}
    query_param = {
        'bike_radar_flag': 'True'
    }
    event = get_event(
        body=input_body,
        query_string_parameters=query_param,
        gigya_uid='test_uid_01',
        path='/model_codes')
    context = {}

    # service.model_service.get_m_modelのモック化
    mocker.patch(
        "service.model_service.get_m_model",
        return_value=[
            {
                "model_code": "abcd",
                "model_name": "CROSSCORE RC",
                'weight': 15,
                'charging_rated_output': 100.0
            }
        ]
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "model_codes": [
            {
                "model_code": "abcd",
                "model_name": "CROSSCORE RC",
                'weight': 15,
                'charging_rated_output': 100.0
            }
        ]
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    異常系 車種マスタ取得API
    """
    event = get_event(gigya_uid='test_uid_01', path='/model_codes')

    context = {}

    # service.model_service.get_m_modelのモック化
    mocker.patch(
        'service.model_service.get_m_model',
        side_effect=NotExpectedError()
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {'code': 'E001',
                   'message': 'システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。',
                   'validationErrors': None},
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 500
    assert body == expected_value


def test_handler_ng_02(mocker):
    """
    異常系 車種マスタ取得API
    """
    # 入力データ
    input_body = {}
    query_param = {
        'bike_radar_flag': '123'
    }
    event = get_event(
        body=input_body,
        query_string_parameters=query_param,
        gigya_uid='test_uid_01',
        path='/model_codes')
    context = {}

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005', 'message': 'validation error',
            'validationErrors': [
                {
                    'code': 'E007',
                    'field': 'bike_radar_flag',
                    'message': 'validation error'
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
