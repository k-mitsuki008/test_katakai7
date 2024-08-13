from importlib import import_module

import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.model_repository')
get_m_model = getattr(module, 'get_m_model')


def test_get_m_model_ok_01():
    """
    正常系: 車種TBL SELECT
    """
    expected_value = [
        {
            'charging_rated_output': 100.0,
            'model_code': 'zzzz',
            'model_name': 'DUMY_MODEL 01',
            'weight': 15
        },
        {
            'model_code': 'abcd',
            'model_name': "CROSSCORE RC",
            'weight': 15,
            'charging_rated_output': 100.0
        }
    ]

    result = get_m_model()
    assert result == expected_value


def test_get_m_model_ok_02():
    """
    正常系: 車種TBL SELECT
    """
    expected_value = [
        {
            'model_code': 'abcd',
            'model_name': "CROSSCORE RC",
            'weight': 15,
            'charging_rated_output': 100.0
        }
    ]

    result = get_m_model(True)
    assert result == expected_value


def test_get_m_model_ok_03():
    """
    正常系: 車種TBL SELECT
    """
    expected_value = [
        {
            'charging_rated_output': 100.0,
            'model_code': 'zzzz',
            'model_name': 'DUMY_MODEL 01',
            'weight': 15
        },
        {
            'model_code': 'abcd',
            'model_name': "CROSSCORE RC",
            'weight': 15,
            'charging_rated_output': 100.0
        }
    ]

    result = get_m_model(False)
    assert result == expected_value
