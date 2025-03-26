from importlib import import_module, reload
import pytest
from common.error.not_expected_error import NotExpectedError
import tests.test_utils.fixtures as fixtures
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.user_setting_maintain_service')
initialize_maintenance_setting = getattr(module, 'initialize_maintenance_setting')
upsert_setting_maintain = getattr(module, 'upsert_setting_maintain')


def test_initialize_maintenance_setting_ok(mocker):
    """
    正常系
    """
    # repository.user_setting_maintain_repository.get_user_setting_maintains のモック化
    mocker.patch("repository.user_setting_maintain_repository.get_user_setting_maintains", return_value=[
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01", "maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_item_alert": None, "maintain_item_alert_status": None},
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01", "maintain_item_code": "00003", "maintain_item_name": "タイヤ摩耗", "maintain_item_alert": None, "maintain_item_alert_status": None},
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "maintain_consciousness": "01", "maintain_item_code": "00004", "maintain_item_name": "チェーン動作", "maintain_item_alert": None, "maintain_item_alert_status": None},
    ])
    # repository.user_setting_maintain_repository.upsert_t_user_setting_maintain のモック化
    mocker.patch("repository.user_setting_maintain_repository.upsert_t_user_setting_maintain", return_value='01')
    # repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain のモック化
    mocker.patch("repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item", return_value=True)

    reload(module)

    # 期待している返却値
    expected_value = {
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "タイヤ空気圧",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00003",
                "maintain_item_name": "タイヤ摩耗",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00004",
                "maintain_item_name": "チェーン動作",
                "maintain_item_alert": True
            }
        ]
    }

    result = initialize_maintenance_setting(1, 'test_uid_01')

    assert result == expected_value


def test_upsert_t_user_setting_maintain_ok_01(mocker):
    """
    正常系
    ユーザメンテナンス設定TBL更新データあり
    ユーザメンテナンス項目設定TBL更新データあり
    """
    # tasks.repository.upsert_t_user_setting_maintainのモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.upsert_t_user_setting_maintain",
        return_value=0
    )
    # tasks.repository.upsert_t_user_setting_maintain_itemのモック化
    mocker.patch(
        "repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item",
        return_value=0
    )
    # tasks.repository.get_user_maintain_setting_user_vehicle_idのモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.get_user_maintain_setting_user_vehicle_id",
        return_value=[
            {
                "user_vehicle_id": 1234,
                "gigya_uid": "test01",
                "maintain_consciousness": "01",
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_item_alert": True,
            },
            {
                "user_vehicle_id": 1234,
                "gigya_uid": "test01",
                "maintain_consciousness": "01",
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_item_alert": True,
            }
        ]
    )
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = {
        "user_vehicle_id": 1234,
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_item_alert": True
            },
        ]
    }

    user_vehicle_id = 1234
    gigya_uid = "test_uid_01"
    recs = {
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00001",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00002",
                "maintain_item_alert": False
            }
        ]
    }
    data = upsert_setting_maintain(gigya_uid, user_vehicle_id, **recs)

    assert data == expected_value


def test_upsert_t_user_setting_maintain_ok_02(mocker):
    """
    正常系
    ユーザメンテナンス設定TBL更新データあり
    ユーザメンテナンス項目設定TBL更新データなし
    """
    # tasks.repository.upsert_t_user_setting_maintainのモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.upsert_t_user_setting_maintain",
        return_value=0
    )
    # tasks.repository.upsert_t_user_setting_maintain_itemのモック化
    mocker.patch(
        "repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item",
        return_value=0
    )
    # tasks.repository.get_user_maintain_setting_user_vehicle_idのモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.get_user_maintain_setting_user_vehicle_id",
        return_value=[
            {
                "user_vehicle_id": 1234,
                "gigya_uid": "test01",
                "maintain_consciousness": "01",
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_item_alert": True,
            },
            {
                "user_vehicle_id": 1234,
                "gigya_uid": "test01",
                "maintain_consciousness": "01",
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_item_alert": True,
            }
        ]
    )
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = {
        "user_vehicle_id": 1234,
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_item_alert": True
            },
        ]
    }

    user_vehicle_id = 1234
    gigya_uid = "test_uid_01"
    recs = {
        "maintain_consciousness": "01"
    }
    data = upsert_setting_maintain(gigya_uid, user_vehicle_id, **recs)

    assert data == expected_value


