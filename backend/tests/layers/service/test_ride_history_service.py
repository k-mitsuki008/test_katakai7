from importlib import import_module, reload
import pytest
from common.error.not_expected_error import NotExpectedError
from datetime import datetime
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.ride_history_service')
upsert_ride_history = getattr(module, 'upsert_ride_history')
get_ride_history = getattr(module, 'get_ride_history')
get_history_limit = getattr(module, 'get_history_limit')
update_ride_history = getattr(module, 'update_ride_history')
delete_ride_history = getattr(module, 'delete_ride_history')


def test_upsert_t_user_setting_ride_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    ライド軌跡TBL更新データあり
    """
    # repository.ride_history_repository.upsert_t_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.upsert_t_ride_history",
        return_value=0
    )
    # repository.ride_history_repository.get_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history",
        return_value={
            "ride_history_id": "1232022-10-06T15:30:31.000",
            "gigya_uid": "test_uid_01",
            "start_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
            "end_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
            "user_vehicle_id": 120, "trip_distance": 1234.5,
            "trip_time": 3600, "total_calorie": 535, "battery_consumption": 72,
            "average_speed": 15, "max_speed": 20, "max_pedaling_power": 6,
            "max_cadence": 126, "ride_name": "ユーザー車両名のライド",
            "bookmark_flg": False,
        }
    )
    # repository.ride_track_repository.upsert_t_ride_trackのモック化
    mocker.patch(
        "repository.ride_track_repository.upsert_t_ride_track",
        return_value=0
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "ride_history_id": "1232022-10-06T15:30:31.000",
    }

    gigya_uid = "test_uid_01"
    ride_history_id = "1232022-10-06T15:30:31.000"
    recs = {
        "start_timestamp": "2022-10-06T15:30:31.000",
        "end_timestamp": "2022-09-01T15:30:31.000",
        "user_vehicle_id": 123,
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "ride_tracks": [
            {
                "track_id": 1,
                "latitude": 35.67506,
                "longitude": 139.763328
            },
            {
                "track_id": 2,
                "latitude": 35.665498,
                "longitude": 139.759649
            }
        ]
    }
    updated_data = upsert_ride_history(gigya_uid, ride_history_id, **recs)

    assert updated_data == expected_value


def test_upsert_t_user_setting_ride_ok_02(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    ライド軌跡TBL更新データなし
    """
    # repository.ride_history_repository.upsert_t_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.upsert_t_ride_history",
        return_value=0
    )
    # repository.ride_history_repository.get_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history",
        return_value={
            "ride_history_id": "1232022-10-06T15:30:31.000",
            "gigya_uid": "test_uid_01",
            "start_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
            "end_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
            "user_vehicle_id": 120, "trip_distance": 1234.5,
            "trip_time": 3600, "total_calorie": 535, "battery_consumption": 72,
            "average_speed": 15, "max_speed": 20, "max_pedaling_power": 6,
            "max_cadence": 126, "ride_name": "ユーザー車両名のライド",
            "bookmark_flg": False,
        }
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "ride_history_id": "1232022-10-06T15:30:31.000",
    }

    gigya_uid = "test_uid_01"
    ride_history_id = "1232022-10-06T15:30:31.000"
    recs = {
        "start_timestamp": "2022-10-06T15:30:31.000",
        "end_timestamp": "2022-09-01T15:30:31.000",
        "user_vehicle_id": 123,
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "ride_tracks": [],
    }
    updated_data = upsert_ride_history(gigya_uid, ride_history_id, **recs)

    assert updated_data == expected_value


