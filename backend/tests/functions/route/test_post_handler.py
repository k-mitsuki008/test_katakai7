import json
from importlib import import_module, reload

import pytest

from tests.test_utils.utils import get_event

module = import_module('src.functions.route.post_handler')
post_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 ルート登録API
    """
    # 入力データ
    input_body = {
        'user_vehicle_id': 1,
        'origin_name': 'test',
        'origin_latitude': 90.0,
        'origin_longitude': 90.0,
        'origin_place_id': 'test123',
        'destination_name': 'test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'destination_place_id': 'test123',
        'save_timestamp': '2023-10-10T10:10:10.000Z',
        'ride_date': '2023-10-23',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [
            {
                'route_type_branch_no': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_via_points': [
                    {
                        'route_via_point_place_id': 'abcde1236',
                        'route_via_point_type': '01',
                        'latitude': 90.0,
                        'longitude': 90.0
                    }
                ]
            }
        ],
        'bicycle_parking': [{
            'bicycle_parking_name': '駐輪場1',
            'bicycle_parking_distance': 123,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0,
        }]
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/route')
    context = {}

    # service.route_service.create_route のモック化
    mocker.patch(
        "service.route_service.create_route",
        return_value={
            'route_id': 123,
            'user_vehicle_id': 1,
            'save_timestamp': '2023-10-10 10:10:10.000',
            'origin_name': 'test',
            'origin_latitude': 90.0,
            'origin_longitude': 90.0,
            'origin_place_id': 'test123',
            'destination_name': 'test',
            'destination_latitude': 90.0,
            'destination_longitude': 90.0,
            'destination_place_id': 'test123',
            'ride_date': '2023-10-23',
            'weather': '001',
            'weather_icon': '001',
            'one_ways': [
                {
                    'route_type_branch_no': 1,
                    'round_trip_type_code': '10',
                    'duration': 123,
                    'distance': 123,
                    'route_type': '12',
                    'route_via_points': [
                        {
                            'route_via_point_type': '01',
                            'latitude': 90.0,
                            'longitude': 90.0,
                            'route_via_point_place_id': 'abcde1236'
                        }
                    ]
                }
            ],
            'bicycle_parking': [
                {
                    'bicycle_parking_name': '駐輪場1',
                    'bicycle_parking_distance': 123,
                    'bicycle_parking_place_id': 'abcd1234',
                    'latitude': 90.0,
                    'longitude': 90.0,
                }
            ]
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect, commit のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})
    mocker.patch('common.rds.connect.DbConnection.commit', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        'route_id': 123,
        'user_vehicle_id': 1,
        'save_timestamp': '2023-10-10 10:10:10.000',
        'origin_name': 'test',
        'origin_latitude': 90.0,
        'origin_longitude': 90.0,
        'origin_place_id': 'test123',
        'destination_name': 'test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'destination_place_id': 'test123',
        'ride_date': '2023-10-23',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [
            {
                'route_type_branch_no': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_via_points': [
                    {
                        'route_via_point_type': '01',
                        'latitude': 90.0,
                        'longitude': 90.0,
                        'route_via_point_place_id': 'abcde1236'
                    }
                ]
            }
        ],
        'bicycle_parking': [
            {
                'bicycle_parking_name': '駐輪場1',
                'bicycle_parking_distance': 123,
                'bicycle_parking_place_id': 'abcd1234',
                'latitude': 90.0,
                'longitude': 90.0,
            }
        ]
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02(mocker):
    """
    正常系 ルート登録API
    Optionalを省略その1
    """
    # 入力データ
    input_body = {
        'user_vehicle_id': 1,
        'origin_latitude': -90.0,
        'origin_longitude': -90.0,
        'destination_name': 'dst_test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'save_timestamp': '2023-10-10T10:10:10.000Z',
        'one_ways': [
            {
                'route_type_branch_no': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_via_points': [
                    {
                        'latitude': 90.0,
                        'longitude': 90.0
                    }
                ]
            }
        ],
        'bicycle_parking': [{
            'bicycle_parking_name': '駐輪場1',
            'bicycle_parking_distance': 123,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0,
        }]
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/route')
    context = {}

    # service.route_service.create_route のモック化
    mocker.patch(
        "service.route_service.create_route",
        return_value={
            'route_id': 123,
            'user_vehicle_id': 1,
            'save_timestamp': '2023-10-10 10:10:10.000',
            'origin_name': None,
            'origin_latitude': -90.0,
            'origin_longitude': -90.0,
            'origin_place_id': 'test123',
            'destination_name': 'test',
            'destination_latitude': 90.0,
            'destination_longitude': 90.0,
            'destination_place_id': 'test123',
            'ride_date': None,
            'weather': None,
            'weather_icon': None,
            'one_ways': [
                {
                    'route_type_branch_no': 1,
                    'round_trip_type_code': '10',
                    'duration': 123,
                    'distance': 123,
                    'route_type': '12',
                    'route_via_points': [
                        {
                            'route_via_point_type': None,
                            'latitude': 90.0,
                            'longitude': 90.0,
                            'route_via_point_place_id': None
                        }
                    ]
                }
            ],
            'bicycle_parking': [
                {
                    'bicycle_parking_name': '駐輪場1',
                    'bicycle_parking_distance': 123,
                    'bicycle_parking_place_id': 'abcd1234',
                    'latitude': 90.0,
                    'longitude': 90.0,
                }
            ]
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect, commit のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})
    mocker.patch('common.rds.connect.DbConnection.commit', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        'route_id': 123,
        'user_vehicle_id': 1,
        'save_timestamp': '2023-10-10 10:10:10.000',
        'origin_name': None,
        'origin_latitude': -90.0,
        'origin_longitude': -90.0,
        'origin_place_id': 'test123',
        'destination_name': 'test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'destination_place_id': 'test123',
        'ride_date': None,
        'weather': None,
        'weather_icon': None,
        'one_ways': [
            {
                'route_type_branch_no': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_via_points': [
                    {
                        'route_via_point_type': None,
                        'latitude': 90.0,
                        'longitude': 90.0,
                        'route_via_point_place_id': None
                    }
                ]
            }
        ],
        'bicycle_parking': [
            {
                'bicycle_parking_name': '駐輪場1',
                'bicycle_parking_distance': 123,
                'bicycle_parking_place_id': 'abcd1234',
                'latitude': 90.0,
                'longitude': 90.0,
            }
        ]
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_03(mocker):
    """
    正常系 ルート登録API
    Optionalを省略その2
    """
    # 入力データ
    input_body = {
        'user_vehicle_id': 1,
        'origin_name': 'org_test',
        'origin_latitude': -90.0,
        'origin_longitude': -90.0,
        'destination_name': 'dst_test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'save_timestamp': '2023-10-10T10:10:10.000Z',
        'ride_date': '2023-10-23',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [
            {
                'route_type_branch_no': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
            }
        ]
    }
    event = get_event(body=input_body, gigya_uid='test_uid_01', path='/route')
    context = {}

    # service.route_service.create_route のモック化
    mocker.patch(
        "service.route_service.create_route",
        return_value={
            'route_id': 123,
            'user_vehicle_id': 1,
            'save_timestamp': '2023-10-10 10:10:10.000',
            'origin_name': 'org_test',
            'origin_latitude': -90.0,
            'origin_longitude': -90.0,
            'origin_place_id': None,
            'destination_name': 'dst_test',
            'destination_latitude': 90.0,
            'destination_longitude': 90.0,
            'destination_place_id': None,
            'ride_date': '2023-10-23',
            'weather': '001',
            'weather_icon': '001',
            'one_ways': [
                {
                    'route_type_branch_no': 1,
                    'round_trip_type_code': '10',
                    'duration': 123,
                    'distance': 123,
                    'route_type': '12',
                    'route_via_points': [
                        {
                            'route_via_point_type': '01',
                            'latitude': 90.0,
                            'longitude': 90.0,
                            'route_via_point_place_id': 'abcde1236'
                        }
                    ]
                }
            ],
            'bicycle_parking': []
        }
    )

    reload(module)

    # common.rds.connect.DbConnection.connect, commit のモック化
    mocker.patch('common.rds.connect.DbConnection.connect', return_value={None})
    mocker.patch('common.rds.connect.DbConnection.commit', return_value={None})

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        'route_id': 123,
        'user_vehicle_id': 1,
        'save_timestamp': '2023-10-10 10:10:10.000',
        'origin_name': 'org_test',
        'origin_latitude': -90.0,
        'origin_longitude': -90.0,
        'origin_place_id': None,
        'destination_name': 'dst_test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'destination_place_id': None,
        'ride_date': '2023-10-23',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [
            {
                'route_type_branch_no': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_via_points': [
                    {
                        'route_via_point_type': '01',
                        'latitude': 90.0,
                        'longitude': 90.0,
                        'route_via_point_place_id': 'abcde1236'
                    }
                ]
            }
        ],
        'bicycle_parking': []
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


@pytest.mark.parametrize(
    ['user_vehicle_id', 'origin_name', 'origin_latitude', 'origin_longitude', 'origin_place_id', 'destination_name',
     'destination_latitude', 'destination_longitude', 'destination_place_id', 'save_timestamp', 'ride_date', 'weather',
     'weather_icon', 'one_ways', 'bicycle_parking', 'error_value_name', 'error_code', 'error_message'],
    [
        ('1', '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'user_vehicle_id', 'E007', 'validation error'),
        (1, 123, 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'origin_name', 'E007', 'validation error'),
        (1, '出発地', '90.0', 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'origin_latitude', 'E007', 'validation error'),
        (1, '出発地', 90.0, '90.0', 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'origin_longitude', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 123, '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'origin_place_id', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', 123, 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'destination_name', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', '90.0', 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'destination_latitude', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, '90.0', 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'destination_longitude', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 1234, '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'destination_place_id', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10 10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'save_timestamp', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         12344, '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'ride_date', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', 123, '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'weather', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', 123,
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'weather_icon', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         None,
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'one_ways', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': '1', 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'route_type_branch_no', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': 1, 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'round_trip_type_code', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': '123',
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'duration', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': '123', 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'distance', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': 1,
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'route_type', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': 1, 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'route_via_point_type', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 123,
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'route_via_point_place_id', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': '90.0', 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'latitude', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': '90.0'}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'longitude', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': 123, 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'bicycle_parking_name', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': '123', 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': 90.0}],
         'bicycle_parking_distance', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 123,
           'latitude': 90.0, 'longitude': 90.0}],
         'bicycle_parking_place_id', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': '90.0', 'longitude': 90.0}],
         'latitude', 'E007', 'validation error'),
        (1, '出発地', 90.0, 90.0, 'abcd123', '目的地', 90.0, 90.0, 'abcd123', '2023-10-10T10:10:10.000Z',
         '2023-10-23', '001', '001',
         [{'route_type_branch_no': 1, 'round_trip_type_code': '10', 'duration': 123,
           'distance': 123, 'route_type': '12',
           'route_via_points': [{'route_via_point_type': '01', 'route_via_point_place_id': 'abcde1236',
                                 'latitude': 90.0, 'longitude': 90.0}]}],
         [{'bicycle_parking_name': '駐輪場1', 'bicycle_parking_distance': 123, 'bicycle_parking_place_id': 'abcd1234',
           'latitude': 90.0, 'longitude': '90.0'}],
         'longitude', 'E007', 'validation error'),
    ]
)
def test_handler_ng_01(
        mocker, user_vehicle_id, origin_name, origin_latitude, origin_longitude, origin_place_id,
        destination_name, destination_latitude, destination_longitude, destination_place_id, save_timestamp,
        ride_date, weather, weather_icon, one_ways, bicycle_parking, error_value_name, error_code, error_message):
    """
    異常系 個人設定設定登録更新API
    バリデーションチェック(画面入力項目:nickname, weight, birth_date, max_heart_rate の型エラー)
    """
    # 入力データ
    input_body = {
        'user_vehicle_id': user_vehicle_id,
        'origin_name': origin_name,
        'origin_latitude': origin_latitude,
        'origin_longitude': origin_longitude,
        'origin_place_id': origin_place_id,
        'destination_name': destination_name,
        'destination_latitude': destination_latitude,
        'destination_longitude': destination_longitude,
        'destination_place_id': destination_place_id,
        'save_timestamp': save_timestamp,
        'ride_date': ride_date,
        'weather': weather,
        'weather_icon': weather_icon,
        'one_ways': one_ways,
        'bicycle_parking': bicycle_parking
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

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 422
    assert body == expected_value
