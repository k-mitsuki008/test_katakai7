from common.error.custom_error import CustomError


class TestCustomError:
    def test_CustomError_デフォルト値(self):
        """
        正常系
        デフォルト値
        """
        e = CustomError()
        assert None == e.error_code
        assert None == e.status_code
        assert () == e.params

    def test_CustomError_値の指定(self):
        """
        正常系
        値の指定
        """
        error_code = '1'
        status_code = 500
        params = ('テスト', 1)
        e = CustomError(error_code, status_code, params)
        assert error_code == e.error_code
        assert status_code == e.status_code
        assert params == e.params
