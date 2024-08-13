from datetime import datetime
from importlib import import_module
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.maintain_item_repository')
get_maintain_items = getattr(module, 'get_maintain_items')
get_maintain_explanation = getattr(module, 'get_maintain_explanation')
get_maintain_count = getattr(module, 'get_maintain_count')


def test_get_maintain_items_ok_01():
    """
    正常系: メンテナンス指示一覧取得
    メンテナンス指示一覧取得APIから実行した場合
    """
    expected_value = [
        {'maintain_item_code': '00002', 'maintain_item_name': 'タイヤ空気圧', 'maintain_type_code': '01',
         "maintain_file_name_icon": "abcde00002.png",
         'maintain_interval': 10, 'priority': 1, 'last_maintain_implement_date': datetime(2022, 5, 11, 0, 0),
         'last_maintain_du_serial_number': '000011',
         'last_maintain_du_last_timestamp': datetime(2022, 5, 11, 12, 0, 0, 000000),
         'last_maintain_du_last_odometer': 5},
        {'maintain_item_code': '00003', 'maintain_item_name': 'タイヤ摩耗', 'maintain_type_code': '02',
         "maintain_file_name_icon": "abcde00003.png",
         'maintain_interval': 100, 'priority': 2, 'last_maintain_implement_date': datetime(2022, 5, 11, 0, 0),
         'last_maintain_du_serial_number': '000011',
         'last_maintain_du_last_timestamp': datetime(2022, 5, 11, 12, 0, 0, 000000),
         'last_maintain_du_last_odometer': 5},
        {'maintain_item_code': '00004', 'maintain_item_name': 'チェーン動作', 'maintain_type_code': '02',
         "maintain_file_name_icon": "abcde00004.png",
         'maintain_interval': 101, 'priority': 3, 'last_maintain_implement_date': datetime(2022, 5, 12, 0, 0),
         'last_maintain_du_serial_number': '000022',
         'last_maintain_du_last_timestamp': datetime(2022, 5, 12, 20, 0, 0, 000000),
         'last_maintain_du_last_odometer': 4},
        {'maintain_item_code': '00005', 'maintain_item_name': 'ブレーキ動作、摩耗', 'maintain_type_code': '02',
         "maintain_file_name_icon": "abcde00005.png",
         'maintain_interval': 102, 'priority': 4, 'last_maintain_implement_date': None,
         'last_maintain_du_serial_number': None, 'last_maintain_du_last_timestamp': None,
         'last_maintain_du_last_odometer': None},
        {'maintain_item_code': '00001', 'maintain_item_name': 'ホイール', 'maintain_type_code': '02',
         "maintain_file_name_icon": "abcde00001.png",
         'maintain_interval': 103, 'priority': 5, 'last_maintain_implement_date': datetime(2022, 10, 11, 0, 0),
         'last_maintain_du_serial_number': '16777215',
         'last_maintain_du_last_timestamp': datetime(2022, 10, 11, 12, 34, 56, 789000),
         'last_maintain_du_last_odometer': 123},
        {'maintain_item_code': '00009', 'maintain_item_name': '定期点検', 'maintain_type_code': '03',
         "maintain_file_name_icon": "abcde00009.png",
         'maintain_interval': 14, 'priority': 9, 'last_maintain_implement_date': datetime(2023, 12, 31, 0, 0),
         'last_maintain_du_serial_number': '000022',
         'last_maintain_du_last_timestamp': datetime(2022, 5, 11, 12, 0, 0, 000000),
         'last_maintain_du_last_odometer': 5}
    ]

    result = get_maintain_items(1)
    assert result == expected_value


def test_get_maintain_items_ok_02():
    """
    正常系: メンテナンス指示一覧取得
    メンテナンス通知処理から実行した場合
    取得対象が2件以上
    """
    expected_value = [
        {'maintain_item_code': '00003', 'maintain_item_name': 'タイヤ摩耗', 'maintain_type_code': '02',
         "maintain_file_name_icon": "abcde00003.png",
         'maintain_interval': 100, 'priority': 2, 'last_maintain_implement_date': datetime(2022, 5, 11, 0, 0),
         'last_maintain_du_serial_number': '000011',
         'last_maintain_du_last_timestamp': datetime(2022, 5, 11, 12, 0, 0, 000000),
         'last_maintain_du_last_odometer': 5},
        {'maintain_item_code': '00001', 'maintain_item_name': 'ホイール', 'maintain_type_code': '02',
         "maintain_file_name_icon": "abcde00001.png",
         'maintain_interval': 103, 'priority': 5, 'last_maintain_implement_date': datetime(2022, 10, 11, 0, 0),
         'last_maintain_du_serial_number': '16777215',
         'last_maintain_du_last_timestamp': datetime(2022, 10, 11, 12, 34, 56, 789000),
         'last_maintain_du_last_odometer': 123}
    ]

    maintain_item_code = "'00001', '00003'"

    result = get_maintain_items(1, maintain_item_code)
    assert result == expected_value


