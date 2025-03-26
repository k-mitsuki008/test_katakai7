import json

from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles.delete_handler')
delete_handler = getattr(module, 'handler')


def test_handler_ok_01(mocker):
    """
    正常系 車両設定削除API
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )
    # 入力データ
    path_parameters = {
        "user_vehicle_id": "121",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/vehicles/121'
    )

    context = {}

    # device.service.get_user_vehicleのモック化
    mocker.patch(
        "service.user_vehicle_service.get_user_vehicle",
        return_value={"user_vehicle_id": 121}
    )

    # device.service.user_vehicle_id_is_existのモック化
    mocker.patch(
        "service.user_vehicle_service.user_vehicle_id_is_exist",
        return_value=True
    )

    # device.service.delete_vehicleのモック化
    mocker.patch(
        "service.user_vehicle_service.delete_vehicle",
        return_value=0
    )

    # device.service.delete_t_user_setting_rideのモック化
    mocker.patch(
        "service.user_setting_ride_service.delete_t_user_setting_ride",
        return_value=None
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 121
    }

    response = delete_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_02(mocker):
    """
    正常系 車両設定削除API
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )
    # 入力データ
    path_parameters = {
        "user_vehicle_id": "122",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_01',
        path='/vehicles/122'
    )

    context = {}

    # device.service.get_user_vehicleのモック化
    mocker.patch(
        "service.user_vehicle_service.get_user_vehicle",
        return_value={"user_vehicle_id": 122}
    )

    # device.service.user_vehicle_id_is_existのモック化
    mocker.patch(
        "service.user_vehicle_service.user_vehicle_id_is_exist",
        return_value=True
    )

    # device.service.delete_vehicleのモック化
    mocker.patch(
        "service.user_vehicle_service.delete_vehicle",
        return_value=2
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 122
    }

    response = delete_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_03():
    """
    正常系 車両設定削除API
    Mock化なし
    """
    # 入力データ
    path_parameters = {
        "user_vehicle_id": "4",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_03',
        path='/vehicles/4'
    )

    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 4,
    }

    response = delete_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ok_04():
    """
    準正常系 車両設定削除API
    登録車両が2件以上で管理対象車両を削除する場合
    """
    # 入力データ
    path_parameters = {
        "user_vehicle_id": "5",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_05',
        path='/vehicles/5'
    )

    context = {}

    response = delete_handler(event, context)
    status_code = response['statusCode']

    assert status_code == 400


def test_handler_ng_01():
    """
    準正常系 車両設定削除API
    存在しない車両IDの場合
    """
    # 入力データ
    path_parameters = {
        "user_vehicle_id": "999999999",
    }
    event = get_event(
        path_parameters=path_parameters,
        gigya_uid='test_uid_05',
        path='/vehicles/999999999'
    )

    context = {}

    response = delete_handler(event, context)
    status_code = response['statusCode']

    assert status_code == 200
