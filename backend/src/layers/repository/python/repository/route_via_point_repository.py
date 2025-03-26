from common.logger import Logger
from common.rds.core import (batch_execute_insert_statement,
                             execute_delete_statement)
from common.utils.time_utils import (convert_datetime_to_str,
                                     get_current_datetime)

log = Logger()


def create_route_via_points(gigya_uid: str, route_id: int, route_one_way_id: int, route_via_spots: list) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')

    for item in route_via_spots:
        item.update({
            'route_id': route_id,
            'route_one_way_id': route_one_way_id,
            'route_via_point_place_id': item.get('route_via_point_place_id'),
            'now_str': now_str,
            'gigya_uid': gigya_uid
        })

    sql = '''
      INSERT INTO
        t_route_via_point(
          route_id,
          route_one_way_id,
          route_via_point_location,
          route_via_point_place_id,
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(route_id)s,
          %(route_one_way_id)s,
          ST_GeomFromText('POINT(%(latitude)s %(longitude)s)', 4326),
          %(route_via_point_place_id)s,
          %(now_str)s,
          %(gigya_uid)s
        );
    '''

    rec = batch_execute_insert_statement(sql, route_via_spots)
    return rec


def delete_t_route_via_point(route_id: int) -> int:
    sql = '''
        DELETE FROM
            t_route_via_point
        WHERE
            route_id = %(route_id)s;
    '''
    params = {'route_id': route_id}
    return execute_delete_statement(sql, params)
