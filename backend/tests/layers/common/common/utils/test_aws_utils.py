import os
from importlib import import_module, reload
from unittest.mock import patch

import boto3
import pytest
import tests.test_utils.fixtures as fixtures
from botocore.exceptions import ClientError
from common.error.dynamo_db_access_error import DynamoDbAccessError
from common.error.s3_access_error import S3AccessError
from moto import mock_s3, mock_secretsmanager

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('common.utils.aws_utils')
get_secret = getattr(module, 'get_secret')
get_s3_url = getattr(module, 'get_s3_url')
get_dynamodb = getattr(module, 'get_dynamodb')
get_query = getattr(module, 'get_query')
get_dynamodb_by_secondary_index = getattr(module, 'get_dynamodb_by_secondary_index')
upsert_dynamodb = getattr(module, 'upsert_dynamodb')
put_dynamodb = getattr(module, 'put_dynamodb')
get_message = getattr(module, 'get_message')
get_constant = getattr(module, 'get_constant')
get_s3_objects = getattr(module, 'get_s3_objects')
delete_s3_objects = getattr(module, 'delete_s3_objects')
get_s3_client = getattr(module, 'get_s3_client')
create_s3_objects = getattr(module, 'create_s3_objects')
get_s3_bucket_key = getattr(module, 'get_s3_bucket_key')

# mockするS3バケットとS3キー名
MOCK_BUCKET_NAME = 'pytest_bucket'
MOCK_KEY_NAME = 'pytest_key'


class TestSecretsManager:
    @pytest.fixture(autouse=True)
    @mock_secretsmanager
    def setup_sercretsmanager(self):
        """
        pytset用
        secretsmanagerを設定
        """
        client = boto3.client('secretsmanager', os.environ["SECRET_MANAGER_REGION"])
        client.create_secret(
            Name='secret-name', SecretString='{"key": "value"}'
        )
        client2 = boto3.client('secretsmanager', os.environ["AURORA_SECRET_MANAGER_REGION"])
        client2.create_secret(
            Name='aurora-secret', SecretString='{"key1": "value1"}'
        )
        # client2.create_secret(
        #     Name='gigya-secret', SecretString='{"key2": "value2"}'
        # )
        # client2.create_secret(
        #     Name='google-secret', SecretString='{"key3": "value3"}'
        # )

    def test_get_secret_ok_01(self):
        """
        正常系
        SECRET_MANAGER_NAMEあり
        """
        env = {'SECRET_MANAGER_NAME': 'secret-name'}
        with patch.dict('os.environ', env):
            result = get_secret()
            assert result == {'key': 'value'}

    def test_get_secret_ok_02(self):
        """
        正常系
        SECRET_MANAGER_NAMEなし
        """
        env = {
            'SECRET_MANAGER_NAME': '',
            'AURORA_SECRET_MANAGER_NAME': 'aurora-secret',
            # 'GIGYA_SECRET_MANAGER_NAME': 'gigya-secret',
            # 'GOOGLE_SECRET_MANAGER_NAME': 'google-secret',
        }
        with patch.dict('os.environ', env):
            result = get_secret()
            assert result == {'key1': 'value1'}


