from importlib import import_module, reload

module = import_module('service.user_info_service')
get_user_info = getattr(module, 'get_user_info')
upsert_user_info = getattr(module, 'upsert_user_info')


def test_get_user_info_ok_01(mocker):
    """
    正常系: ユーザ情報取得
    レコードあり
    """

    # tasks.repository.radar_user_info_setting_repository.get_user_info_setting のモック化
    mocker.patch(
        'repository.radar_user_info_setting_repository.get_user_info_setting',
        return_value={
            'nickname': 'nickname',
            'weight': 60,
            'birth_date': '2000-01-01',
            'max_heart_rate': 150
        }
    )
    reload(module)

    expected_value = {
        'nickname': 'nickname',
        'weight': 60,
        'birth_date': '2000-01-01',
        'max_heart_rate': 150
    }

    result = get_user_info('test_uid_02')
    assert result == expected_value


def test_get_user_info_ng_01(mocker):
    """
    異常系: ユーザ情報取得
    個人設定レコードなし
    """

    # tasks.repository.radar_user_info_setting_repository.get_user_info_setting のモック化
    mocker.patch('repository.radar_user_info_setting_repository.get_user_info_setting', return_value={})
    reload(module)

    expected_value = {
        'nickname': None,
        'weight': None,
        'birth_date': None,
        'max_heart_rate': None
    }

    result = get_user_info('test_uid_02')
    assert result == expected_value


def test_upsert_user_ok_01(mocker):
    """
    正常系 個人設定登録更新
    全項目設定
    """
    # repository.radar_user_info_setting_repository.upsert_user_info のモック化
    m = mocker.patch('repository.radar_user_info_setting_repository.upsert_user_info_setting', return_value={})
    reload(module)

    # 期待している返却値
    expected_value = {}

    upsert_data = upsert_user_info('new_user', 'new_user_1', 60, '2001-01-01', 150)

    assert upsert_data == expected_value

    test_input = {
        'nickname': 'new_user_1',
        'weight': 60,
        'birth_date': '2001-01-01',
        'max_heart_rate': 150
    }
    # ユーザー情報登録がinsertされることを確認
    m.assert_called_with('new_user', **test_input)


def test_upsert_user_ok_02(mocker):
    """
    正常系 個人設定登録更新
    項目不足
    """
    # repository.radar_user_info_setting_repository.upsert_user_info のモック化
    m = mocker.patch('repository.radar_user_info_setting_repository.upsert_user_info_setting', return_value={})
    reload(module)

    # 期待している返却値
    expected_value = {}

    upsert_data = upsert_user_info('new_user', 'new_user_1', 60, None, None)

    assert upsert_data == expected_value

    test_input = {
        'nickname': 'new_user_1',
        'weight': 60
    }
    # ユーザー情報登録がinsertされることを確認
    m.assert_called_with('new_user', **test_input)
