from common.error.db_access_error import DbAccessError


class TestDbAccessError:
    def test_DbAccessError_デフォルト値(self):
        """
        正常系
        デフォルト値
        """
        e = DbAccessError()
        assert 'E002' == e.error_code
        assert 500 == e.status_code

    def test_DbAccessError_値の指定(self):
        """
        正常系
        値の指定
        """
        error_code = '1'
        status_code = 500
        e = DbAccessError(error_code, status_code)
        assert error_code == e.error_code
        assert status_code == e.status_code
