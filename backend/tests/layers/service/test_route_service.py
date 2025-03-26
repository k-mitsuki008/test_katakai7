from datetime import date, datetime
from importlib import import_module, reload

import pytest

from common.error.business_error import BusinessError
from common.error.not_expected_error import NotExpectedError

module = import_module('service.route_service')
get_route_list = getattr(module, 'get_route_list')
create_route = getattr(module, 'create_route')
delete_route = getattr(module, 'delete_route')
update_route = getattr(module, 'update_route')
get_route = getattr(module, 'get_route')


def test_get_route_list_ok_01(mocker):
    """
    正常系
    """

    # repository.route_repository.get_t_route_by_gigya_uidのモック化
    mocker.patch(
        "repository.route_repository.get_t_route_by_gigya_uid",
        return_value=[
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
                    },
                    {
                        'distance': 110,
                        'duration': 110,
                        'round_trip_type_code': '90'
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
    )

    reload(module)

    # 期待している返却値
    expected_value = [
        {
            'route_id': 1,
            'user_vehicle_id': 2,
            'save_timestamp': '2023-09-13T11:27:46.642000Z',
            'destination_name': '虎ノ門ヒルズ森タワー',
            'latitude': 35.667009003,
            'longitude': 139.749387112,
            'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
            'ride_date': '2023-10-02',
            'weather': '001',
            'weather_icon': '001',
            'distance': 210,
            'duration': 210
        },
        {
            'route_id': 2,
            'user_vehicle_id': 2,
            'save_timestamp': '2023-09-12T11:27:46.642000Z',
            'destination_name': '虎ノ門ヒルズ森タワー',
            'latitude': 35.667009003,
            'longitude': 139.749387112,
            'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
            'ride_date': '2023-10-02',
            'weather': '001',
            'weather_icon': '001',
            'distance': 240,
            'duration': 240
        }
    ]
    result = get_route_list(gigya_uid='test_uid_2')
    assert result == expected_value


def test_get_route_list_ok_02(mocker):
    """
    正常系 取得結果が0件の場合
    """

    # repository.route_repository.get_t_route_by_gigya_uidのモック化
    mocker.patch(
        "repository.route_repository.get_t_route_by_gigya_uid",
        return_value=[]
    )

    reload(module)

    # 期待している返却値
    expected_value = []

    result = get_route_list(gigya_uid='test_uid_9')
    assert result == expected_value


def test_create_route_ok_01(mocker):
    """
    正常系 ルート登録
    """

    m_route = mocker.patch(
        "repository.route_repository.create_route",
        return_value=123
    )

    m_route_one_way = mocker.patch(
        "repository.route_one_way_repository.create_route_one_way",
        return_value=123
    )

    m_route_via_point = mocker.patch(
        "repository.route_via_point_repository.create_route_via_points",
        return_value=1
    )

    m_bicycle_parking = mocker.patch(
        "repository.bicycle_parking_repository.create_bicycle_parking",
        return_value=1
    )

    # repository.route_repository.get_joined_routeのモック化
    mocker.patch(
        "repository.route_repository.get_joined_route",
        return_value={
            'route_id': 1,
            'user_vehicle_id': 1,
            'save_timestamp': datetime(2023, 10, 10, 10, 10, 10, 000000),
            'origin_name': 'test',
            'origin_location': '{"type":"Point","coordinates":[90.0,90.0]}',
            'origin_place_id': 'test123',
            'destination_name': 'test',
            'destination_location': '{"type":"Point","coordinates":[90.0,90.0]}',
            'destination_place_id': 'test123',
            'ride_date': date(2023, 10, 23),
            'weather': '001',
            'weather_icon': '001',
            'one_ways': [{
                'route_one_way_id': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [{
                    'route_via_point_id': 1,
                    'route_via_point_type': '01',
                    'route_via_point_location': '{"type":"Point","coordinates":[90.0,90.0]}',
                    'route_via_point_place_id': 'abcde1236'
                }]
            }],
            'bicycle_parking': [{
                'bicycle_parking_id': 1,
                'bicycle_parking_name': '駐輪場1',
                'bicycle_parking_distance': 100,
                'bicycle_parking_location': '{"type":"Point","coordinates":[90.0,90.0]}',
                'bicycle_parking_place_id': 'abcd1234',
            }]
        }
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        'route_id': 1,
        'user_vehicle_id': 1,
        'origin_name': 'test',
        'origin_latitude': 90.0,
        'origin_longitude': 90.0,
        'origin_place_id': 'test123',
        'destination_name': 'test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'destination_place_id': 'test123',
        'save_timestamp': '2023-10-10T10:10:10Z',
        'ride_date': '2023-10-23',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [
            {
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
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
        'bicycle_parking': [
            {
                'bicycle_parking_name': '駐輪場1',
                'bicycle_parking_distance': 100,
                'latitude': 90.0,
                'longitude': 90.0,
                'bicycle_parking_place_id': 'abcd1234'
            }
        ]
    }

    params = {
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
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
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
            'longitude': 90.0
        }]
    }

    result = create_route(gigya_uid='test_uid_9', **params)

    route_params = {
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
        'weather_icon': '001'
    }
    m_route.assert_called_with('test_uid_9', **route_params)

    route_one_way_params = {
        'round_trip_type_code': '10',
        'duration': 123,
        'distance': 123,
        'route_type': '12',
        'route_type_branch_no': 1,
    }
    m_route_one_way.assert_called_with('test_uid_9', 123, **route_one_way_params)

    route_via_points_params = [
        {
            'route_via_point_type': '01',
            'route_via_point_place_id': 'abcde1236',
            'latitude': 90.0,
            'longitude': 90.0
        }
    ]
    m_route_via_point.assert_called_with('test_uid_9', 123, 123, route_via_points_params)

    bicycle_parking_params = [
        {
            'bicycle_parking_name': '駐輪場1',
            'bicycle_parking_distance': 123,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0
        }
    ]
    m_bicycle_parking.assert_called_with('test_uid_9', 123, bicycle_parking_params)
    assert result == expected_value


def test_create_route_ok_02(mocker):
    """
    正常系 ルート登録
    駐輪場情報が存在しない場合
    """

    m_route = mocker.patch(
        "repository.route_repository.create_route",
        return_value=123
    )

    m_route_one_way = mocker.patch(
        "repository.route_one_way_repository.create_route_one_way",
        return_value=123
    )

    m_route_via_point = mocker.patch(
        "repository.route_via_point_repository.create_route_via_points",
        return_value=1
    )

    # repository.route_repository.get_joined_routeのモック化
    mocker.patch(
        "repository.route_repository.get_joined_route",
        return_value={
            'route_id': 1,
            'user_vehicle_id': 1,
            'save_timestamp': datetime(2023, 10, 10, 10, 10, 10, 000000),
            'origin_name': 'test',
            'origin_location': '{"type":"Point","coordinates":[90.0,90.0]}',
            'origin_place_id': 'test123',
            'destination_name': 'test',
            'destination_location': '{"type":"Point","coordinates":[90.0,90.0]}',
            'destination_place_id': 'test123',
            'ride_date': date(2023, 10, 23),
            'weather': '001',
            'weather_icon': '001',
            'one_ways': [{
                'route_one_way_id': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [{
                    'route_via_point_type': '01',
                    'route_via_point_id': 1,
                    'route_via_point_location': '{"type":"Point","coordinates":[90.0,90.0]}',
                    'route_via_point_place_id': 'abcde1236'
                }]
            }],
            'bicycle_parking': None
        }
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        'route_id': 1,
        'user_vehicle_id': 1,
        'origin_name': 'test',
        'origin_latitude': 90.0,
        'origin_longitude': 90.0,
        'origin_place_id': 'test123',
        'destination_name': 'test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'destination_place_id': 'test123',
        'save_timestamp': '2023-10-10T10:10:10Z',
        'ride_date': '2023-10-23',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [
            {
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [
                    {
                        'route_via_point_type': '01',
                        'route_via_point_place_id': 'abcde1236',
                        'latitude': 90.0,
                        'longitude': 90.0
                    }
                ]
            }
        ],
        'bicycle_parking': []
    }

    params = {
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
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [
                    {
                        'route_via_point_type': '01',
                        'route_via_point_place_id': 'abcde1236',
                        'latitude': 90.0,
                        'longitude': 90.0
                    }
                ]
            }
        ],
        'bicycle_parking': []
    }

    result = create_route(gigya_uid='test_uid_9', **params)

    route_params = {
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
        'weather_icon': '001'
    }
    m_route.assert_called_with('test_uid_9', **route_params)

    route_one_way_params = {
        'round_trip_type_code': '10',
        'duration': 123,
        'distance': 123,
        'route_type': '12',
        'route_type_branch_no': 1,
    }
    m_route_one_way.assert_called_with('test_uid_9', 123, **route_one_way_params)

    route_via_points_params = [
        {
            'route_via_point_type': '01',
            'route_via_point_place_id': 'abcde1236',
            'latitude': 90.0,
            'longitude': 90.0
        }
    ]
    m_route_via_point.assert_called_with('test_uid_9', 123, 123, route_via_points_params)

    assert result == expected_value


