from functools import wraps
from common.logger import Logger

from common.error.custom_error import CustomError
from common.error.not_expected_error import NotExpectedError

log: any = Logger()


def service(func: any) -> any:
    @wraps(func)
    def decorated(*args: any, **kwargs: any) -> any:

        try:
            result: any = func(*args, **kwargs)
        except CustomError as e:
            raise e
        except Exception as e:
            raise NotExpectedError() from e

        return result

    return decorated
