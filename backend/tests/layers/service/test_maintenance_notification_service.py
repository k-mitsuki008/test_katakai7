from datetime import datetime, timedelta
from importlib import import_module, reload

from firebase_admin import messaging
from firebase_admin.exceptions import FirebaseError

import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module_1 = import_module('service.maintenance_notification_service')
module_2 = import_module('service.maintain_item_service')
get_maintain_items_list = getattr(module_1, 'get_maintain_items')
create_grouping_vehicle_id = getattr(module_1, 'create_grouping_vehicle_id')
create_maintain_item_code_list = getattr(module_1, 'create_maintain_item_code_list')
request_notification = getattr(module_1, 'request_notification')
create_notification_target_list = getattr(module_1, '_create_notification_target_list')
push_notification_execution = getattr(module_1, '_push_notification_execution')
get_maintain_items = getattr(module_2, 'get_maintain_items')


class Status:
    def __init__(self, success):
        self.success = success


class SendResponses:
    def __init__(self, responses):
        self.responses = responses


def test_get_maintain_items_ok_01(mocker):
    """
    正常系 メンテナンス指示一覧取得
    データあり
    """
    # 期待しているレスポンスボディの値
    expected_value = {
        'maintenance_notification_list': [
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

    result = get_maintain_items_list()
    assert result == expected_value


def test_get_maintain_items_ok_02(mocker):
    """
    正常系 メンテナンス指示一覧取得
    データなし
    """
    mocker.patch(
        "repository.user_setting_maintain_item_repository.get_t_user_setting_maintain_item",
        return_value=[]
    )

    reload(module_1)

    expected_value = {'maintenance_notification_list': []}

    data = get_maintain_items_list()

    assert data == expected_value


def test_get_maintain_items_ok_03(mocker):
    """
    正常系 メンテナンス指示一覧取得
    データが500件の場合
    """

    data_list = []
    # 検証用のデータを500件作成する
    for i in range(500):
        get_data = {
            "device_token": "XXXXX",
            "gigya_uid": "test_uid_02",
            "maintain_item_code": "00001",
            "user_vehicle_id": i + 1,
            "vehicle_name": f"ユーザー指定車両名02-0{i + 1}"
        }
        data_list.append(get_data)

    mocker.patch(
        "repository.user_setting_maintain_item_repository.get_t_user_setting_maintain_item",
        return_value=data_list
    )

    reload(module_1)

    expected_value = {'maintenance_notification_list': [data_list]}

    data = get_maintain_items_list()

    assert data == expected_value


def test_get_maintain_items_ok_04(mocker):
    """
    正常系 メンテナンス指示一覧取得
    データが501件以上の場合分割する
    """

    data_list = []
    # 検証用のデータを501件以上作成する
    for i in range(502):
        get_data = {
            "device_token": "XXXXX",
            "gigya_uid": "test_uid_02",
            "maintain_item_code": "00001",
            "user_vehicle_id": i + 1,
            "vehicle_name": f"ユーザー指定車両名02-0{i + 1}"
        }
        data_list.append(get_data)

    mocker.patch(
        "repository.user_setting_maintain_item_repository.get_t_user_setting_maintain_item",
        return_value=data_list
    )

    reload(module_1)
    return_list_1 = data_list[0:500]  # 最初の500件
    return_list_2 = data_list[-2:]  # 分割したデータの2件

    expected_value = {'maintenance_notification_list': [return_list_1, return_list_2]}

    data = get_maintain_items_list()

    assert data == expected_value


def test_create_grouping_vehicle_id_ok(mocker):
    """
    正常系 vehicle_idごとにデータをグルーピングする
    """

    notification_list = [
        {
            "device_token": "車両トークン",
            "gigya_uid": "gigya_uid",
            "user_vehicle_id": "1",
            "maintain_item_code": "部品コード1",
            "vehicle_name": "バイク名",
        },
        {
            "device_token": "車両トークン",
            "gigya_uid": "gigya_uid",
            "user_vehicle_id": "1",
            "maintain_item_code": "部品コード2",
            "vehicle_name": "バイク名",
        },
        {
            "device_token": "車両トークン",
            "gigya_uid": "gigya_uid",
            "user_vehicle_id": "2",
            "maintain_item_code": "部品コード3",
            "vehicle_name": "バイク名",
        }
    ]

    # 期待しているレスポンスボディの値
    expected_value = [
        {
            'device_token': '車両トークン',
            'gigya_uid': 'gigya_uid',
            'user_vehicle_id': '1',
            'vehicle_name': 'バイク名',
            'item': [
                {
                    'maintain_item_code': '部品コード1'
                },
                {
                    'maintain_item_code': '部品コード2'
                }
            ]
        },
        {
            'device_token': '車両トークン',
            'gigya_uid': 'gigya_uid',
            'user_vehicle_id': '2',
            'vehicle_name': 'バイク名',
            'item': [
                {
                    'maintain_item_code': '部品コード3'
                }
            ]
        }
    ]

    data = create_grouping_vehicle_id(notification_list)

    assert data == expected_value


def test_create_maintain_item_code_list_ok_01(mocker):
    """
    正常系 maintain_item_codeをリスト化する
    2件以上の場合
    """

    items = {
        'device_token': '車両トークン',
        'gigya_uid': 'gigya_uid',
        'user_vehicle_id': '1',
        'vehicle_name': 'バイク名',
        'item': [
            {
                'maintain_item_code': "1"
            },
            {
                'maintain_item_code': "2"
            }
        ]
    }

    # 期待しているレスポンスボディの値
    expected_value = "'1','2'"

    data = create_maintain_item_code_list(items)

    assert data == expected_value


def test_create_maintain_item_code_list_ok_02(mocker):
    """
    正常系 maintain_item_codeをリスト化する
    1件の場合
    """

    items = {
        'device_token': '車両トークン',
        'gigya_uid': 'gigya_uid',
        'user_vehicle_id': '1',
        'vehicle_name': 'バイク名',
        'item': [
            {
                'maintain_item_code': "1"
            }
        ]
    }

    # 期待しているレスポンスボディの値
    expected_value = "'1'"

    data = create_maintain_item_code_list(items)

    assert data == expected_value


def test_get_maintain_items_ok(mocker):
    """
    正常系 vehicle_idとitem_codeに紐づくメンテナンス指示一覧を取得する
    """

    gigya_uid = "test_uid_02"
    user_vehicle_id = 1
    item_code_list = "'00001','00004'"

    # 期待しているレスポンスボディの値
    expected_value = [
        {
            "maintain_item_code": "00004",
            "maintain_item_name": "チェーン動作",
            "maintain_type_code": "02",
            "maintain_interval": 101,
            "priority": 3,
            "maintain_archive": 26
        },
        {
            "maintain_item_code": "00001",
            "maintain_item_name": "ホイール",
            "maintain_type_code": "02",
            "maintain_interval": 103,
            "priority": 5,
            "maintain_archive": 0
        }
    ]

    data = get_maintain_items(gigya_uid, user_vehicle_id, item_code_list)

    assert data == expected_value


def test_request_notification_ok_01(mocker):
    """
    正常系 メンテナンス通知実行
    通知対象あり
    """
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_APPLICATION_CREDENTIALS': '{"test":"test"}'}
    )

    # firebase_admin.credentialsのmock化
    mocker.patch(
        'firebase_admin.credentials.Certificate',
        return_value='{"test":"test"}'
    )

    # firebase_admin.initialize_appのmock化
    mocker.patch(
        'firebase_admin.initialize_app',
        return_value='{"test":"test"}'
    )

    # firebase_admin.messagingのmock化
    mocker.patch(
        'firebase_admin.messaging',
        return_value='{"test":"test"}'
    )

    mocker.patch(
        'firebase_admin.messaging.send_all',
        return_value=SendResponses([Status(True), Status(True)])
    )

    reload(module_1)

    maintain_item_list = [
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 302
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 25
        },
        {
            "maintain_item_code": "00004",
            "maintain_item_name": "チェーン動作",
            "maintain_type_code": "02",
            "maintain_interval": 101,
            "priority": 3,
            "maintain_archive": 26
        },
        {
            "maintain_item_code": "00005",
            "maintain_item_name": "ブレーキ動作、摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 102,
            "priority": 4,
            "maintain_archive": 30
        },
        {
            "maintain_item_code": "00001",
            "maintain_item_name": "ホイール",
            "maintain_type_code": "02",
            "maintain_interval": 103,
            "priority": 5,
            "maintain_archive": 0
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 123,
            "priority": 9,
            "maintain_archive": 302
        }
    ]
    notification = {
        'device_token': 'XXXXX',
        'gigya_uid': 'test_uid_02',
        'user_vehicle_id': 1,
        'vehicle_name': 'ユーザー指定車両名02-01',
        'item': [
            {
                'maintain_item_code': "00001"
            },
            {
                'maintain_item_code': "00002"
            },
            {
                'maintain_item_code': "00003"
            },
            {
                'maintain_item_code': "00004"
            },
            {
                'maintain_item_code': "00005"
            },
            {
                'maintain_item_code': "00009"
            },
        ]
    }

    # 期待しているレスポンスボディの値
    expected_value = {
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

    data = request_notification(notification, maintain_item_list)

    assert data == expected_value


def test_request_notification_ok_02(mocker):
    """
    正常系 メンテナンス通知実行
    通知対象なし
    """
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_APPLICATION_CREDENTIALS': '{"test":"test"}'}
    )

    # firebase_admin.credentialsのmock化
    mocker.patch(
        'firebase_admin.credentials.Certificate',
        return_value='{"test":"test"}'
    )

    # firebase_admin.initialize_appのmock化
    mocker.patch(
        'firebase_admin.initialize_app',
        return_value='{"test":"test"}'
    )

    reload(module_1)

    maintain_item_list = [
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 2
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 25
        },
        {
            "maintain_item_code": "00004",
            "maintain_item_name": "チェーン動作",
            "maintain_type_code": "02",
            "maintain_interval": 101,
            "priority": 3,
            "maintain_archive": 26
        },
        {
            "maintain_item_code": "00005",
            "maintain_item_name": "ブレーキ動作、摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 102,
            "priority": 4,
            "maintain_archive": 30
        },
        {
            "maintain_item_code": "00001",
            "maintain_item_name": "ホイール",
            "maintain_type_code": "02",
            "maintain_interval": 103,
            "priority": 5,
            "maintain_archive": 0
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 123,
            "priority": 9,
            "maintain_archive": 2
        }
    ]

    notification = {
        'device_token': 'XXXXX',
        'gigya_uid': 'test_uid_02',
        'user_vehicle_id': 1,
        'vehicle_name': 'ユーザー指定車両名02-01',
        'item': [
            {
                'maintain_item_code': "00001"
            },
            {
                'maintain_item_code': "00002"
            },
            {
                'maintain_item_code': "00003"
            },
            {
                'maintain_item_code': "00004"
            },
            {
                'maintain_item_code': "00005"
            },
            {
                'maintain_item_code': "00009"
            },
        ]
    }

    # 期待しているレスポンスボディの値
    expected_value = []

    data = request_notification(notification, maintain_item_list)

    assert data == expected_value