def test_delete_route_ok_01(mocker):
    """
    正常系 ルート削除
    """

    # repository.route_repository.get_t_route のモック化
    mocker.patch("repository.route_repository.get_t_route", return_value=1)

    # repository.bicycle_parking_repository.delete_t_bicycle_parking のモック化
    mocker.patch("repository.bicycle_parking_repository.delete_t_bicycle_parking", return_value=1)

    # repository.route_via_point_repository.delete_t_route_via_point のモック化
    mocker.patch("repository.route_via_point_repository.delete_t_route_via_point", return_value=1)

    # repository.route_one_way_repository.delete_t_route_one_way のモック化
    mocker.patch("repository.route_one_way_repository.delete_t_route_one_way", return_value=1)

    # repository.route_repository.delete_t_route のモック化
    mocker.patch("repository.route_repository.delete_t_route", return_value=1)

    reload(module)

    # 期待している返却値
    expected_value = None

    result = delete_route(gigya_uid='test_uid_01', route_id=1)
    assert result == expected_value


def test_delete_route_ng_01(mocker):
    """
    異常系 ルート削除
    取得結果が0件の場合
    """
    # repository.route_repository.get_t_route のモック化
    mocker.patch("repository.route_repository.get_t_route", return_value=0)
    reload(module)

    with pytest.raises(NotExpectedError):
        delete_route(gigya_uid='test_uid_01', route_id=1)


