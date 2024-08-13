import common.cerberus.setting.basic_rules as br
from common.aws.dynamodb import DynamoDb

# dynamoDb定数クラスの初期化
dynamo_db = DynamoDb()
dynamo_db.set_data()


REQUIRED_CATEGORY_ID: dict = {
    'categoryId': {
        **br.REQUIRED_COMMON_INT
    }
}

REQUIRED_ID_TOKEN: dict = {
    'id_token': {
        **br.REQUIRED_COMMON_STRING
    }
}

REQUIRED_GIGYA_UID: dict = {
    "gigya_uid": {
        **br.REQUIRED_COMMON_STRING,
        "minlength": 1,
        "maxlength": 32
    }
}

OPTIONAL_GIGYA_UID: dict = {
    "gigya_uid": {
        **br.OPTIONAL_COMMON_STRING
    }
}

REQUIRED_DEVICE_ID: dict = {
    "device_id": {
        **br.REQUIRED_COMMON_STRING,
        "minlength": 36,
        "maxlength": 36
    }
}

REQUIRED_DEVICE_TOKEN: dict = {
    "device_token": {
        **br.REQUIRED_COMMON_STRING
    }
}

REQUIRED_VEHICLE_ID: dict = {
    "vehicle_id": {
        **br.REQUIRED_VEHICLE_ID,
        "minlength": 12,
        "maxlength": 12,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x2", "0x23", "0x103"]
        }
    }
}


OPTIONAL_VEHICLE_ID: dict = {
    "vehicle_id": {
        **br.OPTIONAL_VEHICLE_ID,
        "minlength": 12,
        "maxlength": 12,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x23", "0x103"]
        }
    }
}

REQUIRED_MODEL_CD: dict = {
    "model_code": {
        **br.REQUIRED_ALPHANUMERIC_STRING,
        "minlength": 4,
        "maxlength": 4
    }
}

OPTIONAL_MODEL_CD: dict = {
    "model_code": {
        **br.OPTIONAL_ALPHANUMERIC_STRING,
        "minlength": 4,
        "maxlength": 4
    }
}

REQUIRED_VEHICLE_NAME: dict = {
    "vehicle_name": {
        **br.REQUIRED_COMMON_STRING,
        "minlength": 1,
        "maxlength": 50,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x2", "0x23", "0x28"]
        }
    }
}

OPTIONAL_VEHICLE_NAME: dict = {
    "vehicle_name": {
        'type': 'string',
        'required': False,
        'nullable': False,
        'empty': False,
        "minlength": 1,
        "maxlength": 50,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x23", "0x28"]
        }
    }
}

REQUIRED_RIDE_HISTORY_ID: dict = {
    "ride_history_id": {
        **br.REQUIRED_COMMON_STRING
    }
}

OPTIONAL_RIDE_NAME: dict = {
    "ride_name": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 1,
        "maxlength": 35,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ['0x28']
        }
    }
}

OPTIONAL_BOOKMARK_FLG: dict = {
    "bookmark_flg": {
        **br.OPTIONAL_COMMON_BOOLEAN
    }
}

OPTIONAL_BATTERY_REMIND_CD: dict = {
    "battery_remind_cd": {
        **br.OPTIONAL_NUMERIC_STRING,
        "allowed": [v for v in DynamoDb().constants.get('BATTERY_REMIND').values()]
    }
}

OPTIONAL_HOME_ASSIST_MODE_NUMBER: dict = {
    "home_assist_mode_number": {
        **br.OPTIONAL_COMMON_STRING,
        "allowed": [v for v in DynamoDb().constants.get('ASSIST_MODE_NUMBER').values()]
    }
}

OPTIONAL_MAINTAIN_LOCATION: dict = {
    "maintain_location": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 1,
        "maxlength": 100,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x100", "0x28"]
        }
    }
}

SHOP_NAME: dict = {
    "shop_name": {
        **br.REQUIRED_COMMON_STRING,
        "minlength": 1,
        "maxlength": 30,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ['0x2', '0x23', '0x28']
        }
    }
}

SHOP_TEL: dict = {
    "shop_tel": {
        **br.OPTIONAL_NUMERIC_STRING,
        "minlength": 1,
        "maxlength": 11,
        "meta": {
            "message_cd": "0x100",
            "err_cds": ['0x100', '0x28']
        }
    }
}

