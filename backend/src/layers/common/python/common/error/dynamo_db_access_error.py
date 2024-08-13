from common.error.custom_error import CustomError


# dynamoDb接続エラー
class DynamoDbAccessError(CustomError):

    def __init__(self, error_code: str = 'E003', status_code: int = 500):
        super().__init__(error_code, status_code, ())
