import pytest
import tests.test_utils.fixtures as fixtures
from common.decorator.default_batch import default_batch
from common.error.custom_error import CustomError
from common.response import get_response_element
from tests.test_utils.utils import get_event

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup


@default_batch()
def sample_handler(params: dict) -> dict:
    result = {
        'result': 'ok'
    }
    return get_response_element(result)


@default_batch()
def sample_handler_ng_custom_error(params: dict) -> dict:
    e = CustomError()
    e.error_code = 'E001'
    e.status_code = 500
    raise e


def test_sample_handler_ok():

    """
    正常系
    """

    # 入力データ
    event = get_event()

    # 期待しているレスポンスボディの値
    expected_value = ({'result': 'ok'}, 200)

    response = sample_handler(event)

    assert response == expected_value


def test_sample_handler_ng_error():

    """
    異常系
    ※ 想定外エラーが発生した時の応答確認
    """

    # 入力データ
    event = get_event()

    with pytest.raises(Exception):
        sample_handler_ng_custom_error(event)