SHOP_LOCATION: dict = {
    "shop_location": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 1,
        "maxlength": 100,
        "meta": {
            "message_cd": "0x28",
            "err_cds": ['0x28']
        }
    }
}

USER_VEHICLE_ID: dict = {
    "user_vehicle_id": {
        **br.REQUIRED_COMMON_INT,
    }
}

OPTIONAL_USER_VEHICLE_ID: dict = {
    "user_vehicle_id": {
        **br.OPTIONAL_COMMON_INT,
    }
}

REGULAR_SHOP_NAME: dict = {
    "regular_shop_name": {
        **br.REQUIRED_COMMON_STRING,
        "minlength": 1,
        "maxlength": 30,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ['0x2', '0x23', '0x28']
        }
    }
}

REGULAR_SHOP_TEL: dict = {
    "regular_shop_tel": {
        **br.OPTIONAL_NUMERIC_STRING,
        "minlength": 1,
        "maxlength": 11,
        "meta": {
            "message_cd": "0x100",
            "err_cds": ['0x100', '0x28']
        }
    }
}

REGULAR_SHOP_LOCATION: dict = {
    "regular_shop_location": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 1,
        "maxlength": 100,
        "meta": {
            "message_cd": "0x28",
            "err_cds": ['0x28']
        }
    }
}

BOOKMARK_FLG: dict = {
    "bookmark_flg": {
        **br.OPTIONAL_COMMON_BOOLEAN,
    }
}
LIMIT: dict = {
    "limit": {
        **br.OPTIONAL_COMMON_INT,
    }
}
OFFSET: dict = {
    "offset": {
        **br.OPTIONAL_COMMON_INT,
    }
}

MAINTAIN_CONSCIOUSNESS: dict = {
    "maintain_consciousness": {
        **br.REQUIRED_COMMON_STRING,
        "allowed": [v for v in DynamoDb().constants.get('MAINTENANCE_CONSCIOUSNESS').values()]
    }
}

MAINTAIN_ALERTS: dict = {
    "maintain_alerts": {
        **br.OPTIONAL_COMMON_LIST,
    }
}

REQUIRED_MAINTAIN_HISTORY_ID: dict = {
    "maintain_history_id": {
        **br.REQUIRED_COMMON_INT,
    }
}

REQUIRED_MAINTAIN_ITEM_CODE: dict = {
    "maintain_item_code": {
        **br.REQUIRED_NUMERIC_STRING,
        "minlength": 5,
        "maxlength": 5,
    }
}

OPTIONAL_MAINTAIN_ITEM_CODE: dict = {
    "maintain_item_code": {
        **br.OPTIONAL_NUMERIC_STRING,
        "minlength": 5,
        "maxlength": 5,
    }
}

REQUIRED_MAINTAIN_IMPLEMENT_DATE: dict = {
    "maintain_implement_date": {
        **br.REQUIRED_MAINTAIN_IMPLEMENT_DATE,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x23", "0x102", "0x107", "0x108"]
        }
    }
}

REQUIRED_DU_SERIAL_NUMBER: dict = {
    "du_serial_number": {
        **br.REQUIRED_ALPHANUMERIC_STRING,
        "minlength": 1,
        "maxlength": 50,
    }
}

REQUIRED_DU_LAST_ODOMETER: dict = {
    "du_last_odometer": {
        **br.REQUIRED_COMMON_INT,
    }
}

REQUIRED_DU_ODOMETER: dict = {
    "du_odometer": {
        **br.REQUIRED_COMMON_INT,
    }
}

BEGIN: dict = {
    "begin": {
        **br.OPTIONAL_TIMESTAMP_STRING,
    }
}

END: dict = {
    "end": {
        **br.OPTIONAL_TIMESTAMP_STRING,
        "greater_date": "begin",
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x106"]
        }
    }
}

REQUIRED_DU_LAST_TIMESTAMP: dict = {
    "du_last_timestamp": {
        **br.REQUIRED_TIMESTAMP_STRING,
    }
}

REQUIRED_TIMESTAMP: dict = {
    "timestamp": {
        **br.REQUIRED_TIMESTAMP_STRING,
    }
}

