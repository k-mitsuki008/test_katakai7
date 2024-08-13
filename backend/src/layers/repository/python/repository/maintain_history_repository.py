from common.logger import Logger
from common.utils.time_utils import convert_datetime_to_str, get_current_datetime
from common.rds.core import execute_select_statement
from common.rds.core import execute_insert_statement
from common.rds.core import execute_update_statement
from common.rds.core import execute_delete_statement
from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def insert_t_maintain_history(**kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')

    sql = f'''
      INSERT INTO
        t_maintain_history(
          {', '.join(kwargs.keys())},
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %({')s, %('.join(kwargs.keys())})s,
          %(now_str)s,
          %(gigya_uid)s
        )
        RETURNING maintain_history_id;
    '''

    params = {**kwargs, 'now_str': now_str}
    rec = execute_insert_statement(sql, params, returning=True)
    return rec[0][0]


def update_t_maintain_history(maintain_history_id: int, gigya_uid: str, maintain_item_code: str, user_vehicle_id: int, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
        UPDATE
            t_maintain_history
        SET
          {update_sets}
        WHERE
            delete_flag = False
            AND maintain_history_id = %(maintain_history_id)s
            AND gigya_uid = %(gigya_uid)s
            AND maintain_item_code = %(maintain_item_code)s
            AND user_vehicle_id = %(user_vehicle_id)s;
    '''

    params = {'maintain_history_id': maintain_history_id,
              'gigya_uid': gigya_uid,
              'maintain_item_code': maintain_item_code,
              'user_vehicle_id': user_vehicle_id,
              **kwargs,
              'now_str': now_str}
    return execute_update_statement(sql, params)


def get_t_maintain_history(gigya_uid: str, user_vehicle_id: int, maintain_item_code: str = None, maintain_implement_date: str = None) -> dict:
    maintain_item_code_selector = "AND maintain_item_code = %(maintain_item_code)s" if maintain_item_code else ''
    maintain_implement_date_selector = "AND maintain_implement_date = to_timestamp(%(maintain_implement_date)s, 'YYYY-MM-DD')" if maintain_implement_date else ''

    sql = f'''
      SELECT 
        maintain_history_id
        , gigya_uid
        , user_vehicle_id
        , maintain_item_code
        , model_code
        , maintain_implement_date
        , maintain_location
        , maintain_cost
        , maintain_required_time
        , maintain_memo
        , maintain_du_serial_number
        , maintain_du_last_timestamp
        , maintain_du_last_odometer
        , maintain_image_ids
      FROM 
        t_maintain_history
      WHERE
        delete_flag = False
        AND gigya_uid = %(gigya_uid)s
        AND user_vehicle_id = %(user_vehicle_id)s
        {maintain_item_code_selector}
        {maintain_implement_date_selector};
    '''

    parameters_dict: dict = {
        'gigya_uid': gigya_uid,
        'user_vehicle_id': user_vehicle_id,
        'maintain_item_code': maintain_item_code,
        'maintain_implement_date': maintain_implement_date
    }
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0] if rec else None


def get_maintain_history_limit(
    gigya_uid: str,
    user_vehicle_id: int,
    limit: int,
    offset: int,
    maintain_item_code: str = None,
) -> list:
    selector = 'AND mh.maintain_item_code = %(maintain_item_code)s' if maintain_item_code else ''

    sql: str = f'''
      SELECT
        mh.maintain_history_id,
        mh.maintain_item_code,
        min.maintain_item_name,
        mh.maintain_implement_date,
        mh.maintain_location
      FROM
        t_maintain_history as mh
        INNER JOIN t_user_vehicle as uv
        ON mh.user_vehicle_id = uv.user_vehicle_id AND uv.delete_flag = false
        INNER JOIN m_maintain_item_name as min
        ON mh.maintain_item_code = min.maintain_item_code
      WHERE
        uv.delete_flag = False
        AND mh.gigya_uid =  %(gigya_uid)s
        AND mh.user_vehicle_id = %(user_vehicle_id)s
        {selector}
      ORDER BY
        mh.maintain_implement_date DESC, min.sort_order
      LIMIT %(limit)s
      OFFSET %(offset)s;
    '''

    parameters_dict: dict = {
        'gigya_uid': gigya_uid,
        'user_vehicle_id': user_vehicle_id,
        'maintain_item_code': maintain_item_code,
        'limit': limit,
        'offset': offset
    }
    rec = execute_select_statement(sql, parameters_dict)

    return rec


def get_maintain_history_all_count(
    gigya_uid: str,
    user_vehicle_id: int,
    maintain_item_code: str = None,
) -> dict:
    selector = 'AND maintain_item_code = %(maintain_item_code)s' if maintain_item_code else ''
    sql: str = F'''
      SELECT
        count(maintain_item_code)
      FROM
        t_maintain_history
      WHERE
        delete_flag = False
      AND gigya_uid = %(gigya_uid)s
      AND user_vehicle_id = %(user_vehicle_id)s
      {selector}
      ;
    '''

    parameters_dict: dict = {
        'gigya_uid': gigya_uid,
        'user_vehicle_id': user_vehicle_id,
        'maintain_item_code': maintain_item_code,
    }
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0]


def delete_t_maintain_history(gigya_uid: str, user_vehicle_id: int) -> int:
    sql = f'''
        DELETE FROM 
            t_maintain_history
        WHERE
            user_vehicle_id = %(user_vehicle_id)s
        AND
            gigya_uid = %(gigya_uid)s;
    '''
    params = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id}
    return execute_delete_statement(sql, params)


def get_maintain_history_detail(gigya_uid: str, maintain_history_id: int, user_vehicle_id: int) -> dict:
    sql = '''
        SELECT 
          mh.maintain_history_id
          , mh.user_vehicle_id
          , mh.maintain_item_code
          , min.maintain_item_name
          , mh.model_code
          , mh.maintain_implement_date
          , mh.maintain_location
          , mh.maintain_cost
          , mh.maintain_required_time
          , mh.maintain_memo
          , mh.maintain_du_serial_number
          , mh.maintain_du_last_timestamp
          , mh.maintain_du_last_odometer
          , mh.maintain_image_ids
        FROM 
          t_maintain_history as mh
        INNER JOIN t_user_vehicle as uv
          ON mh.user_vehicle_id = uv.user_vehicle_id AND uv.delete_flag = false
        INNER JOIN m_maintain_item_name as min
          ON mh.maintain_item_code = min.maintain_item_code
        WHERE
          uv.delete_flag = False
          AND mh.delete_flag = False
          AND mh.gigya_uid = %(gigya_uid)s
          AND mh.user_vehicle_id = %(user_vehicle_id)s
          AND mh.maintain_history_id = %(maintain_history_id)s;
      '''

    parameters_dict: dict = {'gigya_uid': gigya_uid, 'maintain_history_id': maintain_history_id, 'user_vehicle_id': user_vehicle_id}
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0] if rec else None


def delete_t_maintain_history_maintain_history_id(gigya_uid: str, maintain_history_id: int, user_vehicle_id: int) -> int:
    sql = f'''
          DELETE FROM 
              t_maintain_history
          WHERE
              maintain_history_id = %(maintain_history_id)s
          AND
              gigya_uid = %(gigya_uid)s
          AND 
              user_vehicle_id = %(user_vehicle_id)s;
      '''
    params = {'gigya_uid': gigya_uid, 'maintain_history_id': maintain_history_id, "user_vehicle_id": user_vehicle_id}
    return execute_delete_statement(sql, params)


def get_t_maintain_history_all() -> list:
    sql = '''
        SELECT 
          gigya_uid
          , maintain_image_ids
        FROM 
          t_maintain_history
        ORDER BY
          gigya_uid;
      '''
    return execute_select_statement(sql)
