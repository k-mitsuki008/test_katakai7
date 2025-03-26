from decimal import Decimal
from datetime import datetime
from importlib import import_module, reload
import pytest

from common.error.business_error import BusinessError
from common.error.not_expected_error import NotExpectedError
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.maintain_history_service')
insert_maintain_history = getattr(module, 'insert_maintain_history')
update_maintain_history = getattr(module, 'update_maintain_history')
get_maintain_history = getattr(module, 'get_maintain_history')
get_history_limit = getattr(module, 'get_history_limit')
get_maintain_history_detail = getattr(module, 'get_maintain_history_detail')
delete_maintain_history = getattr(module, 'delete_maintain_history')


def test_insert_maintain_history_ok(mocker):
    """
    正常系 メンテナンス記録登録
    """
    # repository.user_vehicle_repository.get_t_user_vehicle のモック化
    mocker.patch("repository.user_vehicle_repository.get_user_vehicle_id", return_value={"user_vehicle_id": 1, "model_code": "zzzz"})
    # repository.maintain_history_repository.insert_t_maintain_history のモック化
    insert_t_maintain_history_mock = \
        mocker.patch("repository.maintain_history_repository.insert_t_maintain_history", return_value=5678)
    # repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item
    upsert_t_user_setting_maintain_item_mock = \
        mocker.patch("repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item", return_value=False)
    reload(module)

    # 期待している返却値
    expected_value = 5678

    rec = {
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-17",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2022-10-17T12:34:56.789",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXX1",
            None,
            "XXXXX2",
        ]
    }
    updated_data = insert_maintain_history(**rec)

    assert updated_data == expected_value

    # repositoryに渡す引数確認
    insert_t_maintain_history_mock.assert_called_with(**{
        "gigya_uid": "test_uid_01",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "model_code": "zzzz",
        "maintain_implement_date": "2022-10-17",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": "2022-10-17T12:34:56.789",
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXX1,null,XXXXX2"
    })

    upsert_t_user_setting_maintain_item_mock.assert_called_with(**{
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "gigya_uid": "test_uid_01",
        "maintain_item_alert_status": Decimal('0')
    })


def test_insert_maintain_history_ng_01(mocker):
    """
    異常系 メンテナンス記録登録
    業務エラー
    """
    # repository.maintain_history_repository.get_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.get_t_maintain_history", return_value={
        'gigya_uid': 'test_uid_02',
        'maintain_cost': 3980,
        'maintain_du_last_odometer': 123,
        'maintain_du_last_timestamp': datetime(2022, 10, 11, 12, 34, 56, 789000),
        'maintain_du_serial_number': '16777215',
        'maintain_history_id': 10,
        'maintain_image_ids': [
            "XXXXX1",
            None,
            "XXXXX2",
        ],
        'maintain_implement_date': datetime(2022, 10, 17, 0, 0),
        'maintain_item_code': '00001',
        'maintain_location': '代官山モトベロ',
        'maintain_memo': '工賃: 〇〇円パーツ代: 〇〇円',
        'maintain_required_time': 120,
        'model_code': 'abcd',
        'user_vehicle_id': 1
    })
    reload(module)

    rec = {
        "gigya_uid": "test_uid_02",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-17",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2022-10-17T12:34:56.789",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXX1",
            None,
            "XXXXX2",
        ]
    }

    with pytest.raises(BusinessError):
        ret = insert_maintain_history(**rec)
        assert ret is None


def test_insert_maintain_history_ng_02(mocker):
    """
    異常系 メンテナンス記録登録
    メンテナンス履歴に１件追加できない場合の想定外エラー
    """
    # repository.maintain_history_repository.insert_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.insert_t_maintain_history",
                 return_value=None)
    reload(module)

    rec = {
        "gigya_uid": "test_uid_02",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-17",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2022-10-17T12:34:56.789",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXX1",
            None,
            "XXXXX2",
        ]
    }

    with pytest.raises(NotExpectedError):
        ret = insert_maintain_history(**rec)
        assert ret is None