def test_update_route_ok_01(mocker):
    """
    正常系 ルート更新
    """

    _ = mocker.patch(
        "repository.route_repository.get_t_route",
        return_value=[{
            'route_id': 1
        }]
    )

    m_route = mocker.patch(
        "repository.route_repository.update_route",
        return_value=123
    )

    _ = mocker.patch(
        "repository.route_one_way_repository.delete_t_route_one_way",
        return_value=123
    )

    m_route_one_way = mocker.patch(
        "repository.route_one_way_repository.create_route_one_way",
        return_value=123
    )

    _ = mocker.patch(
        "repository.route_via_point_repository.delete_t_route_via_point",
        return_value=1
    )

    m_route_via_point = mocker.patch(
        "repository.route_via_point_repository.create_route_via_points",
        return_value=1
    )

    _ = mocker.patch(
        "repository.bicycle_parking_repository.delete_t_bicycle_parking"
    )
    m_bicycle_parking = mocker.patch(
        "repository.bicycle_parking_repository.create_bicycle_parking",
        return_value=1
    )

    # repository.route_repository.get_joined_routeのモック化
    mocker.patch(
        "repository.route_repository.get_joined_route",
        return_value={
            'route_id': 1,
            'user_vehicle_id': 1,
            'save_timestamp': datetime(2023, 10, 10, 10, 10, 10, 000000),
            'origin_name': 'test',
            'origin_location': '{"type":"Point","coordinates":[90.0,90.0]}',
            'origin_place_id': 'test123',
            'destination_name': 'test',
            'destination_location': '{"type":"Point","coordinates":[90.0,90.0]}',
            'destination_place_id': 'test123',
            'ride_date': date(2023, 10, 23),
            'weather': '001',
            'weather_icon': '001',
            'one_ways': [{
                'route_one_way_id': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [{
                    'route_via_point_type': '01',
                    'route_via_point_id': 1,
                    'route_via_point_location': '{"type":"Point","coordinates":[90.0,90.0]}',
                    'route_via_point_place_id': 'abcde1236'
                }]
            }],
            'bicycle_parking': [{
                'bicycle_parking_id': 1,
                'bicycle_parking_name': '駐輪場1',
                'bicycle_parking_distance': 100,
                'bicycle_parking_location': '{"type":"Point","coordinates":[90.0,90.0]}',
                'bicycle_parking_place_id': 'abcd1234',
            }]
        }
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        'route_id': 1,
        'user_vehicle_id': 1,
        'origin_name': 'test',
        'origin_latitude': 90.0,
        'origin_longitude': 90.0,
        'origin_place_id': 'test123',
        'destination_name': 'test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'destination_place_id': 'test123',
        'save_timestamp': '2023-10-10T10:10:10Z',
        'ride_date': '2023-10-23',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [
            {
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [
                    {
                        'route_via_point_type': '01',
                        'route_via_point_place_id': 'abcde1236',
                        'latitude': 90.0,
                        'longitude': 90.0
                    }
                ]
            }
        ],
        'bicycle_parking': [
            {
                'bicycle_parking_name': '駐輪場1',
                'bicycle_parking_distance': 100,
                'latitude': 90.0,
                'longitude': 90.0,
                'bicycle_parking_place_id': 'abcd1234'
            }
        ]
    }

    params = {
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
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [
                    {
                        'route_via_point_type': '01',
                        'route_via_point_place_id': 'abcde1236',
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
            'longitude': 90.0
        }]
    }

    result = update_route(gigya_uid='test_uid_9', route_id=1, **params)

    route_params = {
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
        'weather_icon': '001'
    }
    m_route.assert_called_with('test_uid_9', 1, **route_params)

    route_one_way_params = {
        'round_trip_type_code': '10',
        'duration': 123,
        'distance': 123,
        'route_type': '12',
        'route_type_branch_no': 1,
    }
    m_route_one_way.assert_called_with('test_uid_9', 1, **route_one_way_params)

    route_via_points_params = [
        {
            'route_via_point_type': '01',
            'route_via_point_place_id': 'abcde1236',
            'latitude': 90.0,
            'longitude': 90.0
        }
    ]
    m_route_via_point.assert_called_with('test_uid_9', 1, 123, route_via_points_params)

    bicycle_parking_params = [
        {
            'bicycle_parking_name': '駐輪場1',
            'bicycle_parking_distance': 123,
            'bicycle_parking_place_id': 'abcd1234',
            'latitude': 90.0,
            'longitude': 90.0
        }
    ]
    m_bicycle_parking.assert_called_with('test_uid_9', 1, bicycle_parking_params)
    assert result == expected_value