class TestS3:
    @pytest.fixture(autouse=True)
    def init_s3(self):
        """
        pytset用
        S3バケットを作成とデータのアップロード
        """
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        s3_bucket = 'pytest_bucket'
        s3_key = 'pytest_key'

        with mock_s3():
            session = boto3.Session()
            s3_client = session.client('s3')
            s3_client.create_bucket(Bucket=s3_bucket)
            data = b'abc'
            s3_client.put_object(
                Bucket=s3_bucket, Key=s3_key, Body=data)
            yield

    @pytest.mark.freeze_time('2022-05-13 12:34:56.789101')
    def test_get_s3_url_ok(self):
        """
        正常系
        """
        expires = 900
        http_method = 'put_object'
        result = get_s3_url(MOCK_BUCKET_NAME, MOCK_KEY_NAME, expires, http_method)
        s3_url = 'https://s3.' + os.environ['SECRET_MANAGER_REGION'] + '.amazonaws.com/pytest_bucket/pytest_key?X-Amz-Algorithm='
        assert result.startswith(s3_url) is True

    def test_get_s3_url_ng(self, mocker):
        """
        異常系
        """
        mocker.patch(
            'boto3.client',
            side_effect=ClientError({'Error': {'Code': 'ClientError', 'Message': 'client error.'}}, 'demo')
        )
        reload(module)
        expires = 900
        http_method = 'put_object'
        with pytest.raises(S3AccessError):
            get_s3_url(MOCK_BUCKET_NAME, MOCK_KEY_NAME, expires, http_method)

    def test_get_s3_objects_ok(self):
        """
        正常系
        """
        result = get_s3_objects(MOCK_BUCKET_NAME, MOCK_KEY_NAME)
        assert result['Contents'][0]['Key'] == MOCK_KEY_NAME

    def test_get_s3_objects_ng(self, mocker):
        """
        異常系
        """
        mocker.patch(
            'boto3.client',
            side_effect=ClientError({'Error': {'Code': 'ClientError', 'Message': 'client error.'}}, 'demo')
        )
        reload(module)
        with pytest.raises(S3AccessError):
            get_s3_objects(MOCK_BUCKET_NAME, MOCK_KEY_NAME)

    def test_delete_s3_objects_ok(self):
        """
        正常系
        """
        result = delete_s3_objects(MOCK_BUCKET_NAME, MOCK_KEY_NAME)
        assert result is None

    def test_delete_s3_objects_ng(self, mocker):
        """
        異常系
        """
        mocker.patch(
            'boto3.client',
            side_effect=ClientError({'Error': {'Code': 'ClientError', 'Message': 'client error.'}}, 'demo')
        )
        reload(module)
        with pytest.raises(S3AccessError):
            delete_s3_objects(MOCK_BUCKET_NAME, MOCK_KEY_NAME)

    def test_get_s3_client_ok(self, mocker):
        """
        正常系 boto3の取得
        """
        expected_value = {'test'}
        mocker.patch(
            'boto3.client',
            return_value={'test'}
        )
        reload(module)
        data = get_s3_client()
        assert data == expected_value

    def test_create_s3_objects_ok(self):
        """
        正常系
        """
        json_data = {'pytest': 'pytest'}
        result = create_s3_objects(MOCK_BUCKET_NAME, MOCK_KEY_NAME, json_data)
        assert result is None

    def test_create_s3_objects_ng(self, mocker):
        """
        異常系
        """
        mocker.patch(
            'boto3.client',
            side_effect=ClientError({'Error': {'Code': 'ClientError', 'Message': 'client error.'}}, 'demo')
        )
        reload(module)
        json_data = {'pytest': 'pytest'}
        with pytest.raises(S3AccessError):
            create_s3_objects(MOCK_BUCKET_NAME, MOCK_KEY_NAME, json_data)


