from importlib import import_module, reload
import pytest

from common.error.business_error import BusinessError
from common.error.not_expected_error import NotExpectedError
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.user_vehicle_service')
insert_vehicle = getattr(module, 'insert_vehicle')
update_vehicle = getattr(module, 'update_vehicle')
delete_vehicle = getattr(module, 'delete_vehicle')
get_vehicles = getattr(module, 'get_vehicles')
user_vehicle_id_is_exist = getattr(module, 'user_vehicle_id_is_exist')
get_user_vehicle = getattr(module, 'get_user_vehicle')
count_vehicle_id = getattr(module, 'count_vehicle_id')
vehicle_id_check = getattr(module, 'vehicle_id_check')


def test_insert_vehicle_ok_01(mocker):
    """
    正常系 ユーザ車両設定登録(管理対象フラグ=True、接続管理フラグ=True)
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=0)
    # repository.user_vehicle_repository.insert_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.insert_t_user_vehicle", return_value=1234)
    # repository.user_vehicle_repository.update_t_user_vehicle_unmanaged のモック化
    m = mocker.patch("repository.user_vehicle_repository.update_t_user_vehicle_unmanaged", return_value=3)
    reload(module)

    # 期待している返却値
    expected_value = 1234

    test_input = {
        "gigya_uid": "test_uid_01",
        "vehicle_id": "abcd-1234567",
        "vehicle_name": "ユーザー指定車両名01-01",
        "managed_flag": True,
        "peripheral_identifier": "db4bed0a-4f31-e66d-b576-2fc6a834787e",
        "complete_local_name": "スイッチ-01-01",
        "registered_flag": True,
        "equipment_weight": 10,
        "vehicle_nickname": "ユーザー指定車両名01-01",
    }
    updated_data = insert_vehicle(**test_input)

    assert updated_data == expected_value

    # 他の車両のmanaged_flag、registered_flagがFalseで更新していることを確認
    m.assert_called_with('test_uid_01', 1234, **{"managed_flag": False, "registered_flag": False})


def test_insert_t_user_vehicle_ok_02(mocker):
    """
    正常系 ユーザ車両設定登録(管理対象フラグ=True)
    ※
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=0)
    # repository.user_vehicle_repository.insert_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.insert_t_user_vehicle", return_value=1234)
    # repository.user_vehicle_repository.update_t_user_vehicle_unmanaged のモック化
    m = mocker.patch("repository.user_vehicle_repository.update_t_user_vehicle_unmanaged", return_value=3)
    reload(module)

    # 期待している返却値
    expected_value = 1234

    test_input = {
        "gigya_uid": "test_uid_01",
        "vehicle_id": "abcd-1234567",
        "vehicle_name": "ユーザー指定車両名01-01",
        "managed_flag": True,
    }
    updated_data = insert_vehicle(**test_input)

    assert updated_data == expected_value

    # 他の車両のmanaged_flagがFalseで更新していることを確認
    m.assert_called_with('test_uid_01', 1234, **{"managed_flag": False})


def test_insert_t_user_vehicle_ok_03(mocker):
    """
    正常系 ユーザ車両設定登録(接続登録フラグ=True)
    ※
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=0)
    # repository.user_vehicle_repository.insert_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.insert_t_user_vehicle", return_value=1234)
    # repository.user_vehicle_repository.update_t_user_vehicle_unmanaged のモック化
    m = mocker.patch("repository.user_vehicle_repository.update_t_user_vehicle_unmanaged", return_value=3)
    reload(module)

    # 期待している返却値
    expected_value = 1234

    test_input = {
        "gigya_uid": "test_uid_01",
        "vehicle_id": "abcd-1234567",
        "vehicle_name": "ユーザー指定車両名01-01",
        "peripheral_identifier": "db4bed0a-4f31-e66d-b576-2fc6a834787e",
        "complete_local_name": "スイッチ-01-01",
        "registered_flag": True,
    }
    updated_data = insert_vehicle(**test_input)

    assert updated_data == expected_value

    # 他の車両のregistered_flagがFalseで更新していることを確認
    m.assert_called_with('test_uid_01', 1234, **{"registered_flag": False})


def test_insert_vehicle_ng_02(mocker):
    """
    異常系 追加後の管理対象車両数が５件以上
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=10)
    reload(module)

    test_input = {
        "gigya_uid": "test_uid_02",
        "vehicle_id": "abcd-1234567",
        "vehicle_name": "ユーザー指定車両名01-01",
        "registered_flag": True,
    }

    # BusinessErrorのraiseを確認
    with pytest.raises(BusinessError):
        insert_vehicle(**test_input)


