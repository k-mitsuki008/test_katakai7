from common.decorator.default_batch import default_batch
from service.delete_file_service import get_file


@default_batch()
def handler(event):
    """
    ファイル削除バッチ処理:管理中ファイルID一覧取得
    """
    file_list = get_file()

    return {
        "file_id_list": file_list
    }
