from importlib import import_module
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.app_version_repository')
get_app_version_list = getattr(module, 'get_app_version_list')
upsert_app_version = getattr(module, 'upsert_app_version')


def test_upsert_app_version_ok():
    """
    正常系: アプリバージョンTBL UPDATE
    """
    expected_value = {
        'os': 'android',
        'app_name': 'yamaha_buddy_app_dev',
        'app_version': '1.1.1',
        'app_build_number': 4,
        'expiration_timestamp': 1753050096,
        'update_timestamp': 1752445296
    }

    version_info = {
        'app_name': 'yamaha_buddy_app_dev',
        'app_build_number': 4,
        'expiration_timestamp': 1753050096,
        'update_timestamp': 1752445296,
    }

    res = upsert_app_version('android', '1.1.1', **version_info)
    assert res == expected_value


def test_get_app_version_list_ok():
    """
    正常系: アプリバージョンTBL SELECT 対象あり
    """
    expected_value = [{
        'os': 'android',
        'app_name': 'yamaha_buddy_app_dev',
        'app_version': '1.1.0',
        'app_build_number': 3,
        'update_timestamp': 1703343600
    }, {
        'os': 'android',
        'app_name': 'yamaha_buddy_app_dev',
        'app_version': '0.1.0',
        'app_build_number': 2,
        'expiration_timestamp': 1703948300,
        'update_timestamp': 1703343500
    }, {
        'os': 'android',
        'app_name': 'yamaha_buddy_app_dev',
        'app_version': '0.0.1',
        'app_build_number': 1,
        'expiration_timestamp': 1703948200,
        'update_timestamp': 1703343400
    }]

    res = get_app_version_list('android')
    assert res == expected_value


def test_get_app_version_ng():
    """
    異常系: アプリバージョンTBL SELECT 対象なし
    """
    expected_value = []

    res = get_app_version_list(None)
    assert res == expected_value
