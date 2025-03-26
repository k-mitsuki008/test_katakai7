from common.error.custom_error import CustomError


# 業務エラー
class BusinessError(CustomError):

    def __init__(self, error_code: str = 'E001', status_code: int = 400, params: tuple = ()):
        super().__init__(error_code, status_code, params)
