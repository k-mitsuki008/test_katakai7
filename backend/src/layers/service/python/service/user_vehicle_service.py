from common.logger import Logger
from common.error.not_expected_error import NotExpectedError
from common.decorator.service import service
from common.error.business_error import BusinessError
from common.utils.aws_utils import get_constant
from repository import (
    user_vehicle_repository as repository,
    drive_unit_history_repository,
    maintain_history_repository,
    ride_history_repository,
    user_setting_maintain_repository,
    user_shop_purchase_repository
)
log = Logger()


# ユーザ車両設定登録
@service
def insert_vehicle(**kwargs) -> int:
    gigya_uid = kwargs['gigya_uid']

    # 既に車両が5件以上登録済の場合は業務エラー
    max_count = get_constant('MAX_VEHICLE_COUNT', 'MAX_VEHICLE_COUNT')
    counts = repository.count_t_user_vehicle(gigya_uid)
    if counts >= max_count:
        raise BusinessError(error_code='E038', params=(max_count,))

    # ユーザ車両TBL１件追加
    inserted_user_vehicle_id = repository.insert_t_user_vehicle(**kwargs, unit_no=kwargs['vehicle_id'])

    _update_unmanaged_vehicle(gigya_uid, inserted_user_vehicle_id, kwargs)

    # INSERTしたユーザ車両IDを返却
    return inserted_user_vehicle_id


# ユーザ車両設定更新
@service
def update_vehicle(**kwargs) -> int:
    gigya_uid = kwargs['gigya_uid']
    user_vehicle_id = kwargs['user_vehicle_id']

    # ユーザ車両TBLを更新
    if kwargs.get('vehicle_id'):
        kwargs['unit_no'] = kwargs['vehicle_id']
    update_result = repository.update_t_user_vehicle(**kwargs)
    if update_result != 1:
        raise NotExpectedError()

    _update_unmanaged_vehicle(gigya_uid, user_vehicle_id, kwargs)

    return update_result


def _update_unmanaged_vehicle(gigya_uid: str, user_vehicle_id: int, kwargs: dict):
    # managed_flag、registered_flagがTrueに更新された場合、他の車両をFalseに更新
    ather_vehicle_flags = {}
    if kwargs.get('managed_flag'):
        ather_vehicle_flags['managed_flag'] = False
    if kwargs.get('registered_flag'):
        ather_vehicle_flags['registered_flag'] = False
    if ather_vehicle_flags:
        repository.update_t_user_vehicle_unmanaged(gigya_uid, user_vehicle_id, **ather_vehicle_flags)


# ユーザ車両設定削除
def delete_vehicle(gigya_uid: str, user_vehicle_id: int) -> int:
    # 登録車両件数の確認
    all_count = repository.count_t_user_vehicle(gigya_uid)
    managed_flag = repository.get_user_vehicle_id(gigya_uid, user_vehicle_id).get("managed_flag")

    if all_count >= 2 and managed_flag:
        raise BusinessError(error_code='E045')

    # ユーザ購入店舗テーブル削除処理
    _ = user_shop_purchase_repository.delete_t_user_shop_purchase(gigya_uid, user_vehicle_id)

    # ユーザメンテナンス設定テーブル削除処理
    user_setting_maintain_repository.delete_t_user_setting_maintain(gigya_uid, user_vehicle_id)

    # ドライブユニット履歴テーブル削除処理
    _ = drive_unit_history_repository.delete_t_drive_unit_history(gigya_uid, user_vehicle_id)

    # メンテナンス履歴テーブル削除処理
    _ = maintain_history_repository.delete_t_maintain_history(gigya_uid, user_vehicle_id)

    # ライド履歴テーブル削除処理
    _ = ride_history_repository.delete_t_ride_history_user_vehicle_id(gigya_uid, user_vehicle_id)

    # ユーザ車両テーブル削除処理
    repository.delete_t_user_vehicle(gigya_uid, user_vehicle_id)

    # 削除後の登録車両件数の確認
    result_count = repository.count_t_user_vehicle(gigya_uid)

    return result_count


