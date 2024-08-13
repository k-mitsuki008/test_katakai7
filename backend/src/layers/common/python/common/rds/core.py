from psycopg2.extras import DictCursor
from common.rds.connect import DbConnection
from common.error.db_access_error import DbAccessError
from common.logger import Logger
from typing import Union

log: any = Logger()


def execute_statement(sql: str, parameters_dict: dict = None) -> any:
    dc = DbConnection()
    try:
        with dc.connect().cursor() as cursor:
            _ = cursor.execute(sql, parameters_dict)

    except Exception as e:
        raise DbAccessError() from e

    return cursor


def execute_select_statement(sql: str, parameters_dict: dict = None) -> list:
    dc = DbConnection()
    try:
        with dc.connect().cursor(cursor_factory=DictCursor) as cursor:
            _ = cursor.execute(sql, parameters_dict)
            results_list = cursor.fetchall()
    except Exception as e:
        raise DbAccessError() from e

    results = []
    for row in results_list:
        results.append(dict(row))
    return results


def execute_insert_statement(sql: str, parameters_dict: Union[dict, list] = None, returning: bool = False) -> any:
    dc = DbConnection()
    try:
        with dc.connect().cursor(cursor_factory=DictCursor) as cursor:
            _ = cursor.execute(sql, parameters_dict)

            # 単独で実行された場合はコミットする
            if not dc.is_transactional:
                dc.commit()
            # RETURNING設定ありの場合は取得して返す。
            if returning:
                return cursor.fetchall()
    except Exception as e:
        raise DbAccessError() from e

    return cursor.lastrowid


def execute_update_statement(sql: str, parameters_dict: dict = None, returning: bool = False) -> any:
    dc = DbConnection()
    try:
        with dc.connect().cursor(cursor_factory=DictCursor) as cursor:
            _ = cursor.execute(sql, parameters_dict)

            # 単独で実行された場合はコミットする
            if not dc.is_transactional:
                dc.commit()
            # RETURNING設定ありの場合は取得して返す。
            if returning:
                return cursor.fetchall()
    except Exception as e:
        raise DbAccessError() from e

    return cursor.rowcount


def execute_delete_statement(sql: str, parameters_dict: dict = None, returning: bool = False) -> any:
    dc = DbConnection()
    try:
        with dc.connect().cursor(cursor_factory=DictCursor) as cursor:
            _ = cursor.execute(sql, parameters_dict)

            # 単独で実行された場合はコミットする
            if not dc.is_transactional:
                dc.commit()
            # RETURNING設定ありの場合は取得して返す。
            if returning:
                return cursor.fetchall()
    except Exception as e:
        raise DbAccessError() from e

    return cursor.rowcount


def batch_execute_insert_statement(sql: str, parameters_dict_list: list) -> any:
    """INSERT文実行処理(一括登録)

    Args:
        sql (str): SQL文字列
        parameters_dict_list (list): SQLに組み込むパラメータの辞書のリスト

    Returns:
         row_count (int): 影響を受けたレコード数
    """
    dc = DbConnection()
    try:
        with dc.connect().cursor(cursor_factory=DictCursor) as cursor:
            _ = cursor.executemany(sql, parameters_dict_list)
            rowcount = cursor.rowcount

            # 単独で実行された場合はコミットする
            if not dc.is_transactional:
                dc.commit()

    except Exception as e:
        raise DbAccessError() from e

    return rowcount
