from functools import wraps

from common.rds.core import DbConnection
from common.logger import Logger

log: any = Logger()


def transactional(func: any) -> any:
    @wraps(func)
    def decorated(*args: any, **kwargs: any) -> any:

        # トランザクション開始
        dc = DbConnection()
        dc.start_transaction()

        try:
            result = func(*args, **kwargs)
            dc.commit()

        except Exception as e:
            dc.rollback()
            raise e

        finally:
            # トランザクション終了
            dc.stop_transaction()

        return result

    return decorated