def test_update_route_ok_02(mocker):
    """
    正常系 ルート更新
    リクエストにルート関連情報（往路復路、経由地、駐輪場情報）が存在しない場合
    """

    _ = mocker.patch(
        "repository.route_repository.get_t_route",
        return_value=[{
            'route_id': 1
        }]
    )

    m_route = mocker.patch(
        "repository.route_repository.update_route",
        return_value=123
    )

    _ = mocker.patch(
        "repository.route_one_way_repository.delete_t_route_one_way",
        return_value=123
    )

    # repository.route_repository.get_joined_routeのモック化
    mocker.patch(
        "repository.route_repository.get_joined_route",
        return_value={
            'route_id': 1,
            'user_vehicle_id': 1,
            'save_timestamp': datetime(2023, 10, 10, 10, 10, 10, 000000),
            'origin_name': 'test',
            'origin_location': '{"type":"Point","coordinates":[90.0,90.0]}',
            'origin_place_id': 'test123',
            'destination_name': 'test',
            'destination_location': '{"type":"Point","coordinates":[90.0,90.0]}',
            'destination_place_id': 'test123',
            'ride_date': date(2023, 10, 23),
            'weather': '001',
            'weather_icon': '001',
            'one_ways': [{
                'route_one_way_id': 1,
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [{
                    'route_via_point_type': '01',
                    'route_via_point_id': 1,
                    'route_via_point_location': '{"type":"Point","coordinates":[90.0,90.0]}',
                    'route_via_point_place_id': 'abcde1236'
                }]
            }],
            'bicycle_parking': None
        }
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        'route_id': 1,
        'user_vehicle_id': 1,
        'origin_name': 'test',
        'origin_latitude': 90.0,
        'origin_longitude': 90.0,
        'origin_place_id': 'test123',
        'destination_name': 'test',
        'destination_latitude': 90.0,
        'destination_longitude': 90.0,
        'destination_place_id': 'test123',
        'save_timestamp': '2023-10-10T10:10:10Z',
        'ride_date': '2023-10-23',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [
            {
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [{
                    'route_via_point_type': '01',
                        'route_via_point_place_id': 'abcde1236',
                        'latitude': 90.0,
                        'longitude': 90.0
                    }
                ]
            }
        ],
        'bicycle_parking': []
    }

    params = {
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
        'one_ways': [],
        'bicycle_parking': []
    }

    result = update_route(gigya_uid='test_uid_9', route_id=1, **params)

    route_params = {
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
        'weather_icon': '001'
    }
    m_route.assert_called_with('test_uid_9', 1, **route_params)

    assert result == expected_value


