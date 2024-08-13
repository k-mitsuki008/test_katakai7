from common.error.custom_error import CustomError


# 認証エラー
class AuthorizedError(CustomError):

    def __init__(self, error_code: str = 'E001', status_code: int = 401):
        super().__init__(error_code, status_code, ())