# ユーザ車両設定一覧取得
@service
def get_vehicles(gigya_uid, user_vehicle_id=None) -> list:
    # ユーザに紐づくユーザ車両情報を全件取得
    user_vehicles = repository.get_user_vehicles(gigya_uid, user_vehicle_id)

    # JSON整形処理
    vehicles = []
    bef_user_vehicle_id = None
    for rec in user_vehicles:
        user_vehicle_id = rec['user_vehicle_id']
        # ユーザ車両レコードを追加
        if bef_user_vehicle_id != user_vehicle_id:
            vehicle: dict = {
                "user_vehicle_id": rec['user_vehicle_id'],
                "model_code": rec['model_code'],
                "vehicle_id": rec['vehicle_id'],
                "vehicle_name": rec['vehicle_name'],
                "managed_flag": rec['managed_flag'],
                "registered_flag": rec['registered_flag'],
                "peripheral_identifier": rec['peripheral_identifier'],
                "complete_local_name": rec['complete_local_name'],
                "equipment_weight": rec['equipment_weight'],
                "vehicle_nickname": rec['vehicle_nickname']
            }
            if rec.get('shop_name'):
                vehicle["purchase_shop"] = {
                    "shop_name": rec['shop_name'],
                    "shop_tel": rec['shop_tel'],
                    "shop_location": rec['shop_location'],
                }
            else:
                vehicle["purchase_shop"] = None
            if rec.get('du_serial_number'):
                vehicle["bluetooth"] = {
                    "du_serial_number": rec['du_serial_number'],
                    "du_odometer": rec['du_last_odometer']
                }
            else:
                vehicle["bluetooth"] = None
            if rec.get('contact_title'):
                vehicle["contact"] = {
                    "contact_title": rec['contact_title'],
                    "contact_text": rec['contact_text'],
                    "contact_mail_address": rec['contact_mail_address']
                }
            else:
                vehicle["contact"] = None
                # 問合せ先マスタ無しの場合はエラーログを出力
                log.error(f'm_contact does not exist. model_code: {rec["model_code"]}')
            if rec.get('maintain_consciousness'):
                vehicle["maintain_setting"] = {
                    "maintain_consciousness": rec['maintain_consciousness'],
                    "maintain_alerts": [
                        {
                            "maintain_item_code": rec['maintain_item_code'],
                            "maintain_item_name": rec['maintain_item_name'],
                            "maintain_item_alert": rec['maintain_item_alert'],
                        }
                    ]
                }
            else:
                vehicle["maintain_setting"] = None
                raise BusinessError(error_code='E042', params=('ユーザメンテナンス設定情報',))

            vehicles.append(vehicle)
            bef_user_vehicle_id = user_vehicle_id
        else:
            vehicle["maintain_setting"]["maintain_alerts"].append({
                        "maintain_item_code": rec['maintain_item_code'],
                        "maintain_item_name": rec['maintain_item_name'],
                        "maintain_item_alert": rec['maintain_item_alert'],
                    })
    return vehicles


@service
def user_vehicle_id_is_exist(gigya_uid, user_vehicle_id) -> bool:

    result = repository.get_user_vehicle_id(gigya_uid, user_vehicle_id)
    if not result:
        raise BusinessError(error_code='E042', params=('ユーザ車両ID',))

    return bool(result)


@service
def get_user_vehicle(gigya_uid, user_vehicle_id, is_check=True) -> dict:

    result = repository.get_user_vehicle_id(gigya_uid, user_vehicle_id)
    if is_check and not result:
        raise BusinessError(error_code='E042', params=('ユーザ車両ID',))

    return result


@service
def count_vehicle_id(gigya_uid: str) -> int:

    result = repository.count_t_user_vehicle(gigya_uid)

    return result


@service
def vehicle_id_check(gigya_uid: str, vehicle_id: str) -> None:

    result = repository.get_user_vehicle_check(gigya_uid, vehicle_id)

    if result:
        raise BusinessError(error_code='E040')

    return
