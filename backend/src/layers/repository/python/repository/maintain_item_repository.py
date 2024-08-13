from common.logger import Logger
from common.utils.time_utils import get_current_datetime
from common.rds.core import execute_select_statement
from common.utils.aws_utils import get_constant

log = Logger()


def get_maintain_items(user_vehicle_id: int, maintain_item_code: str = None) -> list:
    """
    メンテナンス指示一覧取得
    """

    add_sql = ""
    # メンテナンス通知のバッチ処理はアイテムコードで絞る
    if maintain_item_code is not None:
        add_sql = f"AND mi.maintain_item_code in ({maintain_item_code})"

    maintenance_consciousness = get_constant('MAINTENANCE_CONSCIOUSNESS')
    sql = f'''
    with mh_latest as (
        -- メンテナンス履歴から最新レコード一覧を取得
        SELECT
            mh.user_vehicle_id
            ,mh.maintain_item_code
            , mh.maintain_implement_date as last_maintain_implement_date
            , mh.maintain_du_serial_number as last_maintain_du_serial_number
            , mh.maintain_du_last_timestamp as last_maintain_du_last_timestamp
            , mh.maintain_du_last_odometer as last_maintain_du_last_odometer
        FROM
            t_maintain_history mh 
        WHERE
            CONCAT(mh.maintain_item_code, to_char(mh.maintain_implement_date, 'YYYYMMDDHH24MISS')) IN ( 
                SELECT
                    CONCAT(mh2.maintain_item_code, to_char(MAX(maintain_implement_date), 'YYYYMMDDHH24MISS'))
                FROM
                    t_maintain_history mh2 
                WHERE
                    mh2.delete_flag = false 
                    AND mh2.user_vehicle_id = %(user_vehicle_id)s
                    AND mh2.maintain_implement_date < %(now)s
                GROUP BY mh2.maintain_item_code
            ) 
            AND mh.user_vehicle_id = %(user_vehicle_id)s
    )
    SELECT 
          mi.maintain_item_code
          , min.maintain_item_name
          , min.maintain_file_name_icon
          , mi.maintain_type_code
          , CASE 
              WHEN usm.maintain_consciousness = '{maintenance_consciousness['HIGH']}' THEN mi.maintain_interval_high
              WHEN usm.maintain_consciousness = '{maintenance_consciousness['MIDDLE']}' THEN mi.maintain_interval_middle
              WHEN usm.maintain_consciousness = '{maintenance_consciousness['LOW']}' THEN mi.maintain_interval_low
              ELSE mi.maintain_interval_high
            END as maintain_interval
          , min.sort_order as priority
          , mh_latest.last_maintain_implement_date as last_maintain_implement_date
          , mh_latest.last_maintain_du_serial_number as last_maintain_du_serial_number
          , mh_latest.last_maintain_du_last_timestamp as last_maintain_du_last_timestamp
          , mh_latest.last_maintain_du_last_odometer as last_maintain_du_last_odometer
    FROM 
          m_maintain_item mi
          INNER JOIN m_maintain_item_name min
          ON mi.maintain_item_code = min.maintain_item_code AND min.delete_flag = false
          INNER JOIN t_user_vehicle uv
          ON mi.model_code = uv.model_code AND uv.user_vehicle_id = %(user_vehicle_id)s AND uv.delete_flag = false
          INNER JOIN t_user_setting_maintain usm
          ON uv.user_vehicle_id = usm.user_vehicle_id AND usm.delete_flag = false
          LEFT OUTER JOIN mh_latest
          ON mi.maintain_item_code = mh_latest.maintain_item_code AND uv.user_vehicle_id = mh_latest.user_vehicle_id
    WHERE
          mi.delete_flag = false
          {add_sql}
    ORDER BY min.sort_order;
    '''

    now = get_current_datetime()
    parameters_dict: dict = {'user_vehicle_id': user_vehicle_id, 'now': now}
    rec = execute_select_statement(sql, parameters_dict)

    return rec


def get_maintain_count(gigya_uid: str, user_vehicle_id: int, maintain_item_code: str) -> int:
    """
    メンテナンス実施回数を取得
    """

    sql = """
    SELECT
        count(maintain_history_id) as maintain_count
    FROM
        t_maintain_history
    WHERE
        delete_flag = false
        AND gigya_uid = %(gigya_uid)s
        AND user_vehicle_id = %(user_vehicle_id)s
        AND maintain_item_code = %(maintain_item_code)s
        AND maintain_implement_date < %(now)s
    """

    now = get_current_datetime()
    parameters_dict: dict = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id, 'maintain_item_code': maintain_item_code, 'now': now}
    rec = execute_select_statement(sql, parameters_dict)

    return rec[0]['maintain_count']


def get_maintain_explanation(model_code: str, maintain_item_code: str) -> list:
    """
    メンテナンス説明取得
    """

    sql = """
    SELECT
        mi.maintain_item_code,
        min.maintain_item_name,
        mi.maintain_file_name_top,
        mt.maintain_title_code,
        me.maintain_explanation_code,
        mt.explanation_title,
        me.explanation_type,
        me.explanation_body
    FROM 
        m_maintain_item mi
        INNER JOIN m_maintain_item_name min
            ON mi.maintain_item_code = min.maintain_item_code AND min.delete_flag = false
        LEFT JOIN m_maintain_title mt
            ON mi.model_code = mt.model_code 
            AND mi.maintain_item_code = mt.maintain_item_code 
            AND mt.delete_flag = false 
        LEFT JOIN m_maintain_explanation me
            ON mt.model_code = me.model_code
            AND mt.maintain_title_code = me.maintain_title_code
            AND mt.maintain_item_code = me.maintain_item_code 
            AND me.delete_flag = false
    WHERE
        mi.delete_flag = false
        AND mi.model_code = %(model_code)s
        AND mi.maintain_item_code = %(maintain_item_code)s
    ORDER BY mt.sort_order, me.sort_order;
    """

    parameters_dict: dict = {'maintain_item_code': maintain_item_code, 'model_code': model_code}
    rec = execute_select_statement(sql, parameters_dict)

    return rec
