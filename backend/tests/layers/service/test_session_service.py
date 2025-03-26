from importlib import import_module, reload
import pytest
from common.error.not_expected_error import NotExpectedError

module = import_module('service.session_service')
login_session = getattr(module, 'login_session')
logout_session = getattr(module, 'logout_session')
get_t_session_by_session_id = getattr(module, 'get_t_session_by_session_id')


@pytest.mark.freeze_time("2022-05-13 12:34:56.123")
def test_login_session_ok(mocker):
    """
    正常系
    """
    # secrets.token_hex のモック化
    mocker.patch(
        "secrets.token_hex", return_value='test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
    )
    # repository.session_repository.upsert_t_session のモック化
    m = mocker.patch("repository.session_repository.upsert_t_session", return_value={
        'gigya_uid': 'test_uid_01',
        'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'create_session_timestamp': '2022-05-13 12:34:56.123',
        'expire_session_timestamp': '2022-05-27 12:34:56.123'
    })
    reload(module)

    # 期待している返却値
    expected_value = {
        'gigya_uid': 'test_uid_01',
        'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'create_session_timestamp': '2022-05-13 12:34:56.123',
        'expire_session_timestamp': '2022-05-27 12:34:56.123'
    }

    updated_data = login_session('test_uid_01', 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    assert updated_data == expected_value

    # 想定したsession_id, 開始日時、終了日時で更新していることを確認。
    m.assert_called_with(
        'test_uid_01',
        session_id='test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        device_id='ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        create_session_timestamp='2022-05-13 12:34:56.123000',
        expire_session_timestamp='2022-05-27 12:34:56.123000'
    )


def test_login_session_ng(mocker):
    """
    異常系　update結果 = None
    """
    # repository.session_repository.upsert_t_session のモック化
    mocker.patch("repository.session_repository.upsert_t_session", return_value=None)
    reload(module)

    with pytest.raises(NotExpectedError) as e:
        ret = login_session('test_uid_01', 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        assert ret is None


@pytest.mark.freeze_time("2022-05-13 12:34:56.123")
def test_logout_session_ok(mocker):
    """
    正常系
    """
    # repository.session_repository.upsert_t_session のモック化
    m = mocker.patch("repository.session_repository.update_t_session", return_value={
        'gigya_uid': 'test_uid_01',
        'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'expire_session_timestamp': '2022-05-13 12:34:56.123',
        'attribute_exists': 'test_uid_01'
    })
    reload(module)

    # 期待している返却値
    expected_value = {
        'gigya_uid': 'test_uid_01',
        'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        'expire_session_timestamp': '2022-05-13 12:34:56.123',
        'attribute_exists': 'test_uid_01'
    }

    updated_data = logout_session('test_uid_01')
    assert updated_data == expected_value


def test_logout_session_ng(mocker):
    """
    異常系　update結果 = None
    """
    # repository.session_repository.upsert_t_session のモック化
    mocker.patch("repository.session_repository.update_t_session", return_value=None)
    reload(module)

    with pytest.raises(NotExpectedError) as e:
        ret = logout_session('test_uid_99')
        assert ret is None


def test_get_t_session_by_session_id_ok(mocker):
    """
    正常系
    """
    # repository.session_repository.upsert_t_session のモック化
    mocker.patch("repository.session_repository.get_t_session_by_session_id", return_value={
        't_session': "test",
        'session_id-index': "test_id_index",
        'session_id': "test_session_id"
    })
    reload(module)

    # 期待している返却値
    expected_value = {
        't_session': "test",
        'session_id-index': "test_id_index",
        'session_id': "test_session_id"
    }

    updated_data = get_t_session_by_session_id('test_session_id')
    assert updated_data == expected_value
