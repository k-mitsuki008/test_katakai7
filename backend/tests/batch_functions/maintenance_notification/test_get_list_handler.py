from importlib import import_module, reload
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.batch_functions.maintenance_notification.get_list_handler')
get_handler = getattr(module, 'handler')


def test_get_maintain_items_ok_01(mocker):
    """
    正常系 メンテナンス通知対象取得処理
    Mock化なし
    """

    # 期待しているレスポンスボディの値
    expected_value = {
        "maintenance_notification_list": [
            [
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00001",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00002",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00003",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00004",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00005",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00009",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                }
            ]
        ]
    }

    response = get_handler(
        {
            'version': '0',
            'id': 'abcde',
            'detail-type': 'Scheduled Event',
            'source': 'aws.events',
            'account': '889185496976',
            'time': '2022-02-22T06:00:00Z',
            'region': 'eu-west-1',
            'resources': 'abcde',
            'detail': {}
        }
    )

    assert response == expected_value


def test_get_maintain_items_ok_02(mocker):
    """
    正常系 メンテナンス通知対象取得処理
    Mock化あり
    """

    mocker.patch(
        'service.maintenance_notification_service.get_maintain_items',
        return_value={
            "maintenance_notification_list": [
                [
                    {
                        "device_token": "XXXXX",
                        "gigya_uid": "test_uid_02",
                        "maintain_item_code": "00001",
                        "user_vehicle_id": 1,
                        "vehicle_name": "ユーザー指定車両名02-01"
                    },
                    {
                        "device_token": "XXXXX",
                        "gigya_uid": "test_uid_02",
                        "maintain_item_code": "00002",
                        "user_vehicle_id": 1,
                        "vehicle_name": "ユーザー指定車両名02-01"
                    },
                    {
                        "device_token": "XXXXX",
                        "gigya_uid": "test_uid_02",
                        "maintain_item_code": "00003",
                        "user_vehicle_id": 1,
                        "vehicle_name": "ユーザー指定車両名02-01"
                    },
                    {
                        "device_token": "XXXXX",
                        "gigya_uid": "test_uid_02",
                        "maintain_item_code": "00004",
                        "user_vehicle_id": 1,
                        "vehicle_name": "ユーザー指定車両名02-01"
                    },
                    {
                        "device_token": "XXXXX",
                        "gigya_uid": "test_uid_02",
                        "maintain_item_code": "00005",
                        "user_vehicle_id": 1,
                        "vehicle_name": "ユーザー指定車両名02-01"
                    },
                    {
                        "device_token": "XXXXX",
                        "gigya_uid": "test_uid_02",
                        "maintain_item_code": "00009",
                        "user_vehicle_id": 1,
                        "vehicle_name": "ユーザー指定車両名02-01"
                    }
                ]
            ]
        }
    )

    # 期待しているレスポンスボディの値
    expected_value = {
        "maintenance_notification_list": [
            [
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00001",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00002",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00003",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00004",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00005",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                },
                {
                    "device_token": "XXXXX",
                    "gigya_uid": "test_uid_02",
                    "maintain_item_code": "00009",
                    "user_vehicle_id": 1,
                    "vehicle_name": "ユーザー指定車両名02-01"
                }
            ]
        ]
    }

    response = get_handler(
        {
            'version': '0',
            'id': 'abcde',
            'detail-type': 'Scheduled Event',
            'source': 'aws.events',
            'account': '889185496976',
            'time': '2022-02-22T06:00:00Z',
            'region': 'eu-west-1',
            'resources': 'abcde',
            'detail': {}
        }
    )

    assert response == expected_value


def test_get_maintain_items_ok_03(mocker):
    """
    正常系 メンテナンス通知対象取得処理
    データなし
    """

    mocker.patch(
        "service.maintenance_notification_service.get_maintain_items",
        return_value={"maintenance_notification_list": []}
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {"maintenance_notification_list": []}

    response = get_handler(
        {
            'version': '0',
            'id': 'abcde',
            'detail-type': 'Scheduled Event',
            'source': 'aws.events',
            'account': '889185496976',
            'time': '2022-02-22T06:00:00Z',
            'region': 'eu-west-1',
            'resources': 'abcde',
            'detail': {}
        }
    )

    assert response == expected_value
