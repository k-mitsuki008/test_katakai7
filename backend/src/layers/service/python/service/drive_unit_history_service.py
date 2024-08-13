from common.logger import Logger
from common.decorator.service import service
from common.error.not_expected_error import NotExpectedError
from repository import drive_unit_history_repository as repository

log = Logger()


@service
def registration_drive_unit_history(**kwargs):
    """
    ドライブユニット履歴テーブル更新登録
    """
    # 最新のドライブユニット履歴から最新のDu識別子を取得
    input_du_serial_number = kwargs['du_serial_number']
    latest_drive_unit_history = repository.get_latest_drive_unit_history(kwargs['gigya_uid'], kwargs['user_vehicle_id'])
    latest_du_serial_number = latest_drive_unit_history.get('du_serial_number') if latest_drive_unit_history else None

    # ドライブユニット履歴を更新登録
    if latest_du_serial_number is None:
        # INPUTのDU識別子レコードを追加
        result = repository.insert_t_drive_unit_history(**kwargs)
    elif input_du_serial_number != latest_du_serial_number:
        # 旧レコードのDU最終接続タイムスタンプを更新
        update_items = {"du_last_timestamp": kwargs['timestamp']}
        result = repository.update_latest_drive_unit_history(kwargs['gigya_uid'], kwargs['user_vehicle_id'], **update_items)
        # INPUTのDU識別子レコードを追加
        result = repository.insert_t_drive_unit_history(**kwargs) if result else None
    else:
        # DU最終ODOMETERを更新
        update_items = {"du_last_odometer": kwargs['du_odometer']}
        result = repository.update_latest_drive_unit_history(kwargs['gigya_uid'], kwargs['user_vehicle_id'], **update_items)

    if result is None:
        raise NotExpectedError()
