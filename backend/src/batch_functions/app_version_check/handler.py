from common.decorator.default_batch import default_batch
from service.app_version_info_service import update_ios_app_version, update_android_app_version


@default_batch()
def handler(event):
    """
    アプリバージョン情報取得バッチ処理
    """
    update_ios_app_version()
    update_android_app_version()
