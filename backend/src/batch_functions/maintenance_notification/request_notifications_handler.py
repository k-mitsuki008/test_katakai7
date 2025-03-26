from common.decorator.default_batch import default_batch
from service import maintenance_notification_service, maintain_item_service
from common.logger import Logger

log = Logger()


@default_batch()
def handler(event):
    log.info(f'input: {event}')

    result_list = []
    # vehicle_idごとにデータをグルーピングする
    notification_list_group = maintenance_notification_service.create_grouping_vehicle_id(event)

    # vehicle_idごとにpush通知をする
    for notification in notification_list_group:

        # maintain_item_codeをリスト化する
        item_code_list = maintenance_notification_service.create_maintain_item_code_list(notification)

        # vehicle_idとitem_codeに紐づくメンテナンス指示一覧を取得する
        maintain_item_list = maintain_item_service.get_maintain_items(notification["gigya_uid"],
                                                                      notification["user_vehicle_id"],
                                                                      item_code_list)

        # push通知をする
        notified_list = maintenance_notification_service.request_notification(notification, maintain_item_list)

        if not notified_list:
            continue

        result_list.append(notified_list)

    result = {
        'result': True,
        'index': result_list
    }

    log.info(f'result: {result}')

    return result