def test_update_vehicle_ok(mocker):
    """
    正常系: ユーザ車両TBL UPDATE
    """
    # repository.user_vehicle_repository.update_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.update_t_user_vehicle", return_value=1)
    # repository.user_vehicle_repository.update_t_user_vehicle_unmanaged のモック化
    m = mocker.patch("repository.user_vehicle_repository.update_t_user_vehicle_unmanaged", return_value=3)
    reload(module)

    # 期待している返却値
    expected_value = 1

    test_input = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
        "vehicle_id": None,
        "vehicle_name": "ユーザー指定車両名01-01",
        "managed_flag": False,
        "peripheral_identifier": "db4bed0a-4f31-e66d-b576-2fc6a834787e",
        "complete_local_name": "スイッチ-01-01",
        "registered_flag": False,
        "equipment_weight": 10,
        "vehicle_nickname": "ユーザー指定車両名01-01",
    }
    result = update_vehicle(**test_input)

    assert result == expected_value

    # 他の車両のmanaged_flag、registered_flagがFalseで更新していないことを確認
    m.assert_not_called()


def test_update_vehicle_ng(mocker):
    """
    異常系: ユーザ車両TBL UPDATE
    NotExpectedError発生時
    """
    # repository.user_vehicle_repository.update_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.update_t_user_vehicle", return_value=2)
    # repository.user_vehicle_repository.update_t_user_vehicle_unmanaged のモック化
    m = mocker.patch("repository.user_vehicle_repository.update_t_user_vehicle_unmanaged", return_value=3)
    reload(module)

    test_input = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
        "vehicle_id": "abcd-1234567",
        "equipment_weight": 10,
        "vehicle_nickname": "ユーザー指定車両名01-01",
    }

    # NotExpectedErrorのraiseを確認
    with pytest.raises(NotExpectedError):
        result = update_vehicle(**test_input)

        # 期待しているレスポンスボディの値
        expected_value = {
            "errors": {
                "code": "E001",
                "message": "システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。",
                "validationErrors": None
            }
        }

        assert result == expected_value


def test_delete_vehicle_ok_01(mocker):
    """
    正常系: ユーザ車両TBL DELETE（登録車両が1件で管理対象車両ではない車両を削除）
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=1)
    # repository.user_vehicle_repository.get_user_vehicle_id のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': False,
        'registered_flag': False,
        'peripheral_identifier': 'switch-02-01',
        'equipment_weight': 10,
        "vehicle_nickname": "ユーザー指定車両名01-01",
    })
    # repository.user_shop_purchase_repository.delete_t_user_shop_purchase のモック化
    mocker.patch("repository.user_shop_purchase_repository.delete_t_user_shop_purchase", return_value=1)
    # repository.user_setting_maintain_repository.delete_t_user_setting_maintain のモック化
    mocker.patch("repository.user_setting_maintain_repository.delete_t_user_setting_maintain", return_value=1)
    # repository.drive_unit_history_repository.delete_t_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.delete_t_drive_unit_history", return_value=1)
    # repository.maintain_history_repository.delete_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.delete_t_maintain_history", return_value=1)
    # repository.ride_history_repository.delete_t_ride_history_user_vehicle_id のモック化
    mocker.patch("repository.ride_history_repository.delete_t_ride_history_user_vehicle_id", return_value=1)
    # repository.user_vehicle_repository.delete_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.delete_t_user_vehicle", return_value=1)
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=0)
    reload(module)

    # 期待している返却値
    expected_value = 0

    test_input = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
    }
    result = delete_vehicle(**test_input)

    assert result == expected_value


def test_delete_vehicle_ok_02(mocker):
    """
    正常系: ユーザ車両TBL DELETE（登録車両が1件で管理対象車両ではない車両を削除）
    ユーザメンテナンス設定テーブル削除処理件数が0件以下の場合
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=0)
    # repository.user_vehicle_repository.get_user_vehicle_id のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': False,
        'registered_flag': False,
        'peripheral_identifier': 'switch-02-01'
    })
    # repository.user_shop_purchase_repository.delete_t_user_shop_purchase のモック化
    mocker.patch("repository.user_shop_purchase_repository.delete_t_user_shop_purchase", return_value=1)
    # repository.user_setting_maintain_repository.delete_t_user_setting_maintain のモック化
    mocker.patch("repository.user_setting_maintain_repository.delete_t_user_setting_maintain", return_value=0)
    # repository.drive_unit_history_repository.delete_t_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.delete_t_drive_unit_history", return_value=1)
    # repository.maintain_history_repository.delete_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.delete_t_maintain_history", return_value=1)
    # repository.ride_history_repository.delete_t_ride_history_user_vehicle_id のモック化
    mocker.patch("repository.ride_history_repository.delete_t_ride_history_user_vehicle_id", return_value=1)
    # repository.user_vehicle_repository.delete_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.delete_t_user_vehicle", return_value=1)
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=0)
    reload(module)

    # 期待している返却値
    expected_value = 0

    test_input = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
    }
    result = delete_vehicle(**test_input)

    assert result == expected_value


