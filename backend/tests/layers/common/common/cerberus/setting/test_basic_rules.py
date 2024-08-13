import re
from datetime import date, datetime
from importlib import import_module
import pytest
import tests.test_utils.fixtures as fixtures
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('common.cerberus.setting.basic_rules')
validate_numeric = getattr(module, 'validate_numeric')
validate_alphanumeric = getattr(module, 'validate_alphanumeric')
validate_alphanumeric_hyphen = getattr(module, 'validate_alphanumeric_hyphen')
validate_calendar = getattr(module, 'validate_calendar')
validate_utc_timestamp = getattr(module, 'validate_utc_timestamp')
validate_vehicle_id = getattr(module, 'validate_vehicle_id')
validate_integer = getattr(module, 'validate_integer')
validate_ccu_id = getattr(module, 'validate_ccu_id')
validate_maintain_implement_date = getattr(module, 'validate_maintain_implement_date')


def test_validate_numeric_ok_01():
    """
    正常系 半角数字チェック
    """

    data = validate_numeric("field", "123", error)

    assert data is None


def test_validate_numeric_ok_02():
    """
    準正常系 半角数字チェック
    型エラーの場合はそのまま返す
    """

    data = validate_numeric("field", 123, error)

    assert data is None
    assert isinstance(123, str) is False


def test_validate_numeric_ok_03():
    """
    準正常系 半角数字チェック
    正規表現エラー
    """

    regex = r'^[0-9]+$'
    value = "123a"
    data = validate_numeric("field", value, error)

    assert data is None
    assert (re.match(regex, value) is not None) is False


def test_validate_alphanumeric_ok_01():
    """
    正常系 半角英数字チェック
    数字
    """

    data = validate_alphanumeric("field", "123", error)

    assert data is None


def test_validate_alphanumeric_ok_02():
    """
    正常系 半角英数字チェック
    小文字英
    """

    data = validate_alphanumeric("field", "abcd", error)

    assert data is None


def test_validate_alphanumeric_ok_03():
    """
    正常系 半角英数字チェック
    大文字英
    """

    data = validate_alphanumeric("field", "ABCD", error)

    assert data is None


def test_validate_alphanumeric_ok_04():
    """
    正常系 半角英数字チェック
    組み合わせ
    """

    data = validate_alphanumeric("field", "aB34", error)

    assert data is None


def test_validate_alphanumeric_ok_05():
    """
    準正常系 半角英数字チェック
    型エラーの場合はそのまま返す
    """

    data = validate_alphanumeric("field", 123, error)

    assert data is None
    assert isinstance(123, str) is False


def test_validate_alphanumeric_ok_06():
    """
    準正常系 半角英数字チェック
    正規表現エラー
    """

    regex = r'^[a-zA-Z0-9]+$'
    value = "123あ"
    data = validate_alphanumeric("field", value, error)

    assert data is None
    assert (re.match(regex, value) is not None) is False


def test_validate_alphanumeric_hyphen_ok_01():
    """
    正常系 半角英数字ハイフンチェック
    ハイフン
    """

    data = validate_alphanumeric_hyphen("field", "-", error)

    assert data is None


def test_validate_alphanumeric_hyphen_ok_02():
    """
    正常系 半角英数字ハイフンチェック
    小文字英
    """

    data = validate_alphanumeric_hyphen("field", "abcd", error)

    assert data is None


def test_validate_alphanumeric_hyphen_ok_03():
    """
    正常系 半角英数字ハイフンチェック
    大文字英
    """

    data = validate_alphanumeric_hyphen("field", "ABCD", error)

    assert data is None


def test_validate_alphanumeric_hyphen_ok_04():
    """
    正常系 半角英数字ハイフンチェック
    数字
    """

    data = validate_alphanumeric_hyphen("field", "1234", error)

    assert data is None


def test_validate_alphanumeric_hyphen_ok_05():
    """
    正常系 半角英数字ハイフンチェック
    組み合わせ
    """

    data = validate_alphanumeric_hyphen("field", "aB3-", error)

    assert data is None


def test_validate_alphanumeric_hyphen_ok_06():
    """
    準正常系 半角英数字ハイフンチェック
    型エラーの場合はそのまま返す
    """

    data = validate_alphanumeric_hyphen("field", 123, error)

    assert data is None
    assert isinstance(123, str) is False


def test_validate_alphanumeric_hyphen_ok_07():
    """
    準正常系 半角英数字ハイフンチェック
    正規表現エラー
    """

    regex = r'^[a-zA-Z0-9-:]+$'
    value = "aA0-_"
    data = validate_alphanumeric_hyphen("field", value, error)

    assert data is None
    assert (re.match(regex, value) is not None) is False


def test_validate_calendar_ok_01():
    """
    正常系 日付チェック
    """

    data = validate_calendar("field", "2023-3-29", error)

    assert data is None


def test_validate_calendar_ok_02():
    """
    準正常系 日付チェック
    型エラーの場合はそのまま返す
    """

    data = validate_calendar("field", date(2023, 3, 29), error)

    assert data is None
    assert isinstance(date(2023, 3, 29), str) is False


def test_validate_calendar_ok_03():
    """
    準正常系 日時チェック
    パースエラー
    """

    data = validate_calendar("field", "aaa", error)

    assert data is None


def test_validate_utc_timestamp_ok_01():
    """
    正常系 日時チェック
    """

    data = validate_utc_timestamp("field", "2023-03-29T16:55:05.343238Z", error)

    assert data is None


