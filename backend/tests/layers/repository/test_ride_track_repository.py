from datetime import datetime

from importlib import import_module
import pytest
from common.utils.time_utils import convert_datetime_to_str, get_current_datetime
from common.rds import execute_select_statement
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('repository.ride_track_repository')
upsert_t_ride_track = getattr(module, 'upsert_t_ride_track')
get_ride_track = getattr(module, 'get_ride_track')
delete_t_ride_track = getattr(module, 'delete_t_ride_track')


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_ride_track_ok_01():
    """
    正常系: ライド軌跡TBL UPSERT(INSERT)
    """
    expected_value = [
        {
            "ride_history_id": "1302022-10-06T15:30:31.000",
            "user_vehicle_id": 130,
            "track_id": 1,
            "latitude": 35.675068,
            "longitude": 139.763328,
            "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None,
            "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None,
            "etxyobi2": None, "etxyobi3": None, "etxyobi4": None,
            "etxyobi5": None, "delete_flag": False, "delete_timestamp": None,
            "delete_user_id": None,
            "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
            "insert_user_id": "test_uid_02", "update_timestamp": None,
            "update_user_id": None
        },
        {
            "ride_history_id": "1302022-10-06T15:30:31.000",
            "user_vehicle_id": 130,
            "track_id": 2,
            "latitude": 35.665498,
            "longitude": 139.759649,
            "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None,
            "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None,
            "etxyobi2": None, "etxyobi3": None, "etxyobi4": None,
            "etxyobi5": None, "delete_flag": False, "delete_timestamp": None,
            "delete_user_id": None,
            "insert_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
            "insert_user_id": "test_uid_02", "update_timestamp": None,
            "update_user_id": None
        }
    ]

    now_str = convert_datetime_to_str(
      get_current_datetime(),
      '%Y/%m/%d %H:%M:%S.%f'
    )

    ride_tracks = [
        ('1302022-10-06T15:30:31.000', 130, 1, 35.675068, 139.763328, now_str, 'test_uid_02'),
        ('1302022-10-06T15:30:31.000', 130, 2, 35.665498, 139.759649, now_str, 'test_uid_02')
    ]

    upsert_t_ride_track(ride_tracks)

    sql: str = '''
      SELECT * FROM t_ride_track
      WHERE ride_history_id = %(ride_history_id)s;
    '''
    parameters_dict: dict = {'ride_history_id': "1302022-10-06T15:30:31.000"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_upsert_t_ride_track_ok_02():
    """
    正常系: ライド軌跡TBL UPSERT(UPDATE)
    """
    expected_value = [{
        "ride_history_id": "1232022-10-06T15:30:31.000",
        "user_vehicle_id": 121,
        "track_id": 2,
        "latitude": 11.111111,
        "longitude": 222.222222,
        "fcdyobi1": None, "fcdyobi2": None, "fcdyobi3": None,
        "fcdyobi4": None, "fcdyobi5": None, "etxyobi1": None,
        "etxyobi2": None, "etxyobi3": None, "etxyobi4": None,
        "etxyobi5": None, "delete_flag": False, "delete_timestamp": None,
        "delete_user_id": None,
        "insert_timestamp": datetime(2022, 11, 17, 17, 17, 17, 610000),
        "insert_user_id": "test_uid_05",
        "update_timestamp": datetime(2022, 5, 13, 12, 34, 56, 789000),
        "update_user_id": "test_uid_02"
    }]

    now_str = convert_datetime_to_str(
      get_current_datetime(),
      '%Y/%m/%d %H:%M:%S.%f'
    )

    ride_tracks = [
        ('1232022-10-06T15:30:31.000', 121, 2, 11.111111, 222.222222, now_str, 'test_uid_02')
    ]

    upsert_t_ride_track(ride_tracks)

    sql: str = '''
      SELECT * FROM t_ride_track
      WHERE ride_history_id = %(ride_history_id)s;
    '''
    parameters_dict: dict = {'ride_history_id': "1232022-10-06T15:30:31.000"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_get_ride_track_ok():
    """
    正常系: ライド軌跡TBL SELECT
    """
    expected_value = [
        {
            "track_id": 1,
            "latitude": 35.67506,
            "longitude": 137.763328,
        },
        {
            "track_id": 2,
            "latitude": 36.67506,
            "longitude": 138.763328,
        },
        {
            "track_id": 3,
            "latitude": 37.67506,
            "longitude": 139.763328,
        },
    ]

    ride_history_id = "2222022-10-06T15:30:31.000"

    result = get_ride_track(ride_history_id)
    assert result == expected_value


def test_get_ride_track_ng():
    """
    異常系: ライド軌跡TBL 対象0件
    """
    expected_value = []

    ride_history_id = "99999"

    result = get_ride_track(ride_history_id)
    assert result == expected_value


def test_delete_t_ride_track_ok_01():
    """
    正常系: ライド軌跡TBL delete
    """
    expected_value = []

    ride_history_id = "1212022-10-06T15:30:31.000"

    delete_t_ride_track(ride_history_id)

    sql: str = '''
       SELECT * FROM t_ride_track
       WHERE ride_history_id = %(ride_history_id)s;
     '''
    parameters_dict: dict = {'ride_history_id': "1212022-10-06T15:30:31.000"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value


def test_delete_t_ride_track_ng_01():
    """
    異常系: ライド軌跡TBL delete
    対象データなし
    """
    expected_value = []

    ride_history_id = "999999999"

    delete_t_ride_track(ride_history_id)

    sql: str = '''
       SELECT * FROM t_ride_track
       WHERE ride_history_id = %(ride_history_id)s;
     '''
    parameters_dict: dict = {'ride_history_id': "999999999"}
    res = execute_select_statement(sql, parameters_dict)
    assert res == expected_value