START_TIMESTAMP: dict = {
    "start_timestamp": {
        **br.REQUIRED_TIMESTAMP_STRING,
    }
}

END_TIMESTAMP: dict = {
    "end_timestamp": {
        **br.OPTIONAL_TIMESTAMP_STRING,
    }
}

TRIP_DISTANCE: dict = {
    "trip_distance": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

TRIP_TIME: dict = {
    "trip_time": {
        **br.REQUIRED_COMMON_INT,
    }
}

TOTAL_CALORIE: dict = {
    "total_calorie": {
        **br.REQUIRED_COMMON_INT,
    }
}

RADAR_TOTAL_CALORIE: dict = {
    "total_calorie": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

BATTERY_CONSUMPTION: dict = {
    "battery_consumption": {
        **br.REQUIRED_COMMON_INT,
    }
}

AVERAGE_SPEED: dict = {
    "average_speed": {
        **br.REQUIRED_COMMON_INT,
    }
}

RADAR_AVERAGE_SPEED: dict = {
    "average_speed": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

MAX_SPEED: dict = {
    "max_speed": {
        **br.REQUIRED_COMMON_INT,
    }
}

RADAR_MAX_SPEED: dict = {
    "max_speed": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

MAX_PEDALING_POWER: dict = {
    "max_pedaling_power": {
        **br.REQUIRED_COMMON_INT,
    }
}

RADAR_MAX_PEDALING_POWER: dict = {
    "max_pedaling_power": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

MAX_CADENCE: dict = {
    "max_cadence": {
        **br.REQUIRED_COMMON_INT,
    }
}

RADAR_MAX_CADENCE: dict = {
    "max_cadence": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

RIDE_TRACKS: dict = {
    "ride_tracks": {
        **br.OPTIONAL_COMMON_LIST,
    }
}

OPTION_MAINTAIN_LOCATION: dict = {
    "maintain_location": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 1,
        "maxlength": 30,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ['0x28']
        }
    }
}

OPTION_MAINTAIN_COST: dict = {
    "maintain_cost": {
        **br.OPTIONAL_COMMON_INT,
        "min": 0,
        "max": 10000000,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x104", "0x42", "0x43"]
        }
    }
}

OPTION_MAINTAIN_REQUIRED_TIME: dict = {
    "maintain_required_time": {
        **br.OPTIONAL_COMMON_INT,
        "min": 0,
        "max": 100000,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x104", "0x42", "0x43"]
        }
    }
}

OPTION_MAINTAIN_MEMO: dict = {
    "maintain_memo": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 0,
        "maxlength": 2000,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x27", "0x28"]
        }
    }
}

REQUIRED_MAINTAIN_IMAGE_IDS: dict = {
    "maintain_image_ids": {
        **br.REQUIRED_COMMON_LIST,
        "minlength": 3,
        "maxlength": 3,
        'schema': {
            **br.OPTIONAL_COMMON_STRING,
            "minlength": 36,
            "maxlength": 36,
            "regex": r"^[a-zA-Z0-9-]+$",
        }
    }
}

REQUIRED_UPLOAD_FILE_COUNTS: dict = {
    "upload_file_counts": {
        **br.REQUIRED_COMMON_INT,
        "min": 1,
        "max": 3,
    }
}

REQUIRED_MANAGED_FLAG: dict = {
    "managed_flag": {
        **br.REQUIRED_COMMON_BOOLEAN
    }
}

OPTIONAL_MANAGED_FLAG: dict = {
    "managed_flag": {
        'type': 'boolean',
        'required': False,
        'nullable': False,
        'empty': False,
    }
}

REQUIRED_PERIPHERAL_IDENTIFIER: dict = {
    "peripheral_identifier": {
        **br.REQUIRED_COMMON_STRING,
        'check_with': br.validate_alphanumeric_hyphen
    }
}

OPTIONAL_PERIPHERAL_IDENTIFIER: dict = {
    "peripheral_identifier": {
        **br.OPTIONAL_COMMON_STRING,
        'check_with': br.validate_alphanumeric_hyphen
    }
}

