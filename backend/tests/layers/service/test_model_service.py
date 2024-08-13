from importlib import import_module, reload
import pytest
from common.error.not_expected_error import NotExpectedError
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.model_service')
get_model = getattr(module, 'get_m_model')


def test_get_m_model_ok_01(mocker):
    """
    正常系　repository関数からの取得値をそのまま返す
    """

    # repository.model_repository.get_modelのモック化
    mocker.patch(
        "repository.model_repository.get_m_model",
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

    # 期待している返却値
    expected_value = [
        {
            "model_code": "abcd",
            "model_name": "CROSSCORE RC",
            'weight': 15,
            'charging_rated_output': 100.0
        }
    ]

    data = get_model()

    assert data == expected_value


def test_get_m_model_ok_02(mocker):
    """
    正常系　bike_radar_flag=True
    """

    # repository.model_repository.get_modelのモック化
    mocker.patch(
        "repository.model_repository.get_m_model",
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

    # 期待している返却値
    expected_value = [
        {
            "model_code": "abcd",
            "model_name": "CROSSCORE RC",
            'weight': 15,
            'charging_rated_output': 100.0
        }
    ]

    data = get_model(True)

    assert data == expected_value


def test_get_m_model_ng_01(mocker):
    """
    異常系　取得できない場合 エラーを返す
    """

    # repository.model_repository.get_modelのモック化
    mocker.patch(
        "repository.model_repository.get_m_model",
        return_value={}
    )

    reload(module)

    with pytest.raises(NotExpectedError):
        get_model()
