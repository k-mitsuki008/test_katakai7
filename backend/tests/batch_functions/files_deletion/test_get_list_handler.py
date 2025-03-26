from importlib import import_module, reload
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.batch_functions.files_deletion.get_list_handler')
handler = getattr(module, 'handler')


def test_handler():
    """
    正常系 ファイル削除バッチ処理
    Mock化なし
    """

    # 期待しているレスポンスボディの値
    expected_value = {
        "file_id_list": [{
            'test_uid_02': ['test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', None, None, None],
            'test_uid_03': [None, None, None, 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1', 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2', None, None, None, None, None, None, None, None, None, None]
        }]
    }

    response = handler({
        'version': '0',
        'id': 'abcde',
        'detail-type': 'Scheduled Event',
        'source': 'aws.events',
        'account': '889185496976',
        'time': '2022-02-22T06:00:00Z',
        'region': 'eu-west-1',
        'resources': 'abcde',
        'detail': {}
    })

    assert response == expected_value


def test_handler_ok(mocker):
    """
    正常系 ファイル削除バッチ処理
    Mock化
    """

    # device.service.delete_file_service import get_file のモック化
    mocker.patch("service.delete_file_service.get_file", return_value=[{
            'test_uid_02': ['test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', None, None, None],
            'test_uid_03': [None, None, None, 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1', 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2', None, None, None, None, None, None, None, None, None, None]
        }])

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "file_id_list": [{
            'test_uid_02': ['test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', 'test1', 'test2', 'test3', None, None, None],
            'test_uid_03': [None, None, None, 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1', 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2', None, None, None, None, None, None, None, None, None, None]
        }]
    }

    response = handler({
        'version': '0',
        'id': 'abcde',
        'detail-type': 'Scheduled Event',
        'source': 'aws.events',
        'account': '889185496976',
        'time': '2022-02-22T06:00:00Z',
        'region': 'eu-west-1',
        'resources': 'abcde',
        'detail': {}
    })

    assert response == expected_value
