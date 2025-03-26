from functools import wraps

from common.stack_trace import get_stack_trace
from common.logger import Logger
from common.rds.connect import DbConnection
from common.aws.dynamodb import DynamoDb

log: any = Logger()


def default_batch() -> any:
    def decorator(func: any) -> any:
        @wraps(func)
        def decorated(*args: any) -> any:

            # daynamoDb定数クラスの初期化
            dynm_db = DynamoDb()
            dynm_db.set_data()

            log.info('event => ')
            log.info(args[0])

            # リクエストのパース処理
            params = parse_request(args[0])
            log.info('parameter => ')
            log.info(params)

            dc = DbConnection()
            try:

                # DBに接続する
                dc.connect()
                # handler関数を実行
                handler_response = func(params)

            except Exception as e:
                log.error(get_stack_trace())
                raise e

            finally:
                # DBとの接続を切る
                dc.close()

            log.info('response => ')
            log.info(handler_response)

            return handler_response

        return decorated

    return decorator


def parse_request(event: any) -> dict:
    # EventBridgeからのeventをパースするため、基本的に処理することはない。
    # 必要に応じて実装追加すること。

    return event