def test_get_tasks_ng_not_expected_error_01(mocker):
    """
    準正常系: upsert_t_ride_historyでエラー
    ※ @serviceでException → NotExpectedError に変換されること
    """
    # repository.ride_history_repository.upsert_t_ride_history のモック化
    mocker.patch(
        "repository.ride_history_repository.upsert_t_ride_history",
        side_effect=Exception
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        upsert_ride_history('test_uid_01', **{})


def test_get_tasks_ng_not_expected_error_02(mocker):
    """
    準正常系: upsert_t_ride_trackでエラー
    ※ @serviceでException → NotExpectedError に変換されること
    """
    # repository.ride_history_repository.upsert_t_ride_history のモック化
    mocker.patch(
        "repository.ride_history_repository.upsert_t_ride_history",
        return_value=0
    )
    # repository.ride_track_repository.upsert_t_ride_trackのモック化
    mocker.patch(
        "repository.ride_track_repository.upsert_t_ride_track",
        return_value=Exception
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        upsert_ride_history('test_uid_01', **{})


def test_get_tasks_ng_not_expected_error_03(mocker):
    """
    準正常系: get_ride_historyでNoneが返却
    ※ @serviceでException → NotExpectedError に変換されること
    """
    # repository.ride_history_repository.upsert_t_ride_history のモック化
    mocker.patch(
        "repository.ride_history_repository.upsert_t_ride_history",
        return_value=0
    )
    # repository.ride_track_repository.upsert_t_ride_trackのモック化
    mocker.patch(
        "repository.ride_track_repository.upsert_t_ride_track",
        return_value=0
    )
    # repository.ride_history_repository.get_ride_history のモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history",
        return_value=None
    )
    reload(module)

    with pytest.raises(NotExpectedError):
        upsert_ride_history('test_uid_01', '', **{})


def test_get_history_limit_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    ライド履歴TBL更新データあり
    """
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_all_count",
        return_value={'count': 13}
    )
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_limit",
        return_value=[
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": datetime(2022, 9, 1, 5, 18, 30, 31),
                "end_timestamp": datetime(2022, 9, 1, 15, 30, 31, 31),
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": True
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": datetime(2022, 10, 1, 14, 18, 30, 000),
                "end_timestamp": datetime(2022, 10, 1, 15, 30, 31, 000),
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": True
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
            "end_of_data": False,
            "ride_histories": [
                {
                    "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                    "start_timestamp": "2022-09-01T05:18:30.000Z",
                    "end_timestamp": "2022-09-01T15:30:31.000Z",
                    "ride_name": "XXXXXXX",
                    "trip_distance": 1234.5,
                    "trip_time": 3600,
                    "bookmark_flg": True
                },
                {
                    "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                    "start_timestamp": "2022-10-01T14:18:30.000Z",
                    "end_timestamp": "2022-10-01T15:30:31.000Z",
                    "ride_name": "YYYYYYY",
                    "trip_distance": 999.9,
                    "trip_time": 72000,
                    "bookmark_flg": True
                }
            ]
        }

    gigya_uid = "test_uid_01"
    begin = "2022-09-01T05:18:30.000"
    end = "2022-10-01T05:18:30.000"
    bookmark_flg = True
    limit = 2
    offset = 0

    result_data = get_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end,
        bookmark_flg,
    )

    assert result_data == expected_value


def test_get_history_limit_ok_02(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    ライド履歴TBL更新データなし
    """
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_all_count",
        return_value={'count': 0}
    )
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_limit",
        return_value=[]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        'end_of_data': True,
        'ride_histories': []
    }

    gigya_uid = "test_uid_01"
    begin = "2022-09-01T05:18:30.000"
    end = "2022-10-01T05:18:30.000"
    bookmark_flg = True
    limit = 5
    offset = 0

    result_data = get_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end,
        bookmark_flg,
    )

    assert result_data == expected_value


def test_get_history_limit_ok_03(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    ライド履歴TBL最終データ
    """
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_all_count",
        return_value={'count': 3}
    )
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_limit",
        return_value=[
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": datetime(2022, 9, 1, 5, 18, 30, 310),
                "end_timestamp": datetime(2022, 9, 1, 15, 30, 30, 310),
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": True
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": datetime(2022, 10, 1, 14, 18, 30, 310),
                "end_timestamp": datetime(2022, 10, 1, 15, 30, 30, 310),
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": True
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "end_of_data": True,
        "ride_histories": [
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": "2022-09-01T05:18:30.000Z",
                "end_timestamp": "2022-09-01T15:30:30.000Z",
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": True
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": "2022-10-01T14:18:30.000Z",
                "end_timestamp": "2022-10-01T15:30:30.000Z",
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": True
            }
        ]
    }

    gigya_uid = "test_uid_01"
    begin = "2022-09-01T05:18:30.000"
    end = "2022-10-01T15:30:31.000"
    bookmark_flg = True
    limit = 2
    offset = 1

    result_data = get_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end,
        bookmark_flg,
    )

    assert result_data == expected_value


def test_get_history_limit_ok_04(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    ライド履歴TBL最終データ
    """
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_all_count",
        return_value={'count': 5}
    )
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_limit",
        return_value=[
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": datetime(2022, 9, 1, 5, 18, 30, 310),
                "end_timestamp": datetime(2022, 9, 1, 15, 30, 30, 310),
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": True
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": datetime(2022, 10, 1, 14, 18, 30, 310),
                "end_timestamp": datetime(2022, 10, 1, 15, 30, 30, 310),
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": True
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "end_of_data": True,
        "ride_histories": [
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": "2022-09-01T05:18:30.000Z",
                "end_timestamp": "2022-09-01T15:30:30.000Z",
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": True
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": "2022-10-01T14:18:30.000Z",
                "end_timestamp": "2022-10-01T15:30:30.000Z",
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": True
            }
        ]
    }

    gigya_uid = "test_uid_01"
    begin = "2022-09-01T05:18:30.000"
    end = "2022-10-01T15:30:31.000"
    bookmark_flg = True
    limit = 2
    offset = 4

    result_data = get_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end,
        bookmark_flg,
    )

    assert result_data == expected_value


