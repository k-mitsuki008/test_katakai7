import json
from importlib import import_module
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.logout.post_handler')
handler = getattr(module, 'handler')


def test_handler_ok():
    """
    正常系 ログアウトAPI
    """
    # 入力データ
    input_body = {}
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/logout')
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
    }

    response = handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value
