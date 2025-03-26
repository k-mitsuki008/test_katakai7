from common.error.s3_access_error import S3AccessError


class TestS3AccessError:
    def test_S3AccessError_デフォルト値(self):
        """
        正常系
        デフォルト値
        """
        e = S3AccessError()
        assert 'E001' == e.error_code
        assert 500 == e.status_code

    def test_S3AccessError_値の指定(self):
        """
        正常系
        値の指定
        """
        error_code = '1'
        status_code = 500
        e = S3AccessError(error_code, status_code)
        assert error_code == e.error_code
        assert status_code == e.status_code
