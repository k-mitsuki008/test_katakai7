from importlib import import_module
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.session_repository')
upsert_t_session = getattr(module, 'upsert_t_session')
update_t_session = getattr(module, 'update_t_session')
get_t_session_by_key = getattr(module, 'get_t_session_by_key')
get_t_session_by_session_id = getattr(module, 'get_t_session_by_session_id')


def test_upsert_t_session_ok_01():
    """
    正常系: セッションTBL UPSERT(INSERT)
    """
    expected_value = {'gigya_uid': 'test_uid_03', 'session_id': 'test_session_03',
                      'create_session_timestamp': '2022/10/07 15:54:44.843'}

    gigya_uid = 'test_uid_03'
    recs = {
        "session_id": 'test_session_03',
        'create_session_timestamp': '2022/10/07 15:54:44.843',
    }

    res = upsert_t_session(gigya_uid, **recs)
    assert res == expected_value


def test_upsert_t_session_ok_02():
    """
    正常系: セッションTBL UPSERT(UPDATE)
    """
    expected_value = {'gigya_uid': 'test_uid_01', 'session_id': 'test_session_01_updated',
                      'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                      'create_session_timestamp': '2022-05-13 12:34:56.789',
                      'expire_session_timestamp': '2022/10/21 12:12:12.111'}

    gigya_uid = 'test_uid_01'
    recs = {
        'session_id': 'test_session_01_updated',
        'expire_session_timestamp': '2022/10/21 12:12:12.111',
    }

    res = upsert_t_session(gigya_uid, **recs)
    assert res == expected_value


def test_update_t_session_ok():
    """
    正常系: セッションTBL UPDATE
    """
    expected_value = {'gigya_uid': 'test_uid_01', 'session_id': 'test_session_01_updated',
                      'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                      'create_session_timestamp': '2022-05-13 12:34:56.789',
                      'expire_session_timestamp': '2022/10/21 12:12:12.111'}

    gigya_uid = 'test_uid_01'
    recs = {
        'session_id': 'test_session_01_updated',
        'expire_session_timestamp': '2022/10/21 12:12:12.111',
    }

    res = update_t_session(gigya_uid, **recs)
    assert res == expected_value


def test_get_t_session_ok():
    """
    正常系: セッションTBL SELECT
    """
    expected_value = {
        'gigya_uid': 'test_uid_01',
        'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'create_session_timestamp': '2022-05-13 12:34:56.789',
        'expire_session_timestamp': '2022-05-27 12:34:56.789'
    }

    res = get_t_session_by_key("test_uid_01")
    assert res == expected_value


def test_get_t_session_by_session_id():
    """
    正常系: セッションTBL SELECT(セッションキー指定)
    """
    expected_value = [{
        'gigya_uid': 'test_uid_01',
        'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'create_session_timestamp': '2022-05-13 12:34:56.789',
        'expire_session_timestamp': '2022-05-27 12:34:56.789'
    }]

    res = get_t_session_by_session_id("test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    assert res == expected_value


def test_get_t_session_ng_01():
    """
    異常系: セッションTBL SELECT 対象0件
    """
    expected_value = None

    result = get_t_session_by_key("test_uid_err")
    assert result == expected_value
