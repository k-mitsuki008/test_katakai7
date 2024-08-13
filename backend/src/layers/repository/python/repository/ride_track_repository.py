from common.logger import Logger

from common.rds.core import execute_insert_statement
from common.rds.core import execute_select_statement
from common.rds.core import execute_delete_statement

log = Logger()


def upsert_t_ride_track(ride_tracks: list) -> int:
    args_str = ','.join(['%s'] * len(ride_tracks))
    sql = f'''
        INSERT INTO
            t_ride_track(ride_history_id, user_vehicle_id, track_id, latitude, longitude, insert_timestamp, insert_user_id)
        VALUES
            {args_str}
        ON CONFLICT ON CONSTRAINT t_ride_track_pkey
        DO UPDATE
        SET
            latitude = EXCLUDED.latitude,
            longitude = EXCLUDED.longitude,
            update_timestamp = EXCLUDED.insert_timestamp,
            update_user_id = EXCLUDED.insert_user_id;
        '''
    return execute_insert_statement(sql, ride_tracks)


def get_ride_track(ride_history_id: str) -> list:
    sql: str = '''
      SELECT
        track_id,
        latitude,
        longitude
      FROM
        t_ride_track
      WHERE
        delete_flag = False
        AND ride_history_id = %(ride_history_id)s
      ORDER BY
        track_id;
    '''

    parameters_dict: dict = {'ride_history_id': ride_history_id}
    rec = execute_select_statement(sql, parameters_dict)

    return rec


def delete_t_ride_track(ride_history_id: str) -> int:
    sql = f'''
        DELETE FROM 
            t_ride_track
        WHERE
            ride_history_id = %(ride_history_id)s;
    '''
    params = {'ride_history_id': ride_history_id}
    return execute_delete_statement(sql, params)
