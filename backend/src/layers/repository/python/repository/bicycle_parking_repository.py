from common.logger import Logger
from common.rds.core import (batch_execute_insert_statement,
                             execute_delete_statement)
from common.utils.time_utils import (convert_datetime_to_str,
                                     get_current_datetime)

log = Logger()


def create_bicycle_parking(gigya_uid: str, route_id: int, bicycle_parking: list) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')

    for item in bicycle_parking:
        item.update({
            'route_id': route_id,
            'now_str': now_str,
            'gigya_uid': gigya_uid
        })

    sql = '''
      INSERT INTO
        t_bicycle_parking(
          route_id,
          bicycle_parking_name,
          bicycle_parking_distance,
          bicycle_parking_location,
          bicycle_parking_place_id,
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(route_id)s,
          %(bicycle_parking_name)s,
          %(bicycle_parking_distance)s,
          ST_GeomFromText('POINT(%(latitude)s %(longitude)s)', 4326),
          %(bicycle_parking_place_id)s,
          %(now_str)s,
          %(gigya_uid)s
        );
    '''

    rec = batch_execute_insert_statement(sql, bicycle_parking)
    return rec


def delete_t_bicycle_parking(route_id: int) -> int:
    sql = '''
        DELETE FROM
            t_bicycle_parking
        WHERE
            route_id = %(route_id)s;
    '''
    params = {'route_id': route_id}
    return execute_delete_statement(sql, params)
