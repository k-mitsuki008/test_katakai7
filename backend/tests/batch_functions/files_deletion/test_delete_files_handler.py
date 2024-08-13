import tests.test_utils.fixtures as fixtures
from importlib import import_module, reload

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.batch_functions.files_deletion.delete_files_handler')
handler = getattr(module, 'handler')


def test_handler_ok(mocker):
    """
    正常系 ファイル削除バッチ処理
    Mock化
    """
    # device.service.delete_file_service import delete_file のモック化
    mocker.patch("service.delete_file_service.delete_file", return_value=None)

    reload(module)

    response = handler({
        'test_uid_01': ['1-1', '1-2', '1-3', '1-4', None, '1-6', '1-7', '1-8', '1-9'],
        'test_uid_02': ['2-7', '2-8', '2-9', '2-1', None, '2-3', '2-4', '2-5', '2-6'],
        'test_uid_03': ['3-1', '3-2', '3-3', '3-4', None, '3-6', '3-7', '3-8', None]
    })

    expected_value = {'result': True}
    assert response == expected_value


def test_handler(mocker):
    """
    正常系 ファイル削除バッチ処理
    Mock化なし
    """
    # common.utils.aws_utils import get_s3_objects のモック化
    def get_s3_objects_dict_list(bucket: str, key: str) -> dict:
        result = {}
        if key == 'test_uid_01':
            result = {
                'Contents': [
                    {'Key': 'test_uid_01/', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 0, 'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_01/8-1.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 4070378, 'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_01/8-2.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687, 'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_01/8-3.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,'StorageClass': 'STANDARD'}
                ]
            }
        elif key == 'test_uid_02':
            result = {
                'Contents': [
                    {'Key': 'test_uid_02/', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 0,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_02/9-1.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 4070378,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_02/9-2.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_02/9-3.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,
                     'StorageClass': 'STANDARD'}
                ]
            }
        elif key == 'test_uid_03':
            result = {
                'Contents': [
                    {'Key': 'test_uid_03/', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 0,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_03/10-1.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 4070378,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_03/10-2.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_03/10-3.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,
                     'StorageClass': 'STANDARD'}
                ]
            }
        return result
    mocker.patch(
        "service.delete_file_service.get_s3_objects",
        side_effect=get_s3_objects_dict_list
    )

    # common.utils.aws_utils import delete_s3_objects のモック化
    delete_s3_objects_mock = \
        mocker.patch("service.delete_file_service.delete_s3_objects", side_effect=lambda *args, **kwargs: args)

    reload(module)

    response = handler({
        'test_uid_01': ['1-1', '1-2', '1-3', '1-4', None, '1-6', '1-7', '1-8', '1-9'],
        'test_uid_02': ['2-7', '2-8', '2-9', '2-1', None, '2-3', '2-4', '2-5', '2-6'],
        'test_uid_03': ['3-1', '3-2', '3-3', '3-4', None, '3-6', '3-7', '3-8', None]
    })

    delete_s3_objects_mock.assert_any_call('spvc-dev-upload-items', 'test_uid_01/8-1.png')
    delete_s3_objects_mock.assert_any_call('spvc-dev-upload-items', 'test_uid_01/8-2.png')
    delete_s3_objects_mock.assert_any_call('spvc-dev-upload-items', 'test_uid_01/8-3.png')

    delete_s3_objects_mock.assert_any_call('spvc-dev-upload-items', 'test_uid_02/9-1.png')
    delete_s3_objects_mock.assert_any_call('spvc-dev-upload-items', 'test_uid_02/9-2.png')
    delete_s3_objects_mock.assert_any_call('spvc-dev-upload-items', 'test_uid_02/9-3.png')

    delete_s3_objects_mock.assert_any_call('spvc-dev-upload-items', 'test_uid_03/10-1.png')
    delete_s3_objects_mock.assert_any_call('spvc-dev-upload-items', 'test_uid_03/10-2.png')
    delete_s3_objects_mock.assert_any_call('spvc-dev-upload-items', 'test_uid_03/10-3.png')

    expected_value = {'result': True}
    assert response == expected_value
