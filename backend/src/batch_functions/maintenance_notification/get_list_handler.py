from common.decorator.default_batch import default_batch
from service import maintenance_notification_service


@default_batch()
def handler(event):
    """
    メンテナンスアラート通知
    """

    user_notification_list = maintenance_notification_service.get_maintain_items()

    return user_notification_list
