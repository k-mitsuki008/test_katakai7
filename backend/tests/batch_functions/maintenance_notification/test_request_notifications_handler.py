from datetime import datetime

import tests.test_utils.fixtures as fixtures
from importlib import import_module, reload

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.batch_functions.maintenance_notification.request_notifications_handler')
handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 メンテナンス通知バッチ処理
    mock化あり
    """
    mocker.patch(
        'service.maintenance_notification_service.create_grouping_vehicle_id',
        return_value=[
            {
                'device_token': 'XXXXX',
                'gigya_uid': 'test_uid_02',
                'user_vehicle_id': 1,
                'vehicle_name': 'ユーザー指定車両名02-01',
                'item': [
                    {
                        'maintain_item_code': '00002',
                        'maintain_item_name': 'タイヤ空気圧'
                    },
                    {
                        'maintain_item_code': '00009',
                        'maintain_item_name': '定期点検'
                    }
                ]
            }
        ]
    )

    mocker.patch(
        'service.maintenance_notification_service.create_maintain_item_code_list',
        return_value="'00002','00009'"
    )

    mocker.patch(
        'service.maintain_item_service.get_maintain_items',
        return_value=[
            {
                "maintain_item_code": "00002",
                "maintain_item_name": "タイヤ空気圧",
                "maintain_type_code": "01",
                "maintain_interval": 10,
                "priority": 1,
                "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
                "last_maintain_du_serial_number": "000011",
                "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
                "last_maintain_du_last_odometer": 5
            },
            {
                "maintain_item_code": "00009",
                "maintain_item_name": "定期点検",
                "maintain_type_code": "03",
                "maintain_interval": 14,
                "priority": 9,
                "last_maintain_implement_date": datetime(2022, 5, 11, 0, 0),
                "last_maintain_du_serial_number": "000022",
                "last_maintain_du_last_timestamp": datetime(2022, 5, 11, 12, 0),
                "last_maintain_du_last_odometer": 5
            }
        ]
    )

    mocker.patch(
        'service.maintenance_notification_service.request_notification',
        return_value={
            'device_token': 'XXXXX',
            'gigya_uid': 'test_uid_02',
            'user_vehicle_id': 1,
            'vehicle_name': 'ユーザー指定車両名02-01',
            'item': [
                {
                    'maintain_item_code': '00002',
                    'maintain_item_name': 'タイヤ空気圧'
                },
                {
                    'maintain_item_code': '00009',
                    'maintain_item_name': '定期点検'
                }
            ]
        }
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'result': True,
        'index': [
            {
                'device_token': 'XXXXX',
                'gigya_uid': 'test_uid_02',
                'user_vehicle_id': 1,
                'vehicle_name': 'ユーザー指定車両名02-01',
                'item': [
                    {
                        'maintain_item_code': '00002',
                        'maintain_item_name': 'タイヤ空気圧'
                    },
                    {
                        'maintain_item_code': '00009',
                        'maintain_item_name': '定期点検'
                    }
                ]
            }
        ]
    }

    response = handler(
        [
            {
                "device_token": "XXXXX",
                "gigya_uid": "test_uid_02",
                "maintain_item_code": "00009",
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
                "maintain_item_code": "00004",
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
                "maintain_item_code": "00002",
                "user_vehicle_id": 1,
                "vehicle_name": "ユーザー指定車両名02-01"
            },
            {
                "device_token": "XXXXX",
                "gigya_uid": "test_uid_02",
                "maintain_item_code": "00001",
                "user_vehicle_id": 1,
                "vehicle_name": "ユーザー指定車両名02-01"
            }
        ]
    )

    assert response == expected_value


def test_handler_ok_02(mocker):
    """
    正常系 メンテナンス通知バッチ処理
    mock化なし
    """
    mocker.patch(
        'service.maintenance_notification_service._get_authentication_preference',
        return_value={}
    )

    mocker.patch(
        'service.maintenance_notification_service._push_notification_execution',
        return_value={
            'device_token': 'XXXXX',
            'gigya_uid': 'test_uid_02',
            'user_vehicle_id': 1,
            'vehicle_name': 'ユーザー指定車両名02-01',
            'item': [
                {
                    'maintain_item_code': '00002',
                    'maintain_item_name': 'タイヤ空気圧'
                },
                {
                    'maintain_item_code': '00009',
                    'maintain_item_name': '定期点検'
                }
            ]
        }
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'result': True,
        'index': [
            {
                'device_token': 'XXXXX',
                'gigya_uid': 'test_uid_02',
                'user_vehicle_id': 1,
                'vehicle_name': 'ユーザー指定車両名02-01',
                'item': [
                    {
                        'maintain_item_code': '00002',
                        'maintain_item_name': 'タイヤ空気圧'
                    },
                    {
                        'maintain_item_code': '00009',
                        'maintain_item_name': '定期点検'
                    }
                ]
            }
        ]
    }

    response = handler(
        [
            {
                "device_token": "XXXXX",
                "gigya_uid": "test_uid_02",
                "maintain_item_code": "00009",
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
                "maintain_item_code": "00004",
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
                "maintain_item_code": "00002",
                "user_vehicle_id": 1,
                "vehicle_name": "ユーザー指定車両名02-01"
            },
            {
                "device_token": "XXXXX",
                "gigya_uid": "test_uid_02",
                "maintain_item_code": "00001",
                "user_vehicle_id": 1,
                "vehicle_name": "ユーザー指定車両名02-01"
            }
        ]
    )

    assert response == expected_value


def test_handler_ok_03(mocker):
    """
    正常系 メンテナンス通知バッチ処理
    通知対象のデータなし
    """
    mocker.patch(
        'service.maintenance_notification_service.request_notification',
        return_value=[]
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        'result': True,
        'index': []
    }

    response = handler(
        [
            {
                "device_token": "XXXXX",
                "gigya_uid": "test_uid_02",
                "maintain_item_code": "00009",
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
                "maintain_item_code": "00004",
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
                "maintain_item_code": "00002",
                "user_vehicle_id": 1,
                "vehicle_name": "ユーザー指定車両名02-01"
            },
            {
                "device_token": "XXXXX",
                "gigya_uid": "test_uid_02",
                "maintain_item_code": "00001",
                "user_vehicle_id": 1,
                "vehicle_name": "ユーザー指定車両名02-01"
            }
        ]
    )

    assert response == expected_value
