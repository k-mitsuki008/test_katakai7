import re
import datetime
from cerberus.errors import ErrorDefinition
from common.utils.aws_utils import get_constant
from common.utils.time_utils import get_current_datetime

NUMERIC: any = ErrorDefinition(0x100, None)
ALPHANUMERIC: any = ErrorDefinition(0x101, None)
CALENDAR: any = ErrorDefinition(0x102, None)
VEHICLE_ID: any = ErrorDefinition(0x103, None)
INTEGER: any = ErrorDefinition(0x104, None)
CCU_ID: any = ErrorDefinition(0x105, None)
MAINTAIN_IMPLEMENT_DATE: any = ErrorDefinition(0x107, None)
OUT_OF_RANGE_DATE: any = ErrorDefinition(0x108, None)


# 半角数字チェック
def validate_numeric(field: any, value: any, error: any) -> None:

    regex: str = r'^[0-9]+$'

    if not isinstance(value, str):
        return

    # pylint: disable-next=superfluous-parens
    if not (re.match(regex, value) is not None):
        error(field, NUMERIC)


# 半角英数字チェック
def validate_alphanumeric(field: any, value: any, error: any) -> None:

    regex: str = r'^[a-zA-Z0-9]+$'

    if not isinstance(value, str):
        # 型エラーなら
        return

    # pylint: disable-next=superfluous-parens
    if not (re.match(regex, value) is not None):
        # 半角英数字なら専用エラーメッセージ発生。
        error(field, ALPHANUMERIC)


# 半角英数字ハイフンチェック
def validate_alphanumeric_hyphen(field: any, value: any, error: any) -> None:

    regex: str = r'^[a-zA-Z0-9-:]+$'

    if not isinstance(value, str):
        # 型エラーなら
        return

    # pylint: disable-next=superfluous-parens
    if not (re.match(regex, value) is not None):
        # 半角英数字ハイフンなら専用エラーメッセージ発生。
        error(field, ALPHANUMERIC)


# 日付チェック
def validate_calendar(field: any, value: any, error: any) -> None:

    if not isinstance(value, str):
        return

    # パース出来たらチェックOK
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')

    except ValueError:
        error(field, CALENDAR)


# 日時チェック
def validate_utc_timestamp(field: any, value: any, error: any) -> None:

    if not isinstance(value, str):
        return

    # パース出来たらチェックOK
    try:
        datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')

    except ValueError:
        error(field, CALENDAR)


# 号機番号のユーザ入力項目チェック
def validate_vehicle_id(field: any, value: any, error: any) -> None:

    regex: str = r'^[a-zA-Z0-9]{4}\-[0-9]{7}$'

    if not isinstance(value, str):
        return

    # pylint: disable-next=superfluous-parens
    if not (re.match(regex, value) is not None):
        # 指定形式以外なら専用エラーメッセージ発生。
        error(field, VEHICLE_ID, 7)


# 整数値チェック
def validate_integer(field: any, value: any, error: any) -> None:

    if not value:
        return

    if not isinstance(value, int):
        error(field, INTEGER)


# ccu_id入力チェック
def validate_ccu_id(field: any, value: any, error: any) -> None:

    if not isinstance(value, str):
        return
    if not value.startswith('0019'):
        error(field, CCU_ID)


# メンテナンス実施日チェック
def validate_maintain_implement_date(field: any, value: any, error: any) -> None:
    min_maintain_implement_date = get_constant('MAINTAIN_IMPLEMENT_DATE', code='MIN', default='2023-01-01')

    if not isinstance(value, str):
        return

    maintain_implement_datetime = None
    try:
        maintain_implement_datetime = datetime.datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        error(field, CALENDAR)

    if maintain_implement_datetime:
        # 入力可能な最大の日は現在日時+14時間（タイムゾーンの最大）
        max_maintain_implement_datetime = get_current_datetime() + datetime.timedelta(hours=14)

        # 日付で比較するのでdate型に変換
        maintain_implement_date = maintain_implement_datetime.date()
        max_maintain_implement_date = max_maintain_implement_datetime.date()

        # 未来日が入力されている場合
        if maintain_implement_date > max_maintain_implement_date:
            error(field, MAINTAIN_IMPLEMENT_DATE)

        min_maintain_implement_datetime = datetime.datetime.strptime(min_maintain_implement_date, '%Y-%m-%d')
        min_maintain_implement_date = min_maintain_implement_datetime.date()
        # 2023-01-01より前の日付が入力されている場合
        if min_maintain_implement_date > maintain_implement_date:
            error(field, OUT_OF_RANGE_DATE)


