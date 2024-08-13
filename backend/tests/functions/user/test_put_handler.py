import json
from importlib import import_module, reload

import pytest

from tests.test_utils.utils import get_event

module = import_module('src.functions.user.put_handler')
put_handler = getattr(module, 'handler')


def test_handler_ok(mocker):
    """
    正常系 個人設定設定登録更新API
    """
    # 入力データ
    input_body = {
        'nickname': 'test_user_01',
        'weight': 60,
        'birth_date': '1990-01-01',
        'max_heart_rate': 100
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/user')
    context = {}

    # service.user_info_service.upsert_user_info のモック化
    mocker.patch("service.user_info_service.upsert_user_info", return_value={})

    reload(module)

    # common.rds.connect.DbConnection.connect, commit のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})
    mocker.patch('common.rds.connect.DbConnection.commit', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


@pytest.mark.parametrize(
    ['nickname', 'weight', 'birth_date', 'max_heart_rate', 'error_value_name', 'error_code', 'error_message'],
    [
        (10, 100, '2000-01-01', 150, 'nickname', 'E007', 'validation error'),
        ('てすと', '100', '2000-01-01', 150, 'weight', 'E007', 'validation error'),
        ('てすと', 100, 20000101, 150, 'birth_date', 'E007', 'validation error'),
        ('てすと', 100, '2000-01-01', '150', 'max_heart_rate', 'E007', 'validation error')
    ]
)
def test_handler_ng_01(
        mocker, nickname, weight, birth_date, max_heart_rate, error_value_name, error_code, error_message):
    """
    異常系 個人設定設定登録更新API
    バリデーションチェック(画面入力項目:nickname, weight, birth_date, max_heart_rate の型エラー)
    """
    # 入力データ
    input_body = {
        'nickname': nickname,
        'weight': weight,
        'birth_date': birth_date,
        'max_heart_rate': max_heart_rate
    }

    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/user')
    context = {}

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {
            'code': 'E005', 'message': 'validation error',
            'validationErrors': [
                {
                    'code': error_code,
                    'field': error_value_name,
                    'message': error_message
                }
            ]
        }
    }

    response = put_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