class TestDynamoDb:

    def test_get_dynamodb_ok_01(self):
        """
        正常系
        """
        table_name = 'm_constant'
        keys = {
            'category_cd': 'FILE_TYPE',
            'code': 'UNEXPECTED'
        }
        result = get_dynamodb(table_name, keys)
        assert result == {'category_cd': 'FILE_TYPE', 'code': 'UNEXPECTED', 'value': 'ERRD'}

    def test_get_dynamodb_error_01(self):
        """
        異常系
        """
        table_name = 'ng_table_name'
        keys = {
            'category_cd': 'FILE_TYPE',
            'code': 'UNEXPECTED'
        }
        with pytest.raises(DynamoDbAccessError):
            get_dynamodb(table_name, keys)

    def test_get_query_ok_01(self):
        """
        正常系
        """
        table_name = 'm_constant'
        key = 'category_cd'
        value = 'FILE_TYPE'
        result = get_query(table_name, key, value)
        assert result == [{'category_cd': 'FILE_TYPE', 'code': 'UNEXPECTED', 'value': 'ERRD'}]

    def test_get_query_error_01(self):
        """
        異常系
        """
        table_name = 'ng_table_name'
        key = 'category_cd'
        value = 'FILE_TYPE'
        with pytest.raises(DynamoDbAccessError):
            get_query(table_name, key, value)

    def test_get_dynamodb_by_secondary_index_ok_01(self):
        """
        正常系
        """
        table_name = 't_session'
        index = 'session_id-index'
        key = 'session_id'
        value = 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        result = get_dynamodb_by_secondary_index(table_name, index, key, value)
        assert result == [{
            'gigya_uid': 'test_uid_01',
            'create_session_timestamp': '2022-05-13 12:34:56.789',
            'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'expire_session_timestamp': '2022-05-27 12:34:56.789',
            'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }]

    def test_get_dynamodb_by_secondary_index_error_01(self):
        """
        異常系
        """
        table_name = 'ng_table_name'
        index = 'session_id-index'
        key = 'session_id'
        value = 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        with pytest.raises(DynamoDbAccessError):
            get_dynamodb_by_secondary_index(table_name, index, key, value)

    def test_upsert_dynamodb_ok_01(self):
        """
        正常系
        """
        table_name = 't_session'
        keys = {'gigya_uid': 'test_uid_01'}
        items = {
            'create_session_timestamp': '2022-05-13 12:34:56.789',
            'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'expire_session_timestamp': '2022-05-27 12:34:56.789',
            'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }
        result = upsert_dynamodb(table_name, keys, items)
        assert result['ResponseMetadata']['HTTPStatusCode'] == 200

    def test_upsert_dynamodb_ok_02(self):
        """
        正常系
        ConditionalCheckFailedExceptionの場合
        """
        table_name = 't_session'
        keys = {'gigya_uid': 'test_uid_012'}
        condition = 'attribute_exists(gigya_uid)'
        items = {
            'create_session_timestamp': '2022-05-13 12:34:56.789',
            'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2',
            'expire_session_timestamp': '2022-05-27 12:34:56.789',
            'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2'
        }
        result = upsert_dynamodb(table_name, keys, items, condition)
        assert result['ResponseMetadata']['HTTPStatusCode'] == 200

    def test_upsert_dynamodb_error_01(self):
        """
        異常系
        """
        table_name = 'ng_table_name'
        keys = {'gigya_uid': 'test_uid_01'}
        items = {
            'create_session_timestamp': '2022-05-13 12:34:56.789',
            'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2',
            'expire_session_timestamp': '2022-05-27 12:34:56.789',
            'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2'
        }
        with pytest.raises(DynamoDbAccessError):
            upsert_dynamodb(table_name, keys, items)

    def test_put_dynamodb_ok_01(self):
        """
        正常系
        """
        table_name = 't_session'
        items = {
            'gigya_uid': 'test_uid_01',
            'create_session_timestamp': '2022-05-13 12:34:56.789',
            'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'expire_session_timestamp': '2022-05-27 12:34:56.789',
            'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }
        result = put_dynamodb(table_name, items)

        assert result['ResponseMetadata']['HTTPStatusCode'] == 200

    def test_put_dynamodb_error_01(self):
        """
        異常系
        """
        table_name = 'ng_table_name'
        keys = {'gigya_uid': 'test_uid_01'}
        items = {
            'gigya_uid': 'test_uid_01',
            'create_session_timestamp': '2022-05-13 12:34:56.789',
            'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'expire_session_timestamp': '2022-05-27 12:34:56.789',
            'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
        }
        with pytest.raises(DynamoDbAccessError):
            put_dynamodb(table_name, keys, items)

    def test_get_message_ok_01(self):
        """
        正常系
        """
        message_cd = 'E005'
        result = get_message(message_cd)
        assert result == 'validation error'

    def test_get_constant_ok_01(self):
        """
        正常系 定数マスタ取得
        code指定あり
        """
        expected_value = '02'
        data = get_constant('MAINTENANCE_TYPE_CODE', 'DISTANCE', '02')
        assert data == expected_value

    def test_get_constant_ok_02(self):
        """
        正常系 定数マスタ取得
        code指定なし
        """
        expected_value = {'DISTANCE': '02', 'ROUTINE': '03', 'TIME': '01'}
        data = get_constant('MAINTENANCE_TYPE_CODE')
        assert data == expected_value

    def test_get_constant_ng(self):
        """
        正常系 定数マスタ取得
        データなし
        """
        expected_value = None
        data = get_constant('test')
        assert data == expected_value

    def test_get_s3_bucket_key_ok(self):
        """
        正常系
        """
        os.environ['STAGE'] = 'dev'
        category_cd = 'S3_BUCKET_PREFIX'
        code = 'EXPLANATION'
        result = get_s3_bucket_key(category_cd, code)
        expected_value = 'explanation-images/'
        assert result == expected_value