def test_delete_vehicle_ok_03(mocker):
    """
    正常系: ユーザ車両TBL DELETE（登録車両が1件で管理対象車両ではない車両を削除）
    ユーザ車両テーブル削除件数が1件ではない場合
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=1)
    # repository.user_vehicle_repository.get_user_vehicle_id のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': False,
        'registered_flag': False,
        'peripheral_identifier': 'switch-02-01'
    })
    # repository.user_shop_purchase_repository.delete_t_user_shop_purchase のモック化
    mocker.patch("repository.user_shop_purchase_repository.delete_t_user_shop_purchase", return_value=1)
    # repository.user_setting_maintain_repository.delete_t_user_setting_maintain のモック化
    mocker.patch("repository.user_setting_maintain_repository.delete_t_user_setting_maintain", return_value=1)
    # repository.drive_unit_history_repository.delete_t_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.delete_t_drive_unit_history", return_value=1)
    # repository.maintain_history_repository.delete_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.delete_t_maintain_history", return_value=1)
    # repository.ride_history_repository.delete_t_ride_history_user_vehicle_id のモック化
    mocker.patch("repository.ride_history_repository.delete_t_ride_history_user_vehicle_id", return_value=1)
    # repository.user_vehicle_repository.delete_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.delete_t_user_vehicle", return_value=2)
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=0)
    reload(module)

    # 期待している返却値
    expected_value = 0

    test_input = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
    }
    result = delete_vehicle(**test_input)

    assert result == expected_value


def test_delete_vehicle_ok_04(mocker):
    """
    正常系: ユーザ車両TBL DELETE（登録車両が2件以上で管理対象車両を削除）
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=3)
    # repository.user_vehicle_repository.get_user_vehicle_id のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01'
    })
    reload(module)

    test_input = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
    }

    with pytest.raises(BusinessError):
        delete_vehicle(**test_input)


