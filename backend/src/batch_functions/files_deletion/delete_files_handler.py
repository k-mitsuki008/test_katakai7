from common.decorator.default_batch import default_batch
from service.delete_file_service import delete_file


@default_batch()
def handler(event):
    """
    ファイル削除バッチ処理:ファイル削除
    """
    delete_file(**event)

    result = {
        'result': True
    }

    return result
