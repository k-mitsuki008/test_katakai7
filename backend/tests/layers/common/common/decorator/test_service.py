
import pytest

from common.decorator.service import service
from common.error.db_access_error import DbAccessError
from common.error.not_expected_error import NotExpectedError


def test_sample_service_ok():

    """
    正常系
    """

    # 期待している返却値
    expected_value = 'ok'
    assert sample_service() == expected_value


def test_sample_service_ng_db_access_error():

    """
    準正常系
    ※ DbAccessErrorが発生した時の応答確認
    """

    with pytest.raises(DbAccessError) as e:
        sample_service_ng_db_access_error()

    assert type(e.value) == DbAccessError


def test_sample_service_ng_other_error():

    """
    準正常系
    ※ DbAccessError以外のエラーが発生した時の応答確認
    """

    with pytest.raises(NotExpectedError) as e:
        sample_service_ng_other_error()

    assert type(e.value) == NotExpectedError


@service
def sample_service():
    return 'ok'


@service
def sample_service_ng_db_access_error():
    raise DbAccessError()


@service
def sample_service_ng_other_error():
    raise NotExpectedError('テスト例外')
