from datetime import date, datetime
from importlib import import_module

import pytest
from common.rds import execute_select_statement

import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.route_repository')
get_t_route = getattr(module, 'get_t_route')
get_t_route_by_gigya_uid = getattr(module, 'get_t_route_by_gigya_uid')
create_route = getattr(module, 'create_route')
delete_t_route = getattr(module, 'delete_t_route')
update_route = getattr(module, 'update_route')
get_joined_route = getattr(module, 'get_joined_route')


def test_get_t_route_ok_01():
    """
    正常系: SELECT
    """
    expected_value = 1
    result = get_t_route(gigya_uid='test_uid_2', route_id=1)
    assert result == expected_value


def test_get_t_route_by_gigya_uid_ok_01():
    """
    正常系: SELECT
    """
    expected_value = [
        {
            'route_id': 1,
            'user_vehicle_id': 2,
            'save_timestamp': datetime(2023, 9, 13, 11, 27, 46, 642000),
            'destination_name': '虎ノ門ヒルズ森タワー',
            'destination_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
            'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
            'ride_date': date(2023, 10, 2),
            'weather': '001',
            'weather_icon': '001',
            'one_ways': [
                {
                    'distance': 100,
                    'duration': 100,
                    'round_trip_type_code': '11'
                },
                {
                    'distance': 110,
                    'duration': 110,
                    'round_trip_type_code': '12'
                }
            ]
        },
        {
            'route_id': 2,
            'user_vehicle_id': 2,
            'save_timestamp': datetime(2023, 9, 12, 11, 27, 46, 642000),
            'destination_name': '虎ノ門ヒルズ森タワー',
            'destination_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
            'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
            'ride_date': date(2023, 10, 2),
            'weather': '001',
            'weather_icon': '001',
            'one_ways': [
                {
                    'distance': 120,
                    'duration': 120,
                    'round_trip_type_code': '10'
                }
            ]
        }
    ]
    result = get_t_route_by_gigya_uid(gigya_uid='test_uid_2')
    assert result == expected_value


def test_get_t_route_by_gigya_uid_ok_02():
    """
    正常系: SELECT 対象0件
    """
    expected_value = []

    result = get_t_route_by_gigya_uid(gigya_uid='test_uid_9')
    assert result == expected_value


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_create_route_ok_01():
    """
    正常系: INSERT
    """
    expected_value = {
        'gigya_uid': 'new_user_1',
        'user_vehicle_id': 2,
        'save_timestamp': datetime(2023, 9, 12, 11, 27, 46, 642000),
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': date(2023, 10, 2),
        'weather': '001',
        'weather_icon': '001',
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
        'user_vehicle_id': 2,
        'save_timestamp': datetime(2023, 9, 12, 11, 27, 46, 642000),
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_latitude': 35.667009003,
        'origin_longitude': 139.749387112,
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_latitude': 35.667009003,
        'destination_longitude': 139.749387112,
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': date(2023, 10, 2),
        'weather': '001',
        'weather_icon': '001'
    }

    route_id = create_route('new_user_1', **params)

    sql: str = '''
        SELECT
            *
        FROM t_route
        WHERE gigya_uid = %(gigya_uid)s
        AND route_id = %(route_id)s;
    '''
    parameters_dict: dict = {
        'gigya_uid': 'new_user_1',
        'route_id': route_id,
    }
    results = execute_select_statement(sql, parameters_dict)
    if results:
        results[0].pop('route_id')
        results[0].pop('origin_location')
        results[0].pop('destination_location')

        assert results[0] == expected_value
    else:
        assert False


