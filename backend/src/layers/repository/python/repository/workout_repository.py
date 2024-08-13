from common.logger import Logger
from common.rds.core import execute_insert_statement
from common.utils.time_utils import (convert_datetime_to_str,
                                     get_current_datetime)
from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def upsert_workout(gigya_uid: str, **kwargs) -> int:
    now_str = convert_datetime_to_str(
        get_current_datetime(),
        '%Y-%m-%d %H:%M:%S.%f'
    )
    update_sets = create_update_set_sql(**kwargs)

    sql = f'''
      INSERT INTO
        t_workout(
          gigya_uid,
          {', '.join(kwargs.keys())},
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(gigya_uid)s,
          %({')s, %('.join(kwargs.keys())})s,
          %(now_str)s,
          %(gigya_uid)s
        )
      ON CONFLICT(data_source_kind_code, data_source_id)
      DO UPDATE SET
        {update_sets}
        RETURNING workout_id;
      '''
    params = {'gigya_uid': gigya_uid, **kwargs, 'now_str': now_str}
    log.info(sql % params)
    rec = execute_insert_statement(sql, params, returning=True)
    return rec[0][0] if rec else None