def test_create_notification_target_list_ok(mocker):
    """
    正常系 通知対象のリストを生成する
    """
    maintain_item_list = [
        {
            "maintain_item_code": "00002",
            "maintain_item_name": "タイヤ空気圧",
            "maintain_type_code": "01",
            "maintain_interval": 10,
            "priority": 1,
            "maintain_archive": 302
        },
        {
            "maintain_item_code": "00003",
            "maintain_item_name": "タイヤ摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 100,
            "priority": 2,
            "maintain_archive": 25
        },
        {
            "maintain_item_code": "00004",
            "maintain_item_name": "チェーン動作",
            "maintain_type_code": "02",
            "maintain_interval": 101,
            "priority": 3,
            "maintain_archive": 26
        },
        {
            "maintain_item_code": "00005",
            "maintain_item_name": "ブレーキ動作、摩耗",
            "maintain_type_code": "02",
            "maintain_interval": 102,
            "priority": 4,
            "maintain_archive": 30
        },
        {
            "maintain_item_code": "00001",
            "maintain_item_name": "ホイール",
            "maintain_type_code": "02",
            "maintain_interval": 103,
            "priority": 5,
            "maintain_archive": 0
        },
        {
            "maintain_item_code": "00009",
            "maintain_item_name": "定期点検",
            "maintain_type_code": "01",
            "maintain_interval": 123,
            "priority": 9,
            "maintain_archive": 302
        }
    ]
    notification = {
        'device_token': 'XXXXX',
        'gigya_uid': 'test_uid_02',
        'user_vehicle_id': 1,
        'vehicle_name': 'ユーザー指定車両名02-01',
        'item': [
            {
                'maintain_item_code': "00001"
            },
            {
                'maintain_item_code': "00002"
            },
            {
                'maintain_item_code': "00003"
            },
            {
                'maintain_item_code': "00004"
            },
            {
                'maintain_item_code': "00005"
            },
            {
                'maintain_item_code': "00009"
            },
        ]
    }

    expected_value = {
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

    data = create_notification_target_list(notification, maintain_item_list)

    assert data == expected_value


def test_push_notification_execution_ok_01(mocker):
    """
    正常系 push通知を実行する
    全て成功
    """
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_APPLICATION_CREDENTIALS': '{"test":"test"}'}
    )

    # firebase_admin.credentialsのmock化
    mocker.patch(
        'firebase_admin.credentials.Certificate',
        return_value='{"test":"test"}'
    )

    # firebase_admin.initialize_appのmock化
    mocker.patch(
        'firebase_admin.initialize_app',
        return_value='{"test":"test"}'
    )

    # firebase_admin.messagingのmock化
    mocker.patch(
        'firebase_admin.messaging.Message',
        return_value='{"test":"test"}'
    )

    m = mocker.patch(
        'firebase_admin.messaging.send_all',
        return_value=SendResponses([Status(True), Status(True)])
    )
    reload(module_1)

    expected_value = {
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

    data = push_notification_execution(expected_value)

    assert data == expected_value
    m.assert_called_with(['{"test":"test"}', '{"test":"test"}'],)


def test_push_notification_execution_ok_02(mocker):
    """
    正常系 push通知を実行する
    送信失敗あり
    """
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_APPLICATION_CREDENTIALS': '{"test":"test"}'}
    )

    # firebase_admin.credentialsのmock化
    mocker.patch(
        'firebase_admin.credentials.Certificate',
        return_value='{"test":"test"}'
    )

    # firebase_admin.initialize_appのmock化
    mocker.patch(
        'firebase_admin.initialize_app',
        return_value='{"test":"test"}'
    )

    # firebase_admin.messagingのmock化
    mocker.patch(
        'firebase_admin.messaging',
        return_value='{"test":"test"}'
    )

    mocker.patch(
        'firebase_admin.messaging.send_all',
        return_value=SendResponses([Status(True), Status(False)])
    )
    reload(module_1)

    notification_target_list = {
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

    expected_value = {
        'device_token': 'XXXXX',
        'gigya_uid': 'test_uid_02',
        'user_vehicle_id': 1,
        'vehicle_name': 'ユーザー指定車両名02-01',
        'item': [
            {
                'maintain_item_code': '00002',
                'maintain_item_name': 'タイヤ空気圧'
            }
        ]
    }

    data = push_notification_execution(notification_target_list)

    assert data == expected_value


def test_push_notification_execution_ng_01(mocker):
    """
    正常系 push通知を実行する
    通知エラー
    """
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_APPLICATION_CREDENTIALS': '{"test":"test"}'}
    )

    # firebase_admin.credentialsのmock化
    mocker.patch(
        'firebase_admin.credentials.Certificate',
        return_value='{"test":"test"}'
    )

    # firebase_admin.initialize_appのmock化
    mocker.patch(
        'firebase_admin.initialize_app',
        return_value='{"test":"test"}'
    )

    # firebase_admin.messagingのmock化
    mocker.patch(
        'firebase_admin.messaging',
        return_value='{"test":"test"}'
    )

    mocker.patch(
        'firebase_admin.messaging.send_all',
        side_effect=FirebaseError(code="test", message="test")
    )
    reload(module_1)

    notification_target_list = {
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

    expected_value = {
        'device_token': 'XXXXX',
        'gigya_uid': 'test_uid_02',
        'user_vehicle_id': 1,
        'vehicle_name': 'ユーザー指定車両名02-01',
        'item': []
    }

    data = push_notification_execution(notification_target_list)

    assert data == expected_value
