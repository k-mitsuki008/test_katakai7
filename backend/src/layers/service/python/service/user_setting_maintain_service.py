from common.logger import Logger
from common.decorator.service import service
from common.utils.aws_utils import get_constant
from repository import user_setting_maintain_repository
from repository import user_setting_maintain_item_repository
from common.error.not_expected_error import NotExpectedError
log = Logger()


@service
def initialize_maintenance_setting(user_vehicle_id: int, gigya_uid: str) -> dict:
    # メンテナンス項目一覧取得
    maintain_items = user_setting_maintain_repository.get_user_setting_maintains(user_vehicle_id)
    # ユーザメンテナンス設定の初期化
    maintain_consciousness = user_setting_maintain_repository.upsert_t_user_setting_maintain(
        user_vehicle_id,
        gigya_uid,
        maintain_consciousness=get_constant('INIT_VALUE', 'MAINTENANCE_CONSCIOUSNESS')
    )

    # ユーザメンテナンス項目設定の初期化
    maintain_alerts = []
    for item in maintain_items:
        maintain_item_code = item['maintain_item_code']
        maintain_item_alert = user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item(
            user_vehicle_id,
            maintain_item_code,
            gigya_uid,
            maintain_item_alert=get_constant('INIT_VALUE', 'MAINTAIN_ITEM_ALERT'),
            maintain_item_alert_status=get_constant('INIT_VALUE', 'MAINTAIN_ITEM_ALERT_STATUS'),
        )

        maintain_alerts.append(
            {
                "maintain_item_code": maintain_item_code,
                "maintain_item_name": item['maintain_item_name'],
                "maintain_item_alert": maintain_item_alert
            }
        )

    return {
        "maintain_consciousness": maintain_consciousness,
        "maintain_alerts": maintain_alerts,
    }


@service
def upsert_setting_maintain(gigya_uid: str, user_vehicle_id: int, **kwargs) -> dict:

    # ユーザメンテナンス設定TBL更新
    if kwargs.get('maintain_consciousness'):
        _ = user_setting_maintain_repository.upsert_t_user_setting_maintain(
            user_vehicle_id,
            gigya_uid,
            maintain_consciousness=kwargs.get('maintain_consciousness')
        )

    maintain_alerts = kwargs.get('maintain_alerts')

    # ユーザメンテナンス項目設定TBL更新
    if maintain_alerts and len(maintain_alerts) > 0:
        for item in maintain_alerts:
            kwargs = {
                "maintain_item_alert": item["maintain_item_alert"]
            }
            _ = user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item(
                user_vehicle_id,
                item["maintain_item_code"],
                gigya_uid,
                **kwargs,
            )

    update_result = user_setting_maintain_repository.get_user_maintain_setting_user_vehicle_id(user_vehicle_id)

    if not update_result:
        raise NotExpectedError()

    # JSON整形処理
    user_vehicle_id = update_result[0].get("user_vehicle_id")
    maintain_consciousness = update_result[0].get("maintain_consciousness")

    maintain_alerts = []
    for rec in update_result:
        maintain_alerts.append(
            {
                "maintain_item_code": rec['maintain_item_code'],
                "maintain_item_name": rec['maintain_item_name'],
                "maintain_item_alert": rec['maintain_item_alert']
            }
        )
    return {
        "user_vehicle_id": user_vehicle_id,
        "maintain_consciousness": maintain_consciousness,
        "maintain_alerts": maintain_alerts,
    }
