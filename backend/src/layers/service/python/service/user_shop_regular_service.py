from common.logger import Logger

from repository import user_shop_regular_repository as repository
from common.decorator.service import service
from common.error.not_expected_error import NotExpectedError

log = Logger()


@service
def upsert_t_user_shop_regular(gigya_uid: str, **kwargs) -> dict:
    params = regular_remove(kwargs)
    _ = repository.upsert_t_user_shop_regular(gigya_uid, **params)

    upsert_result = repository.get_t_user_shop_regular(gigya_uid)
    if not upsert_result:
        raise NotExpectedError()
    result = regular_add(upsert_result)

    return result


@service
def insert_t_user_shop_regular(gigya_uid: str, **kwargs) -> int:
    _ = repository.insert_t_user_shop_regular(gigya_uid, **kwargs)
    return None


@service
def get_t_user_shop_regular(gigya_uid: str) -> dict:
    get_result = repository.get_t_user_shop_regular(gigya_uid)
    if not get_result:
        result = None
    else:
        result = regular_add(get_result)
    return result


def regular_remove(params) -> dict:
    # 項目名からregularを削除
    for x in filter(lambda key: key.startswith("regular_"), list(params.keys())):
        params[x.lstrip("regular_")] = params.pop(x)
    return params


def regular_add(params) -> dict:
    # 項目名にregularを付与
    for x in filter(lambda key: (key != "gigya_uid" and not key.startswith("regular_")), list(params.keys())):
        params["regular_" + x] = params.pop(x)
    return params
