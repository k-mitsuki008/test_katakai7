from datetime import datetime, date

import pytest

from common.utils.time_utils import convert_datetime_to_str, get_current_datetime, convert_str_to_datetime, \
    convert_to_jst, replace_time


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_get_current_datetime_ok():
    assert get_current_datetime() == datetime(2022, 5, 13, 12, 34, 56, 789101)


def test_convert_datetime_to_str_ok_01():
    """
    正常系
    """
    ret = convert_datetime_to_str(date(2022, 12, 31))
    assert ret == '20221231'


def test_convert_datetime_to_str_ok_02():
    """
    正常系
    ※datetime_dateが未設定
    """
    assert not convert_datetime_to_str(None)


def test_convert_str_to_datetime_ok_01():
    """
    正常系
    """
    ret = convert_str_to_datetime('2022-05-13 12:34:56.789101')
    assert ret == datetime(2022, 5, 13, 12, 34, 56, 789101)


def test_convert_to_jst_ok_01():
    """
    正常系
    """
    ret = convert_to_jst(datetime(2022, 5, 13, 12, 34, 56, 789101))
    assert str(ret) == "2022-05-13 12:34:56.789101+09:00"


def test_replace_time_ok_01():
    """
    正常系
    """
    ret = replace_time(datetime(2022, 5, 13, 12, 34, 56, 789101))
    assert str(ret) == "2022-05-13 00:00:00"
