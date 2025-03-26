from common.logger import Logger
from common.utils.aws_utils import get_dynamodb, upsert_dynamodb, get_dynamodb_by_secondary_index

log = Logger()


def upsert_t_session(gigya_uid: str, **kwargs) -> dict:
    upserted_data = upsert_dynamodb(
        't_session',
        {'gigya_uid': gigya_uid},
        kwargs
    )
    return upserted_data.get('Attributes')


def update_t_session(gigya_uid: str, **kwargs) -> dict:
    updated_data = upsert_dynamodb(
        't_session',
        {'gigya_uid': gigya_uid},
        kwargs,
        "attribute_exists(gigya_uid)"
    )
    return updated_data.get('Attributes')


def get_t_session_by_key(gigya_uid: str) -> dict:
    res = get_dynamodb(
        't_session',
        {'gigya_uid': gigya_uid}
    )

    return res if len(res) > 0 else None


def get_t_session_by_session_id(session_id: str) -> list:
    res = get_dynamodb_by_secondary_index(
        't_session',
        'session_id-index',
        'session_id', session_id
    )

    return res
