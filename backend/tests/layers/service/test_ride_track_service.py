from importlib import import_module, reload
import pytest

from common.error.not_expected_error import NotExpectedError
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.ride_track_service')
get_ride_track = getattr(module, 'get_ride_track')
delete_ride_track = getattr(module, 'delete_ride_track')


def test_get_ride_track_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    ライド軌跡TBLデータあり
    """
    # repository.ride_track_repository.get_ride_trackのモック化
    mocker.patch(
        "repository.ride_track_repository.get_ride_track",
        return_value=[
            {
                "track_id": 1,
                "latitude": 35.675069,
                "longitude": 139.763328
            },
            {
                "track_id": 2,
                "latitude": 35.665498,
                "longitude": 139.75964
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = [
        {
            "track_id": 1,
            "latitude": 35.675069,
            "longitude": 139.763328
        },
        {
            "track_id": 2,
            "latitude": 35.665498,
            "longitude": 139.75964
        }
    ]

    ride_history_id = "1232022-10-06T15:30:31.000"

    data = get_ride_track(ride_history_id)

    assert data == expected_value


def test_get_ride_track_ok_02(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    ライド軌跡TBLデータなし
    """
    # repository.ride_track_repository.get_ride_trackのモック化
    mocker.patch(
        "repository.ride_track_repository.get_ride_track",
        return_value=[]
    )
    reload(module)

    # 期待している返却値
    expected_value = []

    ride_history_id = "1232022-10-06T15:30:31.000"

    data = get_ride_track(ride_history_id)

    assert data == expected_value


def test_delete_ride_track_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    """
    # repository.ride_track_repository.delete_t_ride_trackのモック化
    mocker.patch(
        "repository.ride_track_repository.delete_t_ride_track",
        return_value=1
    )

    reload(module)

    # 期待している返却値
    expected_value = None

    ride_history_id = "1232022-10-06T15:30:31.000"

    result_data = delete_ride_track(ride_history_id)

    assert result_data == expected_value


def test_delete_ride_track_ok_02(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    """
    # repository.ride_track_repository.delete_t_ride_trackのモック化
    mocker.patch(
        "repository.ride_track_repository.delete_t_ride_track",
        return_value=0
    )

    reload(module)

    ride_history_id = "1232022-10-06T15:30:31.000"

    with pytest.raises(NotExpectedError):
        delete_ride_track(ride_history_id)
