import tests.test_utils.fixtures as fixtures
from importlib import import_module, reload
import pytest
from common.error.business_error import BusinessError
from botocore.exceptions import ClientError
from common.error.s3_access_error import S3AccessError


db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.bluetooth_unexpected_data_service')
upload_file = getattr(module, 'upload_file')


def test_upload_file_ok(mocker):
    """
    正常系
    """
    # common.utils.aws_utils create_s3_objects のモック化
    mocker.patch(
        "common.utils.aws_utils.create_s3_objects",
        side_effect=lambda *args, **kwargs: args)
    reload(module)

    file: dict = {
        "timestamp": "2020-11-27T12:34:56.789Z",
        "GIGYA-UUID": "0123456789abcdef01234567890abcde",
        "Serial-number": "X123-1234567",
        "Frame-number": "1234567890",
        "RIDE-DATA-1": [
            {"timestamp": "2020-01-07T14:05:08.707+0800",
             "Contents": "1000000000000000000000000000000000000000000000000000FF"},
            {"timestamp": "2020-01-07T14:05:09.707+0800",
             "Contents": "1000000000000000000000000000000000000000000000000000FF"}
        ],
        "RIDE-DATA-2": [
            {"timestamp": "2020-01-07T14:05:08.707+0800",
             "Contents": "1100000000000000000000000000000000000000000000000000FF"},
            {"timestamp": "2020-01-07T14:05:09.707+0800",
             "Contents": "1100000000000000000000000000000000000000000000000000FF"}
        ],
        "DU-SYNCHRONIZATION-DATA-1": [
            {"timestamp": "2020-01-07T14:05:08.707+0800",
             "Contents": "2000000000000000000000000000000000000000000000000000FF"},
            {"timestamp": "2020-01-07T14:05:09.707+0800",
             "Contents": "2000000000000000000000000000000000000000000000000000FF"}
        ],
        "DU-SYNCHRONIZATION-DATA-2": [
            {"timestamp": "2020-01-07T14:05:08.707+0800",
             "Contents": "2100000000000000000000000000000000000000000000000000FF"},
            {"timestamp": "2020-01-07T14:05:09.707+0800",
             "Contents": "2100000000000000000000000000000000000000000000000000FF"}
        ],
        "DU-SYNCHRONIZATION-DATA-3": [
            {"timestamp": "2020-01-07T14:05:08.707+0800",
             "Contents": "2200000000000000000000000000000000000000000000000000FF"},
            {"timestamp": "2020-01-07T14:05:09.707+0800",
             "Contents": "2200000000000000000000000000000000000000000000000000FF"}
        ]
    }

    ccu_id = "0019XXXXXXXXXX"
    gigya_uid = "test_uid_01"

    result_data = upload_file(gigya_uid, ccu_id, **file)
    assert result_data is None


def test_upload_file_ng_01(mocker):
    """
    異常系:boto3エラー
    """
    # boto3.client のモック化
    mocker.patch(
        "boto3.client",
        side_effect=ClientError({'Error': {'Code': 'clientError', 'Message': 'client error.'}}, 'demo')
    )
    reload(module)

    file: dict = {
        "timestamp": "2020-11-27T12:34:56.789Z",
        "GIGYA-UUID": "0123456789abcdef01234567890abcde",
        "Serial-number": "X123-1234567",
        "Frame-number": "1234567890",
        "RIDE-DATA-1": [
            {"timestamp": "2020-01-07T14:05:08.707+0800",
             "Contents": "1000000000000000000000000000000000000000000000000000FF"},
            {"timestamp": "2020-01-07T14:05:09.707+0800",
             "Contents": "1000000000000000000000000000000000000000000000000000FF"}
        ]
    }

    ccu_id = "0019XXXXXXXXXX"
    gigya_uid = "test_uid_01"

    with pytest.raises(S3AccessError):
        upload_file(gigya_uid, ccu_id, **file)


def test_upload_file_ng_02(mocker):
    """
    異常系:timestamp項目が存在しない場合
    """
    # common.utils.aws_utils create_s3_objects のモック化
    mocker.patch(
        "common.utils.aws_utils.create_s3_objects",
        side_effect=lambda *args, **kwargs: args)
    reload(module)

    file: dict = {
        "GIGYA-UUID": "0123456789abcdef01234567890abcde",
        "Serial-number": "X123-1234567",
        "Frame-number": "1234567890",
        "RIDE-DATA-1": [
            {"timestamp": "2020-01-07T14:05:08.707+0800",
             "Contents": "1000000000000000000000000000000000000000000000000000FF"},
            {"timestamp": "2020-01-07T14:05:09.707+0800",
             "Contents": "1000000000000000000000000000000000000000000000000000FF"}
        ]
    }

    ccu_id = "0019XXXXXXXXXX"
    gigya_uid = "test_uid_01"

    with pytest.raises(BusinessError):
        upload_file(gigya_uid, ccu_id, **file)


def test_upload_file_ng_03(mocker):
    """
    異常系:timestamp項目が日付型以外の場合
    """
    # common.utils.aws_utils create_s3_objects のモック化
    mocker.patch(
        "common.utils.aws_utils.create_s3_objects",
        side_effect=lambda *args, **kwargs: args)
    reload(module)

    file: dict = {
        "timestamp": "123456789",
        "GIGYA-UUID": "0123456789abcdef01234567890abcde",
        "Serial-number": "X123-1234567",
        "Frame-number": "1234567890",
        "RIDE-DATA-1": [
            {"timestamp": "2020-01-07T14:05:08.707+0800",
             "Contents": "1000000000000000000000000000000000000000000000000000FF"},
            {"timestamp": "2020-01-07T14:05:09.707+0800",
             "Contents": "1000000000000000000000000000000000000000000000000000FF"}
        ]
    }

    ccu_id = "0019XXXXXXXXXX"
    gigya_uid = "test_uid_01"

    with pytest.raises(BusinessError):
        upload_file(gigya_uid, ccu_id, **file)
