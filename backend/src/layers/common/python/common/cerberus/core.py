from abc import ABC
from common.cerberus.custom_validator import CustomValidator
from cerberus.errors import BasicErrorHandler
from cerberus.errors import ErrorList

from common.cerberus.setting.messages import messages
from common.logger import Logger
from common.utils.aws_utils import get_constant, get_message

log: any = Logger()


def validate(schema: dict, params: dict) -> list:
    """"
    schema: dict バリデーションチェック定義
    params: dict 検証対象JSON
    """
    validator: any = CustomValidator(schema, error_handler=CustomErrorHandler(schema=schema))
    is_ok: bool = validator.validate(params)
    err_list = translate_cerberus_errors(validator, schema)

    if is_ok:
        return []
    return err_list


class CustomErrorHandler(BasicErrorHandler, ABC):

    def __init__(self, schema: any = None, tree: any = None) -> None:
        self.custom_defined_schema = schema

        super(CustomErrorHandler, self).__init__(tree)
        self.messages: any = messages


def translate_cerberus_errors(validator: any, schema: any) -> list:
    errors: list = validator.errors
    keys: list = errors.keys()
    document_error_tree: list = validator.document_error_tree
    error_list: list = []

    for key in keys:
        errors = document_error_tree[key].errors
        log.info(f'ERRORS: {errors}')
        for error in errors:
            info = error.info
            if info and isinstance(info[0], ErrorList):
                # list型エラーの場合
                for inf in info[0]:
                    if inf.info:
                        tmp_inf = get_nested_error(inf.info)
                        if not isinstance(tmp_inf[0], int):
                            inf = tmp_inf[0][0]
                            if isinstance(inf.document_path[-1], str):
                                key = inf.document_path[-1]
                    # field = inf.document_path
                    field = key
                    code = hex(inf.code)  # cerberusのコード
                    value = inf.value
                    constraint = inf.constraint
                    info = error.info

                    meta = schema.get(key, {}).get('meta', None)

                    log.info(
                        f"ERROR_PARAMS: field={field}, code={code}, value={value}, constraint={constraint}, info={info}")
                    if meta:
                        common_cd = meta.get('message_cd')
                        custom_cds = meta.get('err_cds', [])
                        # err_cdsで固有エラーメッセージ指定がある場合、指定コードのメッセージを取得
                        code = code if code in custom_cds else common_cd
                        code, msg = get_error_message(key, code, constraint, value, info)
                    else:
                        # 必須項目エラーの場合
                        if code in ["0x02", "0x2"]:
                            code, msg = 'E006', get_message('E006', 'missing field')
                        else:
                            code, msg = 'E007', get_message('E007', 'validation error')

                    item = {
                        'code': code,
                        'field': field,
                        'message': msg
                    }
                    error_list.append(item)
                    break
            else:
                # dict型エラーの場合
                # ErrorValueの型が配列の場合はカンマ区切りの文字列に変更する
                if error.value and isinstance(error.value, list):
                    if len(error.value) > 0 and isinstance(error.value[0], str):
                        error.value = ','.join(error.value)

                # field = error.document_path
                field = key
                code = hex(error.code)  # cerberusのコード
                value = error.value
                constraint = error.constraint
                info = error.info

                meta = schema.get(key, {}).get('meta', None)

                log.info(
                    f"ERROR_PARAMS: field={field}, code={code}, value={value}, constraint={constraint}, info={info}")
                if meta:
                    common_cd = meta.get('message_cd')
                    custom_cds = meta.get('err_cds', [])
                    # err_cdsで固有エラーメッセージ指定がある場合、指定コードのメッセージを取得
                    code = code if code in custom_cds else common_cd
                    code, msg = get_error_message(key, code, constraint, value, info)
                else:
                    # 必須項目エラーの場合
                    if code in ["0x02", "0x2"]:
                        code, msg = 'E006', get_message('E006', 'missing field')
                    else:
                        code, msg = 'E007', get_message('E007', 'validation error')
                item = {
                    'code': code,
                    'field': field,
                    'message': msg
                }

                error_list.append(item)
                break

    return error_list


def get_nested_error(info):
    inf = info[0]
    if inf and isinstance(inf, list) and inf[0].info:
        return get_nested_error(inf[0].info)
    else:
        return info


def get_error_message(field, err_cd, constraint, value, info=None, field_name=None):
    """
    Parameters
    field: エラー項目名(英字)
    code: cerberusエラーコード
    constraint: cerberus検証ルール
    value: 設定値
    field_name: 項目名

    Returns
    message_id: エラーコード
    msg: エラーメッセージ

    """
    # messagesエラーコードからメッセージIDを取得
    message_id = messages.get(int(err_cd, 16))
    # メッセージIDからメッセージ本文を取得
    message_format = get_message(message_id, '不明なエラーです。message_id: {message_cd}}')

    # field_name指定有ならfield_nameを使用
    if field_name:
        display_field = field_name
    # field_name指定無しなら定数マスタから項目名に対応する日本語を取得（取得できなければそのまま）
    else:
        display_field = get_constant('FIELD_NAME', field, field)
    if isinstance(constraint, dict):
        constraint = ""

    display_info = ""
    if info and len(info) > 0:
        display_info = info[0]

    msg = message_format.format(field=display_field, constraint=constraint, value=value, info=display_info)
    return message_id, msg
