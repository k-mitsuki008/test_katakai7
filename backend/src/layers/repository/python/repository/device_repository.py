from common.logger import Logger

from common.utils.time_utils import convert_datetime_to_str, get_current_datetime
from common.rds.core import execute_select_statement
from common.rds.core import execute_insert_statement
from common.rds.core import execute_update_statement

from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def upsert_t_device(gigya_uid, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    update_sets = create_update_set_sql(**kwargs)
    sql = f'''
      INSERT INTO 
        t_device(
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
        {update_sets};
    '''

    params = {'gigya_uid': gigya_uid, **kwargs, 'now_str': now_str}
    return execute_insert_statement(sql, params)


def update_other_device_token(gigya_uid: str, device_id: str) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')

    sql = f'''
        UPDATE
            t_device
        SET
            device_token = '',
            update_timestamp = %(now_str)s,
            update_user_id = %(gigya_uid)s
        WHERE
            delete_flag = False
            AND gigya_uid != %(gigya_uid)s
            AND device_id = %(device_id)s;
    '''

    params = {
              'gigya_uid': gigya_uid,
              'device_id': device_id,
              'now_str': now_str}

    return execute_update_statement(sql, params)


def get_t_device(gigya_uid) -> dict:
    sql: str = '''
      SELECT 
        device_id,
        device_token
      FROM 
        t_device
      WHERE
        delete_flag = false
        AND gigya_uid = %(gigya_uid)s;
    '''

    parameters_dict: dict = {'gigya_uid': gigya_uid}
    res = execute_select_statement(sql, parameters_dict)

    return res[0] if res else None
