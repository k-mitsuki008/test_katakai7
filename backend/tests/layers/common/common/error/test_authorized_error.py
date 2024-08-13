from common.error.authorized_error import AuthorizedError


class TestAuthorizedError:
    def test_AuthorizedError_デフォルト値(self):
        """
        正常系
        デフォルト値
        """
        e = AuthorizedError()
        assert 'E001' == e.error_code
        assert 401 == e.status_code

    def test_AuthorizedError_値の指定(self):
        """
        正常系
        値の指定
        """
        error_code = '1'
        status_code = 401
        e = AuthorizedError(error_code, status_code)
        assert error_code == e.error_code
        assert status_code == e.status_code
