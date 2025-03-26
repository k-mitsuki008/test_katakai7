import os
from common.logger import Logger
from datetime import datetime
from common.utils.time_utils import get_current_datetime, convert_datetime_to_str, replace_time
from common.utils.aws_utils import get_constant
from common.decorator.service import service
from repository import maintain_item_repository
from repository import drive_unit_history_repository

log = Logger()


@service
def get_maintain_items(gigya_uid: str, user_vehicle_id: int, notifications_maintain_item_code: str = None) -> list:
    """
    メンテナンス指示一覧取得
    """
    maintain_items = maintain_item_repository.get_maintain_items(user_vehicle_id, notifications_maintain_item_code)
    log.info(f'MAINTAIN_ITEMS= {maintain_items}')
    if len(maintain_items) == 0:
        return maintain_items

    # メンテナンスアイコン取得URLを設定
    s3_bucket_prefix = get_constant('S3_BUCKET_PREFIX', code='ICON')
    cloud_front_domain_name = os.environ['CLOUD_FRONT_DOMAIN_NAME']

    # 初回Du接続履歴を取得
    oldest_du_history = drive_unit_history_repository.get_oldest_drive_unit_history(gigya_uid, user_vehicle_id)
    log.info(f'初回接続時点のDU履歴: {oldest_du_history}')

    for item in maintain_items:
        # 前回メンテナンス以降のDuの走行距離or走行時間をmaintain_archiveに設定
        maintain_item_code = item['maintain_item_code']
        maintain_type_code = item['maintain_type_code']
        last_maintain_implement_date = item.pop('last_maintain_implement_date')
        last_maintain_du_serial_number = item.pop('last_maintain_du_serial_number')
        last_maintain_du_timestamp = item.pop('last_maintain_du_last_timestamp')
        last_maintain_du_odometer = item.pop('last_maintain_du_last_odometer')
        log.info(f'\n ITEM={maintain_item_code}, {maintain_type_code}, {last_maintain_du_serial_number}')

        # Du履歴が無ければメンテナンス記録=0
        if oldest_du_history is None:
            item['maintain_archive'] = 0

        else:
            # 前回メンテナンス履歴あり: 前回メンテナンス以降の実績値を計算
            if last_maintain_implement_date:
                # メンテナンス指示種別: 走行距離
                if maintain_type_code == get_constant('MAINTENANCE_TYPE_CODE', 'DISTANCE', '02'):
                    item['maintain_archive'] = _calc_odometer(
                                        gigya_uid, user_vehicle_id,
                                        last_maintain_du_serial_number,
                                        last_maintain_du_timestamp,
                                        last_maintain_du_odometer)
                # メンテナンス指示種別: 経過日数or定期点検
                else:
                    item['maintain_archive'] = _calc_days(last_maintain_implement_date)

            # 前回メンテナンス履歴無し: 初回接続Du履歴以降の実績値を計算
            else:
                # メンテナンス指示種別: 走行距離
                if maintain_type_code == get_constant('MAINTENANCE_TYPE_CODE', 'DISTANCE', '02'):
                    item['maintain_archive'] = _calc_odometer_oldest(gigya_uid, user_vehicle_id)
                # メンテナンス指示種別: 経過日数or定期点検
                else:
                    item['maintain_archive'] = _calc_days_oldest(oldest_du_history)

        # 定期点検の場合、maintain_intervalをメンテナンス回数に応じて設定
        if maintain_type_code == get_constant('MAINTENANCE_TYPE_CODE', 'ROUTINE', '03'):
            maintain_count = maintain_item_repository.get_maintain_count(gigya_uid, user_vehicle_id, maintain_item_code)
            log.info(f'前回メンテナンス回数: {maintain_count}')

            # maintain_intervalは初回は初回DU接続日から60日、その次は前回メンテナンスから120日、それ以降は180日
            if maintain_count == 0:
                interval = 60
            elif maintain_count == 1:
                interval = 120
            else:
                interval = 180
            item['maintain_interval'] = interval
            # フロント返却用にメンテナンス種別を日付に変更。
            item['maintain_type_code'] = get_constant('MAINTENANCE_TYPE_CODE', 'TIME', '01')

        # メンテナンス通知のバッチ処理から処理を呼んだ場合アイコンURLの設定はしない
        if notifications_maintain_item_code is None:
            # アイコンURL設定
            item['maintain_item_icon_url'] = cloud_front_domain_name + s3_bucket_prefix + item["maintain_file_name_icon"]
        item.pop('maintain_file_name_icon')

    return maintain_items