def test_insert_maintain_history_ng_03(mocker):
    """
    異常系 メンテナンス記録登録
    メンテナンス通知設定項目のメンテナンス通知状態を更新できない場合の想定外エラー
    """
    # repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item
    mocker.patch("repository.user_setting_maintain_item_repository.upsert_t_user_setting_maintain_item",
                 return_value=None)
    reload(module)

    rec = {
        "gigya_uid": "test_uid_02",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-17",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2022-10-17T12:34:56.789",
        "maintain_location": "代官山モトベロ",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円",
        "maintain_image_ids": [
            "XXXXX1",
            None,
            "XXXXX2",
        ]
    }

    with pytest.raises(NotExpectedError):
        ret = insert_maintain_history(**rec)
        assert ret is None


def test_update_maintain_history_ok_01(mocker):
    """
    正常系 メンテナンス記録更新
    以下項目に値がある場合
    ・maintain_image_ids
    """
    # repository.maintain_history_repository.get_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.get_maintain_history_detail", return_value={
        "maintain_history_id": 123,
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "ホイール",
        "model_code": "abcd",
        "maintain_implement_date": datetime(2022, 10, 11, 0, 0),
        "maintain_location": "メンテナンス場所",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": datetime(2022, 10, 11, 12, 34, 56, 789000),
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
    })

    # repository.maintain_history_repository.update_t_maintain_history のモック化
    m = mocker.patch("repository.maintain_history_repository.update_t_maintain_history", return_value=1)
    reload(module)

    maintain_history_id = 123
    rec = {
        "gigya_uid": "test_uid_02",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-18",
        "maintain_location": "代官山モトベロ_UPDATE",
        "maintain_cost": 8888,
        "maintain_required_time": 888,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円_UPDATE",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        ]
    }
    update_maintain_history(maintain_history_id, **rec)

    # repositoryに渡す引数確認
    m.assert_called_with(
        123,
        "test_uid_02",
        "00001",
        1,
        **{
            "maintain_implement_date": "2022-10-18",
            "maintain_location": "代官山モトベロ_UPDATE",
            "maintain_cost": 8888,
            "maintain_required_time": 888,
            "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円_UPDATE",
            "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        }
    )


def test_update_maintain_history_ok_02(mocker):
    """
    正常系 メンテナンス記録更新
    以下項目に値がない場合
    ・maintain_image_ids
    """
    # repository.maintain_history_repository.get_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.get_maintain_history_detail", return_value={
        "maintain_history_id": 123,
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "ホイール",
        "model_code": "abcd",
        "maintain_implement_date": datetime(2022, 10, 11, 0, 0),
        "maintain_location": "メンテナンス場所",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": datetime(2022, 10, 11, 12, 34, 56, 789000),
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
    })

    # repository.maintain_history_repository.update_t_maintain_history のモック化
    m = mocker.patch("repository.maintain_history_repository.update_t_maintain_history", return_value=1)
    reload(module)

    maintain_history_id = 123
    rec = {
        "gigya_uid": "test_uid_02",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-18",
        "maintain_location": "代官山モトベロ_UPDATE",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円_UPDATE",
        "maintain_image_ids": [
            None,
            None,
            None
        ]
    }
    update_maintain_history(maintain_history_id, **rec)

    # repositoryに渡す引数確認
    m.assert_called_with(
        123,
        "test_uid_02",
        "00001",
        1,
        **{
            "maintain_implement_date": "2022-10-18",
            "maintain_location": "代官山モトベロ_UPDATE",
            "maintain_cost": 9999,
            "maintain_required_time": 999,
            "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円_UPDATE",
            "maintain_image_ids": "null,null,null"
        }
    )


