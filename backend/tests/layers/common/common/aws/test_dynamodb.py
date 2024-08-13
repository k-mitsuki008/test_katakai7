import pytest
import tests.test_utils.fixtures as fixtures
from common.aws.dynamodb import DynamoDb
from common.error.dynamo_db_access_error import DynamoDbAccessError

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup


def test_set_data_ok_01():
    """
    正常系
    """
    obj = DynamoDb()
    obj.constants = [{'constants': 'pytest'}]
    obj.messages = [{'message': 'pytest'}]
    assert obj.set_data() is None


def test_set_data_ok_02():
    """
    正常系
    """
    obj = DynamoDb()
    obj.constants = None
    obj.messages = None
    assert obj.set_data() is None
    is_messages = True if obj.messages else False
    assert is_messages is True


def test_get_all_ok():
    """
    正常系
    """
    table_name = 'm_message'
    obj = DynamoDb()
    assert obj.get_all(table_name)


def test_get_all_ng():
    """
    異常系
    """
    table_name = 'ng_table_name'
    obj = DynamoDb()
    with pytest.raises(DynamoDbAccessError):
        obj.get_all(table_name)
