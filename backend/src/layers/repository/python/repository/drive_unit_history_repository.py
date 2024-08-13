from common.logger import Logger
from common.utils.time_utils import convert_datetime_to_str, get_current_datetime
from common.rds.core import execute_select_statement
from common.rds.core import execute_insert_statement
from common.rds.core import execute_update_statement
from common.rds.core import execute_delete_statement
from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def insert_t_drive_unit_history(gigya_uid: str, user_vehicle_id: int, du_serial_number: str, timestamp: str, du_odometer: int) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')

    sql = f'''
      INSERT INTO 
        t_drive_unit_history(
          user_vehicle_id,
          du_first_timestamp,
          gigya_uid,
          du_serial_number,
          du_first_odometer,
          du_last_odometer,
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(user_vehicle_id)s,
          %(timestamp)s,
          %(gigya_uid)s,
          %(du_serial_number)s,
          %(du_odometer)s,
          %(du_odometer)s,
          %(now_str)s,
          %(gigya_uid)s
        );
      '''
    params = {'user_vehicle_id': user_vehicle_id,
              'timestamp': timestamp,
              'gigya_uid': gigya_uid,
              'du_serial_number': du_serial_number,
              'du_odometer': du_odometer,
              'now_str': now_str}
    res = execute_insert_statement(sql, params)

    return res


def update_latest_drive_unit_history(gigya_uid: str, user_vehicle_id: int, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    update_sets = create_update_set_sql(**kwargs)
    sql = f'''
        UPDATE
            t_drive_unit_history
        SET
            {update_sets}
        WHERE
            delete_flag = false
            AND user_vehicle_id = %(user_vehicle_id)s
            AND gigya_uid =  %(gigya_uid)s
            AND du_last_timestamp = to_timestamp('9999/12/31 23:59:59.999', 'YYYY/MM/DD HH24:MI:SS.MS')
    '''

    params = {'user_vehicle_id': user_vehicle_id,
              'gigya_uid': gigya_uid,
              **kwargs,
              'now_str': now_str}
    update_count = execute_update_statement(sql, params)
    return update_count


def get_latest_drive_unit_history(gigya_uid: str, user_vehicle_id: int) -> dict:
    """
    最新のドライブユニット履歴を取得
    """
    sql: str = '''
      SELECT 
        du_serial_number,
        du_first_timestamp,
        CASE 
          -- du最終接続タイムスタンプが最新なら現在日時を最終接続タイムスタンプに設定
          WHEN du_last_timestamp = to_timestamp('9999/12/31 23:59:59.999', 'YYYY/MM/DD HH24:MI:SS.US') 
            THEN %(now)s
          ELSE
            du_last_timestamp
        END as du_last_timestamp,
        (du_last_odometer - du_first_odometer) as odometer,
        du_first_odometer,
        du_last_odometer
      FROM
        t_drive_unit_history
      WHERE
        delete_flag = false
        AND user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid =  %(gigya_uid)s
        AND du_last_timestamp = to_timestamp('9999/12/31 23:59:59.999', 'YYYY/MM/DD HH24:MI:SS.US')
      ORDER BY du_last_timestamp DESC
      LIMIT 1;
    '''

    now = get_current_datetime()
    parameters_dict: dict = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id, 'now': now}
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0] if rec else None


def get_oldest_drive_unit_history(gigya_uid: str, user_vehicle_id: int) -> dict:
    """
    初回接続時のドライブユニット履歴を取得
    """
    sql: str = '''
      SELECT 
        du_serial_number,
        du_first_timestamp,
        CASE 
          -- du最終接続タイムスタンプが最新なら現在日時を最終接続タイムスタンプに設定
          WHEN du_last_timestamp = to_timestamp('9999/12/31 23:59:59.999', 'YYYY/MM/DD HH24:MI:SS.US') 
            THEN %(now)s
          ELSE
            du_last_timestamp
        END as du_last_timestamp,
        (du_last_odometer - du_first_odometer) as odometer,
        du_first_odometer,
        du_last_odometer
      FROM
        t_drive_unit_history
      WHERE
        delete_flag = false
        AND user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid =  %(gigya_uid)s
      ORDER BY du_last_timestamp
      LIMIT 1;
    '''

    now = get_current_datetime()
    parameters_dict: dict = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id, 'now': now}
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0] if rec else None