def test_get_history_limit_ok_05(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    bookmark_flg指定なし
    """
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_all_count",
        return_value={'count': 21}
    )
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_limit",
        return_value=[
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": datetime(2022, 9, 1, 5, 18, 30, 310),
                "end_timestamp": datetime(2022, 9, 1, 15, 30, 30, 310),
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": None
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": datetime(2022, 9, 1, 5, 18, 30, 310),
                "end_timestamp": datetime(2022, 9, 1, 15, 30, 30, 310),
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": None
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "end_of_data": True,
        "ride_histories": [
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": "2022-09-01T05:18:30.000Z",
                "end_timestamp": "2022-09-01T15:30:30.000Z",
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": None
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": "2022-09-01T05:18:30.000Z",
                "end_timestamp": "2022-09-01T15:30:30.000Z",
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": None
            }
        ]
    }

    gigya_uid = "test_uid_01"
    limit = 2
    offset = 19
    begin = "2022-09-01T05:18:30.000"
    end = "2022-10-01T15:30:31.000"

    result_data = get_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end
    )

    assert result_data == expected_value


def test_get_history_limit_ok_06(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    start_timestamp,end_timestampの返却値無しの場合
    """
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_all_count",
        return_value={'count': 21}
    )
    # repository.ride_history_repository.get_ride_history_limitのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history_limit",
        return_value=[
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": None,
                "end_timestamp": None,
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": None
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": None,
                "end_timestamp": None,
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": None
            }
        ]
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "end_of_data": True,
        "ride_histories": [
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070231",
                "start_timestamp": None,
                "end_timestamp": None,
                "ride_name": "XXXXXXX",
                "trip_distance": 1234.5,
                "trip_time": 3600,
                "bookmark_flg": None
            },
            {
                "ride_history_id": "qawsedrfgtyhujkiolp1665070999",
                "start_timestamp": None,
                "end_timestamp": None,
                "ride_name": "YYYYYYY",
                "trip_distance": 999.9,
                "trip_time": 72000,
                "bookmark_flg": None
            }
        ]
    }

    gigya_uid = "test_uid_01"
    limit = 2
    offset = 19
    begin = "2022-09-01T05:18:30.000"
    end = "2022-10-01T15:30:31.000"

    result_data = get_history_limit(
        gigya_uid,
        limit,
        offset,
        begin,
        end
    )

    assert result_data == expected_value


def test_get_history_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    ライド履歴TBL更新データあり
    """
    # repository.ride_history_repository.get_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history",
        return_value={
            "ride_history_id": "1222022-10-06T15:30:31.000",
            "start_timestamp": datetime(2022, 9, 1, 5, 30, 31, 00),
            "end_timestamp": datetime(2022, 9, 1, 15, 30, 31, 00),
            "ride_name": "XXXXXXX",
            "trip_distance": 1234.5,
            "trip_time": 3600,
            "total_calorie": 535,
            "battery_consumption": 72,
            "average_speed": 15,
            "max_speed": 20,
            "max_pedaling_power": 6,
            "max_cadence": 126,
            "bookmark_flg": False,
        },
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "ride_history_id": "1222022-10-06T15:30:31.000",
        "start_timestamp": "2022-09-01T05:30:31.000Z",
        "end_timestamp": "2022-09-01T15:30:31.000Z",
        "ride_name": "XXXXXXX",
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max_speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "bookmark_flg": False,
    }

    gigya_uid = "test_uid_01"
    ride_history_id = "1222022-10-06T15:30:31.000"

    result_data = get_ride_history(gigya_uid, ride_history_id)

    assert result_data == expected_value


def test_get_history_ng_01(mocker):
    """
    異常系
    ※ repository関数からの取得値をそのまま返す
    ライド履歴TBL更新データなし
    """
    # repository.ride_history_repository.get_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history",
        return_value=None
    )
    reload(module)

    gigya_uid = "test_uid_01"
    ride_history_id = "1222022-10-06T15:30:31.000"

    with pytest.raises(NotExpectedError):
        get_ride_history(gigya_uid, ride_history_id)


def test_get_history_ng_02(mocker):
    """
    異常系
    ※ repository関数からの取得値をそのまま返す
    ライド履歴TBL更新データあり（以下カラムのみデータなし）
    ・start_timestamp
    ・end_timestamp
    """
    # repository.ride_history_repository.get_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history",
        return_value={
            "ride_history_id": "1222022-10-06T15:30:31.000",
            "start_timestamp": None,
            "end_timestamp": None,
            "ride_name": "XXXXXXX",
            "trip_distance": 1234.5,
            "trip_time": 3600,
            "total_calorie": 535,
            "battery_consumption": 72,
            "average_speed": 15,
            "max_speed": 20,
            "max_pedaling_power": 6,
            "max_cadence": 126,
            "bookmark_flg": False,
        },
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "ride_history_id": "1222022-10-06T15:30:31.000",
        "start_timestamp": None,
        "end_timestamp": None,
        "ride_name": "XXXXXXX",
        "trip_distance": 1234.5,
        "trip_time": 3600,
        "total_calorie": 535,
        "battery_consumption": 72,
        "average_speed": 15,
        "max_speed": 20,
        "max_pedaling_power": 6,
        "max_cadence": 126,
        "bookmark_flg": False,
    }

    gigya_uid = "test_uid_01"
    ride_history_id = "1222022-10-06T15:30:31.000"

    result_data = get_ride_history(gigya_uid, ride_history_id)

    assert result_data == expected_value


def test_update_ride_history_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    """
    # repository.ride_history_repository.update_t_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.update_t_ride_history",
        return_value=0
    )
    # repository.ride_history_repository.get_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history",
        return_value={
            "ride_history_id": "1232022-10-06T15:30:31.000",
            "gigya_uid": "test_uid_01",
            "start_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
            "end_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
            "user_vehicle_id": 120, "trip_distance": 1234.5,
            "trip_time": 3600, "total_calorie": 535, "battery_consumption": 72,
            "average_speed": 15, "max_speed": 20, "max_pedaling_power": 6,
            "max_cadence": 126, "ride_name": "ユーザー車両名のライド",
            "bookmark_flg": False,
        }
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "ride_history_id": "1232022-10-06T15:30:31.000",
        "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": False
    }

    gigya_uid = "test_uid_01"
    ride_history_id = "1232022-10-06T15:30:31.000"
    recs = {
        "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": False
    }

    result_data = update_ride_history(gigya_uid, ride_history_id, **recs)

    assert result_data == expected_value


