from common.decorator.service import service
from common.logger import Logger
from common.error.not_expected_error import NotExpectedError
from repository import model_repository as repository

log = Logger()


@service
def get_m_model(bike_radar_flag=None) -> list:
    get_result = repository.get_m_model(bike_radar_flag)

    if len(get_result) == 0:
        raise NotExpectedError()

    return get_result
