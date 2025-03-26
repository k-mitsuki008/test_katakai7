from common.logger import Logger
from common.rds.core import (execute_delete_statement,
                             execute_insert_statement,
                             execute_select_statement,
                             execute_update_statement)
from common.utils.time_utils import (convert_datetime_to_str,
                                     get_current_datetime)
from repository.utils.repository_utils import create_update_set_sql

log = Logger()


def get_t_route(gigya_uid: str, route_id: int) -> list:
    sql: str = '''
        SELECT
            count(*) as count
        FROM
            t_route
        WHERE
            route_id = %(route_id)s
            AND gigya_uid = %(gigya_uid)s
    '''

    parameters_dict = {'gigya_uid': gigya_uid, 'route_id': route_id}
    res = execute_select_statement(sql, parameters_dict)

    return res[0]['count'] if res else None


def get_t_route_by_gigya_uid(gigya_uid: str) -> list:
    sql: str = '''
        SELECT
            tr.route_id,
            tr.user_vehicle_id,
            tr.save_timestamp,
            tr.destination_name,
            ST_AsGeoJson(tr.destination_location) as destination_location,
            tr.destination_place_id,
            tr.ride_date,
            tr.weather,
            tr.weather_icon,
            tro.one_ways
        FROM
            t_route tr
        INNER JOIN (
            SELECT
                route_id
                , jsonb_agg(
                    jsonb_strip_nulls(
                        jsonb_build_object(
                            'round_trip_type_code', round_trip_type_code,
                            'duration', duration,
                            'distance', distance
                        )
                    )
                ) as one_ways
            FROM t_route_one_way
            GROUP BY route_id
            ) tro
            ON (tr.route_id = tro.route_id)
        WHERE
            tr.gigya_uid = %(gigya_uid)s
        GROUP BY tr.route_id, tro.one_ways
        ORDER BY tr.save_timestamp DESC;
    '''

    parameters_dict: dict = {'gigya_uid': gigya_uid}
    res = execute_select_statement(sql, parameters_dict)

    return res