def test_update_ride_history_ok_02(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    inputデータなし
    """
    # repository.ride_history_repository.update_t_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.update_t_ride_history",
        return_value=0
    )
    # repository.ride_history_repository.get_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history",
        return_value={
            "ride_history_id": "1232022-10-06T15:30:31.000",
            "gigya_uid": "test_uid_01",
            "start_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
            "end_timestamp": datetime(2022, 12, 12, 12, 12, 12, 610000),
            "user_vehicle_id": 120, "trip_distance": 1234.5,
            "trip_time": 3600, "total_calorie": 535, "battery_consumption": 72,
            "average_speed": 15, "max_speed": 20, "max_pedaling_power": 6,
            "max_cadence": 126, "ride_name": "ユーザー車両名のライド",
            "bookmark_flg": False,
        }
    )
    reload(module)

    # 期待している返却値
    expected_value = {
        "ride_history_id": "1232022-10-06T15:30:31.000",
        "ride_name": "ユーザー車両名のライド",
        "bookmark_flg": False
    }

    gigya_uid = "test_uid_01"
    ride_history_id = "1232022-10-06T15:30:31.000"
    recs = {}

    result_data = update_ride_history(gigya_uid, ride_history_id, **recs)

    assert result_data == expected_value


def test_update_ride_history_ok_03(mocker):
    """
    準正常系: get_ride_historyでNoneが返却
    ※ @serviceでException → NotExpectedError に変換されること
    """
    # repository.ride_history_repository.update_t_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.update_t_ride_history",
        return_value=0
    )
    # repository.ride_history_repository.get_ride_history のモック化
    mocker.patch(
        "repository.ride_history_repository.get_ride_history",
        return_value=None
    )
    reload(module)

    gigya_uid = "test_uid_01"
    ride_history_id = "1232022-10-06T15:30:31.000"
    recs = {}

    with pytest.raises(NotExpectedError):
        update_ride_history(gigya_uid, ride_history_id, **recs)


def test_delete_ride_history_ok_01(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    データあり
    """
    # repository.ride_history_repository.delete_t_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.delete_t_ride_history",
        return_value=1
    )

    reload(module)

    # 期待している返却値
    expected_value = None

    gigya_uid = "test_uid_01"
    ride_history_id = "1232022-10-06T15:30:31.000"

    result_data = delete_ride_history(gigya_uid, ride_history_id)

    assert result_data == expected_value


def test_delete_ride_history_ok_02(mocker):
    """
    正常系
    ※ repository関数からの取得値をそのまま返す
    データなし
    """
    # repository.ride_history_repository.delete_t_ride_historyのモック化
    mocker.patch(
        "repository.ride_history_repository.delete_t_ride_history",
        return_value=None
    )

    reload(module)

    # 期待している返却値
    expected_value = None

    gigya_uid = "test_uid_01"
    ride_history_id = "1232022-10-06T15:30:31.000"

    result_data = delete_ride_history(gigya_uid, ride_history_id)

    assert result_data == expected_value
