from common.logger import Logger

from common.utils.time_utils import (
  convert_datetime_to_str,
  get_current_datetime
)
from common.rds.core import execute_select_statement
from common.rds.core import execute_insert_statement
from common.rds.core import execute_update_statement
from common.rds.core import execute_delete_statement

from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def upsert_t_user_shop_purchase(user_vehicle_id: int, **kwargs) -> int:
    now_str = convert_datetime_to_str(
      get_current_datetime(),
      '%Y-%m-%d %H:%M:%S.%f'
    )
    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
      INSERT INTO
        t_user_shop_purchase(
          user_vehicle_id,
          {', '.join(kwargs.keys())},
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(user_vehicle_id)s,
          %({')s, %('.join(kwargs.keys())})s,
          %(now_str)s,
          %(gigya_uid)s
        )
      ON CONFLICT(user_vehicle_id)
      DO UPDATE SET
        {update_sets}
      '''
    params = {'user_vehicle_id': user_vehicle_id, **kwargs, 'now_str': now_str}
    return execute_insert_statement(sql, params)


def update_t_user_shop_purchase(user_vehicle_id: int, **kwargs) -> int:
    now_str = convert_datetime_to_str(
      get_current_datetime(),
      '%Y-%m-%d %H:%M:%S.%f'
    )
    update_sets = create_update_set_sql(**kwargs)
    sql = f'''
        UPDATE
            t_user_shop_purchase
        SET
          {update_sets}
        WHERE
            user_vehicle_id = %(user_vehicle_id)s;
    '''

    params = {'user_vehicle_id': user_vehicle_id, **kwargs, 'now_str': now_str}
    update_count = execute_update_statement(sql, params)
    return update_count


def get_t_user_shop_purchase(user_vehicle_id: int) -> dict:
    sql: str = '''
      SELECT
        user_vehicle_id,
        gigya_uid,
        shop_name,
        shop_tel,
        shop_location
      FROM
        t_user_shop_purchase
      WHERE
        delete_flag = False
        AND user_vehicle_id = %(user_vehicle_id)s;
    '''

    parameters_dict: dict = {'user_vehicle_id': user_vehicle_id}
    rec = execute_select_statement(sql, parameters_dict)

    return rec[0] if rec else None


def delete_t_user_shop_purchase(gigya_uid: str, user_vehicle_id: int) -> int:
    sql = f'''
        DELETE FROM 
            t_user_shop_purchase
        WHERE
            user_vehicle_id = %(user_vehicle_id)s
        AND
            gigya_uid = %(gigya_uid)s;
    '''
    params = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id}
    return execute_delete_statement(sql, params)