OPTIONAL_COMPLETE_LOCAL_NAME: dict = {
    "complete_local_name": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 1,
        "maxlength": 255
    }
}

REQUIRED_REGISTERED_FLAG: dict = {
    "registered_flag": {
        **br.REQUIRED_COMMON_BOOLEAN
    }
}

OPTIONAL_REGISTERED_FLAG: dict = {
    "registered_flag": {
        'type': 'boolean',
        'required': False,
        'nullable': False,
        'empty': False,
    }
}

REQUIRED_UNEXPECTED_DATA: dict = {
    "unexpected_data": {
        **br.REQUIRED_COMMON_DICT,
    }
}

REQUIRED_CCU_ID: dict = {
    "ccu_id": {
        **br.REQUIRED_CCU_ID,
        "minlength": 14,
        "maxlength": 14,
    }
}

REQUIRED_LATITUDE: dict = {
    "latitude": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

REQUIRED_LONGITUDE: dict = {
    "longitude": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

REQUIRED_DESTINATION_LATITUDE: dict = {
    "destination_latitude": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

OPTIONAL_DESTINATION_LATITUDE: dict = {
    "destination_latitude": {
        **br.OPTIONAL_COMMON_FLOAT,
    }
}

REQUIRED_DESTINATION_LONGITUDE: dict = {
    "destination_longitude": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

OPTIONAL_DESTINATION_LONGITUDE: dict = {
    "destination_longitude": {
        **br.OPTIONAL_COMMON_FLOAT,
    }
}

REQUIRED_ORIGIN_LATITUDE: dict = {
    "origin_latitude": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

OPTIONAL_ORIGIN_LATITUDE: dict = {
    "origin_latitude": {
        **br.OPTIONAL_COMMON_FLOAT,
    }
}

REQUIRED_ORIGIN_LONGITUDE: dict = {
    "origin_longitude": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

OPTIONAL_ORIGIN_LONGITUDE: dict = {
    "origin_longitude": {
        **br.OPTIONAL_COMMON_FLOAT,
    }
}

OPTIONAL_RADIUS: dict = {
    "radius": {
        **br.OPTIONAL_COMMON_INT,
    }
}

OPTIONAL_WEIGHT: dict = {
    "weight": {
        **br.OPTIONAL_COMMON_FLOAT,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x02", "0x03", "0x23"]
        }
    }
}

OPTIONAL_NICKNAME: dict = {
    "nickname": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 1,
        "maxlength": 16,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x02", "0x03", "0x23", "0x28"]
        }
    }
}

OPTIONAL_BIRTH_DATE: dict = {
    "birth_date": {
        **br.OPTIONAL_CALENDAR_STRING,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x02", "0x03", "0x23"]
        }
    }
}

OPTIONAL_MAX_HEART_RATE: dict = {
    "max_heart_rate": {
        **br.OPTIONAL_COMMON_INT,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x02", "0x03", "0x23"]
        }
    }
}

REQUIRED_EQUIPMENT_WEIGHT: dict = {
    "equipment_weight": {
        **br.OPTIONAL_COMMON_FLOAT,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x02", "0x03", "0x23"]
        }
    }
}

OPTIONAL_EQUIPMENT_WEIGHT: dict = {
    "equipment_weight": {
        **br.OPTIONAL_COMMON_FLOAT,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x02", "0x03", "0x23"]
        }
    }
}

OPTIONAL_VEHICLE_NICKNAME: dict = {
    "vehicle_nickname": {
        'type': 'string',
        'required': False,
        'nullable': False,
        'empty': False,
        "minlength": 1,
        "maxlength": 18,
        "meta": {
            "message_cd": "0x9999",
            "err_cds": ["0x23", "0x28"]
        }
    }
}

REQUIRED_DATA_SOURCE_KIND_CODE: dict = {
    "data_source_kind_code": {
        **br.REQUIRED_COMMON_STRING,
        "allowed": [v for v in DynamoDb().constants.get('WORKOUT_DATA_SOURCE_KIND_CODE').values()],
        "minlength": 2,
        "maxlength": 2,
    }
}

REQUIRED_DATA_SOURCE_ID: dict = {
    "data_source_id": {
        **br.REQUIRED_COMMON_STRING,
        "minlength": 1,
        "maxlength": 50,
    }
}

