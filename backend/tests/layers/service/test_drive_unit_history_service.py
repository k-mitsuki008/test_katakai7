from importlib import import_module, reload

import pytest

from common.error.not_expected_error import NotExpectedError
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.drive_unit_history_service')
registration_drive_unit_history = getattr(module, 'registration_drive_unit_history')


def test_registration_drive_unit_history_ok_01(mocker):
    """
    正常系 ドライブユニット履歴テーブル更新登録: 初回登録
    """
    # repository.drive_unit_history_repository.get_latest_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.get_latest_drive_unit_history", return_value=None)
    # repository.drive_unit_history_repository.insert_t_drive_unit_history のモック化
    m = mocker.patch("repository.drive_unit_history_repository.insert_t_drive_unit_history", return_value=0)
    reload(module)

    rec = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
        "du_serial_number": "16777215",
        "timestamp": "2022-10-06T15:30:31.000",
        "du_odometer": 120
    }

    registration_drive_unit_history(**rec)

    # repositoryに渡す引数の確認
    m.assert_called_with(**{
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
        "du_serial_number": "16777215",
        "timestamp": "2022-10-06T15:30:31.000",
        "du_odometer": 120,
    })


def test_registration_drive_unit_history_ok_02(mocker):
    """
    正常系 ドライブユニット履歴テーブル更新登録: Du識別子が変更
    """
    # repository.drive_unit_history_repository.get_latest_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.get_latest_drive_unit_history", return_value={"du_serial_number": "000011"})
    # repository.drive_unit_history_repository.update_latest_drive_unit_history のモック化
    update_latest_drive_unit_history_mock = \
        mocker.patch("repository.drive_unit_history_repository.update_latest_drive_unit_history", return_value=1)
    # repository.drive_unit_history_repository.insert_t_drive_unit_history のモック化
    insert_t_drive_unit_history_mock = \
        mocker.patch("repository.drive_unit_history_repository.insert_t_drive_unit_history", return_value=0)
    reload(module)

    rec = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
        "du_serial_number": "16777215",
        "timestamp": "2022-10-06T15:30:31.000",
        "du_odometer": 120
    }

    registration_drive_unit_history(**rec)

    # repositoryに渡す引数の確認
    update_latest_drive_unit_history_mock.assert_called_with(
        "test_uid_01",
        123,
        **{"du_last_timestamp": "2022-10-06T15:30:31.000"},
    )

    insert_t_drive_unit_history_mock.assert_called_with(**{
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
        "du_serial_number": "16777215",
        "timestamp": "2022-10-06T15:30:31.000",
        "du_odometer": 120,
    })


def test_registration_drive_unit_history_ok_03(mocker):
    """
    正常系 ドライブユニット履歴テーブル更新登録: Du識別子が同一
    """
    # repository.drive_unit_history_repository.get_latest_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.get_latest_drive_unit_history", return_value={"du_serial_number": "16777215"})
    # repository.drive_unit_history_repository.update_latest_drive_unit_history のモック化
    m = mocker.patch("repository.drive_unit_history_repository.update_latest_drive_unit_history", return_value=1)
    reload(module)

    rec = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
        "du_serial_number": "16777215",
        "timestamp": "2022-10-06T15:30:31.000",
        "du_odometer": 120
    }

    registration_drive_unit_history(**rec)

    # repositoryに渡す引数の確認
    m.assert_called_with(
        "test_uid_01",
        123,
        **{"du_last_odometer": 120},
    )


def test_registration_drive_unit_history_ng(mocker):
    """
    異常系 ドライブユニット履歴テーブル更新登録: 想定外エラー
    """
    # repository.drive_unit_history_repository.get_latest_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.get_latest_drive_unit_history",
                 return_value={"du_serial_number": "10000000"})
    # repository.drive_unit_history_repository.update_latest_drive_unit_history のモック化
    m = mocker.patch("repository.drive_unit_history_repository.update_latest_drive_unit_history", return_value=None)
    # repository.drive_unit_history_repository.insert_t_drive_unit_history のモック化
    m = mocker.patch("repository.drive_unit_history_repository.insert_t_drive_unit_history", return_value=None)
    reload(module)

    rec = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
        "du_serial_number": "999999999",
        "timestamp": "2022-10-06T15:30:31.000",
        "du_odometer": 120
    }

    with pytest.raises(NotExpectedError):
        registration_drive_unit_history(**rec)
