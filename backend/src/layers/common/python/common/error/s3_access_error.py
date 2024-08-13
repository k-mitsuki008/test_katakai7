from common.error.custom_error import CustomError


# S3接続エラー
class S3AccessError(CustomError):

    def __init__(self, error_code: str = 'E001', status_code: int = 500):
        super().__init__(error_code, status_code, ())
