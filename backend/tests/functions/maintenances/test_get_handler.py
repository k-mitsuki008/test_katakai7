import os
import json
from importlib import import_module, reload
import pytest
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.maintenances.get_handler')
get_handler = getattr(module, 'handler')


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_handler_ok_01(mocker):
    """
    正常系 メンテナンス指示詳細取得API
    Mock化なし
    """
    # 入力データ
    event = get_event(path_parameters={'maintain_item_code': '00002', 'model_code': 'abcd'}, gigya_uid='test_uid_02', path='/maintenances/abcd/00002')
    context = {}

    # 期待しているレスポンスボディの値
    cloud_front_domain_name = os.environ['CLOUD_FRONT_DOMAIN_NAME']
    expected_value = {
        "result": True,
        "maintain_item_code": "00002",
        "maintain_item_name": "タイヤ空気圧",
        "maintain_item_image_url": cloud_front_domain_name + "explanation-images/abcde00002_top.png",
        "maintain_explanations": [
            {
                "explanation_title": "前後タイヤの点検",
                "contents": [
                    {
                        "explanation_type": 1,
                        "explanation_body": "タイヤのが適切でない状態て使用をされますと、急なパンク等の危険やタイヤの路面摩擦増加により、より強い力でこぐ必要が出たり、BTの消耗が早くなるといった不利益につながる危険があります。長く安全にご使用いただくために、定期的に状態を確認してください。"
                    },
                    {
                        "explanation_type": 2,
                        "explanation_body": cloud_front_domain_name + "explanation-images/00002_01_02.png"
                    },
                    {
                        "explanation_type": 1,
                        "explanation_body": "タイヤの空気圧を点検し、不適正な場合は空気圧を調整してください。"
                    },
                    {
                        "explanation_type": 2,
                        "explanation_body": cloud_front_domain_name + "explanation-images/00002_01_04.png"
                    },
                    {
                        "explanation_type": 1,
                        "explanation_body": "空気圧は、YPJに乗車（体重60Kgの方）した状態での接地面の長さで簡易に判定することができます。"
                    }
                ]
            },
            {
                "explanation_title": "前後タイヤの点検2",
                "contents": [
                    {
                        "explanation_type": 1,
                        "explanation_body": "前後のタイヤ点検_説明2"
                    }
                ]
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
    準正常系 メンテナンス指示詳細取得API
    バリデーションチェック
    メンテナンスアイテムID：文字数オーバー
    車種コード：文字数オーバー
    """

    # 入力データ
    path_parameters = {
        "maintain_item_code": "000005",
        "model_code": "abcde"
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/maintenances/abcde/000005'
    )
    context = {}

    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "model_code",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_02(mocker):
    """
    準正常系 メンテナンス指示詳細取得API
    バリデーションチェック
    メンテナンスアイテムID：文字数不足
    車種コード：文字数不足
    """

    # 入力データ
    path_parameters = {
        "maintain_item_code": "0005",
        "model_code": "abc"
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/maintenances/abc/0005'
    )
    context = {}

    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "model_code",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_03(mocker):
    """
    準正常系 メンテナンス指示詳細取得API
    バリデーションチェック
    メンテナンスアイテムID：半角チェック
    車種コード：半角英数字チェック
    """

    # 入力データ
    path_parameters = {
        "maintain_item_code": '００００５',
        "model_code": 'ａｂｃｄ'
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/maintenances/abcd/00005'
    )
    context = {}

    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "model_code",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_04(mocker):
    """
    準正常系 メンテナンス指示詳細取得API
    バリデーションチェック
    メンテナンスアイテムID：必須項目
    車種コード：必須項目
    """

    # 入力データ
    input_body = {
        "maintain_item_code": None,
        "model_code": None
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/maintenances/a/5'
    )
    context = {}

    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "model_code",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_05(mocker):
    """
    準正常系 メンテナンス指示詳細取得API
    バリデーションチェック
    メンテナンスアイテムID：型違い
    """

    # 入力データ
    input_body = {
        "maintain_item_code": 0o0005
    }
    event = get_event(
        body=input_body,
        path_parameters={'maintain_item_code': '00005', 'model_code': 'abcd'},
        gigya_uid='test_uid_01',
        path='/maintenances/0000/5'
    )
    context = {}

    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_06(mocker):
    """
    準正常系 メンテナンス指示詳細取得API
    バリデーションチェック
    メンテナンスアイテムID：空文字入力
    車種コード：空文字入力
    """

    # 入力データ
    path_parameters = {
        "maintain_item_code": "",
        "model_code": ""
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/maintenances/'
    )
    context = {}

    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                    "code": "E007",
                    "field": "maintain_item_code",
                    "message": "validation error"
                },
                {
                    "code": "E007",
                    "field": "model_code",
                    "message": "validation error"
                }
            ]
        }
    }

    response = get_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value
