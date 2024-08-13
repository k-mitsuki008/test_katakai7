from common.logger import Logger
from common.rds.core import execute_select_statement

log = Logger()


def get_m_spot(latitude: float, longitude: float, radius: int) -> list:
    sql: str = '''
        SELECT
            spot_id,
            spot_type_code,
            ST_AsGeoJson(spot_location) as spot_location,
            spot_place_id,
            rechargeable_flag
        FROM
            m_spot
        WHERE
            ST_DWithin(spot_location, ST_GeomFromText('POINT(%(latitude)s %(longitude)s)', 4326), %(radius)s, true)
            AND delete_flag = false
    '''

    parameters_dict: dict = {'latitude': latitude, 'longitude': longitude, 'radius': radius}
    res = execute_select_statement(sql, parameters_dict)

    return res
