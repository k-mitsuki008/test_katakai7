
from importlib import import_module
import pytest

from tests.test_utils.fixtures import dynamodb_setup
from tests.test_utils.utils import get_authorizer_event

module = import_module('src.functions.authorizer.handler')
handler = getattr(module, 'handler')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_handler_ok(mocker):
    """
    正常系 認可OK
    """
    # 入力データ
    event = get_authorizer_event()
    context = {}

    # testメソッド実行
    response = handler(event, context)

    # 期待しているレスポンスボディの値
    expected_value = {
        "principalId": "*",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": "ALLOW",
                    "Resource": "arn:aws:execute-api:eu-west-1:889185496976:8kl2w1h6qf/v1/POST/vehicles/12345/shop",
                }
            ]
        },
        "context": {
            "gigya_uid": "test"
        }
    }
    assert response == expected_value
