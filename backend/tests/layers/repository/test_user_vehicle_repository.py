from datetime import datetime
from importlib import import_module
import pytest

from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.user_vehicle_repository')
insert_t_user_vehicle = getattr(module, 'insert_t_user_vehicle')
update_t_user_vehicle = getattr(module, 'update_t_user_vehicle')
update_t_user_vehicle_unmanaged = getattr(module, 'update_t_user_vehicle_unmanaged')
delete_t_user_vehicle = getattr(module, 'delete_t_user_vehicle')
count_t_user_vehicle = getattr(module, 'count_t_user_vehicle')
get_user_vehicles = getattr(module, 'get_user_vehicles')
get_user_vehicle_id = getattr(module, 'get_user_vehicle_id')
get_user_vehicle_check = getattr(module, 'get_user_vehicle_check')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_insert_t_user_vehicle_ok_01():
    """
    正常系: ユーザー車両TBL INSERT
    """
    expected_value = [
        {"gigya_uid": "test_uid_01", "vehicle_id": "abcd-1234567", "peripheral_identifier": "db4bed0a-4f31-e66d-b576-2fc6a834787e", 'complete_local_name': "スイッチ01-01",  "managed_flag": True, "registered_flag": True, "unit_no": "abcd-1234567", "frame_no": None, "model_code": "abcd","vehicle_name": "ユーザー指定車両名01-01", "equipment_weight": 5, "vehicle_nickname": "ユーザー指定車両名01-01",
         "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01", "update_timestamp": None, "update_user_id": None}
    ]

    recs = {
        "gigya_uid": "test_uid_01",
        "vehicle_id": "abcd-1234567",
        "model_code": "abcd",
        "vehicle_name": "ユーザー指定車両名01-01",
        "managed_flag": True,
        "peripheral_identifier": "db4bed0a-4f31-e66d-b576-2fc6a834787e",
        "complete_local_name": "スイッチ01-01",
        "registered_flag": True,
        "unit_no": "abcd-1234567",
        "equipment_weight": 5,
        "vehicle_nickname": "ユーザー指定車両名01-01",
    }
    inserted_user_vehicle_id = insert_t_user_vehicle(**recs)

    sql: str = '''
      SELECT * FROM t_user_vehicle
      WHERE user_vehicle_id = %(user_vehicle_id)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': inserted_user_vehicle_id}
    results = execute_select_statement(sql, parameters_dict)

    expected_value[0]['user_vehicle_id'] = inserted_user_vehicle_id
    assert results == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_t_user_vehicle_ok_01():
    """
    正常系: ユーザー車両TBL UPDATE
    """
    expected_value = [
        {"user_vehicle_id": 1, "gigya_uid": "test_uid_02", "vehicle_id": "abcd-9999999", "peripheral_identifier": "switch-02-updated", 'complete_local_name': 'スイッチ02-updated', "managed_flag": False, "registered_flag": False, "unit_no": "abcd-9999999", "frame_no": None, "model_code": "abcd", "vehicle_name": "ユーザー指定車両名02-updated", "equipment_weight": 15, "vehicle_nickname": "ユーザー指定車両名02-updated",
         "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None, "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None, "etxyobi2": None, "etxyobi3": None, "etxyobi4": None, "etxyobi5": None, "delete_flag": False, "delete_timestamp": None, "delete_user_id": None, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",  "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"}
    ]

    user_vehicle_id = 1
    recs = {
        "gigya_uid": "test_uid_02",
        "vehicle_id": "abcd-9999999",
        "model_code": "abcd",
        "vehicle_name": "ユーザー指定車両名02-updated",
        "managed_flag": False,
        "peripheral_identifier": "switch-02-updated",
        "complete_local_name": "スイッチ02-updated",
        "registered_flag": False,
        "unit_no": "abcd-9999999",
        "equipment_weight": 15,
        "vehicle_nickname": "ユーザー指定車両名02-updated",
    }

    update_t_user_vehicle(user_vehicle_id, **recs)

    sql: str = '''
      SELECT * FROM t_user_vehicle
      WHERE user_vehicle_id = %(user_vehicle_id)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': user_vehicle_id}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_t_user_vehicle_ng_01():
    """
    異常系: ユーザーライドTBL UPDATE対象なし
    """
    user_vehicle_id = 141
    recs = {
        "gigya_uid": "test_uid_02",
        "vehicle_id": "abcd-12345"
    }

    results = update_t_user_vehicle(user_vehicle_id, **recs)
    assert results == 0


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_t_user_vehicle_unmanaged():
    """
    正常系: ユーザー車両TBL 管理対象フラグ、接続登録フラグ更新。
    """
    expected_value = [
        {"user_vehicle_id": 1, "gigya_uid": 'test_uid_02', "managed_flag": False, "registered_flag": False, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",  "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"},
        {"user_vehicle_id": 2, "gigya_uid": "test_uid_02", "managed_flag": False, "registered_flag": False, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",  "update_timestamp": None, "update_user_id": None},
        {"user_vehicle_id": 3, "gigya_uid": "test_uid_02", "managed_flag": False, "registered_flag": False, "insert_timestamp": datetime(2020, 5, 13, 12, 34, 56, 789000), "insert_user_id": "test_uid_01",  "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000), "update_user_id": "test_uid_02"}
    ]

    gigya_uid = 'test_uid_02'
    user_vehicle_id = 2
    recs = {
        "managed_flag": False,
        "registered_flag": False,
    }

    update_t_user_vehicle_unmanaged(gigya_uid, user_vehicle_id, **recs)

    sql: str = '''
      SELECT user_vehicle_id, gigya_uid, managed_flag, registered_flag, insert_timestamp, insert_user_id, update_timestamp, update_user_id FROM t_user_vehicle
      WHERE gigya_uid = %(gigya_uid)s
      ORDER BY user_vehicle_id;
    '''
    parameters_dict: dict = {'gigya_uid': gigya_uid}
    results = execute_select_statement(sql, parameters_dict)

    assert results == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_delete_t_user_vehicle_ok():
    """
    正常系: ユーザー車両TBL DELETE
    """
    expected_value = 1
    gigya_uid = 'test_uid_06'
    user_vehicle_id = 119
    result = delete_t_user_vehicle(gigya_uid, user_vehicle_id)
    assert result == expected_value

    sql: str = '''
      SELECT * FROM t_user_vehicle
      WHERE user_vehicle_id = %(user_vehicle_id)s;
    '''
    parameters_dict: dict = {'user_vehicle_id': user_vehicle_id}
    result = execute_select_statement(sql, parameters_dict)

    assert not result


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_get_t_user_vehicle_ok_01():
    """
    正常系: ユーザー車両TBL SELECT
    レコードあり
    """
    expected_value = {
        'user_vehicle_id': 1,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'complete_local_name': 'スイッチ-02-01',
        'equipment_weight': 5,
        "vehicle_nickname": "ユーザー指定車両名02-01",
    }

    result = get_user_vehicle_id('test_uid_02', 1)
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_get_t_user_vehicle_ok_02():
    """
    正常系: ユーザー車両TBL SELECT
    レコードなし
    """
    expected_value = None

    result = get_user_vehicle_id('test_uid_99', 9999)
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_count_t_user_vehicle():
    """
    正常系: ユーザー車両TBL SELECT COUNT(*)
    """
    expected_value = 3

    result = count_t_user_vehicle('test_uid_02')
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_get_user_vehicles_ok_01():
    """
    正常系: ユーザー車両関連TBL GIGYA_UIDでSELECT
    """
    expected_value = [
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'complete_local_name': 'スイッチ-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00002', 'maintain_item_name': 'タイヤ空気圧', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'complete_local_name': 'スイッチ-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00003', 'maintain_item_name': 'タイヤ摩耗', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'complete_local_name': 'スイッチ-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00004', 'maintain_item_name': 'チェーン動作', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'complete_local_name': 'スイッチ-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00005', 'maintain_item_name': 'ブレーキ動作、摩耗', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'complete_local_name': 'スイッチ-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00001', 'maintain_item_name': 'ホイール', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'complete_local_name': 'スイッチ-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00009', 'maintain_item_name': '定期点検', 'maintain_item_alert': True},
        {'user_vehicle_id': 2, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000002', 'vehicle_name': 'ユーザー指定車両名02-02', 'managed_flag': False, 'registered_flag': False, 'peripheral_identifier': 'switch-02-02', 'complete_local_name': 'スイッチ-02-02', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-02', 'shop_name': 'test_shop_02-2', 'shop_tel': '0809999999', 'shop_location': '東京都調布市仙川町', 'du_serial_number': None, 'du_last_odometer': None, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00001', 'maintain_item_name': 'ホイール', 'maintain_item_alert': True},
        {'user_vehicle_id': 3, 'model_code': 'zzzz', 'vehicle_id': 'zzzz-9999999', 'vehicle_name': 'ユーザー指定車両名02-03', 'managed_flag': False, 'registered_flag': False, 'peripheral_identifier': 'switch-02-03', 'complete_local_name': 'スイッチ-02-03', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-03', 'shop_name': None, 'shop_tel': None, 'shop_location': None, 'du_serial_number': None, 'du_last_odometer': None, 'contact_title': None, 'contact_text': None, 'contact_mail_address': None, 'maintain_consciousness': '02', 'maintain_item_code': '00001', 'maintain_item_name': 'ホイール', 'maintain_item_alert': True}
    ]

    result = get_user_vehicles('test_uid_02')
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_get_user_vehicles_ok_02():
    """
    正常系: ユーザー車両関連TBL GIGYA_UID+ユーザ車両IDでSELECT
    """
    expected_value = [
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'complete_local_name': 'スイッチ-02-01', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00002', 'maintain_item_name': 'タイヤ空気圧', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'complete_local_name': 'スイッチ-02-01', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00003', 'maintain_item_name': 'タイヤ摩耗', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'complete_local_name': 'スイッチ-02-01', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00004', 'maintain_item_name': 'チェーン動作', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'complete_local_name': 'スイッチ-02-01', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00005', 'maintain_item_name': 'ブレーキ動作、摩耗', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'complete_local_name': 'スイッチ-02-01', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00001', 'maintain_item_name': 'ホイール', 'maintain_item_alert': True},
        {'user_vehicle_id': 1, 'model_code': 'abcd', 'vehicle_id': 'abcd-0000001', 'vehicle_name': 'ユーザー指定車両名02-01', 'managed_flag': True, 'registered_flag': True, 'peripheral_identifier': 'switch-02-01', 'equipment_weight': 5, 'vehicle_nickname': 'ユーザー指定車両名02-01', 'shop_name': 'test_shop_02-1', 'complete_local_name': 'スイッチ-02-01', 'shop_tel': '0212345678', 'shop_location': '東京都世田谷区玉川2丁目2-2', 'du_serial_number': '000011', 'du_last_odometer': 30, 'contact_title': '問合せタイトル', 'contact_text': '問合せ本文', 'contact_mail_address': 'test@test.com', 'maintain_consciousness': '01', 'maintain_item_code': '00009', 'maintain_item_name': '定期点検', 'maintain_item_alert': True},
    ]

    result = get_user_vehicles('test_uid_02', 1)
    assert result == expected_value


def test_get_user_vehicle_check_ok_01():
    """
    正常系: ユーザー車両TBL SELECT(gigya_uid, vehicle_id)
    """
    expected_value = {
        'user_vehicle_id': 1,
        'gigya_uid': 'test_uid_02',
        'model_code': 'abcd',
        'vehicle_id': 'abcd-0000001',
        'vehicle_name': 'ユーザー指定車両名02-01',
        'managed_flag': True,
        'registered_flag': True,
        'peripheral_identifier': 'switch-02-01',
        'complete_local_name': 'スイッチ-02-01'
    }

    result = get_user_vehicle_check('test_uid_02', 'abcd-0000001')
    assert result == expected_value


def test_get_user_vehicle_check_ok_02():
    """
    正常系: ユーザー車両TBL SELECT(gigya_uid, vehicle_id)
    """
    expected_value = None

    result = get_user_vehicle_check('test_uid_98', 'abcd-9999999')
    assert result == expected_value
