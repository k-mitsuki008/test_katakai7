import json
from importlib import import_module, reload

from common.error.not_expected_error import NotExpectedError

from tests.test_utils.utils import get_event

module = import_module('src.functions.route.delete_handler')
delete_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ルート削除API
    """
    # 入力データ
    route_id = '1'
    event = get_event(gigya_uid='test_uid_01', path='/route', path_parameters={'route_id': route_id})
    context = {}

    # service.route_service.delete_route のモック化
    mocker.patch("service.route_service.delete_route", return_value=None)

    reload(module)

    # common.rds.connect.DbConnection.connect, commit のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})
    mocker.patch('common.rds.connect.DbConnection.commit', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True
    }

    response = delete_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    異常系 ルート削除API
    GIGYAユニークIDとルートIDに紐づくルートが存在しない場合
    """
    # 入力データ
    route_id = '1'
    event = get_event(gigya_uid='test_uid_99', path='/route', path_parameters={'route_id': route_id})
    context = {}

    # service.route_service.delete_route のモック化
    mocker.patch("service.route_service.delete_route", side_effect=NotExpectedError)

    reload(module)

    # common.rds.connect.DbConnection.connect, commit のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})
    mocker.patch('common.rds.connect.DbConnection.commit', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        'errors': {'code': 'E001',
                   'message': 'システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。',
                   'validationErrors': None},
    }

    response = delete_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 500
    assert body == expected_value


def test_handler_ng_02():
    """
    異常系 ルート削除API
    バリデーションエラー
    """
    # 入力データ
    route_id = 'a'
    event = get_event(gigya_uid='test_uid_01', path='/route', path_parameters={'route_id': route_id})
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "route_id",
                    "message": "validation error"
                }
            ]
        }
    }

    response = delete_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
