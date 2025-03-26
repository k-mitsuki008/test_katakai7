from importlib import import_module, reload
import pytest

from common.error.not_expected_error import NotExpectedError

module = import_module('service.user_shop_regular_service')
upsert_t_user_shop_regular = getattr(module, 'upsert_t_user_shop_regular')
insert_t_user_shop_regular = getattr(module, 'insert_t_user_shop_regular')
get_t_user_shop_regular = getattr(module, 'get_t_user_shop_regular')


def test_upsert_t_user_shop_regular_ok_01(mocker):
    """
    正常系
    普段利用する店舗TBに登録あり
    ※ repository関数からの取得値をそのまま返す
    """
    # tasks.repository.def upsert_t_user_shop_regular のモック化
    mocker.patch(
        "repository.user_shop_regular_repository.upsert_t_user_shop_regular",
        return_value=0
    )
    # tasks.repository.get_t_user_shop_regular のモック化
    mocker.patch(
        "repository.user_shop_regular_repository.get_t_user_shop_regular",
        return_value={
            "shop_name": "test_shop_02",
            "shop_tel": "0312345678",
            "shop_location": "東京都世田谷区玉川2丁目2-2"
        }
    )
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = {
        'regular_shop_name': 'test_shop_02',
        'regular_shop_tel': '0312345678',
        'regular_shop_location': '東京都世田谷区玉川2丁目2-2',
    }

    gigya_uid = 'test01'
    recs = {
        'regular_shop_name': 'test_shop_02',
        'regular_shop_tel': '0312345678',
        'regular_shop_location': '東京都世田谷区玉川2丁目2-2',
    }
    data = upsert_t_user_shop_regular(gigya_uid, **recs)

    assert data == expected_value


def test_get_tasks_ng_not_expected_error_01(mocker):

    """
    準正常系: upsert_t_user_shop_regularでエラー
    ※ Exception → NotExpectedError に変換されること
    """

    # tasks.repository.upsert_t_user_shop_regular のモック化
    mocker.patch(
        "repository.user_shop_regular_repository.upsert_t_user_shop_regular",
        side_effect=Exception
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        upsert_t_user_shop_regular(8888, **{})


def test_upsert_t_user_shop_regular_ok_02(mocker):
    """
    準正常系: get_t_user_shop_regularでNoneが返却
    ※ Exception → NotExpectedError に変換されること
    """
    # tasks.repository.def upsert_t_user_shop_regular のモック化
    mocker.patch(
        "repository.user_shop_regular_repository.upsert_t_user_shop_regular",
        return_value=0
    )
    # tasks.repository.get_t_user_shop_regular のモック化
    mocker.patch(
        "repository.user_shop_regular_repository.get_t_user_shop_regular",
        return_value=None
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        upsert_t_user_shop_regular(9999, **{})


def test_insert_t_user_shop_regular_ok_01(mocker):
    """
    正常系
    普段利用する店舗TBに登録あり
    ※ repository関数からの取得値をそのまま返す
    """
    # tasks.repository.def insert_t_user_shop_regular のモック化
    mocker.patch(
        "repository.user_shop_regular_repository.insert_t_user_shop_regular",
        return_value=0
    )
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = None

    gigya_uid = 'test01'
    recs = {
        'regular_shop_name': 'test_shop_02',
        'regular_shop_tel': '0312345678',
        'regular_shop_location': '東京都世田谷区玉川2丁目2-2',
    }
    data = insert_t_user_shop_regular(gigya_uid, **recs)

    assert data == expected_value


def test_get_t_user_shop_regular_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    """
    # tasks.repository.def get_t_user_shop_regularのモック化
    mocker.patch(
        "repository.user_shop_regular_repository.get_t_user_shop_regular",
        return_value={
            "shop_name": "test_shop_02",
            "shop_tel": "0312345678",
            "shop_location": "東京都世田谷区玉川2丁目2-2"
        }
    )

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = {
        'regular_shop_name': 'test_shop_02',
        'regular_shop_tel': '0312345678',
        'regular_shop_location': '東京都世田谷区玉川2丁目2-2',
    }

    gigya_uid = 'test01'
    data = get_t_user_shop_regular(gigya_uid)

    assert data == expected_value


def test_get_t_user_shop_regular_ok_02(mocker):
    """
    正常系
    get_t_user_shop_regularがデータ取得出来ない場合
    ※ repository関数からの取得値をそのまま返す
    """
    # tasks.repository.def get_t_user_shop_regularのモック化
    mocker.patch(
        "repository.user_shop_regular_repository.get_t_user_shop_regular",
        return_value=None,
    )

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = None

    gigya_uid = 'test01'
    data = get_t_user_shop_regular(gigya_uid)

    assert data == expected_value
