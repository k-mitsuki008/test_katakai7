import json

from common.aws.dynamodb import DynamoDb
from common.decorator.service import service
from common.error.business_error import BusinessError
from common.error.not_expected_error import NotExpectedError
from common.logger import Logger
from repository import (bicycle_parking_repository, route_one_way_repository,
                        route_repository, route_via_point_repository)

log = Logger()

# 往復種別CD
ROUND_TRIP_TYPE_CODE_CONSTANTS = DynamoDb().constants.get('ROUND_TRIP_TYPE_CODE')


@service
def get_route_list(gigya_uid: str) -> list:

    route_list = route_repository.get_t_route_by_gigya_uid(gigya_uid)
    log.info(f'取得結果: {route_list}')

    convert_route_list = []
    for route in route_list:
        one_ways = route.get('one_ways') if route.get('one_ways') else []
        convert_route_list.append(
            {
                'route_id': route.get('route_id'),
                'user_vehicle_id': route.get('user_vehicle_id'),
                'save_timestamp': f'{route.get("save_timestamp").isoformat()}Z' if route.get('save_timestamp')
                else None,
                'destination_name': route.get('destination_name'),
                'latitude': json.loads(route.get('destination_location')).get('coordinates')[0],
                'longitude': json.loads(route.get('destination_location')).get('coordinates')[1],
                'destination_place_id': route.get('destination_place_id'),
                'ride_date': str(route.get('ride_date')) if route.get('ride_date') else None,
                'weather': route.get('weather'),
                'weather_icon': route.get('weather_icon'),
                'duration': _calculate_duration(one_ways),
                'distance': _calculate_distance(one_ways),
            }
        )

    return convert_route_list


@service
def create_route(gigya_uid: str, user_vehicle_id, origin_name, origin_latitude, origin_longitude, origin_place_id,
                 destination_name, destination_latitude, destination_longitude, destination_place_id, save_timestamp,
                 ride_date, weather, weather_icon, one_ways, bicycle_parking):
    route_data = {
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
        'weather_icon': weather_icon
    }
    route_id = route_repository.create_route(gigya_uid, **route_data)

    for one_way in one_ways:
        via_spots = one_way.pop('route_via_points', None)
        route_one_way_id = route_one_way_repository.create_route_one_way(gigya_uid, route_id, **one_way)
        _ = route_via_point_repository.create_route_via_points(gigya_uid, route_id, route_one_way_id, via_spots)

    if bicycle_parking:
        _ = bicycle_parking_repository.create_bicycle_parking(gigya_uid, route_id, bicycle_parking)

    route = route_repository.get_joined_route(gigya_uid, route_id)
    log.info(f'取得結果: {route}')

    return _convert_route(route)


@service
def delete_route(gigya_uid: str, route_id: int) -> None:

    # ルート情報がGIGYAユニークIDのものか確認する
    route_count = route_repository.get_t_route(gigya_uid, route_id)

    # 存在しない場合はシステムエラー
    if not route_count:
        raise NotExpectedError()

    # ルート関連情報の削除
    _ = bicycle_parking_repository.delete_t_bicycle_parking(route_id)
    _ = route_via_point_repository.delete_t_route_via_point(route_id)
    _ = route_one_way_repository.delete_t_route_one_way(route_id)
    _ = route_repository.delete_t_route(gigya_uid, route_id)

    return


@service
def update_route(gigya_uid: str, route_id, user_vehicle_id, origin_name, origin_latitude, origin_longitude,
                 origin_place_id, destination_name, destination_latitude, destination_longitude, destination_place_id,
                 save_timestamp, ride_date, weather, weather_icon, one_ways, bicycle_parking):

    # ルート情報がGIGYAユニークIDのものか確認する
    route_count = route_repository.get_t_route(gigya_uid, route_id)

    # 存在しない場合はシステムエラー
    if not route_count:
        raise NotExpectedError()

    route_data = {
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
        'weather_icon': weather_icon
    }
    _ = route_repository.update_route(gigya_uid, route_id, **route_data)

    # ルート関連情報は一度消してから登録
    if bicycle_parking:
        _ = bicycle_parking_repository.delete_t_bicycle_parking(route_id)
        _ = bicycle_parking_repository.create_bicycle_parking(gigya_uid, route_id, bicycle_parking)

    if one_ways:
        _ = route_via_point_repository.delete_t_route_via_point(route_id)
        _ = route_one_way_repository.delete_t_route_one_way(route_id)

        for one_way in one_ways:
            via_spots = one_way.pop('route_via_points', None)
            route_one_way_id = route_one_way_repository.create_route_one_way(gigya_uid, route_id, **one_way)
            _ = route_via_point_repository.create_route_via_points(gigya_uid, route_id, route_one_way_id, via_spots)

    route = route_repository.get_joined_route(gigya_uid, route_id)
    log.info(f'取得結果: {route}')

    return _convert_route(route)


