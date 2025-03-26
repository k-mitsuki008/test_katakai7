from datetime import datetime
from importlib import import_module

import pytest
from common.rds import execute_select_statement

import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.bicycle_parking_repository')
create_bicycle_parking = getattr(module, 'create_bicycle_parking')
delete_t_bicycle_parking = getattr(module, 'delete_t_bicycle_parking')


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_create_bicycle_parking_ok_01():
    """
    正常系: BULK INSERT
    """
    expected_value = [
        {
            'route_id': 2,
            'bicycle_parking_name': '駐輪場1',
            'bicycle_parking_distance': 123,
            'bicycle_parking_place_id': 'abcd1234',
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
            'insert_user_id': 'test_uid',
            'update_timestamp': None,
            'update_user_id': None
        },
        {
            'route_id': 2,
            'bicycle_parking_name': '駐輪場2',
            'bicycle_parking_distance': 124,
            'bicycle_parking_place_id': 'abcd1234',
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
            'insert_user_id': 'test_uid',
            'update_timestamp': None,
            'update_user_id': None
        },
        {
            'route_id': 2,
            'bicycle_parking_name': '駐輪場3',
            'bicycle_parking_distance': 125,
            'bicycle_parking_place_id': 'abcd1234',
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
            'insert_user_id': 'test_uid',
            'update_timestamp': None,
            'update_user_id': None
        }
    ]

    params = [
        {
            'bicycle_parking_name': '駐輪場1',
            'bicycle_parking_distance': 123,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0,
            'now_str': datetime.now()
        },
        {
            'bicycle_parking_name': '駐輪場2',
            'bicycle_parking_distance': 124,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0,
            'now_str': datetime.now()
        },
        {
            'bicycle_parking_name': '駐輪場3',
            'bicycle_parking_distance': 125,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0,
            'now_str': datetime.now()
        }
    ]

    count = create_bicycle_parking('test_uid', 2, params)

    assert count == 3

    sql: str = '''
        SELECT *
        FROM t_bicycle_parking
        WHERE route_id = %(route_id)s
        ORDER BY bicycle_parking_distance;
    '''
    inserted_info = execute_select_statement(sql, {'route_id': 2})
    for info in inserted_info:
        info.pop('bicycle_parking_id')
        info.pop('bicycle_parking_location')
    assert inserted_info == expected_value


def test_delete_t_bicycle_parking_ok_01():
    """
    正常系: DELETE
    """
    delete_count = delete_t_bicycle_parking(1)
    assert delete_count == 1

    sql: str = '''
        SELECT
            count(*) as count
        FROM t_bicycle_parking
        WHERE route_id = %(route_id)s;
    '''
    parameters_dict = {'route_id': 1}
    results = execute_select_statement(sql, parameters_dict)
    assert results[0]['count'] == 0