def test_delete_t_route_ok_01():
    """
    正常系: DELETE
    """
    delete_count = delete_t_route(gigya_uid='test_uid_2', route_id=6)
    assert delete_count == 1

    sql: str = '''
        SELECT
            count(*) as count
        FROM t_route
        WHERE gigya_uid = %(gigya_uid)s
            AND route_id = %(route_id)s;
    '''
    parameters_dict = {'gigya_uid': 'test_uid_2', 'route_id': 6}
    results = execute_select_statement(sql, parameters_dict)
    assert results[0]['count'] == 0


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_update_route_ok_01():
    """
    正常系: UPDATE
    """
    expected_value = {
        'gigya_uid': 'test_uid_2',
        'user_vehicle_id': 2,
        'save_timestamp': datetime(2023, 9, 12, 11, 27, 46, 642000),
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': date(2023, 10, 2),
        'weather': '001',
        'weather_icon': '001',
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
        'insert_timestamp': None,
        'insert_user_id': None,
        'update_timestamp': datetime(2023, 5, 13, 12, 34, 56, 789000),
        'update_user_id': 'test_uid_2',
    }

    params = {
        'user_vehicle_id': 2,
        'save_timestamp': datetime(2023, 9, 12, 11, 27, 46, 642000),
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_latitude': 35.667009003,
        'origin_longitude': 139.749387112,
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_latitude': 35.667009003,
        'destination_longitude': 139.749387112,
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': date(2023, 10, 2),
        'weather': '001',
        'weather_icon': '001'
    }

    route_id = update_route('test_uid_2', 1, **params)

    sql: str = '''
        SELECT
            *
        FROM t_route
        WHERE gigya_uid = %(gigya_uid)s
        AND route_id = %(route_id)s;
    '''
    parameters_dict: dict = {
        'gigya_uid': 'test_uid_2',
        'route_id': route_id,
    }
    results = execute_select_statement(sql, parameters_dict)

    if results:
        results[0].pop('route_id')
        results[0].pop('origin_location')
        results[0].pop('destination_location')

        assert results[0] == expected_value
    else:
        assert False


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_get_joined_route_ok_01():
    """
    正常系: GET
    """
    expected_value = {
        'route_id': 3,
        'user_vehicle_id': 2,
        'save_timestamp': datetime(2023, 9, 12, 11, 27, 46, 642000),
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': date(2023, 10, 2),
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [{
            'route_one_way_id': 13,
            'round_trip_type_code': '10',
            'duration': 123,
            'distance': 123,
            'route_type': '11',
            'route_type_branch_no': 1
        }],
        'bicycle_parking': None
    }

    results = get_joined_route('test_uid_3', 3)

    assert results == expected_value


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_get_joined_route_ok_02():
    """
    正常系: GET
    """
    expected_value = {
        'route_id': 4,
        'user_vehicle_id': 2,
        'save_timestamp': datetime(2023, 9, 12, 11, 27, 46, 642000),
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': date(2023, 10, 2),
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [{
            'route_one_way_id': 14,
            'round_trip_type_code': '10',
            'duration': 123,
            'distance': 123,
            'route_type': '12',
            'route_type_branch_no': 1,
            'route_via_points': [{
                'route_via_point_type': '01',
                'route_via_point_id': 2,
                'route_via_point_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
                'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }]
        }],
        'bicycle_parking': [{
            'bicycle_parking_id': 2,
            'bicycle_parking_name': 'テスト駐輪場',
            'bicycle_parking_distance': 100,
            'bicycle_parking_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
            'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
        }]
    }

    results = get_joined_route('test_uid_4', 4)

    assert results == expected_value


@pytest.mark.freeze_time('2023-05-13 12:34:56.789101')
def test_get_joined_route_ok_03():
    """
    正常系: GET
    """
    expected_value = {
        'route_id': 5,
        'user_vehicle_id': 2,
        'save_timestamp': datetime(2023, 9, 12, 11, 27, 46, 642000),
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': date(2023, 10, 2),
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [{
            'route_one_way_id': 15,
            'round_trip_type_code': '10',
            'duration': 123,
            'distance': 123,
            'route_type': '21',
            'route_type_branch_no': 1,
            'route_via_points': [
                {
                    'route_via_point_type': '01',
                    'route_via_point_id': 3,
                    'route_via_point_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
                    'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
                },
                {
                    'route_via_point_id': 4,
                    'route_via_point_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
                    'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
                }
            ]
        }],
        'bicycle_parking': [{
            'bicycle_parking_id': 3,
            'bicycle_parking_name': 'テスト駐輪場',
            'bicycle_parking_distance': 100,
            'bicycle_parking_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
            'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
        }, {
            'bicycle_parking_id': 4,
            'bicycle_parking_name': 'テスト駐輪場',
            'bicycle_parking_distance': 100,
            'bicycle_parking_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
            'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
        }]
    }

    results = get_joined_route('test_uid_5', 5)

    assert results == expected_value