def _calc_odometer(gigya_uid: str, user_vehicle_id: int, last_maintain_du_serial_number: str, last_maintain_du_timestamp: datetime, last_maintain_du_odometer: int) -> int:
    """
    前回メンテナンス以降の走行距離を算出
    走行距離 = メンテナンス履歴Duに紐づくDu履歴の「DU最終接続Odometer」 - メンテナンス履歴の「メンテナンスDU最終接続Odometer」の値 +
             メンテナンス履歴Duより後に追加された車両に紐づくDu履歴の「DU最終接続Odometer」 - 「DU初回接続Odometer」の合算値
    """
    # 前回メンテナンス時点のDU履歴を取得
    last_maintain_du_timestamp_str = convert_datetime_to_str(last_maintain_du_timestamp, '%Y-%m-%d %H:%M:%S.%f')
    log.info(f'前回メンテナンスdu更新日時={last_maintain_du_timestamp}')

    last_du_history = drive_unit_history_repository.get_last_maintain_archive(
        gigya_uid, user_vehicle_id, last_maintain_du_serial_number, last_maintain_du_timestamp_str)
    log.info(f'前回メンテナンス日時時点のDU履歴: {last_du_history}')

    # 前回メンテナンス履歴のDUより後に追加されたDUの走行距離、走行時間のリストを取得
    after_last_du_history_list = drive_unit_history_repository.get_after_last_maintain_archive_list(
                                            gigya_uid, user_vehicle_id, last_maintain_du_timestamp_str)
    log.info(f'前回メンテより後に更新されたDUの走行距離、日数リスト: {after_last_du_history_list}')

    # 前回メンテナンス以降の走行距離を取得
    last_archive = 0
    if last_du_history:
        last_archive = last_du_history.get("du_last_odometer") - last_maintain_du_odometer
        log.info("前回メンテナンス以降の走行距離 = 前回メンテナンスDU最終走行距離 - 前回メンテナンスDU走行距離")
        log.info(f'{last_archive} = {last_du_history.get("du_last_odometer")} - {last_maintain_du_odometer}')

    last_after_archive = sum([x.get("odometer", 0) for x in after_last_du_history_list])
    log.info(f'前回メンテナンスより後の走行距離: {last_after_archive}')
    maintain_archive = last_archive + last_after_archive

    return maintain_archive


def _calc_odometer_oldest(gigya_uid: str, user_vehicle_id: int) -> int:
    """
    初回Du接続以降に追加されたDuの走行距離の合計を取得
    """
    after_last_du_history_list = drive_unit_history_repository.get_after_last_maintain_archive_list(
                                                gigya_uid, user_vehicle_id, '1900-01-01 00:00:00.000')
    log.info(f'初回Du接続以降に追加されたDUの走行距離、日数リスト: {after_last_du_history_list}')

    maintain_archive = sum([x.get("odometer", 0) for x in after_last_du_history_list])
    log.info(f'初回Du接続以降に追加されたDUの走行距離: {maintain_archive}')

    return maintain_archive


def _calc_days(last_maintain_implement_date: datetime) -> int:
    """
    前回メンテナンス以降の経過日数の算出
    経過日数 = 現在日(00:00:00+00:00) - 前回メンテナンス履歴.メンテナンス日付(00:00:00+00:00)
    """
    # 前回メンテナンス以降の経過日数を取得
    now_date = replace_time(get_current_datetime())
    last_maintain_date = replace_time(last_maintain_implement_date)

    last_archive = now_date - last_maintain_date
    log.info("前回メンテナンス以降の経過日数 = 現在日時 - 前回メンテナンスDU更新日時")
    log.info(f"{last_archive} = {now_date} - {last_maintain_date}")

    return last_archive.days


def _calc_days_oldest(oldest_du_history: dict) -> int:
    """
    初回Du接続以降の経過日数の算出
    経過日数 = 現在日(00:00:00+00:00) - 初回接続時点のDU履歴.DU初回接続タイムスタンプの日付(00:00:00+00:00)
    """
    # 前回メンテナンス以降の経過日数を取得
    now_date = replace_time(get_current_datetime())
    last_maintain_date = replace_time(oldest_du_history.get('du_first_timestamp'))

    last_archive = now_date - last_maintain_date
    log.info("前回メンテナンス以降の経過日数 = 現在日時 - 前回メンテナンスDU更新日時")
    log.info(f"{last_archive} = {now_date} - {last_maintain_date}")

    return last_archive.days


@service
def get_maintain_explanation(model_code: str, maintain_item_code: str) -> dict:
    """
    メンテナンス説明取得
    """
    s3_bucket_prefix = get_constant('S3_BUCKET_PREFIX', code='EXPLANATION')
    cloud_front_domain_name = os.environ['CLOUD_FRONT_DOMAIN_NAME']
    body_type_image = get_constant('MAINTENANCE_EXPLANATION_TYPE', 'IMAGE', 2)
    maintain_item_image_url = ''

    # メンテナンス説明を取得
    maintain_explanation_list = maintain_item_repository.get_maintain_explanation(model_code, maintain_item_code)

    # JSON整形処理
    maintain_explanations = []
    bef_title_code = None

    title_rec = []
    for rec in maintain_explanation_list:
        if rec['maintain_title_code'] is None:
            continue

        title_code = rec['maintain_title_code']
        # ユーザ車両レコードを追加
        if bef_title_code != title_code:
            title_rec = {
                "explanation_title": rec['explanation_title'],
                "contents": []
            }
            maintain_explanations.append(title_rec)

        # メンテナンス説明レコードを追加
        if rec['explanation_type'] == body_type_image:
            body = cloud_front_domain_name + s3_bucket_prefix + rec["explanation_body"]
        else:
            body = rec["explanation_body"]

        explanation_rec = {
            "explanation_type": rec['explanation_type'],
            "explanation_body": body
        }
        title_rec['contents'].append(explanation_rec)
        bef_title_code = rec['maintain_title_code']
        maintain_item_image_url = cloud_front_domain_name + s3_bucket_prefix + rec["maintain_file_name_top"]

    result = {
        "maintain_item_code": maintain_item_code,
        "maintain_item_name": maintain_explanation_list[0]['maintain_item_name'] if len(maintain_explanation_list) > 0 else "",
        "maintain_item_image_url": maintain_item_image_url,
        "maintain_explanations": maintain_explanations
    }

    return result
