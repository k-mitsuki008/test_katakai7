from typing import Tuple

from common.rds.transactional import transactional
from common.response import get_response_element
from common.logger import Logger
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import REQUIRED_GIGYA_UID, REQUIRED_ROUTE_ID, USER_VEHICLE_ID, \
    OPTIONAL_DESTINATION_NAME, OPTIONAL_DESTINATION_LATITUDE, OPTIONAL_DESTINATION_LONGITUDE, \
    OPTIONAL_DESTINATION_PLACE_ID, OPTIONAL_ORIGIN_NAME, OPTIONAL_ORIGIN_LATITUDE, OPTIONAL_ORIGIN_LONGITUDE, \
    OPTIONAL_ORIGIN_PLACE_ID, REQUIRED_SAVE_TIMESTAMP, OPTIONAL_RIDE_DATE, OPTIONAL_WEATHER,\
    OPTIONAL_WEATHER_ICON, OPTIONAL_ONE_WAYS, OPTIONAL_BICYCLE_PARKING
from service import route_service


log = Logger()

# cerberusのvalidation定義を設定
PUT_SCHEMA: dict = {
    **REQUIRED_GIGYA_UID,
    **REQUIRED_ROUTE_ID,
    **USER_VEHICLE_ID,
    **OPTIONAL_DESTINATION_NAME,
    **OPTIONAL_DESTINATION_LATITUDE,
    **OPTIONAL_DESTINATION_LONGITUDE,
    **OPTIONAL_DESTINATION_PLACE_ID,
    **OPTIONAL_ORIGIN_NAME,
    **OPTIONAL_ORIGIN_LATITUDE,
    **OPTIONAL_ORIGIN_LONGITUDE,
    **OPTIONAL_ORIGIN_PLACE_ID,
    **REQUIRED_SAVE_TIMESTAMP,
    **OPTIONAL_RIDE_DATE,
    **OPTIONAL_WEATHER,
    **OPTIONAL_WEATHER_ICON,
    **OPTIONAL_ONE_WAYS,
    **OPTIONAL_BICYCLE_PARKING
}


# pylint: disable=unused-argument
@default_api(schema=PUT_SCHEMA, method='PUT')
@transactional
def handler(params: dict, headers: dict = None) -> Tuple[dict, int]:
    """
    ルート更新API
    """
    log.info(f'params={params}')
    gigya_uid = params['gigya_uid']
    route_id = params.get('route_id')
    user_vehicle_id = params.get('user_vehicle_id')
    origin_name = params.get('origin_name')
    origin_latitude = params.get('origin_latitude')
    origin_longitude = params.get('origin_longitude')
    origin_place_id = params.get('origin_place_id')
    destination_name = params.get('destination_name')
    destination_latitude = params.get('destination_latitude')
    destination_longitude = params.get('destination_longitude')
    destination_place_id = params.get('destination_place_id')
    save_timestamp = params.get('save_timestamp')
    ride_date = params.get('ride_date')
    weather = params.get('weather')
    weather_icon = params.get('weather_icon')
    one_ways = params.get('one_ways')
    bicycle_parking = params.get('bicycle_parking')

    route_info = route_service.update_route(
        gigya_uid,
        route_id,
        user_vehicle_id,
        origin_name,
        origin_latitude,
        origin_longitude,
        origin_place_id,
        destination_name,
        destination_latitude,
        destination_longitude,
        destination_place_id,
        save_timestamp,
        ride_date,
        weather,
        weather_icon,
        one_ways,
        bicycle_parking
    )

    result: dict = {
        **{"result": True},
        **route_info
    }

    return get_response_element(result)
