from common.error.custom_error import CustomError


# DB接続エラー
class DbAccessError(CustomError):

    def __init__(self, error_code: str = 'E002', status_code: int = 500):
        super().__init__(error_code, status_code, ())
