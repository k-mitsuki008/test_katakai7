from common.logger import Logger
from common.rds.core import execute_delete_statement, execute_insert_statement
from common.utils.time_utils import (convert_datetime_to_str,
                                     get_current_datetime)

log = Logger()


def create_route_one_way(gigya_uid: str, route_id: int, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')

    sql = f'''
      INSERT INTO
        t_route_one_way(
          route_id,
          {', '.join(kwargs.keys())},
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(route_id)s,
          %({')s, %('.join(kwargs.keys())})s,
          %(now_str)s,
          %(gigya_uid)s
        )
        RETURNING route_one_way_id;
    '''

    params = {
        'gigya_uid': gigya_uid,
        'route_id': route_id,
        **kwargs,
        'now_str': now_str
    }
    rec = execute_insert_statement(sql, params, returning=True)
    return rec[0][0] if rec else None


def delete_t_route_one_way(route_id: int) -> int:
    sql = '''
        DELETE FROM
            t_route_one_way
        WHERE
            route_id = %(route_id)s;
    '''
    params = {'route_id': route_id}
    return execute_delete_statement(sql, params)
