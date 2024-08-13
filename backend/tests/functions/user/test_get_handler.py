import json
from importlib import import_module, reload

from tests.test_utils.utils import get_event

module = import_module('src.functions.user.get_handler')
get_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ユーザー設定情報取得API
    """
    event = get_event(gigya_uid='test_uid_02', path='/user')

    context = {}

    # service.user_info_service.get_user_infoのモック化
    mocker.patch(
        'service.user_info_service.get_user_info',
        return_value={
            'nickname': 'nickname',
            'weight': 60,
            'birth_date': '2000-01-01',
            'max_heart_rate': 150
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        'result': True,
        'nickname': 'nickname',
        'weight': 60,
        'birth_date': '2000-01-01',
        'max_heart_rate': 150
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    異常系 ユーザー設定情報取得API
    バリデーションチェック(不正項目連携)
    """
    event = get_event(body={'ng_key': 'ng_value'}, gigya_uid='test_uid_02', path='/user')
    context = {}

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005',
            'message': 'validation error',
            'validationErrors': [
                {
                    'code': 'E007',
                    'field': 'ng_key',
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