def test_update_maintain_history_ok_03(mocker):
    """
    正常系 メンテナンス記録更新
    メンテナンス実施日を変更していない場合は重複チェックを行わない
    """
    # repository.maintain_history_repository.get_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.get_maintain_history_detail", return_value={
        "maintain_history_id": 123,
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "ホイール",
        "model_code": "abcd",
        "maintain_implement_date": datetime(2022, 10, 11, 0, 0),
        "maintain_location": "メンテナンス場所",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": datetime(2022, 10, 11, 12, 34, 56, 789000),
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
    })

    # repository.maintain_history_repository.update_t_maintain_history のモック化
    m = mocker.patch("repository.maintain_history_repository.update_t_maintain_history", return_value=1)

    reload(module)

    maintain_history_id = 123
    rec = {
        "gigya_uid": "test_uid_02",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-11",
        "maintain_location": "代官山モトベロ_UPDATE",
        "maintain_cost": 8888,
        "maintain_required_time": 888,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円_UPDATE",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        ]
    }
    update_maintain_history(maintain_history_id, **rec)

    # repositoryに渡す引数確認
    m.assert_called_with(
        123,
        "test_uid_02",
        "00001",
        1,
        **{
            "maintain_implement_date": "2022-10-11",
            "maintain_location": "代官山モトベロ_UPDATE",
            "maintain_cost": 8888,
            "maintain_required_time": 888,
            "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円_UPDATE",
            "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        }
    )


def test_update_maintain_history_ng(mocker):
    """
    異常系: メンテナンス記録更新 更新対象0件
    """
    # repository.maintain_history_repository.get_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.get_maintain_history_detail", return_value={
        "maintain_history_id": 123,
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "ホイール",
        "model_code": "abcd",
        "maintain_implement_date": datetime(2022, 10, 11, 0, 0),
        "maintain_location": "メンテナンス場所",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": datetime(2022, 10, 11, 12, 34, 56, 789000),
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
    })

    # repository.maintain_history_repository.update_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.update_t_maintain_history", return_value=0)
    reload(module)

    maintain_history_id = 123
    rec = {
        "gigya_uid": "test_uid_02",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-18",
        "maintain_location": "代官山モトベロ_UPDATE",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円_UPDATE",
        "maintain_image_ids": [
            None,
            None,
            None
        ]
    }

    with pytest.raises(NotExpectedError) as e:
        ret = update_maintain_history(maintain_history_id, **rec)
        assert ret is None


def test_update_maintain_history_ng_02(mocker):
    """
    異常系 メンテナンス実施日重複登録
    業務エラー
    """
    # repository.maintain_history_repository.get_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.get_maintain_history_detail", return_value={
        "maintain_history_id": 123,
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "ホイール",
        "model_code": "abcd",
        "maintain_implement_date": datetime(2022, 10, 11, 0, 0),
        "maintain_location": "メンテナンス場所",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": datetime(2022, 10, 11, 12, 34, 56, 789000),
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
    })

    # repository.maintain_history_repository.get_t_maintain_history のモック化
    mocker.patch("repository.maintain_history_repository.get_t_maintain_history", return_value={
        'gigya_uid': 'test_uid_02',
        'maintain_cost': 3980,
        'maintain_du_last_odometer': 123,
        'maintain_du_last_timestamp': datetime(2022, 10, 11, 12, 34, 56, 789000),
        'maintain_du_serial_number': '16777215',
        'maintain_history_id': 10,
        'maintain_image_ids': [
            "XXXXX1",
            None,
            "XXXXX2",
        ],
        'maintain_implement_date': datetime(2022, 10, 17, 0, 0),
        'maintain_item_code': '00001',
        'maintain_location': '代官山モトベロ',
        'maintain_memo': '工賃: 〇〇円パーツ代: 〇〇円',
        'maintain_required_time': 120,
        'model_code': 'abcd',
        'user_vehicle_id': 1
    })
    reload(module)

    maintain_history_id = 123
    rec = {
        "gigya_uid": "test_uid_02",
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-17",
        "maintain_location": "代官山モトベロ_UPDATE",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "工賃: 〇〇円パーツ代: 〇〇円_UPDATE",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        ]
    }

    with pytest.raises(BusinessError) as e:
        update_maintain_history(maintain_history_id, **rec)
    assert e.value.error_code == 'E044'


def test_get_maintain_history_ok_01(mocker):
    """
    正常系: メンテナンス履歴取得
    以下項目に値がある場合
    ・maintain_implement_date
    ・maintain_du_last_timestamp
    ・maintain_image_ids
    """

    # repository.maintain_history_repository.get_maintain_history_detail のモック化
    mocker.patch("repository.maintain_history_repository.get_maintain_history_detail", return_value={
        "maintain_history_id": 123,
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "ホイール",
        "model_code": "abcd",
        "maintain_implement_date": datetime(2022, 10, 11, 0, 0),
        "maintain_location": "メンテナンス場所",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": datetime(2022, 10, 11, 12, 34, 56, 789000),
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
    })
    reload(module)

    expected_value = {
        "maintain_history_id": 123,
        "maintain_item_code": "00001",
        "maintain_implement_date": "2022-10-11",
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": "2022-10-11T12:34:56.789Z",
        "maintain_location": "メンテナンス場所",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_image_ids": [
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
            "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3"
        ]
    }

    result = get_maintain_history('test_uid_02', 123, 1)
    assert result == expected_value


