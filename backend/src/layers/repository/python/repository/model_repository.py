from common.logger import Logger

from common.rds.core import execute_select_statement

log = Logger()


def get_m_model(bike_radar_flag=None) -> list:

    bike_radar_filter = 'bike_radar_flag = True' if bike_radar_flag else ''
    where = 'WHERE' if bike_radar_filter else ''

    sql: str = f'''
      SELECT
        model_code,
        model_name,
        weight,
        charging_rated_output
      FROM
        m_model
      {where}
        {bike_radar_filter}
      ORDER BY sort_order;
    '''

    res = execute_select_statement(sql, {})

    return res
