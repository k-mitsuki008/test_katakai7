from common.logger import Logger
from common.utils.time_utils import convert_datetime_to_str, get_current_datetime
from common.rds.core import execute_select_statement
from common.rds.core import execute_insert_statement
from common.rds.core import execute_delete_statement
from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def upsert_t_user_setting_maintain(user_vehicle_id: int, gigya_uid: str, **kwargs) -> any:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    update_sets = create_update_set_sql(gigya_uid=gigya_uid, **kwargs)

    sql = f'''
      INSERT INTO 
        t_user_setting_maintain(
          user_vehicle_id,
          gigya_uid,
          {', '.join(kwargs.keys())},
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(user_vehicle_id)s,
          %(gigya_uid)s,
          %({')s, %('.join(kwargs.keys())})s,
          %(now_str)s,
          %(gigya_uid)s
        )
      ON CONFLICT(user_vehicle_id)
      DO UPDATE SET
        {update_sets}
      RETURNING maintain_consciousness;
      '''
    params = {'user_vehicle_id': user_vehicle_id, 'gigya_uid': gigya_uid, **kwargs, 'now_str': now_str}
    rec = execute_insert_statement(sql, params, returning=True)
    return rec[0][0]


def get_user_setting_maintains(user_vehicle_id: int) -> list:
    sql = f'''
        SELECT
            usm.user_vehicle_id
            , usm.gigya_uid
            , usm.maintain_consciousness
            , mi.maintain_item_code
            , min.maintain_item_name
            , usmi.maintain_item_alert
            , usmi.maintain_item_alert_status 
        FROM
            t_user_vehicle uv
            INNER JOIN m_maintain_item mi
            ON uv.user_vehicle_id = %(user_vehicle_id)s AND uv.model_code = mi.model_code AND uv.delete_flag = false AND mi.delete_flag = false
            INNER JOIN m_maintain_item_name min
            ON mi.maintain_item_code = min.maintain_item_code AND min.delete_flag = false
            LEFT JOIN t_user_setting_maintain usm 
            ON uv.user_vehicle_id = usm.user_vehicle_id AND usm.delete_flag = false
            LEFT JOIN t_user_setting_maintain_item usmi 
            ON usm.user_vehicle_id = usmi.user_vehicle_id AND mi.maintain_item_code = usmi.maintain_item_code AND usmi.delete_flag = false
        ORDER BY
            min.sort_order
    '''
    parameters_dict = {'user_vehicle_id': user_vehicle_id}
    rec = execute_select_statement(sql, parameters_dict)
    return rec


def get_user_maintain_setting_user_vehicle_id(user_vehicle_id: int) -> list:
    sql: str = '''
      SELECT
        usm.user_vehicle_id,
        usm.maintain_consciousness,
        usmi.maintain_item_code,
        min.maintain_item_name,
        usmi.maintain_item_alert
      FROM
        t_user_setting_maintain_item usmi
        INNER JOIN m_maintain_item_name min
        ON usmi.maintain_item_code = min.maintain_item_code
        INNER JOIN t_user_setting_maintain usm
        ON usmi.user_vehicle_id = usm.user_vehicle_id
      WHERE
        usmi.delete_flag = false
      AND usmi.user_vehicle_id = %(user_vehicle_id)s
      ORDER BY
        min.sort_order;
    '''

    parameters_dict: dict = {'user_vehicle_id': user_vehicle_id}
    rec = execute_select_statement(sql, parameters_dict)
    return rec


def delete_t_user_setting_maintain(gigya_uid: str, user_vehicle_id: int) -> int:
    sql = f'''
        WITH delete_user_setting_maintain as (
            DELETE FROM 
                t_user_setting_maintain
            WHERE
                user_vehicle_id = %(user_vehicle_id)s
                AND gigya_uid = %(gigya_uid)s
            RETURNING user_vehicle_id
        )
         DELETE FROM 
             t_user_setting_maintain_item
         WHERE
             user_vehicle_id IN (
                SELECT
                    user_vehicle_id
                FROM
                    delete_user_setting_maintain
             );
    '''
    params = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id}
    return execute_delete_statement(sql, params)