def test_delete_vehicle_ok_05(mocker):
    """
    正常系: ユーザ車両TBL DELETE（登録車両が2件以上で管理対象車両ではない車両を削除）
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=3)
    # repository.user_vehicle_repository.get_user_vehicle_id のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': False,
        'registered_flag': False,
        'peripheral_identifier': 'switch-02-01'
    })
    # repository.user_shop_purchase_repository.delete_t_user_shop_purchase のモック化
    mocker.patch("repository.user_shop_purchase_repository.delete_t_user_shop_purchase", return_value=1)
    # repository.user_setting_maintain_repository.delete_t_user_setting_maintain のモック化
    mocker.patch("repository.user_setting_maintain_repository.delete_t_user_setting_maintain", return_value=1)
    # repository.drive_unit_history_repository.delete_t_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.delete_t_drive_unit_history", return_value=1)
    # repository.maintain_history_repository.delete_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.delete_t_maintain_history", return_value=1)
    # repository.ride_history_repository.delete_t_ride_history_user_vehicle_id のモック化
    mocker.patch("repository.ride_history_repository.delete_t_ride_history_user_vehicle_id", return_value=1)
    # repository.user_vehicle_repository.delete_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.delete_t_user_vehicle", return_value=1)
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=2)
    reload(module)

    # 期待している返却値
    expected_value = 2

    test_input = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
    }
    result = delete_vehicle(**test_input)

    assert result == expected_value


def test_delete_vehicle_ok_06(mocker):
    """
    正常系: ユーザ車両TBL DELETE（登録車両が1件で管理対象車両を削除）
    """
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=1)
    # repository.user_vehicle_repository.get_user_vehicle_id のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01'
    })
    # repository.user_shop_purchase_repository.delete_t_user_shop_purchase のモック化
    mocker.patch("repository.user_shop_purchase_repository.delete_t_user_shop_purchase", return_value=1)
    # repository.user_setting_maintain_repository.delete_t_user_setting_maintain のモック化
    mocker.patch("repository.user_setting_maintain_repository.delete_t_user_setting_maintain", return_value=1)
    # repository.drive_unit_history_repository.delete_t_drive_unit_history のモック化
    mocker.patch("repository.drive_unit_history_repository.delete_t_drive_unit_history", return_value=1)
    # repository.maintain_history_repository.delete_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.delete_t_maintain_history", return_value=1)
    # repository.ride_history_repository.delete_t_ride_history_user_vehicle_id のモック化
    mocker.patch("repository.ride_history_repository.delete_t_ride_history_user_vehicle_id", return_value=1)
    # repository.user_vehicle_repository.delete_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.delete_t_user_vehicle", return_value=1)
    # repository.user_vehicle_repository.count_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.count_t_user_vehicle", return_value=0)
    reload(module)

    # 期待している返却値
    expected_value = 0

    test_input = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 123,
    }
    result = delete_vehicle(**test_input)

    assert result == expected_value


def test_get_vehicles_ok_01(mocker):

    """
    正常系: ユーザ車両設定一覧（GIGYA_UIDのみで検索）
    """

    # tasks.repository.get_user_vehicles のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicles", return_value=[
        # 全情報あり
        {'user_vehicle_id': 1, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'complete_local_name': 'スイッチ-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'du_last_battery_rsoc': 50, 'du_last_nominal_capacity': 1000, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00002', 'maintain_item_name': 'タイヤ空気圧', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'complete_local_name': 'スイッチ-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'du_last_battery_rsoc': 50, 'du_last_nominal_capacity': 1000, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00003', 'maintain_item_name': 'タイヤ摩耗', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'complete_local_name': 'スイッチ-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'du_last_battery_rsoc': 50, 'du_last_nominal_capacity': 1000, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00004', 'maintain_item_name': 'チェーン動作', 'maintain_item_alert': True},
        # ユーザー車両+ユーザメンテナンス通知情報
        {'user_vehicle_id': 5, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-05', 'managed_flag': False, 'registered_flag': False, 'peripheral_identifier': 'switch-02-05', 'complete_local_name': 'スイッチ-02-05', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-05', 'shop_name': None, 'shop_tel': None, 'shop_location': None, 'du_serial_number': None, 'du_last_odometer': None, 'maintain_consciousness': '01', 'maintain_item_code': '00005', 'maintain_item_name': 'ブレーキ動作、摩耗', 'maintain_item_alert': False},
        {'user_vehicle_id': 5, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-05', 'managed_flag': False, 'registered_flag': False, 'peripheral_identifier': 'switch-02-05', 'complete_local_name': 'スイッチ-02-05', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-05', 'shop_name': None, 'shop_tel': None, 'shop_location': None, 'du_serial_number': None, 'du_last_odometer': None, 'maintain_consciousness': '01', 'maintain_item_code': '00006', 'maintain_item_name': '前照灯', 'maintain_item_alert': True},
    ])
    reload(module)

    expected_value = [
        {
            "user_vehicle_id": 1,
            "model_code": "zzzz",
            "vehicle_id": "zzzz-9999999",
            "vehicle_name": "ユーザー指定車両名02-01",
            "managed_flag": True,
            "registered_flag": True,
            "peripheral_identifier": "switch-02-01",
            "complete_local_name": "スイッチ-02-01",
            'equipment_weight': 5,
            "vehicle_nickname": "ユーザー指定車両名02-01",
            "purchase_shop": {
                "shop_name": "test_shop_02-1",
                "shop_tel": "0212345678",
                "shop_location": "東京都世田谷区玉川2丁目2-2"
            },
            "bluetooth": {
                "du_serial_number": "000011",
                "du_odometer": 30
            },
            "contact": {
                "contact_title": "問合せタイトル",
                "contact_text": "問合せ本文",
                "contact_mail_address": "test@test.com"
            },
            "maintain_setting": {
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
        },
        {
            "user_vehicle_id": 5,
            "model_code": "zzzz",
            "vehicle_id": "zzzz-9999999",
            "vehicle_name": "ユーザー指定車両名02-05",
            "managed_flag": False,
            "registered_flag": False,
            "peripheral_identifier": "switch-02-05",
            'complete_local_name': 'スイッチ-02-05',
            'equipment_weight': 5,
            "vehicle_nickname": "ユーザー指定車両名02-05",
            "purchase_shop": None,
            "bluetooth": None,
            "contact": None,
            "maintain_setting": {
                "maintain_consciousness": "01",
                "maintain_alerts": [
                    {
                        "maintain_item_code": "00005",
                        "maintain_item_name": "ブレーキ動作、摩耗",
                        "maintain_item_alert": False
                    },
                    {
                        "maintain_item_code": "00006",
                        "maintain_item_name": "前照灯",
                        "maintain_item_alert": True
                    }
                ]
            }
        },
    ]

    result = get_vehicles('test_uid_02')
    assert result == expected_value


def test_get_vehicles_ok_02(mocker):
    """
    正常系: ユーザ車両設定一覧（GIGYA_UID、ユーザ車両IDで検索）
    """

    # tasks.repository.get_user_vehicles のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicles", return_value=[
        # 全情報あり
        {'user_vehicle_id': 1, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'complete_local_name': 'スイッチ-02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'du_last_battery_rsoc': 50, 'du_last_nominal_capacity': 1000, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00002', 'maintain_item_name': 'タイヤ空気圧', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'complete_local_name': 'スイッチ-02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'du_last_battery_rsoc': 50, 'du_last_nominal_capacity': 1000, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00003', 'maintain_item_name': 'タイヤ摩耗', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'complete_local_name': 'スイッチ-02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'du_last_battery_rsoc': 50, 'du_last_nominal_capacity': 1000, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00004', 'maintain_item_name': 'チェーン動作', 'maintain_item_alert': True},
    ])
    reload(module)

    expected_value = [
        {
            "user_vehicle_id": 1,
            "model_code": "zzzz",
            "vehicle_id": "zzzz-9999999",
            "vehicle_name": "ユーザー指定車両名02-01",
            "managed_flag": True,
            "registered_flag": True,
            "peripheral_identifier": "switch-02-01",
            "complete_local_name": "スイッチ-02-01",
            'equipment_weight': 5,
            "vehicle_nickname": "ユーザー指定車両名02-01",
            "purchase_shop": {
                "shop_name": "test_shop_02-1",
                "shop_tel": "0212345678",
                "shop_location": "東京都世田谷区玉川2丁目2-2"
            },
            "bluetooth": {
                "du_serial_number": "000011",
                "du_odometer": 30
            },
            "contact": {
                "contact_title": "問合せタイトル",
                "contact_text": "問合せ本文",
                "contact_mail_address": "test@test.com"
            },
            "maintain_setting": {
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
        }
    ]

    result = get_vehicles('test_uid_02', 1)
    assert result == expected_value


def test_get_vehicles_ng_01(mocker):
    """
    異常系: ユーザ車両設定一覧 取得対象0件
    """

    # tasks.repository.get_user_vehicles のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicles", return_value=[])
    reload(module)

    result = get_vehicles('test_uid_02')
    [] = result


def test_get_vehicles_ng_02(mocker):
    """
    異常系: システムエラー(ユーザメンテナンス設定情報無し)
    """
    # tasks.repository.get_user_vehicles のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicles", return_value=[
        # ユーザー車両+購入店舗+bluetooth情報
        {'user_vehicle_id': 4, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-04', 'managed_flag': False, 'registered_flag': False, 'complete_local_name': 'スイッチ名称-02-04', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-04', 'peripheral_identifier': 'switch-02-04', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'maintain_consciousness': None, 'maintain_item_code': None, 'maintain_item_name': None, 'maintain_item_alert': None}
    ])
    reload(module)

    # BusinessErrorのraiseを確認
    with pytest.raises(BusinessError) as e:
        get_vehicles('test_uid_02')
        assert e.error_code == 'E042'
        assert e.params == tuple('ユーザメンテナンス設定情報')


def test_get_user_vehicle_ok(mocker):
    """
    正常系: gigya_uidとuser_vehicle_idで正誤性チェック
    """
    # tasks.repository.get_user_vehicle_id のモック化
    mocker.patch(
        "repository.user_vehicle_repository.get_user_vehicle_id",
        return_value={
            'user_vehicle_id': 1234,
            'gigya_uid': 'test_uid_02',
            'model_code': 'abcd',
            'vehicle_id': 'abcd-0000001',
            'vehicle_name': 'ユーザー指定車両名02-01',
            'managed_flag': True,
            'registered_flag': True,
            'peripheral_identifier': 'switch-02-01'
        })
    reload(module)

    expected_value = {
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01'
    }

    gigya_uid = "test_uid_02"
    user_vehicle_id = 1234

    result = get_user_vehicle(gigya_uid, user_vehicle_id)
    assert result == expected_value


def test_get_user_vehicle_ng(mocker):
    """
    異常系: 業務エラー（gigya_uidとuser_vehicle_idで正誤性不一致）
    """
    # tasks.repository.get_user_vehicle_id のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value=[])
    reload(module)

    gigya_uid = "test_uid_02"
    user_vehicle_id = 1234

    # BusinessErrorのraiseを確認
    with pytest.raises(BusinessError):
        result = get_user_vehicle(gigya_uid, user_vehicle_id)

        # 期待しているレスポンスボディの値
        expected_value = {
            "errors": {
                "code": "E042",
                'message': 'ユーザ車両IDが存在しません。',
                "validationErrors": None
            }
        }

        assert result == expected_value


def test_get_user_vehicle_id_ok(mocker):
    """
    正常系: gigya_uidとuser_vehicle_idで正誤性チェック
    """
    # tasks.repository.get_user_vehicle_id のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value={
        'user_vehicle_id': 1234,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'complete_local_name': 'スイッチ-02-01'
    })
    reload(module)

    expected_value = True

    gigya_uid = "test_uid_02"
    user_vehicle_id = 1234

    result = user_vehicle_id_is_exist(gigya_uid, user_vehicle_id)
    assert result == expected_value


def test_get_user_vehicle_id_ng(mocker):
    """
    異常系: gigya_uidとuser_vehicle_idで正誤性チェック
    """
    # tasks.repository.get_user_vehicle_id のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value=[])
    reload(module)

    gigya_uid = "test_uid_02"
    user_vehicle_id = 1234

    # BusinessErrorのraiseを確認
    with pytest.raises(BusinessError):
        user_vehicle_id_is_exist(gigya_uid, user_vehicle_id)


def test_count_vehicle_id_ok(mocker):
    """
    正常系: gigya_uidのデータ数取得
    """
    # tasks.repository.count_t_user_vehicle のモック化
    mocker.patch(
        "repository.user_vehicle_repository.count_t_user_vehicle",
        return_value={
            'count': 12,
        })
    reload(module)

    expected_value = {
        'count': 12,
    }

    gigya_uid = "test_uid_02"

    result = count_vehicle_id(gigya_uid)
    assert result == expected_value


def test_vehicle_id_check_ok_01(mocker):
    """
    正常系: 同一車両存在チェック
    """
    # tasks.repository.get_user_vehicle_check のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_check", return_value=None)
    reload(module)

    expected_value = None

    gigya_uid = "test_uid_02"
    vehicle_id = "abcd-0000001"

    result = vehicle_id_check(gigya_uid, vehicle_id)
    assert result == expected_value


def test_vehicle_id_check_ng_01(mocker):
    """
    異常系: 同一車両存在チェック
    """
    # tasks.repository.get_user_vehicle_check のモック化
    mocker.patch(
        "repository.user_vehicle_repository.get_user_vehicle_check",
        return_value={
            'user_vehicle_id': 1234,
            'gigya_uid': 'test_uid_02',
            'model_code': 'abcd',
            'vehicle_id': 'abcd-0000001',
            'vehicle_name': 'ユーザー指定車両名02-01',
            'managed_flag': True,
            'registered_flag': True,
            'peripheral_identifier': 'switch-02-01'
        })
    reload(module)

    gigya_uid = "test_uid_02"
    vehicle_id = "abcd-0000001"

    # BusinessErrorのraiseを確認
    with pytest.raises(BusinessError):
        vehicle_id_check(gigya_uid, vehicle_id)
