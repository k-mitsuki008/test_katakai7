from datetime import datetime
from importlib import import_module

import pytest
from common.rds import execute_select_statement

import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.route_one_way_repository')
create_route_one_way = getattr(module, 'create_route_one_way')
delete_t_route_one_way = getattr(module, 'delete_t_route_one_way')


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_create_route_one_way_ok_01():
    """
    正常系: INSERT
    """
    expected_value = {
        'route_id': 1,
        'round_trip_type_code': '10',
        'duration': 123,
        'distance': 123,
        'route_type': '12',
        'route_type_branch_no': 1,
        'fcdyobi1': None,
        'fcdyobi2': None,
        'fcdyobi3': None,
        'fcdyobi4': None,
        'fcdyobi5': None,
        'etxyobi1': None,
        'etxyobi2': None,
        'etxyobi3': None,
        'etxyobi4': None,
        'etxyobi5': None,
        'delete_flag': False,
        'delete_timestamp': None,
        'delete_user_id': None,
        'insert_timestamp': datetime(2023, 5, 13, 12, 34, 56, 789000),
        'insert_user_id': 'new_user_1',
        'update_timestamp': None,
        'update_user_id': None
    }

    params = {
        'round_trip_type_code': '10',
        'duration': 123,
        'distance': 123,
        'route_type': '12',
        'route_type_branch_no': 1,
    }

    route_one_way_id = create_route_one_way('new_user_1', 1, **params)

    sql: str = '''
        SELECT
            *
        FROM t_route_one_way
        WHERE route_one_way_id = %(route_one_way_id)s;
    '''
    parameters_dict: dict = {
        'route_one_way_id': route_one_way_id,
    }
    results = execute_select_statement(sql, parameters_dict)
    if results:
        results[0].pop('route_one_way_id')

        assert results[0] == expected_value
    else:
        assert False


def test_delete_t_route_one_way_ok_01():
    """
    正常系: DELETE
    """
    delete_count = delete_t_route_one_way(3)
    assert delete_count == 1

    sql: str = '''
        SELECT
            count(*) as count
        FROM t_route_one_way
        WHERE route_id = %(route_id)s;
    '''
    parameters_dict = {'route_id': 3}
    results = execute_select_statement(sql, parameters_dict)
    assert results[0]['count'] == 0