REQUIRED_WORKOUT_TIME: dict = {
    "workout_time": {
        **br.REQUIRED_COMMON_INT,
    }
}

OPTIONAL_HEARTBEAT_ZONE_1_TIME: dict = {
    "heartbeat_zone_1_time": {
        **br.OPTIONAL_COMMON_INT,
    }
}

OPTIONAL_HEARTBEAT_ZONE_2_TIME: dict = {
    "heartbeat_zone_2_time": {
        **br.OPTIONAL_COMMON_INT,
    }
}

OPTIONAL_HEARTBEAT_ZONE_3_TIME: dict = {
    "heartbeat_zone_3_time": {
        **br.OPTIONAL_COMMON_INT,
    }
}

OPTIONAL_HEARTBEAT_ZONE_4_TIME: dict = {
    "heartbeat_zone_4_time": {
        **br.OPTIONAL_COMMON_INT,
    }
}

OPTIONAL_HEARTBEAT_ZONE_5_TIME: dict = {
    "heartbeat_zone_5_time": {
        **br.OPTIONAL_COMMON_INT,
    }
}

REQUIRED_AVERAGE_HEART_RATE: dict = {
    "average_heart_rate": {
        **br.REQUIRED_COMMON_INT,
    }
}

OPTIONAL_RADAR_AVERAGE_HEART_RATE: dict = {
    "average_heart_rate": {
        **br.OPTIONAL_COMMON_FLOAT,
    }
}

REQUIRED_AVERAGE_CADENCE: dict = {
    "average_cadence": {
        **br.REQUIRED_COMMON_INT,
    }
}

RADAR_REQUIRED_AVERAGE_CADENCE: dict = {
    "average_cadence": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

OPTIONAL_WEATHER: dict = {
    "weather": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 3,
        "maxlength": 3,
    }
}

OPTIONAL_TEMPERATURE: dict = {
    "temperature": {
        **br.OPTIONAL_COMMON_FLOAT,
    }
}

OPTIONAL_HUMIDITY: dict = {
    "humidity": {
        **br.OPTIONAL_COMMON_INT,
    }
}

REQUIRED_WORKOUT_MODE_CODE: dict = {
    "workout_mode_code": {
        **br.REQUIRED_COMMON_STRING,
        "allowed": [v for v in DynamoDb().constants.get('WORKOUT_MODE_CODE').values()],
        "minlength": 2,
        "maxlength": 2,
    }
}

REQUIRED_AVERAGE_PEDALING_POWER: dict = {
    "average_pedaling_power": {
        **br.REQUIRED_COMMON_INT,
    }
}

REQUIRED_DESTINATION_NAME: dict = {
    "destination_name": {
        **br.REQUIRED_COMMON_STRING,
        "minlength": 1,
        "maxlength": 100,
    }
}

OPTIONAL_DESTINATION_NAME: dict = {
    "destination_name": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 1,
        "maxlength": 100,
    }
}

OPTIONAL_DESTINATION_PLACE_ID: dict = {
    "destination_place_id": {
        **br.OPTIONAL_COMMON_PLACE_ID
    }
}

REQUIRED_ORIGIN_NAME: dict = {
    "origin_name": {
        **br.REQUIRED_COMMON_STRING,
        "minlength": 1,
        "maxlength": 100,
    }
}

OPTIONAL_ORIGIN_NAME: dict = {
    "origin_name": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 1,
        "maxlength": 100,
    }
}

OPTIONAL_ORIGIN_PLACE_ID: dict = {
    "origin_place_id": {
        **br.OPTIONAL_COMMON_PLACE_ID
    }
}

REQUIRED_SAVE_TIMESTAMP: dict = {
    "save_timestamp": {
        **br.REQUIRED_TIMESTAMP_STRING,
    }
}

REQUIRED_RIDE_DATE: dict = {
    "ride_date": {
        **br.REQUIRED_CALENDAR_STRING
    }
}

OPTIONAL_RIDE_DATE: dict = {
    "ride_date": {
        **br.OPTIONAL_CALENDAR_STRING
    }
}

OPTIONAL_WEATHER_ICON: dict = {
    "weather_icon": {
        **br.OPTIONAL_COMMON_STRING,
        "minlength": 3,
        "maxlength": 3,
    }
}

