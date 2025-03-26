from common.logger import Logger
from common.decorator.service import service
from common.error.not_expected_error import NotExpectedError
from common.utils.time_utils import convert_datetime_to_str, get_current_datetime
from repository import ride_history_repository as repository_history
from repository import ride_track_repository as repository_track
log = Logger()


@service
def upsert_ride_history(gigya_uid: str, ride_history_id: str, **kwargs) -> dict:
    ride_tracks = kwargs.pop('ride_tracks', None)
    # ライド履歴TBL更新
    _ = repository_history.upsert_t_ride_history(
        gigya_uid,
        ride_history_id,
        **kwargs
    )

    # ライド軌跡TBL更新
    if ride_tracks and len(ride_tracks) > 0:
        user_vehicle_id = kwargs.get('user_vehicle_id')
        now_str = convert_datetime_to_str(
            get_current_datetime(),
            '%Y/%m/%d %H:%M:%S.%f'
        )
        ride_tracks_params = [
            (
                ride_history_id,
                user_vehicle_id,
                x.get('track_id'),
                x.get('latitude'),
                x.get('longitude'),
                now_str,
                gigya_uid
            ) for x in ride_tracks
        ]
        repository_track.upsert_t_ride_track(ride_tracks_params)

    update_result = repository_history.get_ride_history(gigya_uid, ride_history_id)

    if update_result is None:
        raise NotExpectedError()

    return {
        "ride_history_id": update_result.get("ride_history_id")
    }


@service
def get_ride_history(gigya_uid: str, ride_history_id: str) -> dict:
    get_result = repository_history.get_ride_history(gigya_uid, ride_history_id)

    if get_result is None:
        raise NotExpectedError()

    # pylint: disable=unsupported-assignment-operation
    if get_result.get("start_timestamp"):
        start_timestamp_str = get_result.get("start_timestamp").isoformat(timespec="milliseconds") + "Z"
        get_result["start_timestamp"] = start_timestamp_str
    if get_result.get("end_timestamp"):
        end_timestamp_str = get_result.get("end_timestamp").isoformat(timespec="milliseconds") + "Z"
        get_result["end_timestamp"] = end_timestamp_str

    return get_result


@service
def get_history_limit(
    gigya_uid: str,
    limit: int,
    offset: int,
    begin: str,
    end: str,
    bookmark_flg: bool = None,
) -> dict:

    # ライド履歴TBLの全件数を取得
    all_count = repository_history.get_ride_history_all_count(
            gigya_uid,
            begin,
            end,
            bookmark_flg,
    )
    # ライド履歴TBL取得
    get_result = repository_history.get_ride_history_limit(
            gigya_uid,
            limit,
            offset,
            begin,
            end,
            bookmark_flg,
    )
    for item in get_result:
        if item.get("start_timestamp"):
            start_timestamp_str = item.get("start_timestamp").isoformat(timespec="milliseconds") + "Z"
            item["start_timestamp"] = start_timestamp_str
        if item.get("end_timestamp"):
            end_timestamp_str = item.get("end_timestamp").isoformat(timespec="milliseconds") + "Z"
            item["end_timestamp"] = end_timestamp_str

    end_of_data = False

    if limit + offset >= all_count.get("count"):
        end_of_data = True

    result = {
        "end_of_data": end_of_data,
        "ride_histories": get_result
    }

    return result


@service
def update_ride_history(gigya_uid: str, ride_history_id: str, **kwargs) -> dict:
    # ライド履歴TBL更新
    if kwargs:
        _ = repository_history.update_t_ride_history(
            gigya_uid,
            ride_history_id,
            **kwargs
        )

    update_result = repository_history.get_ride_history(gigya_uid, ride_history_id)

    if update_result is None:
        raise NotExpectedError()

    return {
        "ride_history_id": update_result.get("ride_history_id"),
        "ride_name": update_result.get("ride_name"),
        "bookmark_flg": update_result.get("bookmark_flg"),
    }


@service
def delete_ride_history(gigya_uid: str, ride_history_id: str) -> None:
    # ライド軌跡削除
    repository_track.delete_t_ride_track(ride_history_id)
    # ライド履歴TBL削除
    repository_history.delete_t_ride_history(gigya_uid, ride_history_id)

    return