OPTIONAL: dict = {
    'required': False,
    'nullable': True,
    'empty': True
}

REQUIRED: dict = {
    'required': True,
    'empty': False
}

OPTIONAL_COMMON_STRING: dict = {
    'type': 'string',
    **OPTIONAL
}

REQUIRED_COMMON_STRING: dict = {
    'type': 'string',
    **REQUIRED
}

OPTIONAL_NUMERIC_STRING: dict = {
    **OPTIONAL_COMMON_STRING,
    'check_with': validate_numeric
}

REQUIRED_NUMERIC_STRING: dict = {
    **REQUIRED_COMMON_STRING,
    'check_with': validate_numeric
}

OPTIONAL_ALPHANUMERIC_STRING: dict = {
    **OPTIONAL_COMMON_STRING,
    'check_with': validate_alphanumeric
}

REQUIRED_ALPHANUMERIC_STRING: dict = {
    **REQUIRED_COMMON_STRING,
    'check_with': validate_alphanumeric
}

REQUIRED_CALENDAR_STRING: dict = {
    **REQUIRED_COMMON_STRING,
    'check_with': validate_calendar
}

OPTIONAL_CALENDAR_STRING: dict = {
    **OPTIONAL_COMMON_STRING,
    'check_with': validate_calendar
}

REQUIRED_TIMESTAMP_STRING: dict = {
    **REQUIRED_COMMON_STRING,
    'check_with': validate_utc_timestamp
}

OPTIONAL_TIMESTAMP_STRING: dict = {
    **OPTIONAL_COMMON_STRING,
    'check_with': validate_utc_timestamp
}

REQUIRED_VEHICLE_ID: dict = {
    **REQUIRED_COMMON_STRING,
    'check_with': validate_vehicle_id
}

REQUIRED_MAINTAIN_IMPLEMENT_DATE: dict = {
    **REQUIRED_COMMON_STRING,
    'check_with': validate_maintain_implement_date
}

OPTIONAL_VEHICLE_ID: dict = {
    'type': 'string',
    'required': False,
    'nullable': False,
    'empty': False,
    'check_with': validate_vehicle_id
}

OPTIONAL_COMMON_INT: dict = {
    'check_with': validate_integer,
    ** OPTIONAL,
}

REQUIRED_COMMON_INT: dict = {
    'check_with': validate_integer,
    ** REQUIRED,
}

OPTIONAL_COMMON_BOOLEAN: dict = {
    'type': 'boolean',
    **OPTIONAL
}

REQUIRED_COMMON_BOOLEAN: dict = {
    'type': 'boolean',
    **REQUIRED
}

OPTIONAL_COMMON_LIST: dict = {
    'type': 'list',
    **OPTIONAL
}

REQUIRED_COMMON_LIST: dict = {
    'type': 'list',
    **REQUIRED
}

OPTIONAL_COMMON_DICT: dict = {
    'type': 'dict',
    **OPTIONAL
}

REQUIRED_COMMON_DICT: dict = {
    'type': 'dict',
    **REQUIRED
}

OPTIONAL_LATITUDE: dict = {
    'type': 'float',
    **OPTIONAL,
}
OPTIONAL_LONGITUDE: dict = {
    'type': 'float',
    **OPTIONAL,
}

REQUIRED_COMMON_FLOAT: dict = {
    'type': 'float',
    **REQUIRED
}

OPTIONAL_COMMON_FLOAT: dict = {
    'type': 'float',
    **OPTIONAL
}

REQUIRED_CCU_ID: dict = {
    **REQUIRED_COMMON_STRING,
    'check_with': validate_ccu_id
}

REQUIRED_COMMON_PLACE_ID: dict = {
    **REQUIRED_COMMON_STRING,
    "minlength": 1,
}

OPTIONAL_COMMON_PLACE_ID: dict = {
    **OPTIONAL_COMMON_STRING,
    "minlength": 1,
}
