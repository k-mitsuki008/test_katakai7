from common.logger import Logger
from common.utils.time_utils import convert_datetime_to_str, get_current_datetime
from common.rds.core import execute_select_statement, execute_insert_statement, execute_update_statement, execute_delete_statement
from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def insert_t_user_vehicle(**kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')

    sql = f'''
      INSERT INTO
        t_user_vehicle(
          {', '.join(kwargs.keys())},
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %({')s, %('.join(kwargs.keys())})s,
          %(now_str)s,
          %(gigya_uid)s
        )
        RETURNING user_vehicle_id;
    '''

    params = {**kwargs, 'now_str': now_str}
    rec = execute_insert_statement(sql, params, returning=True)
    return rec[0][0] if rec else None


def update_t_user_vehicle(user_vehicle_id: int, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')

    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
        UPDATE
            t_user_vehicle
        SET
          {update_sets}
        WHERE
            delete_flag = False
            AND user_vehicle_id = %(user_vehicle_id)s;
    '''

    params = {'user_vehicle_id': user_vehicle_id, **kwargs, 'now_str': now_str}
    return execute_update_statement(sql, params)


def update_t_user_vehicle_unmanaged(gigya_uid: str, user_vehicle_id: int, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
        UPDATE
            t_user_vehicle
        SET
          {update_sets}
        WHERE
            delete_flag = False
            AND gigya_uid = %(gigya_uid)s
            AND user_vehicle_id != %(user_vehicle_id)s;
    '''

    params = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id, **kwargs, 'now_str': now_str}
    return execute_update_statement(sql, params)


def delete_t_user_vehicle(gigya_uid: str, user_vehicle_id: int) -> int:
    sql = f'''
        DELETE FROM 
            t_user_vehicle
        WHERE
            gigya_uid = %(gigya_uid)s
            AND user_vehicle_id = %(user_vehicle_id)s;
    '''
    params = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id}
    return execute_delete_statement(sql, params)


def get_user_vehicle_id(gigya_uid: str, user_vehicle_id: int) -> dict:
    sql = '''
      SELECT
        user_vehicle_id
        , gigya_uid
        , model_code
        , vehicle_id
        , vehicle_name
        , managed_flag
        , registered_flag
        , peripheral_identifier
        , complete_local_name
        , equipment_weight
        , vehicle_nickname
      FROM
        t_user_vehicle
      WHERE
        delete_flag = False
        AND user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
    '''

    parameters_dict: dict = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id}
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0] if rec else None


def count_t_user_vehicle(gigya_uid: str) -> int:
    sql = '''
      SELECT 
        count(*) as count
      FROM 
        t_user_vehicle
      WHERE
        delete_flag = False
        AND gigya_uid = %(gigya_uid)s;
    '''

    parameters_dict: dict = {'gigya_uid': gigya_uid}
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0]['count'] if rec else None


def get_user_vehicles(gigya_uid: str, user_vehicle_id=None) -> list:
    selector = 'AND uv.user_vehicle_id = %(user_vehicle_id)s' if user_vehicle_id else ''

    sql = f'''
      SELECT
          uv.user_vehicle_id
          , uv.model_code
          , uv.vehicle_id
          , uv.vehicle_name
          , uv.managed_flag
          , uv.registered_flag
          , uv.peripheral_identifier
          , uv.complete_local_name
          , uv.equipment_weight
          , uv.vehicle_nickname
          , usp.shop_name
          , usp.shop_tel
          , usp.shop_location
          , duh.du_serial_number
          , duh.du_last_odometer
          , c.contact_title
          , c.contact_text
          , c.contact_mail_address
          , usm.maintain_consciousness
          , usmi.maintain_item_code
          , min.maintain_item_name
          , usmi.maintain_item_alert
      FROM
          t_user_vehicle uv
          LEFT JOIN t_drive_unit_history duh
          ON(uv.user_vehicle_id = duh.user_vehicle_id AND uv.gigya_uid = duh.gigya_uid AND duh.du_last_timestamp = '9999/12/31 23:59:59.999' AND duh.delete_flag = False)
          LEFT JOIN t_user_shop_purchase usp
          ON(uv.user_vehicle_id = usp.user_vehicle_id AND uv.gigya_uid = usp.gigya_uid AND usp.delete_flag = False)
          LEFT JOIN m_contact c
          ON(uv.model_code = c.model_code AND c.delete_flag = False )
          LEFT JOIN t_user_setting_maintain usm
          ON(uv.user_vehicle_id = usm.user_vehicle_id AND uv.gigya_uid = usm.gigya_uid AND usm.delete_flag = False)
          LEFT JOIN t_user_setting_maintain_item usmi
          ON(uv.user_vehicle_id = usmi.user_vehicle_id AND usmi.delete_flag = False)
          LEFT JOIN m_maintain_item_name min
          ON(usmi.maintain_item_code = min.maintain_item_code AND min.delete_flag = False)
      WHERE
          uv.delete_flag = False
          AND uv.gigya_uid =  %(gigya_uid)s
          {selector}
      ORDER BY
          uv.user_vehicle_id, uv.model_code, min.sort_order;
    '''

    parameters_dict: dict = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id}
    rec = execute_select_statement(sql, parameters_dict)
    return rec


def get_user_vehicle_check(gigya_uid: str, vehicle_id: str) -> dict:
    sql = '''
      SELECT
        user_vehicle_id
        , gigya_uid
        , model_code
        , vehicle_id
        , vehicle_name
        , managed_flag
        , registered_flag
        , peripheral_identifier
        , complete_local_name
      FROM
        t_user_vehicle
      WHERE
        delete_flag = False
        AND vehicle_id = %(vehicle_id)s
        AND gigya_uid = %(gigya_uid)s;
    '''

    parameters_dict: dict = {'gigya_uid': gigya_uid, 'vehicle_id': vehicle_id}
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0] if rec else None
