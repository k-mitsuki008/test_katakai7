import json

import firebase_admin
from firebase_admin import messaging
from firebase_admin.exceptions import FirebaseError

from common.decorator.service import service
from common.logger import Logger
from common.stack_trace import get_stack_trace
from common.utils.aws_utils import get_constant, get_secret, get_message
from repository import user_setting_maintain_item_repository

log = Logger()


@service
def get_maintain_items() -> dict:
    """
    メンテナンス指示一覧取得
    """

    notification_list = dict(
        maintenance_notification_list=user_setting_maintain_item_repository.get_t_user_setting_maintain_item())

    notification_list["maintenance_notification_list"] = _get_create_list(
        notification_list["maintenance_notification_list"],
        int(get_constant('INIT_VALUE', 'NOTIFICATION_LIMIT')))

    return notification_list


# 1stepで通知が最大500件なので500件ごとに配列を切り分ける
def _get_create_list(maintain_items, notification_limit):
    return [maintain_items[i:i + notification_limit] for i in range(0, len(maintain_items), notification_limit)]


@service
def request_notification(notification: dict, maintain_item_list: list) -> list:
    """
    メンテナンス通知
    """

    # push通知認証設定
    _get_authentication_preference()

    # 通知対象のリストを生成する
    notification_target_list = _create_notification_target_list(notification, maintain_item_list)

    # 通知対象がない場合次の車両にいく
    if len(notification_target_list["item"]) == 0:
        return []

    # メンテナンス対象のpush通知を実行する
    return _push_notification_execution(notification_target_list)


# vehicle_idごとにデータをグルーピングする
def create_grouping_vehicle_id(notification_list):
    """

    Parameters
    ----------
    [
        {
            "device_token": "車両トークン",
            "gigya_uid": "gigya_uid",
            "user_vehicle_id": "1",
            "maintain_item_code": "部品コード1",
            "vehicle_name": "バイク名",
        },
        {
            "device_token": "車両トークン",
            "gigya_uid": "gigya_uid",
            "user_vehicle_id": "1",
            "maintain_item_code": "部品コード2",
            "vehicle_name": "バイク名",
        },
        {
            "device_token": "車両トークン",
            "gigya_uid": "gigya_uid",
            "user_vehicle_id": "2",
            "maintain_item_code": "部品コード3",
            "vehicle_name": "バイク名",
        }
    ]

    Returns 車両IDが一致するデータをマッピングする
    -------
    [
        {
            'device_token': '車両トークン',
            'gigya_uid': 'gigya_uid',
            'user_vehicle_id': '1',
            'vehicle_name': 'バイク名',
            'item': [
                {
                    'maintain_item_code': '部品コード1'
                },
                {
                    'maintain_item_code': '部品コード2'
                }
            ]
        },
        {
            'device_token': '車両トークン',
            'gigya_uid': 'gigya_uid',
            'user_vehicle_id': '2',
            'vehicle_name': 'バイク名',
            'item': [
                {
                    'maintain_item_code': '部品コード3'
                }
            ]
        },
    ]
    """
    # 辞書に変換するための初期化
    dict_users = {}
    # グルーピングする
    for item in notification_list:
        token = item['device_token']
        gigya_uid = item['gigya_uid']
        user_vehicle_id = item['user_vehicle_id']
        maintain_item_code = item['maintain_item_code']
        vehicle_name = item['vehicle_name']
        if user_vehicle_id not in dict_users:
            dict_users[user_vehicle_id] = {'device_token': token, 'gigya_uid': gigya_uid,
                                           'user_vehicle_id': user_vehicle_id,
                                           'vehicle_name': vehicle_name,
                                           'item': []}
        dict_users[user_vehicle_id]['item'].append(
            {'maintain_item_code': maintain_item_code})

    result = []
    for user_dict in dict_users.values():
        result.append(user_dict)

    return result


# 通知対象の判定と通知リストを生成する
def _create_notification_target_list(notification, maintain_item_list):
    maintain_notification_target = get_constant('INIT_VALUE', code='MAINTENANCE_NOTIFICATION_TARGET')

    target_item_list = []

    for item in maintain_item_list:
        if item["maintain_interval"] - item["maintain_archive"] <= maintain_notification_target:
            target_item_list.append(
                {"maintain_item_code": item["maintain_item_code"], "maintain_item_name": item["maintain_item_name"]})

    notification["item"] = target_item_list
    log.info(f'通知対象リスト: {notification}')

    return notification


# push通知を実行する
def _push_notification_execution(notification_target_list):
    messages_list = []
    push_success_result = []
    code = "N001"
    for push_list in notification_target_list["item"]:
        message = get_message(code)
        message_text = messaging.Message(
            notification=messaging.Notification(
                body=message.format(notification_target_list["vehicle_name"], push_list["maintain_item_name"])
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound='default'
                    )
                )
            ),
            token=notification_target_list["device_token"],
            data={
                "user_vehicle_id": str(notification_target_list["user_vehicle_id"]),
                "maintain_item_code": push_list["maintain_item_code"]
            }
        )
        messages_list.append(message_text)

    try:
        send_responses = messaging.send_all(messages_list)

        for idx, status in enumerate(send_responses.responses):
            # 通知成功(1)にアップデートする
            if status.success:
                _update_maintain_item_alert_status(notification_target_list,
                                                   notification_target_list["item"][idx],
                                                   get_constant('MAINTENANCE_ALERT_STATUS', code='NOTIFIED'))
                push_success_result.append(notification_target_list["item"][idx])
                log.info(f'通知成功: {notification_target_list}')
            # 通知失敗(2)にアップデートする
            else:
                _update_maintain_item_alert_status(notification_target_list,
                                                   notification_target_list["item"][idx],
                                                   get_constant('MAINTENANCE_ALERT_STATUS', code='FAILED'))
                log.info(f'通知失敗: {notification_target_list}')

        # 通知に成功した車両アイテムのみ返す
        notification_target_list["item"] = push_success_result
        return notification_target_list

    except (FirebaseError, ValueError):
        log.error(get_stack_trace())
        log.error(messages_list)

        # 通知失敗(2)にアップデートする
        for item_code in notification_target_list["item"]:
            _update_maintain_item_alert_status(notification_target_list,
                                               item_code,
                                               get_constant('MAINTENANCE_ALERT_STATUS', code='FAILED'))

        notification_target_list["item"] = push_success_result
        log.info(f'通知エラー: {notification_target_list}')
        return notification_target_list


def _update_maintain_item_alert_status(notification_target_list, item_code, maintain_item_alert_status):
    # アラート通知ステータスをアップデートする
    user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item(
        notification_target_list["user_vehicle_id"], item_code["maintain_item_code"],
        notification_target_list["gigya_uid"],
        maintain_item_alert_status=maintain_item_alert_status)


# maintain_item_codeをリスト化する
@service
def create_maintain_item_code_list(notification: dict) -> str:
    item_code_list = []
    for item in notification["item"]:
        item_code_list.append(item["maintain_item_code"])
    item_code = ",".join(['\'' + item + '\'' for item in item_code_list])

    return item_code


def _get_authentication_preference():
    # デフォルト認証情報（ADC）を設定。
    secrets = get_secret()
    api_key = secrets.get('GOOGLE_APPLICATION_CREDENTIALS')
    service_account_info = json.loads(api_key)

    # pylint: disable-next=protected-access
    if not firebase_admin._apps:
        # build credentials with the service account dict
        creds = firebase_admin.credentials.Certificate(service_account_info)

        # SDKを初期化
        _ = firebase_admin.initialize_app(creds)
