from importlib import import_module

import pytest
from common.rds import execute_select_statement

import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.route_via_point_repository')
create_route_via_points = getattr(module, 'create_route_via_points')
delete_t_route_via_point = getattr(module, 'delete_t_route_via_point')


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_create_route_via_points_ok_01():
    """
    正常系: BULK INSERT
    """

    params = [
        {
            'route_via_point_place_id': 'abcde1234',
            'latitude': 90.0,
            'longitude': 90.0
        },
        {
            'route_via_point_place_id': 'abcde1235',
            'latitude': 90.0,
            'longitude': 90.0
        },
        {
            'latitude': 90.0,
            'longitude': 90.0
        }
    ]

    count = create_route_via_points('test_uid', 1, 10, params)

    assert count == 3


def test_delete_t_route_via_point_ok_01():
    """
    正常系: DELETE
    """
    delete_count = delete_t_route_via_point(1)
    assert delete_count == 1

    sql: str = '''
        SELECT
            count(*) as count
        FROM t_route_via_point
        WHERE route_id = %(route_id)s;
    '''
    parameters_dict = {'route_id': 1}
    results = execute_select_statement(sql, parameters_dict)
    assert results[0]['count'] == 0
