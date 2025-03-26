from common.error.business_error import BusinessError


class TestBusinessError:
    def test_BusinessError_デフォルト値(self):
        """
        正常系
        デフォルト値
        """
        e = BusinessError()
        assert 'E001' == e.error_code
        assert 400 == e.status_code
        assert () == e.params

    def test_BusinessError_値の指定(self):
        """
        正常系
        値の指定
        """
        error_code = '1'
        status_code = 400
        params = ('テスト', 1)
        e = BusinessError(error_code, status_code, params)
        assert error_code == e.error_code
        assert status_code == e.status_code
        assert params == e.params
