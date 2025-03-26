import json

from common.decorator.service import service
from common.logger import Logger
from repository import spot_repository as repository

log = Logger()


@service
def get_spot(latitude: float, longitude: float, radius: int) -> list:

    spot_list = repository.get_m_spot(latitude, longitude, radius)
    log.info(f'取得結果: {spot_list}')

    convert_spot_list = []
    for spot in spot_list:
        convert_spot_list.append(
            {
                'spot_id': spot.get('spot_id'),
                'spot_type_code': spot.get('spot_type_code'),
                'latitude': json.loads(spot.get('spot_location')).get('coordinates')[0],
                'longitude': json.loads(spot.get('spot_location')).get('coordinates')[1],
                'spot_place_id': spot.get('spot_place_id'),
                'rechargeable_flag': spot.get('rechargeable_flag'),
            }
        )

    return convert_spot_list
