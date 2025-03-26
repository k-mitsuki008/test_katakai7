from common.logger import Logger
from common.decorator.service import service
from common.error.not_expected_error import NotExpectedError
from repository import ride_track_repository as repository
log = Logger()


@service
def get_ride_track(ride_history_id: str) -> list:
    get_result = repository.get_ride_track(ride_history_id)
    return get_result


@service
def delete_ride_track(ride_history_id: str) -> None:
    # ライド軌跡TBL削除
    delete_result = repository.delete_t_ride_track(ride_history_id)

    if delete_result <= 0:
        raise NotExpectedError()

    return