def test_get_maintain_history_ok_02(mocker):
    """
    正常系: メンテナンス履歴取得
    以下項目に値がない場合
    ・maintain_implement_date
    ・maintain_du_last_timestamp
    ・maintain_image_ids
    """

    # repository.maintain_history_repository.get_maintain_history_detail のモック化
    mocker.patch("repository.maintain_history_repository.get_maintain_history_detail", return_value={
        "maintain_history_id": 123,
        "user_vehicle_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "ホイール",
        "model_code": "abcd",
        "maintain_implement_date": None,
        "maintain_location": "メンテナンス場所",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_du_serial_number": "16777215",
        "maintain_du_last_timestamp": None,
        "maintain_du_last_odometer": 123,
        "maintain_image_ids": "null,null,null"
    })
    reload(module)

    expected_value = {
        "maintain_history_id": 123,
        "maintain_item_code": "00001",
        "maintain_implement_date": None,
        "du_serial_number": "16777215",
        "du_last_odometer": 123,
        "du_last_timestamp": None,
        "maintain_location": "メンテナンス場所",
        "maintain_cost": 9999,
        "maintain_required_time": 999,
        "maintain_memo": "メンテナンスメモ",
        "maintain_image_ids": [
            None,
            None,
            None,
        ]
    }

    result = get_maintain_history('test_uid_02', 123, 1)
    assert result == expected_value


def test_get_maintain_history_ng(mocker):
    """
    異常系: メンテナンス履歴取得 取得対象0件
    """

    # repository.maintain_history_repository.get_maintain_history_detail のモック化
    mocker.patch("repository.maintain_history_repository.get_maintain_history_detail", return_value=None)
    reload(module)

    with pytest.raises(NotExpectedError) as e:
        ret = get_maintain_history('test_uid_02', 1, 1)
        assert ret is None


def test_get_history_limit_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    メンテナンス履歴TBLデータあり
    """
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_all_count",
        return_value={'count': 13}
    )
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_limit",
        return_value=[
            {
                "maintain_history_id": 1,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": datetime(2022, 6, 23, 5, 18, 30, 310),
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 2,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": datetime(2022, 6, 15, 5, 18, 30, 310),
                "maintain_location": "ル・サイクル仙台店"
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
            "end_of_data": False,
            "maintain_histories": [
                {
                    "maintain_history_id": 1,
                    "maintain_item_code": "00001",
                    "maintain_item_name": "タイヤの空気圧",
                    "maintain_implement_date": "2022-06-23",
                    "maintain_location": "ル・サイクル仙台店"
                },
                {
                    "maintain_history_id": 2,
                    "maintain_item_code": "00001",
                    "maintain_item_name": "タイヤの空気圧",
                    "maintain_implement_date": "2022-06-15",
                    "maintain_location": "ル・サイクル仙台店"
                }
            ]
        }

    gigya_uid = "test_uid_01"
    user_vehicle_id = 1
    maintain_item_code = "00001"
    limit = 2
    offset = 0

    result_data = get_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
        maintain_item_code,
    )

    assert result_data == expected_value


def test_get_history_limit_ok_02(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    メンテナンス履歴TBL更新データなし
    """
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_all_count",
        return_value={'count': 0}
    )
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_limit",
        return_value=[]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        'end_of_data': True,
        'maintain_histories': []
    }

    gigya_uid = "test_uid_01"
    maintain_item_code = "99999"
    user_vehicle_id = 1
    limit = 5
    offset = 0

    result_data = get_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
        maintain_item_code,
    )

    assert result_data == expected_value


