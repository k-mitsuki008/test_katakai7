from common.error.old_app_version_error import OldAppVersionError


class TestOldAppVersionError:
    def test_OldAppVersionError_デフォルト値(self):
        """
        正常系
        デフォルト値
        """
        e = OldAppVersionError()
        assert 'E035' == e.error_code
        assert 403 == e.status_code

    def test_OldAppVersionError_値の指定(self):
        """
        正常系
        値の指定
        """
        error_code = '1'
        status_code = 403
        e = OldAppVersionError(error_code, status_code)
        assert error_code == e.error_code
        assert status_code == e.status_code
