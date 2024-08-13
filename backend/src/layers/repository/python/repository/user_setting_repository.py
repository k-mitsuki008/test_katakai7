from common.logger import Logger
from common.utils.time_utils import convert_datetime_to_str, get_current_datetime
from common.rds.core import execute_select_statement
from common.rds.core import execute_insert_statement
from common.rds.core import execute_update_statement
from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def upsert_t_user_setting_ride(gigya_uid: str, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
      INSERT INTO 
        t_user_setting_ride(
          gigya_uid,
          {', '.join(kwargs.keys())},
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(gigya_uid)s,
          %({')s, %('.join(kwargs.keys())})s,
          %(now_str)s,
          %(gigya_uid)s
        )
      ON CONFLICT(gigya_uid)
      DO UPDATE SET
        {update_sets}
      '''
    params = {'gigya_uid': gigya_uid, **kwargs, 'now_str': now_str}
    return execute_insert_statement(sql, params)


def update_t_user_setting_ride(gigya_uid: str, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    update_sets = create_update_set_sql(**kwargs)
    sql = f'''
        UPDATE
            t_user_setting_ride
        SET
          {update_sets}
        WHERE
            gigya_uid = %(gigya_uid)s;
    '''

    params = {'gigya_uid': gigya_uid, **kwargs, 'now_str': now_str}
    update_count = execute_update_statement(sql, params)
    return update_count


def get_t_user_setting_ride(gigya_uid: str) -> dict:
    sql: str = '''
      SELECT 
        gigya_uid,
        battery_remind_latitude,
        battery_remind_longitude,
        battery_remind_cd,
        battery_remind_voice_notice,
        safety_ride_alert,
        long_drive_alert,
        speed_over_alert,
        no_light_alert,
        safety_ride_voice_notice,
        home_assist_mode_number
      FROM
        t_user_setting_ride
      WHERE
        delete_flag = false
        AND gigya_uid = %(gigya_uid)s;
    '''

    parameters_dict: dict = {'gigya_uid': gigya_uid}
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0] if rec else None
