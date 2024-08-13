import json
from typing import Tuple

import tests.test_utils.fixtures as fixtures
from common.cerberus.custom_rules import (REQUIRED_CATEGORY_ID,
                                          REQUIRED_GIGYA_UID)
from common.decorator.default_api import default_api
from common.error.custom_error import CustomError
from common.response import get_response_element
from tests.test_utils.utils import get_event

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

POST_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_CATEGORY_ID
}

POST_SCHEMA2: dict = {
    **REQUIRED_GIGYA_UID,
    **{
        'user_vehicle_id': {
            'required': True,
            'empty': False
        },
        'maintain_history_id': {
            'required': True,
            'empty': False
        }
    }
}


@default_api(schema=POST_SCHEMA, method='POST')
def sample_handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    result = {
        'result': 'ok'
    }
    return get_response_element(result)


@default_api(schema=POST_SCHEMA2, method='POST')
def sample_handler2(params: dict, headers: dict = None) -> Tuple[dict, int]:
    result = {
        'result': 'ok'
    }
    return get_response_element(result)


@default_api(schema=POST_SCHEMA, method='POST')
def sample_handler_ng_custom_error(params: dict, headers: dict = None) -> Tuple[dict, int]:
    e = CustomError()
    e.error_code = 'E001'
    e.status_code = 500
    raise e


@default_api(schema=POST_SCHEMA, method='POST')
def sample_handler_ng_key_error(params: dict, headers: dict = None) -> Tuple[dict, int]:
    e = KeyError()
    raise e


def test_sample_handler_ok_01():

    """
    正常系
    """

    # 入力データ
    event = get_event(body={'categoryId': 1}, gigya_uid='test_uid_01')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        'result': 'ok'
    }

    # pylint: disable-next=too-many-function-args
    response = sample_handler(event, context)
    # pylint: disable-next=no-member
    status_code = response.get('statusCode')
    # pylint: disable-next=no-member
    body = json.loads(response.get('body'))

    assert status_code == 200
    assert body == expected_value


def test_sample_handler_ok_02():

    """
    正常系
    クエリパラメーターが設定されている場合
    """

    # 入力データ
    query_params = {'user_vehicle_id': '123', 'maintain_history_id': 'true'}
    event = get_event(query_string_parameters=query_params, gigya_uid='test_uid_01')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        'result': 'ok'
    }

    response = sample_handler2(event, context)
    # pylint: disable-next=no-member
    status_code = response.get('statusCode')
    # pylint: disable-next=no-member
    body = json.loads(response.get('body'))

    assert status_code == 200
    assert body == expected_value


def test_sample_handler_ng_validation_error():

    """
    準正常系
    ※ バリデーションエラーが発生した時の応答確認
    """

    # 入力データ
    event = get_event(body={}, path='/sample', gigya_uid='test_uid_01')
    context = {}

    # pylint: disable-next=too-many-function-args
    response = sample_handler(event, context)
    # pylint: disable-next=no-member
    status_code = response.get('statusCode')
    # pylint: disable-next=no-member
    body = json.loads(response.get('body'))

    assert status_code == 422
    assert body['errors']['code'] == 'E005'
    assert body['errors']['message'] == 'validation error'
    assert body['errors']['validationErrors'] == [{'code': 'E006', 'field': 'categoryId', 'message': 'missing field'}]


def test_sample_handler_ng_custom_error():

    """
    準正常系
    ※ CustomErrorが発生した時の応答確認
    """

    # 入力データ
    event = get_event(body={'categoryId': 1}, path='/sample', gigya_uid='test_uid_01')
    context = {}

    # pylint: disable-next=too-many-function-args
    response = sample_handler_ng_custom_error(event, context)
    # pylint: disable-next=no-member
    status_code = response.get('statusCode')
    # pylint: disable-next=no-member
    body = json.loads(response.get('body'))

    assert status_code == 500
    assert body['errors']['code'] == 'E001'
    assert body['errors']['message'] == 'システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。'
    assert not body['errors']['validationErrors']


def test_sample_handler_ng_error():

    """
    異常系
    ※ 想定外エラーが発生した時の応答確認
    """

    # 入力データ
    event = get_event(body={'categoryId': 1}, path='/sample', gigya_uid='test_uid_01')
    context = {}

    # pylint: disable-next=too-many-function-args
    response = sample_handler_ng_key_error(event, context)
    # pylint: disable-next=no-member
    status_code = response.get('statusCode')
    # pylint: disable-next=no-member
    body = json.loads(response.get('body'))

    assert status_code == 500
    assert body['errors']['code'] == 'E001'
    assert body['errors']['message'] == 'システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。'
    assert not body['errors']['validationErrors']
