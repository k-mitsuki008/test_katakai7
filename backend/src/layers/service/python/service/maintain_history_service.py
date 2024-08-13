import os
from common.logger import Logger
from common.utils.time_utils import convert_datetime_to_str
from common.utils.aws_utils import get_s3_url, get_constant, get_s3_bucket_key
from common.decorator.service import service
from common.error.business_error import BusinessError
from common.error.not_expected_error import NotExpectedError
from repository import user_vehicle_repository, maintain_history_repository, user_setting_maintain_item_repository

log = Logger()


@service
def insert_maintain_history(**kwargs) -> int:
    """
    メンテナンス履歴TBL登録
    """
    # メンテナンス日付の重複チェック
    result = maintain_history_repository.get_t_maintain_history(
        kwargs['gigya_uid'], kwargs['user_vehicle_id'], kwargs['maintain_item_code'], kwargs['maintain_implement_date'])
    if result and convert_datetime_to_str(result.get('maintain_implement_date'), '%Y-%m-%d') == kwargs['maintain_implement_date']:
        raise BusinessError(error_code='E044')

    # メンテナンス記録画像IDリストを','区切りの文字列に整形
    images_str = ','.join([x if x else 'null' for x in kwargs['maintain_image_ids']])
    kwargs['maintain_image_ids'] = images_str
    # 項目名の変更
    kwargs['maintain_du_serial_number'] = kwargs.pop('du_serial_number')
    kwargs['maintain_du_last_timestamp'] = kwargs.pop('du_last_timestamp')
    kwargs['maintain_du_last_odometer'] = kwargs.pop('du_last_odometer')

    # model_codeを取得
    user_vehicle = user_vehicle_repository.get_user_vehicle_id(kwargs['gigya_uid'], kwargs['user_vehicle_id'])
    kwargs['model_code'] = user_vehicle.get('model_code')

    # メンテナンス履歴に１件追加
    inserted_maintain_history_id = maintain_history_repository.insert_t_maintain_history(**kwargs)
    if not inserted_maintain_history_id:
        raise NotExpectedError()

    # メンテナンス通知設定項目のメンテナンス通知状態を更新
    maintain_item_alert = user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item(
                                                                user_vehicle_id=kwargs['user_vehicle_id'],
                                                                maintain_item_code=kwargs['maintain_item_code'],
                                                                gigya_uid=kwargs['gigya_uid'],
                                                                maintain_item_alert_status=get_constant(
                                                                    'INIT_VALUE', 'MAINTAIN_ITEM_ALERT_STATUS'))
    if maintain_item_alert is None:
        raise NotExpectedError()

    # INSERTしたメンテナンス履歴IDを返却
    return inserted_maintain_history_id


@service
def update_maintain_history(maintain_history_id: int, **kwargs):
    """
    メンテナンス履歴TBL更新
    """
    input_gigya_uid = kwargs['gigya_uid']
    input_user_vehicle_id = kwargs['user_vehicle_id']
    input_maintain_implement_date = kwargs['maintain_implement_date']
    input_maintain_item_code = kwargs['maintain_item_code']

    # メンテナンス履歴IDから更新対象のデータを取得
    target_maintain_history = maintain_history_repository.get_maintain_history_detail(input_gigya_uid, maintain_history_id, input_user_vehicle_id)
    # メンテナンス実施日が変更されている場合は日付の重複チェックを行う
    if input_maintain_implement_date != convert_datetime_to_str(target_maintain_history.get('maintain_implement_date'), '%Y-%m-%d'):
        # メンテナンス日付の重複チェック
        result = maintain_history_repository.get_t_maintain_history(
            input_gigya_uid, input_user_vehicle_id, input_maintain_item_code, input_maintain_implement_date)
        if result:
            raise BusinessError(error_code='E044')

    # メンテナンス記録画像IDリストを','区切りの文字列に整形
    images_str = ','.join([x if x else 'null' for x in kwargs['maintain_image_ids']])
    kwargs['maintain_image_ids'] = images_str

    gigya_uid = kwargs.pop('gigya_uid')
    maintain_item_code = kwargs.pop('maintain_item_code')
    user_vehicle_id = kwargs.pop('user_vehicle_id')
    update_count = maintain_history_repository.update_t_maintain_history(maintain_history_id, gigya_uid, maintain_item_code, user_vehicle_id, **kwargs)
    if update_count != 1:
        raise NotExpectedError()

    return