def test_update_route_ng_01(mocker):
    """
    異常系 ルート更新
    取得結果が0件の場合
    """
    # repository.route_repository.get_t_route のモック化
    mocker.patch("repository.route_repository.get_t_route", return_value=0)
    reload(module)

    params = {
        'user_vehicle_id': 9999,
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
                'round_trip_type_code': '10',
                'duration': 123,
                'distance': 123,
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [
                    {
                        'route_via_point_type': '01',
                        'route_via_point_place_id': 'abcde1236',
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
            'longitude': 90.0
        }]
    }

    with pytest.raises(NotExpectedError):
        update_route(gigya_uid='test_uid_9', route_id=1, **params)


def test_get_route_ok_01(mocker):
    """
    正常系 その1
    """

    # repository.route_repository.get_joined_routeのモック化
    mocker.patch(
        "repository.route_repository.get_joined_route",
        return_value={
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
                'route_type': '12',
                'route_type_branch_no': 1,
            }]
        }
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        'route_id': 3,
        'user_vehicle_id': 2,
        'save_timestamp': '2023-09-12T11:27:46.642000Z',
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_latitude': 35.667009003,
        'origin_longitude': 139.749387112,
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_latitude': 35.667009003,
        'destination_longitude': 139.749387112,
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': '2023-10-02',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [{
            'round_trip_type_code': '10',
            'duration': 123,
            'distance': 123,
            'route_type': '12',
            'route_type_branch_no': 1,
            'route_via_points': []
        }],
        'bicycle_parking': []
    }
    result = get_route(gigya_uid='test_uid_3', route_id=3)
    assert result == expected_value


