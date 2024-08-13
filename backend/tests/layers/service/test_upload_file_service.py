import os
from importlib import import_module, reload
import pytest
import boto3
from botocore.exceptions import ClientError
from moto import mock_s3
from common.error.s3_access_error import S3AccessError
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.upload_file_service')
get_upload_urls = getattr(module, 'get_upload_urls')
secret_manager_region = os.environ['SECRET_MANAGER_REGION']

@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
@mock_s3
def test_get_upload_urls_ok_01(mocker):
    """
    正常系 アップロードファイルURL取得
    """
    # uuid.uuid4 のモック化
    mocker.patch("uuid.uuid4", side_effect=("XXXXX", "YYYYY", "ZZZZZ"))
    reload(module)

    # モックS3バケット生成
    s3 = boto3.resource("s3", region_name='eu-west-1')
    s3.create_bucket(Bucket='spvc-dev-upload-items', CreateBucketConfiguration={'LocationConstraint': 'eu-west-1'})

    # 期待している返却値
    expected_value1 = {
        "file_id": "XXXXX",
        "s3_url": "https://spvc-dev-upload-items.s3.amazonaws.com/test_uid_02/XXXXX?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=foobar_key%2F20220513%2F" + secret_manager_region + "%2Fs3%2Faws4_request&X-Amz-Date=20220513T123456Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature="
    }
    expected_value2 = {
        "file_id": "YYYYY",
        "s3_url": "https://spvc-dev-upload-items.s3.amazonaws.com/test_uid_02/YYYYY?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=foobar_key%2F20220513%2F" + secret_manager_region + "%2Fs3%2Faws4_request&X-Amz-Date=20220513T123456Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature="
    }
    expected_value3 = {
        "file_id": "ZZZZZ",
        "s3_url": "https://spvc-dev-upload-items.s3.amazonaws.com/test_uid_02/ZZZZZ?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=foobar_key%2F20220513%2F" + secret_manager_region + "%2Fs3%2Faws4_request&X-Amz-Date=20220513T123456Z&X-Amz-Expires=900&X-Amz-SignedHeaders=host&X-Amz-Signature="
    }
    upload_urls = get_upload_urls('test_uid_02', 3)

    assert any(item["s3_url"].startswith(expected_value1["s3_url"]) and item["file_id"] == expected_value1["file_id"] for item in upload_urls)
    assert any(item["s3_url"].startswith(expected_value2["s3_url"]) and item["file_id"] == expected_value2["file_id"] for item in upload_urls)
    assert any(item["s3_url"].startswith(expected_value3["s3_url"]) and item["file_id"] == expected_value3["file_id"] for item in upload_urls)


def test_get_upload_urls_ok_02(mocker):
    """
    準正常系 アップロードファイルURL0件
    """
    # 期待している返却値
    expected_value = []

    upload_urls = get_upload_urls('test_uid_02', 0)

    assert upload_urls == expected_value


def test_get_upload_urls_ng_01(mocker):
    """
    異常系 S3アクセスエラー
    """
    # boto3.client でエラー発生
    mocker.patch(
        "boto3.client",
        side_effect=ClientError({'Error': {'Code':'ClientError', 'Message': 'client error.'}}, 'demo')
    )
    reload(module)

    # 期待している返却値
    with pytest.raises(S3AccessError):
        get_upload_urls('test_uid_02', 1)
