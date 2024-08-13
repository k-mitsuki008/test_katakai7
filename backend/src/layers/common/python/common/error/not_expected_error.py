from common.error.custom_error import CustomError


# 想定外エラー
class NotExpectedError(CustomError):

    def __init__(self, error_code: str = 'E001', status_code: int = 500):
        super().__init__(error_code, status_code, ())
