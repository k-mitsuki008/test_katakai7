from importlib import import_module
import tests.test_utils.fixtures as fixtures

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('common.cerberus.core')
validate = getattr(module, 'validate')
translate_cerberus_errors = getattr(module, 'translate_cerberus_errors')
get_error_message = getattr(module, 'get_error_message')
CustomErrorHandler = getattr(module, 'CustomErrorHandler')


def test_validate_ok():
    """
    正常系
    """
    schema = {
        'key': {
            'type': 'string',
            'required': True,
            'empty': False
        }
    }
    params = {'key': 'value'}
    result = validate(schema, params)
    assert result == []


def test_validate_error_dict_01():
    """
    dict型エラーの場合
    必須エラー
    """
    schema = {
        'key': {
            'type': 'string',
            'required': True,
            'empty': False
        }
    }
    params = {}
    result = validate(schema, params)
    expected = [{'code': 'E006', 'field': 'key', 'message': 'missing field'}]
    assert result == expected


def test_validate_error_dict_02():
    """
    dict型エラーの場合
    必須項目型エラー
    """
    schema = {
        'key': {
            'type': 'string',
            'required': True,
            'empty': False
        }
    }
    params = {'key': 1}
    result = validate(schema, params)
    expected = [{'code': 'E007', 'field': 'key', 'message': 'validation error'}]
    assert result == expected


def test_validate_error_dict_03():
    """
    dict型エラーの場合
    必須項目文字数エラー
    metaあり
    """
    schema = {
        'key': {
            'required': True,
            'empty': False,
            'minlength': 3,
            'maxlength': 3,
            'meta': {
                'message_cd': '0x9999',
                'err_cds': ['0x27', '0x28']
            }
        }
    }
    params = {'key': '1234'}
    result = validate(schema, params)
    expected = [{'code': 'E016', 'field': 'key', 'message': '3文字以下で入力してください。'}]
    assert result == expected


def test_validate_error_list_01():
    """
    list型エラーの場合
    文字数エラー
    """
    schema = {
        'pytest_list': {
            'type': 'list',
            'minlength': 3,
            'maxlength': 3,
            'schema': {
                'type': 'string',
                'minlength': 36,
                'maxlength': 36,
                'regex': r'^[a-zA-Z0-9-]+$',
            }
        }
    }
    params = {
        'pytest_list': [
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXNG1',
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXNG2',
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXNG3'
        ]
    }
    result = validate(schema, params)
    expected = [{'code': 'E007', 'field': 'pytest_list', 'message': 'validation error'}]
    assert result == expected


def test_validate_error_list_02():
    """
    list型エラーの場合
    文字数エラー
    metaあり
    """
    schema = {
        'pytest_list': {
            'type': 'list',
            'minlength': 3,
            'maxlength': 3,
            'schema': {
                'type': 'string',
                'minlength': 36,
                'maxlength': 36,
                'regex': r'^[a-zA-Z0-9-]+$',
            },
            'meta': {
                'message_cd': '0x9999',
                'err_cds': ['0x27', '0x28']
            }
        }
    }
    params = {
        'pytest_list': [
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXNG1',
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXNG2',
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXNG3'
        ]
    }
    result = validate(schema, params)
    expected = [{'code': 'E018', 'field': 'pytest_list', 'message': '36文字以上で入力してください。'}]
    assert result == expected


def test_validate_error_list_03():
    """
    list型エラーの場合
    要素数エラー
    metaあり
    """
    schema = {
        'pytest_list': {
            'type': 'list',
            'required': True,
            'empty': False,
            'minlength': 3,
            'maxlength': 3,
            'schema': {
                'type': 'string',
                'minlength': 36,
                'maxlength': 36,
                'regex': r'^[a-zA-Z0-9-]+$',
            },
            'meta': {
                'message_cd': '0x9999',
                'err_cds': ['0x27', '0x28']
            }
        }
    }
    params = {
        'pytest_list': [
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1',
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2',
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX3',
            'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX4'
        ]
    }
    result = validate(schema, params)
    expected = [{'code': 'E016', 'field': 'pytest_list', 'message': '3文字以下で入力してください。'}]
    assert result == expected


def test_validate_error_list_04():
    """
    list型エラーの場合
    必須エラー
    """
    schema = {
        'pytest_dict': {
            'type': 'dict',
            'required': True,
            'empty': False,
            'minlength': 1,
            'maxlength': 1,
            'schema': {
                'key': {
                    'type': 'string',
                    'required': True,
                    'empty': False,
                    'minlength': 36,
                    'maxlength': 36,
                    'regex': r'^[a-zA-Z0-9-]+$'
                }
            }
        }
    }
    params = {
        'pytest_dict': {
            'key1': 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1'
        }
    }
    result = validate(schema, params)
    expected = [{'code': 'E006', 'field': 'pytest_dict', 'message': 'missing field'}]
    assert result == expected


def test_get_error_message_add_field_name_and_constraint_is_dict():
    """
    メッセージ取得
    エラー項目名が設定されていて、constraintが辞書型の場合
    """
    field = 'error_value'
    field_name = 'エラー項目名'
    err_cd = '0x02'
    constraint = {'エラー項目名': 'value'}
    value = 'value'
    result = get_error_message(field, err_cd, constraint, value, field_name=field_name)
    expected = ('E010', 'エラー項目名は必須入力項目です。')
    assert result == expected