def test_validate_utc_timestamp_ok_02():
    """
    準正常系 日時チェック
    型エラーの場合はそのまま返す
    """

    data = validate_utc_timestamp("field", datetime(2020, 7, 22, 13, 37, 4, 332170), error)

    assert data is None
    assert isinstance(datetime(2020, 7, 22, 13, 37, 4, 332170), str) is False


def test_validate_utc_timestamp_ok_03():
    """
    準正常系 日時チェック
    パースエラー
    """

    data = validate_utc_timestamp("field", "aaa", error)

    assert data is None


def test_validate_vehicle_id_ok_01():
    """
    正常系 号機番号のユーザ入力項目チェック
    前半4桁小文字英
    """

    data = validate_vehicle_id("field", "abcd-1234567", error)

    assert data is None


def test_validate_vehicle_id_ok_02():
    """
    正常系 号機番号のユーザ入力項目チェック
    前半4桁大文字英
    """

    data = validate_vehicle_id("field", "ABCD-1234567", error)

    assert data is None


def test_validate_vehicle_id_ok_03():
    """
    正常系 号機番号のユーザ入力項目チェック
    前半4桁数字
    """

    data = validate_vehicle_id("field", "1234-1234567", error)

    assert data is None


def test_validate_vehicle_id_ok_04():
    """
    正常系 号機番号のユーザ入力項目チェック
    前半4桁組み合わせ
    """

    data = validate_vehicle_id("field", "aB34-1234567", error)

    assert data is None


def test_validate_vehicle_id_ok_05():
    """
    準正常系 号機番号のユーザ入力項目チェック
    型エラーの場合はそのまま返す
    """

    data = validate_vehicle_id("field", 1234567, error)

    assert data is None
    assert isinstance(1234567, str) is False


def test_validate_vehicle_id_ok_06():
    """
    準正常系 号機番号のユーザ入力項目チェック
    正規表現エラー
    """

    regex = r'^[a-zA-Z0-9]{4}\-[0-9]{7}$'
    value = "0000-000000x"
    data = validate_vehicle_id("field", value, error)

    assert data is None
    assert (re.match(regex, value) is not None) is False


def test_validate_integer_ok_01():
    """
    正常系 整数値チェック
    """

    data = validate_integer("field", 12345, error)

    assert data is None


def test_validate_integer_ok_02():
    """
    準正常系 整数値チェック
    valueがFalseの場合▼None
    """

    value = None
    data = validate_integer("field", value, error)

    assert data is None


def test_validate_integer_ok_03():
    """
    準正常系 整数値チェック
    valueがFalseの場合▼真偽値
    """

    value = False
    data = validate_integer("field", value, error)

    assert data is None


def test_validate_integer_ok_04():
    """
    準正常系 整数値チェック
    valueがFalseの場合▼文字列
    """

    value = ""
    data = validate_integer("field", value, error)

    assert data is None


def test_validate_integer_ok_05():
    """
    準正常系 整数値チェック
    valueがFalseの場合▼数値
    """

    value = 0
    data = validate_integer("field", value, error)

    assert data is None


def test_validate_integer_ok_06():
    """
    準正常系 整数値チェック
    型エラー
    """

    data = validate_integer("field", "12345", error)

    assert data is None
    assert isinstance("12345", int) is False


def test_validate_integer_ok_07():
    """
    準正常系 整数値チェック
    整数値エラー
    """
    value = 1.111
    data = validate_integer("field", value, error)

    assert data is None
    assert isinstance(value, int) is False


def test_validate_ccu_id_ok_01():
    """
    正常系 ccu_id入力チェック
    """

    data = validate_ccu_id("field", "0019XXXXXXXXXX", error)

    assert data is None


def test_validate_ccu_id_ok_02():
    """
    準正常系 ccu_id入力チェック
    型エラーの場合はそのまま返す
    """

    data = validate_ccu_id("field", int("00190000000000"), error)

    assert data is None
    assert isinstance(int("00190000000000"), str) is False


def test_validate_ccu_id_ok_03():
    """
    準正常系 ccu_id入力チェック
    書式エラー
    """
    value = "00019XXXX"
    data = validate_ccu_id("field", value, error)

    assert data is None
    assert value.startswith('0019') is False


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_validate_maintain_implement_date_ok_01():
    """
    正常系 メンテナンス実施日入力チェック
    """
    value = "2023-06-02"
    data = validate_maintain_implement_date("field", value, error)

    assert data is None


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_validate_maintain_implement_date_ok_02():
    """
    準正常系 メンテナンス実施日入力チェック
    型エラー
    """
    value = 20230601
    data = validate_maintain_implement_date("field", value, error)

    assert data is None
    assert isinstance(value, str) is False


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_validate_maintain_implement_date_ok_03():
    """
    準正常系 メンテナンス実施日入力チェック
    形式エラー
    """
    value = '2023/06/01'
    data = validate_maintain_implement_date("field", value, error)

    assert data is None
    try:
        datetime.strptime(value, '%Y-%m-%d')
    except ValueError as e:
        assert isinstance(e, ValueError)


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_validate_maintain_implement_date_ok_04():
    """
    準正常系 メンテナンス実施日入力チェック
    未来日
    """
    value = '2023-06-03'
    data = validate_maintain_implement_date("field", value, error)

    assert data is None


@pytest.mark.freeze_time("2023-06-01 12:00:00.000000")
def test_validate_maintain_implement_date_ok_05():
    """
    準正常系 メンテナンス実施日入力チェック
    2023/01/01より前
    """
    value = '2022-12-31'
    data = validate_maintain_implement_date("field", value, error)

    assert data is None


def error(field, error_item, other_item=None):
    error_list = error_item
    return error_list