def create_route(gigya_uid: str, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')
    origin_latitude = kwargs.pop('origin_latitude')
    origin_longitude = kwargs.pop('origin_longitude')
    destination_latitude = kwargs.pop('destination_latitude')
    destination_longitude = kwargs.pop('destination_longitude')

    sql = f'''
      INSERT INTO
        t_route(
          gigya_uid,
          {', '.join(kwargs.keys())},
          origin_location,
          destination_location,
          insert_timestamp,
          insert_user_id
        ) VALUES (
          %(gigya_uid)s,
          %({')s, %('.join(kwargs.keys())})s,
          ST_GeomFromText('POINT(%(origin_latitude)s %(origin_longitude)s)', 4326),
          ST_GeomFromText('POINT(%(destination_latitude)s %(destination_longitude)s)', 4326),
          %(now_str)s,
          %(gigya_uid)s
        )
        RETURNING route_id;
    '''

    params = {
        'gigya_uid': gigya_uid,
        **kwargs,
        'origin_latitude': origin_latitude,
        'origin_longitude': origin_longitude,
        'destination_latitude': destination_latitude,
        'destination_longitude': destination_longitude,
        'now_str': now_str
    }
    rec = execute_insert_statement(sql, params, returning=True)
    return rec[0][0] if rec else None


def delete_t_route(gigya_uid: str, route_id: int) -> int:
    sql = '''
        DELETE FROM
            t_route
        WHERE
            route_id = %(route_id)s
        AND
            gigya_uid = %(gigya_uid)s;
    '''
    params = {'gigya_uid': gigya_uid, 'route_id': route_id}
    return execute_delete_statement(sql, params)


def update_route(gigya_uid: str, route_id, **kwargs) -> int:
    now_str = convert_datetime_to_str(get_current_datetime(), '%Y-%m-%d %H:%M:%S.%f')

    origin_latitude = kwargs.pop('origin_latitude')
    origin_longitude = kwargs.pop('origin_longitude')
    destination_latitude = kwargs.pop('destination_latitude')
    destination_longitude = kwargs.pop('destination_longitude')

    update_sets = create_update_set_sql(**kwargs)

    if origin_latitude and origin_longitude:
        update_sets += "\n ,origin_location = ST_GeomFromText('POINT(%(origin_latitude)s %(origin_longitude)s)', 4326)"
    if destination_latitude and destination_longitude:
        update_sets += "\n ,destination_location = " \
                       "ST_GeomFromText('POINT(%(destination_latitude)s %(destination_longitude)s)', 4326)"

    sql = f'''
        UPDATE
            t_route
        SET
          {update_sets}
        WHERE
            delete_flag = False
            AND route_id = %(route_id)s;
    '''

    params = {
        'gigya_uid': gigya_uid,
        'route_id': route_id,
        **kwargs,
        'origin_latitude': origin_latitude,
        'origin_longitude': origin_longitude,
        'destination_latitude': destination_latitude,
        'destination_longitude': destination_longitude,
        'now_str': now_str
    }
    return execute_update_statement(sql, params)


def get_joined_route(gigya_uid: str, route_id: int) -> dict:
    sql: str = '''
        SELECT
            tr.route_id
            , tr.user_vehicle_id
            , tr.save_timestamp
            , tr.origin_name
            , ST_AsGeoJson(tr.origin_location) as origin_location
            , tr.origin_place_id
            , tr.destination_name
            , ST_AsGeoJson(tr.destination_location) as destination_location
            , tr.destination_place_id
            , tr.ride_date
            , tr.weather
            , tr.weather_icon
            , tro.one_ways
            , tbp.bicycle_parking
        FROM
            t_route tr
            LEFT JOIN (
                SELECT
                    tro2.route_id
                    , jsonb_agg(
                        jsonb_strip_nulls(
                            jsonb_build_object(
                                'route_one_way_id', tro2.route_one_way_id,
                                'round_trip_type_code', tro2.round_trip_type_code,
                                'duration', tro2.duration,
                                'distance', tro2.distance,
                                'route_type', tro2.route_type,
                                'route_type_branch_no', tro2.route_type_branch_no,
                                'route_via_points', trv.route_via_points
                            )
                        )
                    ) as one_ways
                FROM t_route_one_way tro2
                    LEFT JOIN (
                        SELECT
                            route_id
                            , route_one_way_id
                            , json_agg(
                                jsonb_strip_nulls(
                                    jsonb_build_object(
                                        'route_via_point_type', route_via_point_type,
                                        'route_via_point_id', route_via_point_id,
                                        'route_via_point_location', ST_AsGeoJson(route_via_point_location),
                                        'route_via_point_place_id', route_via_point_place_id
                                    )
                                )
                            ) as route_via_points
                        FROM t_route_via_point
                        GROUP BY route_id, route_one_way_id
                    ) trv
                    ON(tro2.route_id = trv.route_id AND tro2.route_one_way_id = trv.route_one_way_id)
                GROUP BY tro2.route_id
            ) tro
            ON(tr.route_id = tro.route_id)
            LEFT JOIN (
                SELECT
                    route_id
                    , jsonb_agg(
                        jsonb_strip_nulls(
                            jsonb_build_object(
                                'bicycle_parking_id', bicycle_parking_id,
                                'bicycle_parking_name', bicycle_parking_name,
                                'bicycle_parking_distance', bicycle_parking_distance,
                                'bicycle_parking_location', ST_AsGeoJson(bicycle_parking_location),
                                'bicycle_parking_place_id', bicycle_parking_place_id
                            )
                        )
                    ) as bicycle_parking
                FROM t_bicycle_parking
                GROUP BY route_id
            ) tbp
            ON(tr.route_id = tbp.route_id)
        WHERE
            tr.route_id = %(route_id)s
            AND tr.gigya_uid = %(gigya_uid)s
            AND tr.delete_flag = false
        GROUP BY tr.route_id, tro.one_ways, tbp.bicycle_parking
    '''

    params = {
        "route_id": route_id,
        "gigya_uid": gigya_uid
    }

    rec = execute_select_statement(sql, params)

    return rec[0] if rec else None
