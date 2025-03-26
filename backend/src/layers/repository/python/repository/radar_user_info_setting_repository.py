from common.logger import Logger
from common.rds.core import execute_insert_statement, execute_select_statement
from common.utils.time_utils import (convert_datetime_to_str,
                                     get_current_datetime)
from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def get_user_info_setting(gigya_uid: str) -> dict:
    # pylint: disable=f-string-without-interpolation
    sql = '''
      SELECT
        gigya_uid
        , nickname
        , weight
        , birth_date
        , max_heart_rate
      FROM
        t_user_setting
      WHERE
        delete_flag = False
        AND gigya_uid = %(gigya_uid)s;
    '''

    parameters_dict: dict = {'gigya_uid': gigya_uid}
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0] if rec else {}


def upsert_user_info_setting(gigya_uid: str, **kwargs) -> int:
    now_str = convert_datetime_to_str(
        get_current_datetime(),
        '%Y-%m-%d %H:%M:%S.%f'
    )
    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
      INSERT INTO
        t_user_setting(
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
    log.info(sql % params)
    return execute_insert_statement(sql, params)
