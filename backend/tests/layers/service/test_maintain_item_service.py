import os
from datetime import datetime, timedelta
import pytest
from importlib import import_module, reload
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.maintain_item_service')
get_maintain_items = getattr(module, 'get_maintain_items')
get_maintain_explanation = getattr(module, 'get_maintain_explanation')
cloud_front_domain_name = os.environ['CLOUD_FRONT_DOMAIN_NAME']


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_items_ok_01(mocker):
    """
    正常系 前回メンテナンス履歴:あり、前回メンテ時点のDU履歴:あり、前回メンテより後のDU履歴:あり
    """
    # repository.maintain_item_repository.get_maintain_items のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_items", return_value=[
        {
            # パターン1: メンテナンス指示種別:経過日数
            "maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_type_code": "01",
            "maintain_file_name_icon": "abcde00002.png",
            "maintain_interval": 10,
            "priority": 1,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000011",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        },
        {
            # パターン2: メンテナンス指示種別:走行距離
            "maintain_item_code": "00003", "maintain_item_name": "タイヤ摩耗", "maintain_type_code": "02",
            "maintain_file_name_icon": "abcde00003.png",
            "maintain_interval": 100,
            "priority": 2,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000011",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        },
        {
            # パターン3: メンテナンス指示種別:定期点検
            "maintain_item_code": "00009", "maintain_item_name": "定期点検", "maintain_type_code": "03",
            "maintain_file_name_icon": "abcde00009.png",
            "maintain_interval": 14,
            "priority": 9,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000022",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        }
    ])

    # repository.maintain_item_repository.get_maintain_count のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_count", return_value=2)

    # repository.rive_unit_history_repository.get_last_maintain_archive のモック化
    def get_last_maintain_archive_mock(gigya_uid: str, user_vehicle_id: int, last_maintain_du_serial_number: str, last_maintain_du_timestamp: str) -> dict:
        return {'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000011', 'du_last_timestamp': datetime(2022, 5, 11, 12, 34, 56, 789000), 'odometer': 10, 'du_first_odometer': 0, 'du_last_odometer': 10}
    mocker.patch("repository.drive_unit_history_repository.get_last_maintain_archive", side_effect=get_last_maintain_archive_mock)

    # repository.rive_unit_history_repository.get_after_last_maintain_archive_list のモック化
    def get_after_last_maintain_archive_list_mock(gigya_uid: str, user_vehicle_id: int, timestamp: str) -> list:
        return [{'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000011', 'days': timedelta(days=1), 'odometer': 10},
                {'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000022', 'days': timedelta(days=1), 'odometer': 10},
                {'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000011', 'days': timedelta(days=1, microseconds=101), 'odometer': 0}]
    mocker.patch("repository.drive_unit_history_repository.get_after_last_maintain_archive_list", side_effect=get_after_last_maintain_archive_list_mock)

    reload(module)

    # 期待している返却値
    expected_value = [
        #
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 3,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00002.png"
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 25,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00003.png"
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 180,
            "priority": 9,
            "maintain_archive": 3,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00009.png"
        }
    ]

    maintain_items = get_maintain_items('test_uid_02', 1)

    assert maintain_items == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_items_ok_02(mocker):
    """
    正常系 前回メンテナンス履歴:あり、前回メンテ時点のDU履歴:あり、前回メンテより後のDU履歴:無し
    """
    # repository.maintain_item_repository.get_maintain_items のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_items", return_value=[
        {
            # パターン1: メンテナンス指示種別:経過日数
            "maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_type_code": "01",
            "maintain_file_name_icon": "abcde00002.png",
            "maintain_interval": 10,
            "priority": 1,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000011",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        },
        {
            # パターン2: メンテナンス指示種別:走行距離
            "maintain_item_code": "00003", "maintain_item_name": "タイヤ摩耗", "maintain_type_code": "02",
            "maintain_file_name_icon": "abcde00003.png",
            "maintain_interval": 100,
            "priority": 2,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000011",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        },
        {
            # パターン3: メンテナンス指示種別:定期点検
            "maintain_item_code": "00009", "maintain_item_name": "定期点検", "maintain_type_code": "03",
            "maintain_file_name_icon": "abcde00009.png",
            "maintain_interval": 14,
            "priority": 9,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000022",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        }
    ])

    # repository.maintain_item_repository.get_maintain_count のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_count", return_value=1)

    # repository.rive_unit_history_repository.get_last_maintain_archive のモック化
    def get_last_maintain_archive_mock(gigya_uid: str, user_vehicle_id: int, last_maintain_du_serial_number: str, last_maintain_du_timestamp: str) -> dict:
        return {'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000011', 'du_last_timestamp': datetime(2022, 5, 11, 12, 34, 56, 789000), 'odometer': 10, 'du_first_odometer': 0, 'du_last_odometer': 10}
    mocker.patch("repository.drive_unit_history_repository.get_last_maintain_archive", side_effect=get_last_maintain_archive_mock)

    # repository.rive_unit_history_repository.get_after_last_maintain_archive_list のモック化
    def get_after_last_maintain_archive_list_mock(gigya_uid: str, user_vehicle_id: int, timestamp: str) -> list:
        return []
    mocker.patch("repository.drive_unit_history_repository.get_after_last_maintain_archive_list", side_effect=get_after_last_maintain_archive_list_mock)

    reload(module)

    # 期待している返却値
    expected_value = [
        #
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 3,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00002.png"
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 5,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00003.png"
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 120,
            "priority": 9,
            "maintain_archive": 3,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00009.png"
        }
    ]

    maintain_items = get_maintain_items('test_uid_02', 1)

    assert maintain_items == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_items_ok_03(mocker):
    """
    正常系 前回メンテナンス履歴:あり、前回メンテ時点のDU履歴:無し、前回メンテより後のDU履歴:あり
    """
    # repository.maintain_item_repository.get_maintain_items のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_items", return_value=[
        {
            # パターン1: メンテナンス指示種別:経過日数
            "maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_type_code": "01",
            "maintain_file_name_icon": "abcde00002.png",
            "maintain_interval": 10,
            "priority": 1,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000011",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        },
        {
            # パターン2: メンテナンス指示種別:走行距離
            "maintain_item_code": "00003", "maintain_item_name": "タイヤ摩耗", "maintain_type_code": "02",
            "maintain_file_name_icon": "abcde00003.png",
            "maintain_interval": 100,
            "priority": 2,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000011",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        },
        {
            # パターン3: メンテナンス指示種別:定期点検
            "maintain_item_code": "00009", "maintain_item_name": "定期点検", "maintain_type_code": "03",
            "maintain_file_name_icon": "abcde00009.png",
            "maintain_interval": 14,
            "priority": 9,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000022",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        }
    ])

    # repository.maintain_item_repository.get_maintain_count のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_count", return_value=1)

    # repository.rive_unit_history_repository.get_last_maintain_archive のモック化
    def get_last_maintain_archive_mock(gigya_uid: str, user_vehicle_id: int, last_maintain_du_serial_number: str, last_maintain_du_timestamp: str):
        return None
    mocker.patch("repository.drive_unit_history_repository.get_last_maintain_archive", side_effect=get_last_maintain_archive_mock)

    # repository.rive_unit_history_repository.get_after_last_maintain_archive_list のモック化
    def get_after_last_maintain_archive_list_mock(gigya_uid: str, user_vehicle_id: int, timestamp: str) -> list:
        return [{'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000011', 'days': timedelta(days=1), 'odometer': 10},
                {'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000022', 'days': timedelta(days=1), 'odometer': 10},
                {'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000011', 'days': timedelta(days=1, microseconds=101), 'odometer': 0}]
    mocker.patch("repository.drive_unit_history_repository.get_after_last_maintain_archive_list", side_effect=get_after_last_maintain_archive_list_mock)

    reload(module)

    # 期待している返却値
    expected_value = [
        #
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 3,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00002.png"
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 20,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00003.png"
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 120,
            "priority": 9,
            "maintain_archive": 3,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00009.png"
        }
    ]

    maintain_items = get_maintain_items('test_uid_02', 1)

    assert maintain_items == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_items_ok_04(mocker):
    """
    正常系 前回メンテナンス履歴:無し、DU履歴:1件
    """
    # repository.maintain_item_repository.get_maintain_items のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_items", return_value=[
        {
            "maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_type_code": "01",
            "maintain_file_name_icon": "abcde00002.png",
            "maintain_interval": 10,
            "priority": 1,
            "last_maintain_implement_date": None,
            "last_maintain_du_serial_number": None,
            "last_maintain_du_last_timestamp": None,
            "last_maintain_du_last_odometer": None
        },
        {
            "maintain_item_code": "00003", "maintain_item_name": "タイヤ摩耗", "maintain_type_code": "02",
            "maintain_file_name_icon": "abcde00003.png",
            "maintain_interval": 100,
            "priority": 2,
            "last_maintain_implement_date": None,
            "last_maintain_du_serial_number": None,
            "last_maintain_du_last_timestamp": None,
            "last_maintain_du_last_odometer": None
        },
        {
            "maintain_item_code": "00009", "maintain_item_name": "定期点検", "maintain_type_code": "03",
            "maintain_file_name_icon": "abcde00009.png",
            "maintain_interval": 14,
            "priority": 9,
            "last_maintain_implement_date": None,
            "last_maintain_du_serial_number": None,
            "last_maintain_du_last_timestamp": None,
            "last_maintain_du_last_odometer": None
        }
    ])

    # repository.maintain_item_repository.get_maintain_count のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_count", return_value=0)

    # repository.rive_unit_history_repository.get_last_maintain_archive のモック化
    def get_last_maintain_archive_mock(gigya_uid: str, user_vehicle_id: int, last_maintain_du_serial_number: str, last_maintain_du_timestamp: str):
        return None
    mocker.patch("repository.drive_unit_history_repository.get_last_maintain_archive", side_effect=get_last_maintain_archive_mock)

    # repository.drive_unit_history_repository.get_after_last_maintain_archive_list のモック化
    def get_after_last_maintain_archive_list_mock(gigya_uid: str, user_vehicle_id: int, timestamp: str) -> list:
        return [{'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000011', 'days': timedelta(days=1), 'odometer': 10}]
    mocker.patch("repository.drive_unit_history_repository.get_after_last_maintain_archive_list", side_effect=get_after_last_maintain_archive_list_mock)

    # repository.drive_unit_history_repository.get_oldest_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.get_oldest_drive_unit_history", return_value={
        'du_serial_number': '000011', 'du_first_timestamp': datetime(2022, 5, 10, 12, 34, 56, 789000), 'du_last_timestamp': datetime(2022, 5, 11, 12, 34, 56, 789000),
        'odometer': 10, 'du_first_odometer': 0, 'du_last_odometer': 10})

    reload(module)

    # 期待している返却値
    expected_value = [
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 4,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00002.png"
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 10,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00003.png"
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 60,
            "priority": 9,
            "maintain_archive": 4,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00009.png"
        }
    ]

    maintain_items = get_maintain_items('test_uid_02', 1)

    assert maintain_items == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_items_ok_05(mocker):
    """
    正常系 前回メンテナンス履歴:無し、DU履歴:複数件
    """
    # repository.maintain_item_repository.get_maintain_items のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_items", return_value=[
        {
            "maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_type_code": "01",
            "maintain_file_name_icon": "abcde00002.png",
            "maintain_interval": 10,
            "priority": 1,
            "last_maintain_implement_date": None,
            "last_maintain_du_serial_number": None,
            "last_maintain_du_last_timestamp": None,
            "last_maintain_du_last_odometer": None
        },
        {
            "maintain_item_code": "00003", "maintain_item_name": "タイヤ摩耗", "maintain_type_code": "02",
            "maintain_file_name_icon": "abcde00003.png",
            "maintain_interval": 100,
            "priority": 2,
            "last_maintain_implement_date": None,
            "last_maintain_du_serial_number": None,
            "last_maintain_du_last_timestamp": None,
            "last_maintain_du_last_odometer": None
        },
        {
            "maintain_item_code": "00009", "maintain_item_name": "定期点検", "maintain_type_code": "03",
            "maintain_file_name_icon": "abcde00009.png",
            "maintain_interval": 14,
            "priority": 9,
            "last_maintain_implement_date": None,
            "last_maintain_du_serial_number": None,
            "last_maintain_du_last_timestamp": None,
            "last_maintain_du_last_odometer": None
        }
    ])

    # repository.maintain_item_repository.get_maintain_count のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_count", return_value=0)

    # repository.rive_unit_history_repository.get_last_maintain_archive のモック化
    def get_last_maintain_archive_mock(gigya_uid: str, user_vehicle_id: int, last_maintain_du_serial_number: str, last_maintain_du_timestamp: str):
        return None
    mocker.patch("repository.drive_unit_history_repository.get_last_maintain_archive", side_effect=get_last_maintain_archive_mock)

    # repository.rive_unit_history_repository.get_after_last_maintain_archive_list のモック化
    def get_after_last_maintain_archive_list_mock(gigya_uid: str, user_vehicle_id: int, timestamp: str) -> list:
        return [{'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000011', 'days': timedelta(days=1), 'odometer': 10},
                {'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000022', 'days': timedelta(days=1), 'odometer': 10},
                {'user_vehicle_id': 1, 'gigya_uid': 'test_uid_02', 'du_serial_number': '000011', 'days': timedelta(days=1, microseconds=101), 'odometer': 0}]
    mocker.patch("repository.drive_unit_history_repository.get_after_last_maintain_archive_list", side_effect=get_after_last_maintain_archive_list_mock)

    # repository.drive_unit_history_repository.get_oldest_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.get_oldest_drive_unit_history", return_value={
        'du_serial_number': '000011', 'du_first_timestamp': datetime(2022, 5, 10, 12, 34, 56, 789000), 'du_last_timestamp': datetime(2022, 5, 11, 12, 34, 56, 789000),
        'odometer': 10, 'du_first_odometer': 0, 'du_last_odometer': 10})

    reload(module)

    # 期待している返却値
    expected_value = [
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 4,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00002.png"
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 20,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00003.png"
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 60,
            "priority": 9,
            "maintain_archive": 4,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00009.png"
        }
    ]

    maintain_items = get_maintain_items('test_uid_02', 1)

    assert maintain_items == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_items_ok_06(mocker):
    """
    正常系 前回メンテナンス履歴:無し、DU履歴:無し
    """
    # repository.maintain_item_repository.get_maintain_items のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_items", return_value=[
        {
            "maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_type_code": "01",
            "maintain_file_name_icon": "abcde00002.png",
            "maintain_interval": 10,
            "priority": 1,
            "last_maintain_implement_date": None,
            "last_maintain_du_serial_number": None,
            "last_maintain_du_last_timestamp": None,
            "last_maintain_du_last_odometer": None
        },
        {
            "maintain_item_code": "00003", "maintain_item_name": "タイヤ摩耗", "maintain_type_code": "02",
            "maintain_file_name_icon": "abcde00003.png",
            "maintain_interval": 100,
            "priority": 2,
            "last_maintain_implement_date": None,
            "last_maintain_du_serial_number": None,
            "last_maintain_du_last_timestamp": None,
            "last_maintain_du_last_odometer": None
        },
        {
            "maintain_item_code": "00009", "maintain_item_name": "定期点検", "maintain_type_code": "03",
            "maintain_file_name_icon": "abcde00009.png",
            "maintain_interval": 14,
            "priority": 9,
            "last_maintain_implement_date": None,
            "last_maintain_du_serial_number": None,
            "last_maintain_du_last_timestamp": None,
            "last_maintain_du_last_odometer": None
        }
    ])

    # repository.maintain_item_repository.get_maintain_count のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_count", return_value=0)

    # repository.rive_unit_history_repository.get_last_maintain_archive のモック化
    def get_last_maintain_archive_mock(gigya_uid: str, user_vehicle_id: int, last_maintain_du_serial_number: str, last_maintain_du_timestamp: str):
        return None
    mocker.patch("repository.drive_unit_history_repository.get_last_maintain_archive", side_effect=get_last_maintain_archive_mock)

    # repository.rive_unit_history_repository.get_after_last_maintain_archive_list のモック化
    def get_after_last_maintain_archive_list_mock(gigya_uid: str, user_vehicle_id: int, timestamp: str) -> list:
        return []
    mocker.patch("repository.drive_unit_history_repository.get_after_last_maintain_archive_list", side_effect=get_after_last_maintain_archive_list_mock)

    # repository.drive_unit_history_repository.get_oldest_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.get_oldest_drive_unit_history", return_value=None)

    reload(module)

    # 期待している返却値
    expected_value = [
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 0,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00002.png"
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 0,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00003.png"
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 60,
            "priority": 9,
            "maintain_archive": 0,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00009.png"
        }
    ]

    maintain_items = get_maintain_items('test_uid_02', 1)

    assert maintain_items == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_items_ok_07(mocker):
    """
    正常系 メンテナンス指示一覧取得
    対象データなし
    """
    # repository.maintain_item_repository.get_maintain_items のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_items", return_value=[])

    # 期待している返却値
    expected_value = []

    maintain_items = get_maintain_items('test_uid_9999', 9999)

    assert maintain_items == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_items_ng_01(mocker):
    """
    異常系 前回メンテナンス履歴有り、DU履歴なし
    """
    # repository.maintain_item_repository.get_maintain_items のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_items", return_value=[
        {
            # パターン1: メンテナンス指示種別:経過日数
            "maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_type_code": "01",
            "maintain_file_name_icon": "abcde00002.png",
            "maintain_interval": 10,
            "priority": 1,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000011",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        },
        {
            # パターン2: メンテナンス指示種別:走行距離
            "maintain_item_code": "00003", "maintain_item_name": "タイヤ摩耗", "maintain_type_code": "02",
            "maintain_file_name_icon": "abcde00003.png",
            "maintain_interval": 100,
            "priority": 2,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000011",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        },
        {
            # パターン3: メンテナンス指示種別:定期点検
            "maintain_item_code": "00009", "maintain_item_name": "定期点検", "maintain_type_code": "03",
            "maintain_file_name_icon": "abcde00009.png",
            "maintain_interval": 14,
            "priority": 9,
            "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
            "last_maintain_du_serial_number": "000022",
            "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
            "last_maintain_du_last_odometer": 5
        }
    ])

    # repository.maintain_item_repository.get_maintain_count のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_count", return_value=1)

    # repository.rive_unit_history_repository.get_last_maintain_archive のモック化
    def get_last_maintain_archive_mock(gigya_uid: str, user_vehicle_id: int, last_maintain_du_serial_number: str, last_maintain_du_timestamp: str):
        return None
    mocker.patch("repository.drive_unit_history_repository.get_last_maintain_archive", side_effect=get_last_maintain_archive_mock)

    # repository.rive_unit_history_repository.get_after_last_maintain_archive_list のモック化
    def get_after_last_maintain_archive_list_mock(gigya_uid: str, user_vehicle_id: int, timestamp: str) -> list:
        return []
    mocker.patch("repository.drive_unit_history_repository.get_after_last_maintain_archive_list", side_effect=get_after_last_maintain_archive_list_mock)

    reload(module)

    # 期待している返却値
    expected_value = [
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 3,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00002.png"
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 0,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00003.png"
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 120,
            "priority": 9,
            "maintain_archive": 3,
            "maintain_item_icon_url": cloud_front_domain_name + "icons/abcde00009.png"
        }
    ]

    maintain_items = get_maintain_items('test_uid_02', 1)

    assert maintain_items == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_explanation_ok(mocker):
    """
    正常系　ユーザ車両設定一覧取得API
    取得あり
    """
    expected_value = {
        "maintain_item_code": "00002",
        "maintain_item_name": "タイヤ空気圧",
        "maintain_item_image_url": cloud_front_domain_name + 'explanation-images/abcde00002_top.png',
        "maintain_explanations": [
            {
                "explanation_title": "前後タイヤの点検",
                "contents": [
                    {
                        "explanation_type": 1,
                        "explanation_body": "タイヤのが適切でない状態て使用をされますと、急なパンク等の危険やタイヤの路面摩擦増加により、より強い力でこぐ必要が出たり、BTの消耗が早くなるといった不利益につながる危険があります。長く安全にご使用いただくために、定期的に状態を確認してください。"
                    },
                    {
                        "explanation_type": 2,
                        "explanation_body": cloud_front_domain_name + "explanation-images/00002_01_02.png"
                    },
                    {
                        "explanation_type": 1,
                        "explanation_body": "タイヤの空気圧を点検し、不適正な場合は空気圧を調整してください。"
                    },
                    {
                        "explanation_type": 2,
                        "explanation_body": cloud_front_domain_name + "explanation-images/00002_01_04.png"
                    }
                ]
            },
            {
                "explanation_title": "前後タイヤの点検2",
                "contents": [
                    {
                        "explanation_type": 1,
                        "explanation_body": "前後のタイヤ点検_説明2"
                    }
                ]
            }
        ]
    }

    # repository.maintain_item_repository.get_maintain_explanation のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_explanation", return_value=[
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_title_code": "00201", "maintain_file_name_top": "abcde00002_top.png", "maintain_explanation_code": "20101", "explanation_title": "前後タイヤの点検", "explanation_type": 1, "explanation_body": "タイヤのが適切でない状態て使用をされますと、急なパンク等の危険やタイヤの路面摩擦増加により、より強い力でこぐ必要が出たり、BTの消耗が早くなるといった不利益につながる危険があります。長く安全にご使用いただくために、定期的に状態を確認してください。"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_title_code": "00201", "maintain_file_name_top": "abcde00002_top.png", "maintain_explanation_code": "20102", "explanation_title": "前後タイヤの点検", "explanation_type": 2, "explanation_body": "00002_01_02.png"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_title_code": "00201", "maintain_file_name_top": "abcde00002_top.png", "maintain_explanation_code": "20103", "explanation_title": "前後タイヤの点検", "explanation_type": 1, "explanation_body": "タイヤの空気圧を点検し、不適正な場合は空気圧を調整してください。"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_title_code": "00201", "maintain_file_name_top": "abcde00002_top.png", "maintain_explanation_code": "20104", "explanation_title": "前後タイヤの点検", "explanation_type": 2, "explanation_body": "00002_01_04.png"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_title_code": None, "maintain_file_name_top": "abcde00002_top.png", "maintain_explanation_code": "20105", "explanation_title": "前後タイヤの点検", "explanation_type": 1, "explanation_body": "空気圧は、YPJに乗車（体重60Kgの方）した状態での接地面の長さで簡易に判定することができます。"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧", "maintain_title_code": "00202", "maintain_file_name_top": "abcde00002_top.png", "maintain_explanation_code": "20201", "explanation_title": "前後タイヤの点検2", "explanation_type": 1, "explanation_body": "前後のタイヤ点検_説明2"},
    ])

    reload(module)

    result = get_maintain_explanation('abcd', '00002')

    assert result == expected_value


@pytest.mark.freeze_time("2022-05-14 12:34:56.789101")
def test_get_maintain_explanation_ng(mocker):
    """
    異常系　ユーザ車両設定一覧取得API
    取得なし
    """
    expected_value = {
        "maintain_item_code": "99999",
        "maintain_item_name": "",
        "maintain_item_image_url": "",
        "maintain_explanations": []
    }

    # repository.maintain_item_repository.get_maintain_explanation のモック化
    mocker.patch("repository.maintain_item_repository.get_maintain_explanation", return_value=[])

    reload(module)

    result = get_maintain_explanation('abcd', '99999')

    assert result == expected_value