REQUIRED_ONE_WAYS: dict = {
    "one_ways": {
        **br.REQUIRED_COMMON_LIST,
        'schema': {
            'type': 'dict',
            'schema': {
                'round_trip_type_code': {
                    **br.REQUIRED_COMMON_STRING,
                    "allowed": [v for v in DynamoDb().constants.get('ROUND_TRIP_TYPE_CODE').values()],
                    "minlength": 2,
                    "maxlength": 2
                },
                "route_type": {
                    **br.REQUIRED_COMMON_STRING,
                    "allowed": [v for v in DynamoDb().constants.get('ROUTE_TYPE_CODE').values()],
                    "minlength": 2,
                    "maxlength": 2
                },
                "route_type_branch_no": {
                    **br.REQUIRED_COMMON_INT
                },
                "distance": {
                    **br.REQUIRED_COMMON_INT
                },
                "duration": {
                    **br.REQUIRED_COMMON_INT
                },
                "route_via_points": {
                    **br.OPTIONAL_COMMON_LIST,
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "route_via_point_place_id": {
                                **br.OPTIONAL_COMMON_PLACE_ID
                            },
                            **REQUIRED_LATITUDE,
                            **REQUIRED_LONGITUDE,
                            "route_via_point_type": {
                                **br.OPTIONAL_COMMON_STRING,
                                "minlength": 2,
                                "maxlength": 2
                            }
                        }
                    }
                }
            }
        }
    }
}

OPTIONAL_ONE_WAYS: dict = {
    "one_ways": {
        **br.OPTIONAL_COMMON_LIST,
        'schema': {
            'type': 'dict',
            'schema': {
                'round_trip_type_code': {
                    **br.REQUIRED_COMMON_STRING,
                    "allowed": [v for v in DynamoDb().constants.get('ROUND_TRIP_TYPE_CODE').values()],
                    "minlength": 2,
                    "maxlength": 2
                },
                "route_type": {
                    **br.REQUIRED_COMMON_STRING,
                    "allowed": [v for v in DynamoDb().constants.get('ROUTE_TYPE_CODE').values()],
                    "minlength": 2,
                    "maxlength": 2
                },
                "route_type_branch_no": {
                    **br.REQUIRED_COMMON_INT
                },
                "distance": {
                    **br.REQUIRED_COMMON_INT
                },
                "duration": {
                    **br.REQUIRED_COMMON_INT
                },
                "route_via_points": {
                    **br.OPTIONAL_COMMON_LIST,
                    "schema": {
                        "type": "dict",
                        "schema": {
                            "route_via_point_place_id": {
                                **br.OPTIONAL_COMMON_PLACE_ID
                            },
                            **REQUIRED_LATITUDE,
                            **REQUIRED_LONGITUDE,
                            "route_via_point_type": {
                                **br.OPTIONAL_COMMON_STRING,
                                "minlength": 2,
                                "maxlength": 2
                            }
                        }
                    }
                }
            }
        }
    }
}

OPTIONAL_BICYCLE_PARKING: dict = {
    "bicycle_parking": {
        **br.OPTIONAL_COMMON_LIST,
        'schema': {
            'type': 'dict',
            'schema': {
                "bicycle_parking_name": {
                    **br.REQUIRED_COMMON_STRING
                },
                "bicycle_parking_distance": {
                    **br.REQUIRED_COMMON_INT
                },
                **REQUIRED_LATITUDE,
                **REQUIRED_LONGITUDE,
                "bicycle_parking_place_id": {
                    **br.OPTIONAL_COMMON_PLACE_ID
                }
            }
        }
    }
}

RADAR_REQUIRED_AVERAGE_PEDALING_POWER: dict = {
    "average_pedaling_power": {
        **br.REQUIRED_COMMON_FLOAT,
    }
}

REQUIRED_ROUTE_ID: dict = {
    "route_id": {
        **br.REQUIRED_COMMON_INT,
    }
}

OPTIONAL_BIKE_RADAR_FLAG: dict = {
    "bike_radar_flag": {
        **br.OPTIONAL_COMMON_BOOLEAN,
    }
}