def test_get_maintain_items_ok_03():
    """
    正常系: メンテナンス指示一覧取得
    メンテナンス通知処理から実行した場合
    取得対象が1件
    """
    expected_value = [
        {'maintain_item_code': '00003', 'maintain_item_name': 'タイヤ摩耗', 'maintain_type_code': '02',
         "maintain_file_name_icon": "abcde00003.png",
         'maintain_interval': 100, 'priority': 2, 'last_maintain_implement_date': datetime(2022, 5, 11, 0, 0),
         'last_maintain_du_serial_number': '000011',
         'last_maintain_du_last_timestamp': datetime(2022, 5, 11, 12, 0, 0, 000000),
         'last_maintain_du_last_odometer': 5
         }
    ]

    maintain_item_code = "'00003'"

    result = get_maintain_items(1, maintain_item_code)
    assert result == expected_value


def test_get_maintain_items_ng():
    """
    異常系: メンテナンス指示一覧取得 対象0件
    """
    expected_value = []

    result = get_maintain_items(9999)
    assert result == expected_value


def test_get_maintain_count_ok_01():
    """
    正常系: メンテナンス実施回数を取得
    メンテナンス実施履歴あり
    """
    expected_value = 2

    gigya_uid = "test_uid_02"
    user_vehicle_id = 1
    maintain_item_code = "00002"

    result = get_maintain_count(gigya_uid, user_vehicle_id, maintain_item_code)
    assert result == expected_value


def test_get_maintain_count_ok_02():
    """
    正常系: メンテナンス実施回数を取得
    メンテナンス実施履歴なし
    """
    expected_value = 0

    gigya_uid = "test_uid_99"
    user_vehicle_id = 99999
    maintain_item_code = "00001"

    result = get_maintain_count(gigya_uid, user_vehicle_id, maintain_item_code)
    assert result == expected_value


def test_get_maintain_explanation_ok():
    """
    正常系: メンテナンス説明取得
    """
    expected_value = [
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧",
         "maintain_file_name_top": "abcde00002_top.png", "maintain_title_code": "001",
         "maintain_explanation_code": "001", "explanation_title": "前後タイヤの点検", "explanation_type": 1,
         "explanation_body": "タイヤのが適切でない状態て使用をされますと、急なパンク等の危険やタイヤの路面摩擦増加により、より強い力でこぐ必要が出たり、BTの消耗が早くなるといった不利益につながる危険があります。長く安全にご使用いただくために、定期的に状態を確認してください。"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧",
         "maintain_file_name_top": "abcde00002_top.png", "maintain_title_code": "001",
         "maintain_explanation_code": "002", "explanation_title": "前後タイヤの点検", "explanation_type": 2,
         "explanation_body": "00002_01_02.png"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧",
         "maintain_file_name_top": "abcde00002_top.png", "maintain_title_code": "001",
         "maintain_explanation_code": "003", "explanation_title": "前後タイヤの点検", "explanation_type": 1,
         "explanation_body": "タイヤの空気圧を点検し、不適正な場合は空気圧を調整してください。"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧",
         "maintain_file_name_top": "abcde00002_top.png", "maintain_title_code": "001",
         "maintain_explanation_code": "004", "explanation_title": "前後タイヤの点検", "explanation_type": 2,
         "explanation_body": "00002_01_04.png"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧",
         "maintain_file_name_top": "abcde00002_top.png", "maintain_title_code": "001",
         "maintain_explanation_code": "005", "explanation_title": "前後タイヤの点検", "explanation_type": 1,
         "explanation_body": "空気圧は、YPJに乗車（体重60Kgの方）した状態での接地面の長さで簡易に判定することができます。"},
        {"maintain_item_code": "00002", "maintain_item_name": "タイヤ空気圧",
         "maintain_file_name_top": "abcde00002_top.png", "maintain_title_code": "002",
         "maintain_explanation_code": "001", "explanation_title": "前後タイヤの点検2", "explanation_type": 1,
         "explanation_body": "前後のタイヤ点検_説明2"},
    ]

    result = get_maintain_explanation('abcd', '00002')
    assert result == expected_value


def test_get_maintain_explanation_ng():
    """
    異常系: メンテナンス説明取得 対象0件
    """
    expected_value = []

    result = get_maintain_explanation('abcd', '99999')
    assert result == expected_value