def test_upsert_t_user_setting_maintain_ok_03(mocker):
    """
    正常系
    ユーザメンテナンス設定TBL更新データなし
    ユーザメンテナンス項目設定TBL更新データあり
    """
    # tasks.repository.upsert_t_user_setting_maintainのモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.upsert_t_user_setting_maintain",
        return_value=0
    )
    # tasks.repository.upsert_t_user_setting_maintain_itemのモック化
    mocker.patch(
        "repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item",
        return_value=0
    )
    # tasks.repository.get_user_maintain_setting_user_vehicle_idのモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.get_user_maintain_setting_user_vehicle_id",
        return_value=[
            {
                "user_vehicle_id": 1234,
                "maintain_consciousness": "01",
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_item_alert": True,
            },
            {
                "user_vehicle_id": 1234,
                "maintain_consciousness": "01",
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_item_alert": True,
            }
        ]
    )
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = {
        "user_vehicle_id": 1234,
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_item_alert": True
            },
        ]
    }

    user_vehicle_id = 1234
    gigya_uid = "test_uid_01"
    recs = {
        "maintain_alerts": [
            {
                "maintain_item_code": "00001",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00002",
                "maintain_item_alert": False
            }
        ]
    }
    data = upsert_setting_maintain(gigya_uid, user_vehicle_id, **recs)

    assert data == expected_value


def test_upsert_t_user_setting_maintain_ok_04(mocker):
    """
    正常系
    ユーザメンテナンス設定TBL更新データあり
    ユーザメンテナンス項目設定TBL更新データあり
    """
    # tasks.repository.upsert_t_user_setting_maintainのモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.upsert_t_user_setting_maintain",
        return_value=0
    )
    # tasks.repository.upsert_t_user_setting_maintain_itemのモック化
    mocker.patch(
        "repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item",
        return_value=0
    )
    # tasks.repository.get_user_maintain_setting_user_vehicle_idのモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.get_user_maintain_setting_user_vehicle_id",
        return_value=[
            {
                "user_vehicle_id": 1234,
                "gigya_uid": "test01",
                "maintain_consciousness": "01",
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_item_alert": True,
            },
            {
                "user_vehicle_id": 1234,
                "gigya_uid": "test01",
                "maintain_consciousness": "01",
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_item_alert": True,
            }
        ]
    )
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch("common.rds.connect.DbConnection.connect", return_value=None)
    reload(module)

    # 期待している返却値
    expected_value = {
        "user_vehicle_id": 1234,
        "maintain_consciousness": "01",
        "maintain_alerts": [
            {
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_item_alert": True
            },
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_item_alert": True
            },
        ]
    }

    user_vehicle_id = 1234
    gigya_uid = "test_uid_01"
    recs = {
        "maintain_consciousness": "01",
        "maintain_alerts": []
    }
    data = upsert_setting_maintain(gigya_uid, user_vehicle_id, **recs)

    assert data == expected_value


def test_get_tasks_ng_not_expected_error_01(mocker):
    """
    準正常系: update_t_user_setting_maintain
    ※ Exception → NotExpectedError に変換されること
    """

    # tasks.repository.update_t_user_setting_maintainのモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.upsert_t_user_setting_maintain",
        side_effect=Exception
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        upsert_setting_maintain(8888, **{})


def test_get_tasks_ng_not_expected_error_02(mocker):
    """
    準正常系: get_user_maintain_setting_user_vehicle_idでNoneが返却
    """
    # tasks.repository.update_t_user_setting_maintain のモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.upsert_t_user_setting_maintain",
        return_value=0
    )
    # tasks.repository.get_user_maintain_setting_user_vehicle_id のモック化
    mocker.patch(
        "repository.user_setting_maintain_repository.get_user_maintain_setting_user_vehicle_id",
        return_value=None
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        upsert_setting_maintain(9999, 9999,  **{})
