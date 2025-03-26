from importlib import import_module

import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.spot_repository')
get_m_spot = getattr(module, 'get_m_spot')


def test_get_m_spot_ok_01():
    """
    正常系: SELECT
    """
    expected_value = [
        {
            'spot_id': 1,
            'spot_place_id': None,
            'spot_type_code': '00001',
            'spot_location': '{"type":"Point","coordinates":[35.686178921,139.70299927]}',
            'rechargeable_flag': True
        }
    ]

    latitude, longitude, radius = 35.68617892085704, 139.70299926999502, 10
    result = get_m_spot(latitude, longitude, radius)
    assert result == expected_value


def test_get_m_spot_ok_02():
    """
    正常系: SELECT 対象0件
    """
    expected_value = []

    latitude, longitude, radius = 30.68617892085704, 130.70299926999502, 10
    result = get_m_spot(latitude, longitude, radius)
    assert result == expected_value
