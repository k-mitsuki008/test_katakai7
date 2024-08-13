from common.logger import Logger
from common.utils.time_utils import convert_datetime_to_str, get_current_datetime
from common.rds.core import execute_insert_statement
from repository.utils.repository_utils import create_update_set_sql
from common.rds.core import execute_select_statement

log = Logger()


def upsert_t_user_setting_maintain_item(user_vehicle_id: int, maintain_item_code: str, gigya_uid: str, **kwargs) -> any:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
      INSERT INTO 
        t_user_setting_maintain_item(
          user_vehicle_id,
          maintain_item_code,
          {', '.join(kwargs.keys())},
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(user_vehicle_id)s,
          %(maintain_item_code)s,
          %({')s, %('.join(kwargs.keys())})s,
          %(now_str)s,
          %(gigya_uid)s
        )
      ON CONFLICT(user_vehicle_id, maintain_item_code)
      DO UPDATE SET
        {update_sets}
      RETURNING maintain_item_alert;
    '''
    params = {'user_vehicle_id': user_vehicle_id, 'maintain_item_code': maintain_item_code, **kwargs, 'now_str': now_str, 'gigya_uid': gigya_uid}
    rec = execute_insert_statement(sql, params, returning=True)
    return rec[0][0]


def get_t_user_setting_maintain_item() -> list:
    """
    メンテナンス指示一覧取得
    """
    sql = f'''
    SELECT 
        uv.user_vehicle_id,
        uv.gigya_uid,
        usmi.maintain_item_code,
        uv.vehicle_name,
        de.device_token

    FROM 
        t_user_setting_maintain_item usmi
        INNER JOIN t_user_vehicle uv ON uv.user_vehicle_id = usmi.user_vehicle_id
        INNER JOIN t_device de ON de.gigya_uid = uv.gigya_uid


    WHERE
        managed_flag = true
        AND maintain_item_alert = true
        AND maintain_item_alert_status in (0,2)
    ORDER BY user_vehicle_id ;
    '''

    rec = execute_select_statement(sql)

    return rec