@service
def get_route(gigya_uid: str, route_id: int) -> dict:

    route = route_repository.get_joined_route(gigya_uid, route_id)
    log.info(f'取得結果: {route}')

    return _convert_route(route)


def _calculate_duration(one_ways):
    # 所要時間の算出
    duration = 0
    for i in one_ways:
        if i['round_trip_type_code'] == ROUND_TRIP_TYPE_CODE_CONSTANTS['ROUND_TRIP']:
            return i['duration'] * 2
        if i['round_trip_type_code'] in \
                [ROUND_TRIP_TYPE_CODE_CONSTANTS['OUTWARD'], ROUND_TRIP_TYPE_CODE_CONSTANTS['RETURN']]:
            duration += i['duration']
    return duration


def _calculate_distance(one_ways):
    # ルート距離の算出
    distance = 0
    for i in one_ways:
        if i['round_trip_type_code'] == ROUND_TRIP_TYPE_CODE_CONSTANTS['ROUND_TRIP']:
            return i['distance'] * 2
        if i['round_trip_type_code'] in \
                [ROUND_TRIP_TYPE_CODE_CONSTANTS['OUTWARD'], ROUND_TRIP_TYPE_CODE_CONSTANTS['RETURN']]:
            distance += i['distance']
    return distance


def _convert_route(route):

    if not route:
        raise BusinessError(error_code='E042', params=('ルートID',))

    origin_location = route.pop('origin_location')
    destination_location = route.pop('destination_location')

    convert_route = {
        'route_id': route.get('route_id'),
        'user_vehicle_id': route.get('user_vehicle_id'),
        'save_timestamp': f'{route.get("save_timestamp").isoformat()}Z' if route.get('save_timestamp') else None,
        'origin_name': route.get('origin_name'),
        'origin_latitude': json.loads(origin_location).get('coordinates')[0],
        'origin_longitude': json.loads(origin_location).get('coordinates')[1],
        'origin_place_id': route.get('origin_place_id'),
        'destination_name': route.get('destination_name'),
        'destination_latitude': json.loads(destination_location).get('coordinates')[0],
        'destination_longitude': json.loads(destination_location).get('coordinates')[1],
        'destination_place_id': route.get('destination_place_id'),
        'ride_date': str(route.get('ride_date')) if route.get('ride_date') else None,
        'weather': route.get('weather'),
        'weather_icon': route.get('weather_icon'),
        'one_ways': [],
        'bicycle_parking': []
    }
    one_ways = route.get('one_ways') if route.get('one_ways') else []
    for item in one_ways:
        one_way = {
            'route_type_branch_no': item.get('route_type_branch_no'),
            'round_trip_type_code': item.get('round_trip_type_code'),
            'route_type': item.get('route_type'),
            'distance': item.get('distance'),
            'duration': item.get('duration'),
            'route_via_points': []
        }
        via_points = item.get('route_via_points') if item.get('route_via_points') else []
        for via_point_item in via_points:
            location = via_point_item.get('route_via_point_location')
            via_point = {
                'route_via_point_type': via_point_item.get('route_via_point_type'),
                'route_via_point_place_id': via_point_item.get('route_via_point_place_id'),
                'latitude': json.loads(location).get('coordinates')[0],
                'longitude': json.loads(location).get('coordinates')[1],
            }
            one_way['route_via_points'].append(via_point)
        convert_route['one_ways'].append(one_way)

    bicycle_parking = route.get('bicycle_parking') if route.get('bicycle_parking') else []
    for item in bicycle_parking:
        location = item.get('bicycle_parking_location')
        parking = {
            'bicycle_parking_name': item.get('bicycle_parking_name'),
            'bicycle_parking_distance': item.get('bicycle_parking_distance'),
            'latitude': json.loads(location).get('coordinates')[0],
            'longitude': json.loads(location).get('coordinates')[1],
            'bicycle_parking_place_id': item.get('bicycle_parking_place_id'),
        }
        convert_route['bicycle_parking'].append(parking)

    return convert_route
