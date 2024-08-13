from common.error.custom_error import CustomError


# アプリバージョンエラー
class OldAppVersionError(CustomError):

    def __init__(self, error_code: str = 'E035', status_code: int = 403):
        super().__init__(error_code, status_code, ())