def test_get_history_limit_ok_03(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    メンテナンス履歴TBL最終データ
    """
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_all_count",
        return_value={'count': 3}
    )
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_limit",
        return_value=[
            {
                "maintain_history_id": 1,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": datetime(2022, 6, 23, 5, 18, 30, 310),
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 2,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": datetime(2022, 6, 15, 5, 18, 30, 310),
                "maintain_location": "ル・サイクル仙台店"
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "end_of_data": True,
        "maintain_histories": [
            {
                "maintain_history_id": 1,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-23",
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 2,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-15",
                "maintain_location": "ル・サイクル仙台店"
            }
        ]
    }

    gigya_uid = "test_uid_01"
    user_vehicle_id = 1
    maintain_item_code = "00009"
    limit = 2
    offset = 1

    result_data = get_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
        maintain_item_code,
    )

    assert result_data == expected_value


def test_get_history_limit_ok_04(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    メンテナンス履歴TBL最終データ
    """
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_all_count",
        return_value={'count': 5}
    )
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_limit",
        return_value=[
            {
                "maintain_history_id": 1,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": datetime(2022, 6, 23, 5, 18, 30, 310),
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 2,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": datetime(2022, 6, 15, 5, 18, 30, 310),
                "maintain_location": "ル・サイクル仙台店"
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "end_of_data": True,
        "maintain_histories": [
            {
                "maintain_history_id": 1,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-23",
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 2,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-15",
                "maintain_location": "ル・サイクル仙台店"
            }
        ]
    }

    gigya_uid = "test_uid_01"
    user_vehicle_id = 1
    maintain_item_code = "00002"
    limit = 2
    offset = 4

    result_data = get_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
        maintain_item_code,
    )

    assert result_data == expected_value