def test_get_route_ok_02(mocker):
    """
    正常系 その2
    """

    # repository.route_repository.get_joined_routeのモック化
    mocker.patch(
        "repository.route_repository.get_joined_route",
        return_value={
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
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        'route_id': 4,
        'user_vehicle_id': 2,
        'save_timestamp': '2023-09-12T11:27:46.642000Z',
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_latitude': 35.667009003,
        'origin_longitude': 139.749387112,
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_latitude': 35.667009003,
        'destination_longitude': 139.749387112,
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': '2023-10-02',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [{
            'round_trip_type_code': '10',
            'duration': 123,
            'distance': 123,
            'route_type': '12',
            'route_type_branch_no': 1,
            'route_via_points': [{
                'route_via_point_type': '01',
                'latitude': 35.667009003,
                'longitude': 139.749387112,
                'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }]
        }],
        'bicycle_parking': [{
            'bicycle_parking_name': 'テスト駐輪場',
            'bicycle_parking_distance': 100,
            'latitude': 35.667009003,
            'longitude': 139.749387112,
            'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
        }]
    }
    result = get_route(gigya_uid='test_uid_4', route_id=4)
    assert result == expected_value


def test_get_route_ok_03(mocker):
    """
    正常系 その3
    """

    # repository.route_repository.get_joined_routeのモック化
    mocker.patch(
        "repository.route_repository.get_joined_route",
        return_value={
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
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [
                    {
                        'route_via_point_type': '01',
                        'route_via_point_id': 3,
                        'route_via_point_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
                        'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
                    },
                    {
                        'route_via_point_type': '01',
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
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        'route_id': 5,
        'user_vehicle_id': 2,
        'save_timestamp': '2023-09-12T11:27:46.642000Z',
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_latitude': 35.667009003,
        'origin_longitude': 139.749387112,
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_latitude': 35.667009003,
        'destination_longitude': 139.749387112,
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': '2023-10-02',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [{
            'round_trip_type_code': '10',
            'duration': 123,
            'distance': 123,
            'route_type': '12',
            'route_type_branch_no': 1,
            'route_via_points': [{
                'route_via_point_type': '01',
                'latitude': 35.667009003,
                'longitude': 139.749387112,
                'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }, {
                'route_via_point_type': '01',
                'latitude': 35.667009003,
                'longitude': 139.749387112,
                'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }]
        }],
        'bicycle_parking': [{
            'bicycle_parking_name': 'テスト駐輪場',
            'bicycle_parking_distance': 100,
            'latitude': 35.667009003,
            'longitude': 139.749387112,
            'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
        }, {
            'bicycle_parking_name': 'テスト駐輪場',
            'bicycle_parking_distance': 100,
            'latitude': 35.667009003,
            'longitude': 139.749387112,
            'bicycle_parking_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
        }]
    }
    result = get_route(gigya_uid='test_uid_5', route_id=5)
    assert result == expected_value


def test_get_route_ok_04(mocker):
    """
    正常系
    駐輪場情報が存在しない場合
    """

    # repository.route_repository.get_joined_routeのモック化
    mocker.patch(
        "repository.route_repository.get_joined_route",
        return_value={
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
                'route_type': '12',
                'route_type_branch_no': 1,
                'route_via_points': [
                    {
                        'route_via_point_type': '01',
                        'route_via_point_id': 3,
                        'route_via_point_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
                        'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
                    },
                    {
                        'route_via_point_type': '01',
                        'route_via_point_id': 4,
                        'route_via_point_location': '{"type":"Point","coordinates":[35.667009003,139.749387112]}',
                        'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
                    }
                ]
            }],
            'bicycle_parking': None
        }
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        'route_id': 5,
        'user_vehicle_id': 2,
        'save_timestamp': '2023-09-12T11:27:46.642000Z',
        'origin_name': '虎ノ門ヒルズ森タワー',
        'origin_latitude': 35.667009003,
        'origin_longitude': 139.749387112,
        'origin_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'destination_name': '虎ノ門ヒルズ森タワー',
        'destination_latitude': 35.667009003,
        'destination_longitude': 139.749387112,
        'destination_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0',
        'ride_date': '2023-10-02',
        'weather': '001',
        'weather_icon': '001',
        'one_ways': [{
            'round_trip_type_code': '10',
            'duration': 123,
            'distance': 123,
            'route_type': '12',
            'route_type_branch_no': 1,
            'route_via_points': [{
                'route_via_point_type': '01',
                'latitude': 35.667009003,
                'longitude': 139.749387112,
                'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }, {
                'route_via_point_type': '01',
                'latitude': 35.667009003,
                'longitude': 139.749387112,
                'route_via_point_place_id': 'ChIJdc0fopOLGGARm4DVQaWiPZ0'
            }]
        }],
        'bicycle_parking': []
    }
    result = get_route(gigya_uid='test_uid_5', route_id=5)
    assert result == expected_value


def test_get_route_ng_01(mocker):
    """
    異常系 取得結果が0件の場合
    """

    # repository.route_repository.get_joined_routeのモック化
    mocker.patch(
        "repository.route_repository.get_joined_route",
        return_value=[]
    )

    reload(module)

    with pytest.raises(BusinessError):
        _ = get_route(gigya_uid='test_uid_9', route_id=999)
