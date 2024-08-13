from common.error.not_expected_error import NotExpectedError


class TestNotExpectedError:
    def test_NotExpectedError_デフォルト値(self):
        """
        正常系
        デフォルト値
        """
        e = NotExpectedError()
        assert 'E001' == e.error_code
        assert 500 == e.status_code

    def test_NotExpectedError_値の指定(self):
        """
        正常系
        値の指定
        """
        error_code = '1'
        status_code = 500
        e = NotExpectedError(error_code, status_code)
        assert error_code == e.error_code
        assert status_code == e.status_code
