from common.logger import Logger
from common.utils.aws_utils import get_dynamodb, put_dynamodb, upsert_dynamodb, get_query

log = Logger()


def put_app_version(**kwargs) -> dict:
    put_data = put_dynamodb(
        't_app_version',
        kwargs
    )
    return put_data.get('Attributes')


def upsert_app_version(os_name: str, app_version: str, **kwargs) -> dict:
    upserted_data = upsert_dynamodb(
        't_app_version',
        {'os': os_name, 'app_version': app_version},
        kwargs
    )
    return upserted_data.get('Attributes')


def get_app_version(os_name: str, version: str) -> dict:
    res = get_dynamodb(
        't_app_version',
        {'os': os_name, 'app_version': version}
    )
    return res if len(res) > 0 else None


def get_app_version_list(os_name: str) -> list:
    res = get_query(
        't_app_version',
        'os',
        os_name
    )

    return sorted(res, key=lambda x: x['update_timestamp'], reverse=True) if res else []