@service
def get_maintain_history(gigya_uid: str, maintain_history_id: int, user_vehicle_id: int) -> dict:
    """
    メンテナンス記録登録、メンテナンス記録更新のレスポンス項目を取得
    """
    # メンテナンス履歴IDに紐づくメンテナンス履歴を取得
    result = maintain_history_repository.get_maintain_history_detail(gigya_uid, maintain_history_id, user_vehicle_id)

    if not result:
        raise NotExpectedError()

    # JSON整形
    maintain_image_ids = [x if x != "null" else None for x in result.get('maintain_image_ids').split(',')]
    maintain_implement_date = \
        convert_datetime_to_str(result.get("maintain_implement_date"), '%Y-%m-%d') if result.get("maintain_implement_date") else None
    du_last_timestamp = \
        result.get("maintain_du_last_timestamp").isoformat(timespec="milliseconds") + "Z" if result.get("maintain_du_last_timestamp") else None
    return {
        "maintain_history_id": result.get("maintain_history_id"),
        "maintain_item_code": result.get("maintain_item_code"),
        "maintain_implement_date": maintain_implement_date,
        "du_serial_number": result.get("maintain_du_serial_number"),
        "du_last_odometer": result.get("maintain_du_last_odometer"),
        "du_last_timestamp": du_last_timestamp,
        "maintain_location": result.get("maintain_location"),
        "maintain_cost": result.get("maintain_cost"),
        "maintain_required_time": result.get("maintain_required_time"),
        "maintain_memo": result.get("maintain_memo"),
        "maintain_image_ids": maintain_image_ids
    }


@service
def get_history_limit(
        gigya_uid: str,
        user_vehicle_id: int,
        limit: int,
        offset: int,
        maintain_item_code: str = None
) -> dict:

    # メンテナンス履歴TBLの全件数を取得
    all_count = maintain_history_repository.get_maintain_history_all_count(gigya_uid, user_vehicle_id, maintain_item_code)

    # メンテナンス履歴TBL取得
    get_result = maintain_history_repository.get_maintain_history_limit(gigya_uid, user_vehicle_id, limit, offset, maintain_item_code)

    for item in get_result:
        maintain_implement_date_str = convert_datetime_to_str(item.get("maintain_implement_date"), '%Y-%m-%d')
        item["maintain_implement_date"] = maintain_implement_date_str

    end_of_data = False

    if limit + offset >= all_count.get("count"):
        end_of_data = True

    result = {
        "end_of_data": end_of_data,
        "maintain_histories": get_result
    }

    return result


@service
def delete_maintain_history(gigya_uid: str, maintain_history_id: int, user_vehicle_id: int) -> None:
    maintain_history_repository.delete_t_maintain_history_maintain_history_id(gigya_uid, maintain_history_id, user_vehicle_id)

    return


def get_maintain_history_detail(gigya_uid: str, maintain_history_id: int, user_vehicle_id: int) -> dict:
    """
    メンテナンス履歴詳細取得
    """
    # メンテナンス履歴IDに紐づくメンテナンス履歴を取得
    result = maintain_history_repository.get_maintain_history_detail(gigya_uid, maintain_history_id, user_vehicle_id)

    if not result:
        raise NotExpectedError()

    # JSON整形
    # pylint: disable=unsupported-assignment-operation
    maintain_implement_date = \
        convert_datetime_to_str(result.get("maintain_implement_date"), '%Y-%m-%d') if result.get("maintain_implement_date") else None

    # メンテナンスイメージURL取得
    maintain_image_ids = [x if x != "null" else None for x in result.pop('maintain_image_ids').split(',')]
    maintain_image_urls = []
    for item in maintain_image_ids:
        if item:
            s3_bucket_key = get_s3_bucket_key('S3_BUCKET', code='UPLOAD')
            s3_url = get_s3_url(s3_bucket_key, gigya_uid + "/" + item, http_method='get_object')
            maintain_image_urls.append({
                "file_id": item,
                "s3_url": s3_url
            })
        else:
            maintain_image_urls.append({
                "file_id": None,
                "s3_url": None,
            })

    return {
        "maintain_history_id": result.get("maintain_history_id"),
        "maintain_item_code": result.get("maintain_item_code"),
        "maintain_item_name": result.get("maintain_item_name"),
        "maintain_implement_date": maintain_implement_date,
        "maintain_location": result.get("maintain_location"),
        "maintain_item_file_id": result.get("maintain_item_code"),
        "maintain_cost": result.get("maintain_cost"),
        "maintain_required_time": result.get("maintain_required_time"),
        "maintain_memo": result.get("maintain_memo"),
        "maintain_image_urls": maintain_image_urls
    }
