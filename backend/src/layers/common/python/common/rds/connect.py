import psycopg2
import psycopg2.extras
import time

from common.error.db_access_error import DbAccessError
from common.logger import Logger
from common.stack_trace import get_stack_trace
from common.utils.aws_utils import get_secret

log = Logger()


class Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kargs)
        return cls._instance


class DbConnection(Singleton):
    conn = None
    __is_transactional = False

    def __del__(self):
        self.close()

    def connect(self: any) -> any:

        if self.conn:
            return self.conn

        rds_params = get_secret()
        log.info(f'CON_RDS_PARAMS:{rds_params}')
        try:
            start_time = time.time()
            url = "postgresql://{username}:{password}@{host}:{port}/{dbClusterIdentifier}".format(**rds_params)
            self.conn = psycopg2.connect(url)
            log.info(f'coonection_create_sec: {time.time() - start_time}')
        except Exception as e:
            log.error(get_stack_trace())
            raise DbAccessError() from e

        return self.conn

    def commit(self: any) -> None:
        self.conn.commit()

    def rollback(self: any) -> None:
        self.conn.rollback()

    def close(self: any) -> None:
        if not self.conn:
            return

        self.conn.close()
        self.conn = None

    @property
    def is_transactional(self: any) -> bool:
        return self.__is_transactional

    def start_transaction(self: any) -> None:
        self.__is_transactional = True

    def stop_transaction(self: any) -> None:
        self.__is_transactional = False
