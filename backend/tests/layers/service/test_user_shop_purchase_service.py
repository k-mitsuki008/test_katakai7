
from importlib import import_module, reload
import pytest

from common.error.not_expected_error import NotExpectedError

module = import_module('service.user_shop_purchase_service')
upsert_t_user_shop_purchase = getattr(module, 'upsert_t_user_shop_purchase')


def test_upsert_t_user_shop_purchase_ok(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    """
    # tasks.repository.upsert_t_user_shop_purchase のモック化
    mocker.patch(
        "repository.user_shop_purchase_repository.upsert_t_user_shop_purchase",
        return_value=0
    )
    # tasks.repository.get_t_user_shop_purchase のモック化
    mocker.patch(
        "repository.user_shop_purchase_repository.get_t_user_shop_purchase",
        return_value={
            'user_vehicle_id': 1234,
            'shop_name': 'test_shop_02',
            'shop_tel': '0312345678',
            'shop_location': '東京都世田谷区玉川2丁目2-2',
        }
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        'user_vehicle_id': 1234,
        'shop_name': 'test_shop_02',
        'shop_tel': '0312345678',
        'shop_location': '東京都世田谷区玉川2丁目2-2',
    }

    user_vehicle_id = 1234
    recs = {
        'shop_name': 'test_shop_02',
        'shop_tel': '0312345678',
        'shop_location': '東京都世田谷区玉川2丁目2-2',
    }
    updated_data = upsert_t_user_shop_purchase(user_vehicle_id, **recs)

    assert updated_data == expected_value


def test_get_tasks_ng_not_expected_error_01(mocker):

    """
    準正常系: upsert_t_user_shop_purchaseでエラー
    ※ Exception → NotExpectedError に変換されること
    """

    # tasks.repository.upsert_t_user_shop_purchase のモック化
    mocker.patch(
        "repository.user_shop_purchase_repository.upsert_t_user_shop_purchase",
        side_effect=Exception
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        upsert_t_user_shop_purchase(8888, **{})


def test_get_tasks_ng_not_expected_error_02(mocker):

    """
    準正常系: get_t_user_shop_purchaseでNoneが返却
    ※ Exception → NotExpectedError に変換されること
    """

    # tasks.repository.upsert_t_user_shop_purchase のモック化
    mocker.patch(
        "repository.user_shop_purchase_repository.upsert_t_user_shop_purchase",
        return_value=0
    )
    # tasks.repository.get_t_user_shop_purchase のモック化
    mocker.patch(
        "repository.user_shop_purchase_repository.get_t_user_shop_purchase",
        return_value=None
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        upsert_t_user_shop_purchase(9999, **{})
