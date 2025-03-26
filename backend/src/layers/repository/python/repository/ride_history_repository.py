from common.logger import Logger

from common.utils.time_utils import (
  convert_datetime_to_str,
  get_current_datetime
)
from common.rds.core import execute_select_statement
from common.rds.core import execute_insert_statement
from common.rds.core import execute_delete_statement
from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def upsert_t_ride_history(gigya_uid: str, ride_history_id: str, **kwargs) -> int:
    now_str = convert_datetime_to_str(
      get_current_datetime(),
      '%Y-%m-%d %H:%M:%S.%f'
    )
    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
      INSERT INTO
        t_ride_history(
          gigya_uid,
          ride_history_id,
          {', '.join(kwargs.keys())},
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(gigya_uid)s,
          %(ride_history_id)s,
          %({')s, %('.join(kwargs.keys())})s,
          %(now_str)s,
          %(gigya_uid)s
        )
      ON CONFLICT(ride_history_id)
      DO UPDATE SET
        {update_sets}
      '''
    params = {'gigya_uid': gigya_uid, 'ride_history_id': ride_history_id, **kwargs, 'now_str': now_str}
    return execute_insert_statement(sql, params)


def get_ride_history(gigya_uid: str, ride_history_id: str) -> dict:
    sql: str = '''
      SELECT
        ride_history_id,
        start_timestamp,
        end_timestamp,
        trip_distance,
        trip_time,
        total_calorie,
        battery_consumption,
        average_speed,
        max_speed,
        max_pedaling_power,
        max_cadence,
        ride_name,
        bookmark_flg
      FROM
        t_ride_history
      WHERE
        delete_flag = False
        AND ride_history_id = %(ride_history_id)s
        AND gigya_uid = %(gigya_uid)s;
    '''

    parameters_dict: dict = {'gigya_uid': gigya_uid, 'ride_history_id': ride_history_id}
    rec = execute_select_statement(sql, parameters_dict)

    return rec[0] if rec else None


def get_ride_history_limit(
    gigya_uid: str,
    limit: int,
    offset: int,
    begin: str = None,
    end: str = None,
    bookmark_flg: bool = None,
) -> list:
    bookmark_flg_selector = 'AND bookmark_flg = %(bookmark_flg)s' if type(bookmark_flg) is bool else ''

    sql: str = f'''
      SELECT
        ride_history_id,
        start_timestamp,
        end_timestamp,
        ride_name,
        trip_distance,
        trip_time,
        bookmark_flg
      FROM
        t_ride_history
      WHERE
        delete_flag = False
      AND gigya_uid = %(gigya_uid)s
      AND start_timestamp BETWEEN %(begin)s AND %(end)s
      {bookmark_flg_selector}
      ORDER BY
        start_timestamp DESC
      LIMIT %(limit)s
      OFFSET %(offset)s;
    '''

    parameters_dict: dict = {
        'gigya_uid': gigya_uid,
        'begin': begin,
        'end': end,
        'bookmark_flg': bookmark_flg,
        'limit': limit,
        'offset': offset
    }
    rec = execute_select_statement(sql, parameters_dict)

    return rec


def get_ride_history_all_count(
    gigya_uid: str,
    begin: str,
    end: str,
    bookmark_flg: bool = None,
) -> dict:
    bookmark_flg_selector = 'AND bookmark_flg = %(bookmark_flg)s' if type(bookmark_flg) is bool else ''
    sql: str = F'''
      SELECT
        count(start_timestamp)
      FROM
        t_ride_history
      WHERE
        delete_flag = False
      AND gigya_uid = %(gigya_uid)s
      AND start_timestamp BETWEEN %(begin)s AND %(end)s
      {bookmark_flg_selector}
      ;
    '''

    parameters_dict: dict = {
        'gigya_uid': gigya_uid,
        'begin': begin,
        'end': end,
        'bookmark_flg': bookmark_flg,
    }
    rec = execute_select_statement(sql, parameters_dict)

    return rec[0]


def update_t_ride_history(gigya_uid: str, ride_history_id: str, **kwargs) -> int:
    now_str = convert_datetime_to_str(
        get_current_datetime(),
        '%Y-%m-%d %H:%M:%S.%f'
    )
    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
        UPDATE
          t_ride_history
        SET
          {update_sets}
        WHERE
          delete_flag = False
        AND
          ride_history_id = %(ride_history_id)s
        AND
          gigya_uid = %(gigya_uid)s
        '''
    params = {'gigya_uid': gigya_uid, 'ride_history_id': ride_history_id, **kwargs, 'now_str': now_str}
    return execute_insert_statement(sql, params)


def delete_t_ride_history(gigya_uid: str, ride_history_id: str) -> int:
    sql = f'''
         DELETE FROM 
             t_ride_history
         WHERE
             gigya_uid = %(gigya_uid)s
             AND ride_history_id = %(ride_history_id)s;
     '''
    params = {'gigya_uid': gigya_uid, 'ride_history_id': ride_history_id}
    return execute_delete_statement(sql, params)


def delete_t_ride_history_user_vehicle_id(gigya_uid: str, user_vehicle_id: int) -> int:
    sql = f'''
        WITH delete_history as (
            DELETE FROM
                t_ride_history
            WHERE
                gigya_uid = %(gigya_uid)s
                AND user_vehicle_id = %(user_vehicle_id)s
            RETURNING ride_history_id
        )
         DELETE FROM 
             t_ride_track
         WHERE
             ride_history_id IN (
                SELECT
                    ride_history_id
                FROM
                    delete_history
             )
     '''
    params = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id}
    return execute_delete_statement(sql, params)