def test_get_history_limit_ok_05(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    メンテナンス履歴TBL
    maintain_item_code指定なし
    """
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_all_count",
        return_value={'count': 10}
    )
    # repository.maintain_history_repository.get_maintain_history_limitのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_limit",
        return_value=[
            {
                "maintain_history_id": 1,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": datetime(2022, 6, 23, 5, 18, 30, 310),
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 2,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": datetime(2022, 6, 15, 5, 18, 30, 310),
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 3,
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_implement_date": datetime(2022, 5, 31, 5, 18, 30, 310),
                "maintain_location": "代官山モトベロ"
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "end_of_data": False,
        "maintain_histories": [
            {
                "maintain_history_id": 1,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-23",
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 2,
                "maintain_item_code": "00001",
                "maintain_item_name": "タイヤの空気圧",
                "maintain_implement_date": "2022-06-15",
                "maintain_location": "ル・サイクル仙台店"
            },
            {
                "maintain_history_id": 3,
                "maintain_item_code": "00002",
                "maintain_item_name": "ブレーキ",
                "maintain_implement_date": "2022-05-31",
                "maintain_location": "代官山モトベロ"
            }
        ]
    }

    gigya_uid = "test_uid_01"
    user_vehicle_id = 1
    limit = 3
    offset = 4

    result_data = get_history_limit(
        gigya_uid,
        user_vehicle_id,
        limit,
        offset,
    )

    assert result_data == expected_value


def test_get_maintain_history_detail_ok_01(mocker):
    """
    正常系: メンテナンス履歴詳細取得
    """
    # common.utils.aws_utils import get_s3_url のモック化
    mocker.patch("common.utils.aws_utils.get_s3_url", side_effect=lambda *args, **kwargs: args)

    # repository.maintain_history_repository.get_maintain_history_detailのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_detail",
        return_value={
            "maintain_history_id": 1,
            "user_vehicle_id": 4,
            "maintain_item_code": "00001",
            "maintain_item_name": "タイヤの空気圧",
            "model_code": "abcd",
            "maintain_implement_date": datetime(2022, 6, 23, 5, 18, 30, 310),
            "maintain_location": "ル・サイクル仙台店",
            "maintain_item_file_id": "00001",
            "maintain_cost": 3980,
            "maintain_required_time": 120,
            "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
            "maintain_du_serial_number": "16777215",
            "maintain_du_last_timestamp": datetime(2022, 10, 11, 12, 34, 56, 789000),
            "maintain_du_last_odometer": 123,
            "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,null"
        }
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        "maintain_history_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "タイヤの空気圧",
        "maintain_implement_date": "2022-06-23",
        "maintain_location": "ル・サイクル仙台店",
        "maintain_item_file_id": "00001",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_urls": [
            {
                "file_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
                "s3_url": ("spvc-dev-upload-items", "test_uid_01/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1")
            },
            {
                "file_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
                "s3_url": ("spvc-dev-upload-items", "test_uid_01/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2")
            },
            {
                "file_id": None,
                "s3_url": None
            }
        ]
    }

    gigya_uid = "test_uid_01"
    maintain_history_id = 1
    user_vehicle_id = 4

    result_data = get_maintain_history_detail(
        gigya_uid,
        maintain_history_id,
        user_vehicle_id,
    )
    assert result_data == expected_value


def test_get_maintain_history_detail_ok_02(mocker):
    """
    正常系: メンテナンス履歴詳細取得
    メンテナンス実施日が取得出来なかった場合
    """
    # common.utils.aws_utils import get_s3_url のモック化
    mocker.patch("common.utils.aws_utils.get_s3_url", side_effect=lambda *args, **kwargs: args)

    # repository.maintain_history_repository.get_maintain_history_detailのモック化
    mocker.patch(
        "repository.maintain_history_repository.get_maintain_history_detail",
        return_value={
            "maintain_history_id": 1,
            "user_vehicle_id": 4,
            "maintain_item_code": "00001",
            "maintain_item_name": "タイヤの空気圧",
            "model_code": "abcd",
            "maintain_implement_date": None,
            "maintain_location": "ル・サイクル仙台店",
            "maintain_item_file_id": "00001",
            "maintain_cost": 3980,
            "maintain_required_time": 120,
            "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
            "maintain_du_serial_number": "16777215",
            "maintain_du_last_timestamp": datetime(2022, 10, 11, 12, 34, 56, 789000),
            "maintain_du_last_odometer": 123,
            "maintain_image_ids": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,null"
        }
    )

    reload(module)

    # 期待している返却値
    expected_value = {
        "maintain_history_id": 1,
        "maintain_item_code": "00001",
        "maintain_item_name": "タイヤの空気圧",
        "maintain_implement_date": None,
        "maintain_location": "ル・サイクル仙台店",
        "maintain_item_file_id": "00001",
        "maintain_cost": 3980,
        "maintain_required_time": 120,
        "maintain_memo": "工賃: 〇〇円\nパーツ代: 〇〇円",
        "maintain_image_urls": [
            {
                "file_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1",
                "s3_url": ("spvc-dev-upload-items", "test_uid_01/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1")
            },
            {
                "file_id": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2",
                "s3_url": ("spvc-dev-upload-items", "test_uid_01/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2")
            },
            {
                "file_id": None,
                "s3_url": None
            }
        ]
    }

    gigya_uid = "test_uid_01"
    maintain_history_id = 1
    user_vehicle_id = 4

    result_data = get_maintain_history_detail(
        gigya_uid,
        maintain_history_id,
        user_vehicle_id,
    )
    assert result_data == expected_value


def test_get_maintain_history_detail_ng(mocker):
    """
    異常系: メンテナンス履歴詳細取得 取得対象0件
    """

    # repository.maintain_history_repository.get_maintain_history_detail のモック化
    mocker.patch("repository.maintain_history_repository.get_maintain_history_detail", return_value=None)
    reload(module)

    with pytest.raises(NotExpectedError):
        get_maintain_history_detail('test_uid_99', 1, 9)


def test_delete_maintain_history_ok(mocker):
    """
    正常系: メンテナンス履歴削除
    """

    # repository.maintain_history_repository.delete_t_maintain_history_maintain_history_id のモック化
    mocker.patch("repository.maintain_history_repository.delete_t_maintain_history_maintain_history_id", return_value=1)
    reload(module)

    expected_value = None

    result = delete_maintain_history('test_uid_02', 1, 123)
    assert result == expected_value


def test_delete_maintain_history_ng(mocker):
    """
    異常系: メンテナンス履歴削除 削除対象0件
    """

    # repository.maintain_history_repository.delete_t_maintain_history_maintain_history_id のモック化
    mocker.patch("repository.maintain_history_repository.delete_t_maintain_history_maintain_history_id", return_value=0)
    reload(module)

    expected_value = None

    result = delete_maintain_history('test_uid_02', 9, 9)
    assert result == expected_value
