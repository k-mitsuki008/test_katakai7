from common.error.dynamo_db_access_error import DynamoDbAccessError


class TestDynamoDbAccessError:
    def test_DynamoDbAccessError_デフォルト値(self):
        """
        正常系
        デフォルト値
        """
        e = DynamoDbAccessError()
        assert 'E003' == e.error_code
        assert 500 == e.status_code

    def test_DynamoDbAccessError_値の指定(self):
        """
        正常系
        値の指定
        """
        error_code = '1'
        status_code = 500
        e = DynamoDbAccessError(error_code, status_code)
        assert error_code == e.error_code
        assert status_code == e.status_code
