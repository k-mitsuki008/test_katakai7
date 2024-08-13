import secrets
from datetime import timedelta
from common.logger import Logger
from common.decorator.service import service
from common.utils.time_utils import get_current_datetime, convert_datetime_to_str
from common.utils.aws_utils import get_constant
from common.error.not_expected_error import NotExpectedError
from repository import session_repository as repository

log = Logger()


@service
def login_session(gigya_uid: str, device_id: str) -> dict:
    session_id = create_session_id()
    create_session_timestamp = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    session_expires = get_constant('SESSION_EXPIRES', code='SESSION_EXPIRES', default=14)
    expire_session_timestamp = convert_datetime_to_str(get_current_datetime() + timedelta(days=int(session_expires)),
                                                       '%Y-%m-%d %H:%M:%S.%f')
    updated_data = repository.upsert_t_session(
        gigya_uid,
        session_id=session_id,
        device_id=device_id,
        create_session_timestamp=create_session_timestamp,
        expire_session_timestamp=expire_session_timestamp)

    if updated_data is None:
        raise NotExpectedError()

    return updated_data


@service
def logout_session(gigya_uid: str) -> dict:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    updated_data = repository.update_t_session(gigya_uid, expire_session_timestamp=now_str)

    if updated_data is None:
        raise NotExpectedError()

    return updated_data


@service
def get_t_session_by_session_id(session_id: str) -> list:
    t_session = repository.get_t_session_by_session_id(session_id)
    return t_session


def create_session_id():
    return secrets.token_hex(64)