def get_last_maintain_archive(gigya_uid: str, user_vehicle_id: int, last_maintain_du_serial_number: str, last_maintain_du_timestamp: str) -> dict:
    """
    前回メンテナンス時点のDUの走行距離、走行時間を取得
    """
    sql: str = '''
      SELECT 
        du_serial_number,
        du_first_timestamp,
        CASE 
          -- du最終接続タイムスタンプが最新なら現在日時を最終接続タイムスタンプに設定
          WHEN du_last_timestamp = to_timestamp('9999/12/31 23:59:59.999', 'YYYY/MM/DD HH24:MI:SS.US') 
            THEN %(now)s
          ELSE
            du_last_timestamp
        END as du_last_timestamp,
        (du_last_odometer - du_first_odometer) as odometer,
        du_first_odometer,
        du_last_odometer
      FROM
        t_drive_unit_history
      WHERE
        delete_flag = false
        AND user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid =  %(gigya_uid)s
        AND du_serial_number = %(last_maintain_du_serial_number)s
        AND du_last_timestamp > to_timestamp(%(last_maintain_du_timestamp)s, 'YYYY/MM/DD HH24:MI:SS.US')
      ORDER BY du_last_timestamp
      LIMIT 1;
    '''

    now = get_current_datetime()
    parameters_dict: dict = {
        'gigya_uid': gigya_uid,
        'user_vehicle_id': user_vehicle_id,
        'last_maintain_du_serial_number': last_maintain_du_serial_number,
        'last_maintain_du_timestamp': last_maintain_du_timestamp,
        'now': now
    }
    rec = execute_select_statement(sql, parameters_dict)
    return rec[0] if rec else None


def get_after_last_maintain_archive_list(gigya_uid: str, user_vehicle_id: int, last_maintain_du_timestamp: str) -> list:
    """
   　前回メンテナンス履歴のDUより後に追加されたDUの走行距離、走行時間のリストを取得
    """
    sql: str = '''
      SELECT 
        user_vehicle_id,
        gigya_uid,
        du_serial_number,
        CASE 
          WHEN du_last_timestamp = to_timestamp('9999/12/31 23:59:59.999', 'YYYY/MM/DD HH24:MI:SS.US') 
            THEN 
              (%(now)s - du_first_timestamp)
          ELSE
              (du_last_timestamp - du_first_timestamp)
        END as days,
        (du_last_odometer - du_first_odometer) as odometer
      FROM
        t_drive_unit_history
      WHERE
        delete_flag = false
        AND user_vehicle_id = %(user_vehicle_id)s
        AND gigya_uid =  %(gigya_uid)s
        AND du_first_timestamp > to_timestamp(%(last_maintain_du_timestamp)s, 'YYYY/MM/DD HH24:MI:SS.US')
      ORDER BY du_last_timestamp;
    '''

    now = get_current_datetime()
    parameters_dict: dict = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id,
                             'last_maintain_du_timestamp': last_maintain_du_timestamp,
                             'now': now}
    rec = execute_select_statement(sql, parameters_dict)

    return rec


def delete_t_drive_unit_history(gigya_uid: str, user_vehicle_id: int) -> int:
    sql = f'''
        DELETE FROM 
            t_drive_unit_history
        WHERE
            user_vehicle_id = %(user_vehicle_id)s
        AND
            gigya_uid = %(gigya_uid)s;
    '''
    params = {'gigya_uid': gigya_uid, 'user_vehicle_id': user_vehicle_id}
    return execute_delete_statement(sql, params)
