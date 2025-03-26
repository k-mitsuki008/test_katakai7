import os
from decimal import Decimal
import boto3
import pytest
from moto import mock_dynamodb
from common.rds.connect import DbConnection
from common.rds import execute_insert_statement, execute_delete_statement, execute_select_statement
from common.aws.dynamodb import DynamoDb

# LOCALDB接続情報
rds_params = {
    'username': 'admin',
    'password': 'spvc_admin',
    'host': 'localhost',
    'port': 15432,
    'dbClusterIdentifier': 'spvc_local',
}


@pytest.fixture(scope='class', autouse=True)
def dynamodb_setup():
    # DynamoDB テーブル定義
    with mock_dynamodb():
        # DynamoDbリソースをMock化して定数クラスを上書き
        const_dynamodb = DynamoDb()
        const_dynamodb.dynamodb_resource = boto3.resource(
            'dynamodb',
            region_name=os.environ.get('SECRET_MANAGER_REGION', os.environ.get('AURORA_SECRET_MANAGER_REGION'))
        )
        # メッセージマスタ、定数マスタを初期化
        const_dynamodb.messages = None
        const_dynamodb.constants = None
        dynamodb = const_dynamodb.resource()

        # 定数マスタ生成
        dynamodb.create_table(
            TableName='m_constant',
            KeySchema=[
                {'AttributeName': 'category_cd', 'KeyType': 'HASH'},
                {'AttributeName': 'code', 'KeyType': 'RANGE'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'category_cd', 'AttributeType': 'S'},
                {'AttributeName': 'code', 'AttributeType': 'S'},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            }
        )
        m_constant_list = [
            {"category_cd": "MAINTENANCE_TYPE_CODE", "code": "TIME", "value": "01"},
            {"category_cd": "MAINTENANCE_TYPE_CODE", "code": "DISTANCE", "value": "02"},
            {"category_cd": "MAINTENANCE_TYPE_CODE", "code": "ROUTINE", "value": "03"},
            {"category_cd": "SHOP_TYPE", "code": "REGULAR", "value": "01"},
            {"category_cd": "SHOP_TYPE", "code": "PURCHASE", "value": "02"},
            {"category_cd": "FILE_TYPE", "code": "UNEXPECTED", "value": "ERRD"},
            {"category_cd": "MAINTENANCE_CONSCIOUSNESS", "code": "HIGH", "value": "01"},
            {"category_cd": "MAINTENANCE_CONSCIOUSNESS", "code": "MIDDLE", "value": "02"},
            {"category_cd": "MAINTENANCE_CONSCIOUSNESS", "code": "LOW", "value": "03"},
            {"category_cd": "MAINTENANCE_EXPLANATION_TYPE", "code": "STRING", "value": 1},
            {"category_cd": "MAINTENANCE_EXPLANATION_TYPE", "code": "IMAGE", "value": 2},
            {"category_cd": "MAINTENANCE_VEHICLE_IMAGE_SUFFIX", "code": "SUFFIX", "value": "_top.png"},
            {"category_cd": "BATTERY_REMIND", "code": "LONG_LIFE", "value": "01"},
            {"category_cd": "BATTERY_REMIND", "code": "ASSIST", "value": "02"},
            {"category_cd": "BATTERY_REMIND", "code": "NO_NOTIFICATION", "value": "00"},
            {"category_cd": "ASSIST_MODE_NUMBER", "code": "EXPW", "value": "00"},
            {"category_cd": "ASSIST_MODE_NUMBER", "code": "HIGH", "value": "01"},
            {"category_cd": "ASSIST_MODE_NUMBER", "code": "STD", "value": "02"},
            {"category_cd": "ASSIST_MODE_NUMBER", "code": "ECO", "value": "03"},
            {"category_cd": "ASSIST_MODE_NUMBER", "code": "PLUS_ECO", "value": "04"},
            {"category_cd": "TIMEOUT", "code": "REQUEST_TIMEOUT", "value": 10},
            {"category_cd": "SESSION_EXPIRES", "code": "SESSION_EXPIRES", "value": 14},
            {"category_cd": "S3_URL_EXPIRES", "code": "S3_URL_EXPIRES", "value": 900},
            {"category_cd": "MAINTENANCE_ALERT_STATUS", "code": "UNNOTIFIED", "value": "0"},
            {"category_cd": "MAINTENANCE_ALERT_STATUS", "code": "NOTIFIED", "value": "1"},
            {"category_cd": "MAINTENANCE_ALERT_STATUS", "code": "FAILED", "value": "2"},
            {"category_cd": "S3_BUCKET_PREFIX", "code": "ICON", "value": "icons/"},
            {"category_cd": "S3_BUCKET_PREFIX", "code": "EXPLANATION",
             "value": "explanation-images/"},
            {"category_cd": "S3_BUCKET", "code": "UPLOAD", "value": "spvc-{env}-upload-items"},
            {"category_cd": "S3_BUCKET", "code": "UNEXPECTED", "value": "spvc-{env}-unexpected-data"},
            {"category_cd": "MAX_VEHICLE_COUNT", "code": "MAX_VEHICLE_COUNT", "value": 5},
            {"category_cd": "MAINTAIN_IMPLEMENT_DATE", "code": "MIN", "value": "2023-01-01"},
            {"category_cd": "INIT_VALUE", "code": "BATTERY_REMIND_CD", "value": "00"},
            {"category_cd": "INIT_VALUE", "code": "BATTERY_REMIND_SPOT_LATITUDE", "value": Decimal(str(153.9807))},
            {"category_cd": "INIT_VALUE", "code": "BATTERY_REMIND_SPOT_LONGITUDE", "value": Decimal(str(24.2867))},
            {"category_cd": "INIT_VALUE", "code": "BATTERY_REMIND_VOICE_NOTICE", "value": False},
            {"category_cd": "INIT_VALUE", "code": "SAFETY_RIDE_ALERT", "value": False},
            {"category_cd": "INIT_VALUE", "code": "LONG_DRIVE_ALERT", "value": False},
            {"category_cd": "INIT_VALUE", "code": "SPEED_OVER_ALERT", "value": False},
            {"category_cd": "INIT_VALUE", "code": "NO_LIGHT_ALERT", "value": False},
            {"category_cd": "INIT_VALUE", "code": "SAFETY_RIDE_VOICE_NOTICE", "value": False},
            {"category_cd": "INIT_VALUE", "code": "MAINTAIN_ITEM_ALERT", "value": True},
            {"category_cd": "INIT_VALUE", "code": "MAINTAIN_ITEM_ALERT_STATUS", "value": 0},
            {"category_cd": "INIT_VALUE", "code": "BOOKMARK_FLG", "value": False},
            {"category_cd": "INIT_VALUE", "code": "MAINTENANCE_CONSCIOUSNESS", "value": "01"},
            {"category_cd": "INIT_VALUE", "code": "HOME_ASSIST_MODE_NUMBER", "value": "02"},
            {"category_cd": "INIT_VALUE", "code": "NOTIFICATION_LIMIT", "value": 500},
            {"category_cd": "INIT_VALUE", "code": "MAINTENANCE_NOTIFICATION_TARGET", "value": 0},
            {"category_cd": "FIELD_NAME", "code": "vehicle_id", "value": "号機番号"},
            {"category_cd": "FIELD_NAME", "code": "vehicle_name", "value": "車両名"},
            {"category_cd": "FIELD_NAME", "code": "maintain_item_code", "value": "メンテナンス項目CD"},
            {"category_cd": "FIELD_NAME", "code": "maintain_item_alert", "value": "メンテナンス部位通知フラグ"},
            {"category_cd": "FIELD_NAME", "code": "maintain_alerts", "value": "メンテナンス通知フラグリスト"},
            {"category_cd": "FIELD_NAME", "code": "shop_name", "value": "購入店舗名"},
            {"category_cd": "FIELD_NAME", "code": "shop_tel", "value": "電話番号"},
            {"category_cd": "FIELD_NAME", "code": "shop_location", "value": "住所"},
            {"category_cd": "FIELD_NAME", "code": "regular_shop_name", "value": "普段利用店舗名"},
            {"category_cd": "FIELD_NAME", "code": "battery_remind_latitude", "value": "バッテリーリマインド通知緯度"},
            {"category_cd": "FIELD_NAME", "code": "battery_remind_longitude", "value": "バッテリーリマインド通知経度"},
            {"category_cd": "FIELD_NAME", "code": "battery_remind_cd", "value": "バッテリーリマインド通知設定CD"},
            {"category_cd": "FIELD_NAME", "code": "battery_remind_voice_notice", "value": "バッテリーリマインド音声通知"},
            {"category_cd": "FIELD_NAME", "code": "safety_ride_alert", "value": "セーフティライド通知"},
            {"category_cd": "FIELD_NAME", "code": "long_drive_alert", "value": "長時間運転アラート"},
            {"category_cd": "FIELD_NAME", "code": "speed_over_alert", "value": "制限速度超過アラート"},
            {"category_cd": "FIELD_NAME", "code": "no_light_alert", "value": "ライト無灯火アラート"},
            {"category_cd": "FIELD_NAME", "code": "safety_ride_voice_notice", "value": "セーフティライド音声通知"},
            {"category_cd": "FIELD_NAME", "code": "home_assist_mode_number", "value": "HOME設定アシストモード"},
            {"category_cd": "FIELD_NAME", "code": "end", "value": "期間設定終了日"},
            {"category_cd": "FIELD_NAME", "code": "begin", "value": "期間設定開始日"},
            {"category_cd": "FIELD_NAME", "code": "maintain_implement_date", "value": "日付"},
            {"category_cd": "OS_KIND", "code": "ANDROID", "value": "android"},
            {"category_cd": "OS_KIND", "code": "IOS", "value": "ios"},
            {"category_cd": "APP_INFO", "code": "EXPIRATION_DELTA", "value": 7},
            {"category_cd": "APP_INFO", "code": "IOS_APP_ID", "value": 7},
            {"category_cd": "APP_INFO", "code": "ANDROID_PKG_NAME", "value": "com.yamaha.buddy.app.dev"},
            {"category_cd": "APP_INFO", "code": "ANDROID_TRACK", "value": "alpha"},
            {"category_cd": "ROUND_TRIP_TYPE_CODE", "code": "OUTWARD", "value": "11"},
            {"category_cd": "ROUND_TRIP_TYPE_CODE", "code": "RETURN", "value": "12"},
            {"category_cd": "ROUND_TRIP_TYPE_CODE", "code": "ROUND_TRIP", "value": "10"},
            {"category_cd": "ROUND_TRIP_TYPE_CODE", "code": "UNSELECTED", "value": "90"},
            {"category_cd": "ROUTE_TYPE_CODE", "code": "GOOGLE_MAP_2", "value": "11"},
            {"category_cd": "ROUTE_TYPE_CODE", "code": "GOOGLE_MAP_3", "value": "12"},
            {"category_cd": "ROUTE_TYPE_CODE", "code": "MAPBOX_2", "value": "21"},
            {"category_cd": "SPOT_TYPE_CODE", "code": "CHARGING", "value": "10010"},
            {"category_cd": "WORKOUT_DATA_SOURCE_KIND_CODE", "code": "IOS", "value": "01"},
            {"category_cd": "WORKOUT_MODE_CODE", "code": "BURNING", "value": "10"},
            {"category_cd": "WORKOUT_MODE_CODE", "code": "FREE", "value": "20"},
            {"category_cd": "WORKOUT_MODE_CODE", "code": "LEARNING", "value": "30"},
        ]
        table = dynamodb.Table('m_constant')
        for item in m_constant_list:
            table.put_item(Item=item)

        # メッセージマスタ生成
        dynamodb.create_table(
            TableName='m_message',
            KeySchema=[{'AttributeName': 'message_cd', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'message_cd', 'AttributeType': 'S'}, ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            }
        )
        m_message_list = [
            {"message_cd": "E001", "message": "システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。"},
            {"message_cd": "E002", "message": "システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。"},
            {"message_cd": "E003", "message": "システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。"},
            {"message_cd": "E004", "message": "システムエラーが発生しました。\n時間をあけて再度操作をお願いいたします。"},
            {"message_cd": "E005", "message": "validation error"},
            {"message_cd": "E006", "message": "missing field"},
            {"message_cd": "E007", "message": "validation error"},
            {"message_cd": "E009", "message": "日付の形式が無効です。"},
            {"message_cd": "E010", "message": "{field}は必須入力項目です。"},
            {"message_cd": "E014", "message": "{field}には{info}以降の日付を入力してください。"},
            {"message_cd": "E016", "message": "{constraint}文字以下で入力してください。"},
            {"message_cd": "E017", "message": "{info}文字で入力してください。"},
            {"message_cd": "E018", "message": "{constraint}文字以上で入力してください。"},
            {"message_cd": "E019", "message": "半角数字で入力してください。"},
            {"message_cd": "E020", "message": "半角英数字で入力してください。"},
            {"message_cd": "E031", "message": "リストの長さは{0}としてください。"},
            {"message_cd": "E032", "message": "{constraint}以下で入力してください。"},
            {"message_cd": "E033", "message": "{constraint}以上で入力してください。"},
            {"message_cd": "E035", "message": "新しいバージョンのアプリがあります。\n最新のバージョンにアップデートしてください。"},
            {"message_cd": "E038", "message": "車両は{0}件まで登録できます。"},
            {"message_cd": "E040", "message": "入力された号機番号の車両はすでに登録されています。"},
            {"message_cd": "E042", "message": "{0}が存在しません。"},
            {"message_cd": "E043", "message": "型式が異なります。"},
            {"message_cd": "E044", "message": "1回目のメンテナンス記録を編集してください。"},
            {"message_cd": "E045", "message": "管理対象車両を変更してください。"},
            {"message_cd": "E051", "message": "メンテナンス実施日には本日以前の日付を入力してください。"},
            {"message_cd": "E052", "message": "入力できない日付です。"},
            {"message_cd": "N001", "message": "{0}の{1}のメンテナンスを推奨します。 長く安全に走行できるようメンテナンスを実施してください。"}
        ]
        table = dynamodb.Table('m_message')
        for item in m_message_list:
            table.put_item(Item=item)

        # セッションTBL生成
        dynamodb.create_table(
            TableName='t_session',
            KeySchema=[
                {'AttributeName': 'gigya_uid', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'gigya_uid', 'AttributeType': 'S'},
                {'AttributeName': 'session_id', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "session_id-index",
                    "KeySchema": [{"AttributeName": "session_id", "KeyType": "HASH"}],
                    "Projection": {
                        "ProjectionType": "ALL"
                    },
                    "ProvisionedThroughput": {
                        "ReadCapacityUnits": 1,
                        "WriteCapacityUnits": 1
                    }
                }
            ]
        )
        t_session_list = [
            {'gigya_uid': 'test_uid_01',
             'session_id': 'test_session_01_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
             'device_id': 'ANDROID-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
             'create_session_timestamp': '2022-05-13 12:34:56.789',
             'expire_session_timestamp': '2022-05-27 12:34:56.789'},
            {'gigya_uid': 'test_uid_02',
             'session_id': 'test_session_02_bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
             'device_id': 'ANDROID-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',
             'create_session_timestamp': '2022/10/07 15:54:44.843',
             'expire_session_timestamp': '2022/10/07 15:54:44.843'}
        ]
        table = dynamodb.Table('t_session')
        for item in t_session_list:
            table.put_item(Item=item)

        # メッセージマスタ生成
        dynamodb.create_table(
            TableName='t_app_version',
            KeySchema=[{'AttributeName': 'os', 'KeyType': 'HASH'}, {'AttributeName': 'app_version', 'KeyType': 'RANGE'}],
            AttributeDefinitions=[{'AttributeName': 'os', 'AttributeType': 'S'}, {'AttributeName': 'app_version', 'AttributeType': 'S'}],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            }
        )
        t_app_info_list = [
            {'os': 'android', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '1.1.0', 'app_build_number': 3, 'update_timestamp': 1703343600},   # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
            {'os': 'android', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '0.1.0', 'app_build_number': 2, 'expiration_timestamp': 1703948300, 'update_timestamp': 1703343500},  # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
            {'os': 'android', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '0.0.1', 'app_build_number': 1, 'expiration_timestamp': 1703948200, 'update_timestamp': 1703343400},  # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
            {'os': 'ios', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '0.0.0', 'app_build_number': 0, 'expiration_timestamp': 1703947400, 'update_timestamp': 1703342600},  # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
            {'os': 'ios', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '0.1.0', 'app_build_number': 1, 'update_timestamp': 1703343600}        # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
        ]
        table = dynamodb.Table('t_app_version')
        for item in t_app_info_list:
            table.put_item(Item=item)

        # モック化したメッセージマスタ、定数マスタを設定
        const_dynamodb.set_data()
        yield


@pytest.fixture(scope='function', autouse=True)
def db_setup(mocker):
    # 接続先のmock化
    mocker.patch('common.rds.connect.get_secret', return_value=rds_params)
    dc = DbConnection()
    dc.connect()

    init_t_user_shop_regular()
    init_t_device()
    init_t_user_setting_ride()
    init_t_user_shop_purchase()
    init_t_user_setting_maintain_item()
    init_t_user_setting_maintain()
    init_t_drive_unit_history()
    init_t_ride_track()
    init_t_ride_history()
    init_t_maintain_history()
    init_t_workout()
    init_t_bicycle_parking()
    init_t_route_via_point()
    init_t_route_one_way()
    init_t_route()
    init_t_user_vehicle()
    init_m_maintain_explanation()
    init_m_maintain_title()
    init_m_maintain_item()
    init_m_maintain_item_name()
    init_m_model()
    init_m_contact()
    init_t_user_setting()
    init_m_spot()

    add_m_contact()
    add_m_model()
    add_m_maintain_item_name()
    add_m_maintain_item()
    add_m_maintain_title()
    add_m_maintain_explanation()
    add_t_user_vehicle()
    add_t_maintain_history()
    add_t_ride_history()
    add_t_ride_track()
    add_t_drive_unit_history()
    add_t_user_setting_maintain()
    add_t_user_setting_maintain_item()
    add_t_user_shop_purchase()
    add_t_user_setting_ride()
    add_t_device()
    add_t_user_shop_regular()
    add_t_user_setting()
    add_m_spot()
    add_t_workout()
    add_t_route()
    add_t_route_one_way()
    add_t_bicycle_parking()
    add_t_route_via_point()

    yield
    dc.close()


def init_m_model():
    sql: str = 'DELETE FROM m_model;'
    return execute_delete_statement(sql)


def add_m_model():
    sql: str = '''
    INSERT INTO m_model( 
        model_code
        , model_name
        , sort_order
        , weight
        , charging_rated_output
        , bike_radar_flag
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    ('abcd','CROSSCORE RC',2, 15, 100, true, '2020/05/13 12:34:56.789','test_uid_01'),
    ('zzzz','DUMY_MODEL 01',1, 15, 100, false, '2020/05/13 12:34:56.789','test_uid_01');
    '''
    return execute_insert_statement(sql)


def init_m_maintain_item_name():
    sql: str = 'DELETE FROM m_maintain_item_name;'
    return execute_delete_statement(sql)


def add_m_maintain_item_name():
    sql: str = '''
    INSERT INTO m_maintain_item_name(
        maintain_item_code
        , maintain_item_name
        , maintain_file_name_icon
        , sort_order
    )
    VALUES
    ('00001', 'ホイール', 'abcde00001.png', 5),
    ('00002', 'タイヤ空気圧', 'abcde00002.png', 1),
    ('00003', 'タイヤ摩耗', 'abcde00003.png', 2),
    ('00004', 'チェーン動作', 'abcde00004.png', 3),
    ('00005', 'ブレーキ動作、摩耗', 'abcde00005.png', 4),
    -- ('00006', '前照灯', 'abcde00006.png', 6),
    -- ('00007', 'リフレクター', 'abcde00007.png', 7),
    -- ('00008', 'ベル', 'abcde00008.png', 8),
    ('00009', '定期点検', 'abcde00009.png', 9),
    ('00010', '別メンテナンス項目', 'abcde00010.png', 10);
    '''
    return execute_insert_statement(sql)


def init_m_maintain_item():
    sql: str = 'DELETE FROM m_maintain_item;'
    return execute_delete_statement(sql)


def add_m_maintain_item():
    sql: str = '''
    INSERT INTO m_maintain_item(
        maintain_item_code
        , model_code
        , maintain_type_code
        , maintain_interval_high
        , maintain_interval_middle
        , maintain_interval_low
        , maintain_file_name_top
    )
    VALUES
    ('00001', 'abcd', '02', 103, 203, 303, 'abcde00001_top.png'),
    ('00002', 'abcd', '01', 10, 20, 30, 'abcde00002_top.png'),
    ('00003', 'abcd', '02', 100, 200, 300,'abcde00003_top.png'),
    ('00004', 'abcd', '02', 101, 201, 301, 'abcde00004_top.png'),
    ('00005', 'abcd', '02', 102, 202, 302, 'abcde00005_top.png'),
    -- ('00006', 'abcd', '02', 11, 21, 31, 'abcde00006_top.png'),
    -- ('00007', 'abcd', '02', 12, 22, 32, 'abcde00007_top.png',),
    -- ('00008', 'abcd', '02', 13, 23, 33, 'abcde00008_top.png'),
    ('00009', 'abcd', '03', 14, 24, 34, 'abcde00009_top.png'),
    ('00001', 'zzzz', '01', 99, 99, 99, 'abcde00010_top.png');
    '''
    return execute_insert_statement(sql)


def init_m_maintain_title():
    sql: str = 'DELETE FROM m_maintain_title;'
    return execute_delete_statement(sql)


def add_m_maintain_title():
    sql: str = '''
    INSERT 
    INTO m_maintain_title( 
        model_code
        , maintain_item_code
        , maintain_title_code
        , explanation_title
        , sort_order
        , insert_timestamp
        , insert_user_id
    
    ) 
    VALUES 
    ('abcd', '00002', '001', '前後タイヤの点検', 1, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00002', '002', '前後タイヤの点検2', 2, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00003', '001', 'タイヤの摩耗、破損状態の点検', 1, '2020/05/13 12:34:56.789', 'test_uid_01');
    '''

    return execute_insert_statement(sql)


def init_m_maintain_explanation():
    sql: str = 'DELETE FROM m_maintain_explanation;'
    return execute_delete_statement(sql)


def add_m_maintain_explanation():
    sql: str = '''
    INSERT 
    INTO m_maintain_explanation( 
        model_code
        , maintain_item_code
        , maintain_title_code
        , maintain_explanation_code
        , explanation_type
        , explanation_body
        , sort_order
        , insert_timestamp
        , insert_user_id
    ) 
    VALUES 
    ('abcd', '00002', '001', '001', 1, 'タイヤのが適切でない状態て使用をされますと、急なパンク等の危険やタイヤの路面摩擦増加により、より強い力でこぐ必要が出たり、BTの消耗が早くなるといった不利益につながる危険があります。長く安全にご使用いただくために、定期的に状態を確認してください。', 1, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00002', '001', '002', 2, '00002_01_02.png', 2, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00002', '001', '003', 1, 'タイヤの空気圧を点検し、不適正な場合は空気圧を調整してください。', 3, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00002', '001', '004', 2, '00002_01_04.png', 4, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00002', '001', '005', 1, '空気圧は、YPJに乗車（体重60Kgの方）した状態での接地面の長さで簡易に判定することができます。', 5, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00002', '002', '001', 1, '前後のタイヤ点検_説明2', 5, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00003', '001', '001', 1, 'タイヤの変形、摩耗や破損といった異常箇所をそのままに使用をされますと、急なパンクや出かけた先で空気抜けの発生等の危険や、さらにそのまま走行してしまうとタイヤやホイールの傷や破損など部品の交換が必要となるなどの不利益につながる危険があります。長く安全にご使用いただくために、定期的に状態を確認してください。', 1, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00003', '001', '002', 2, '00003_01_02.png', 2, '2020/05/13 12:34:56.789', 'test_uid_01'),
    ('abcd', '00003', '001', '003', 1, 'タイヤが摩耗していないか、深い傷はないか、異物やくぎなどが刺さっていないかを点検します', 3, '2020/05/13 12:34:56.789', 'test_uid_01');
    '''

    return execute_insert_statement(sql)


def init_m_contact():
    sql: str = 'DELETE FROM m_contact;'
    return execute_delete_statement(sql)


def add_m_contact():
    sql: str = '''
    INSERT INTO m_contact( 
        model_code
        , contact_title
        , contact_text
        , contact_mail_address
        , insert_timestamp
        , insert_user_id
    ) 
    VALUES 
    ('abcd', '問合せタイトル', '問合せ本文', 'test@test.com', '2023/01/26 15:32:12.676', 'test_uid_01');
    '''
    return execute_insert_statement(sql)


def init_t_device():
    sql: str = 'DELETE FROM t_device ;'
    return execute_delete_statement(sql)


def add_t_device():
    sql: str = '''
    INSERT 
    INTO t_device( 
        gigya_uid
        , device_id
        , device_token
        , insert_timestamp
        , insert_user_id
    ) 
    VALUES
    ('test_uid_02','RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX','XXXXX', '2020/05/13 12:34:56.789','test_uid_01'),
    ('test_uid_03','RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX','XXXXX', '2020/05/13 12:34:56.789','test_uid_01');
    '''

    return execute_insert_statement(sql)


def init_t_user_setting_ride():
    sql: str = 'DELETE FROM t_user_setting_ride ;'
    return execute_delete_statement(sql)


def add_t_user_setting_ride():
    sql: str = '''
    INSERT INTO t_user_setting_ride( 
        gigya_uid
        , battery_remind_latitude
        , battery_remind_longitude
        , battery_remind_cd
        , battery_remind_voice_notice
        , safety_ride_alert
        , long_drive_alert
        , speed_over_alert
        , no_light_alert
        , safety_ride_voice_notice
        , home_assist_mode_number
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    ('test_uid_02',35.123456,139.123456,'02',true,true,true,true,true,true,'02','2020/05/13 12:34:56.789','test_uid_01');
    '''

    return execute_insert_statement(sql)


def init_t_user_vehicle():
    sql: str = 'DELETE FROM t_user_vehicle;'
    return execute_delete_statement(sql)


def add_t_user_vehicle():
    sql: str = '''
    INSERT INTO t_user_vehicle( 
        user_vehicle_id
        , gigya_uid
        , vehicle_id
        , peripheral_identifier
        , complete_local_name
        , managed_flag
        , registered_flag
        , unit_no
        , frame_no
        , model_code
        , vehicle_name
        , equipment_weight
        , vehicle_nickname
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    (1, 'test_uid_02', 'abcd-0000001', 'switch-02-01', 'スイッチ-02-01', True, True,   'abcd-0000001', NULL, 'abcd', 'ユーザー指定車両名02-01', 5, 'ユーザー指定車両名02-01', '2020/05/13 12:34:56.789','test_uid_01'),
    (2, 'test_uid_02', 'abcd-0000002', 'switch-02-02', 'スイッチ-02-02', False, False, 'abcd-0000002', NULL, 'abcd', 'ユーザー指定車両名02-02', 5, 'ユーザー指定車両名02-02', '2020/05/13 12:34:56.789','test_uid_01'),
    (3, 'test_uid_02', 'zzzz-9999999', 'switch-02-03', 'スイッチ-02-03', False, False, 'zzzz-9999999', NULL, 'zzzz', 'ユーザー指定車両名02-03', 5, 'ユーザー指定車両名02-03', '2020/05/13 12:34:56.789','test_uid_01'),
    (4, 'test_uid_03', 'abcd-9999999', 'switch-03-01', 'スイッチ-03-01', False, False, 'abcd-9999999', NULL, 'abcd', 'ユーザー指定車両名03-01', 5, 'ユーザー指定車両名03-01', '2020/05/13 12:34:56.789','test_uid_01'),
    (5, 'test_uid_05', 'abcd-0000002', 'switch-02-02', 'スイッチ-02-02', True, False, 'abcd-0000002', NULL, 'abcd', 'ユーザー指定車両名02-02', 5, 'ユーザー指定車両名02-02', '2020/05/13 12:34:56.789','test_uid_01'),
    (6, 'test_uid_05', 'zzzz-9999999', 'switch-02-03', 'スイッチ-02-03', False, False, 'zzzz-9999999', NULL, 'zzzz', 'ユーザー指定車両名02-03', 5, 'ユーザー指定車両名02-03', '2020/05/13 12:34:56.789','test_uid_01'),
    (7, 'test_uid_05', 'abcd-9999999', 'switch-03-01', 'スイッチ-03-01', False, False, 'abcd-9999999', NULL, 'abcd', 'ユーザー指定車両名03-01', 5, 'ユーザー指定車両名03-01', '2020/05/13 12:34:56.789','test_uid_01'),
    (99, 'test_uid_99', 'abcd-9999999', 'switch-99-01', 'スイッチ-99-01', False, False, 'abcd-9999999', NULL, 'abcd', 'ユーザー指定車両名99-01', 5, 'ユーザー指定車両名99-01', '2020/05/13 12:34:56.789','test_uid_01'),
    (119, 'test_uid_06', 'abcd-0000004', 'switch-02-04', 'スイッチ-02-04', True, True, 'abcd-0000004', NULL, 'abcd', 'ユーザー指定車両名02-04', 5, 'ユーザー指定車両名02-04', '2020/05/13 12:34:56.789','test_uid_01'),
    (120, 'test_uid_xx', 'abcd-0000001', 'switch-xx-01', 'スイッチ-xx-01', True, True, 'abcd-0000001', NULL, 'abcd', 'ユーザー指定車両名xx-01', 5, 'ユーザー指定車両名xx-01', '2020/05/13 12:34:56.789','test_uid_01'),
    (121, 'test_uid_01', 'abcd-0000003', 'switch-02-01', 'スイッチ-02-01', True, True, 'abcd-0000001', NULL, 'abcd', 'ユーザー指定車両名02-01', 5, 'ユーザー指定車両名02-01', '2020/05/13 12:34:56.789','test_uid_01'),
    (122, 'test_uid_xx', 'abcd-0000002', 'switch-xx-02', 'スイッチ-xx-02', True, True, 'abcd-0000002', NULL, 'abcd', 'ユーザー指定車両名xx-02', 5, 'ユーザー指定車両名xx-02', '2020/05/13 12:34:56.789','test_uid_01'),
    (123, 'test_uid_xx', 'abcd-0000003', 'switch-xx-03', 'スイッチ-xx-03', True, True, 'abcd-0000003', NULL, 'abcd', 'ユーザー指定車両名xx-03', 5, 'ユーザー指定車両名xx-03', '2020/05/13 12:34:56.789','test_uid_01'),
    (124, 'test_uid_xx', 'abcd-0000004', 'switch-xx-04', 'スイッチ-xx-04', True, True, 'abcd-0000004', NULL, 'abcd', 'ユーザー指定車両名xx-04', 5, 'ユーザー指定車両名xx-04', '2020/05/13 12:34:56.789','test_uid_01'),
    (125, 'test_uid_xx', 'abcd-0000005', 'switch-xx-05', 'スイッチ-xx-05', True, True, 'abcd-0000005', NULL, 'abcd', 'ユーザー指定車両名xx-05', 5, 'ユーザー指定車両名xx-05', '2020/05/13 12:34:56.789','test_uid_01'),
    (126, 'test_uid_xx', 'abcd-0000006', 'switch-xx-06', 'スイッチ-xx-06', True, True, 'abcd-0000006', NULL, 'abcd', 'ユーザー指定車両名xx-06', 5, 'ユーザー指定車両名xx-06', '2020/05/13 12:34:56.789','test_uid_01'),
    (127, 'test_uid_xx', 'abcd-0000007', 'switch-xx-07', 'スイッチ-xx-07', True, True, 'abcd-0000007', NULL, 'abcd', 'ユーザー指定車両名xx-07', 5, 'ユーザー指定車両名xx-07', '2020/05/13 12:34:56.789','test_uid_01'),
    (128, 'test_uid_xx', 'abcd-0000008', 'switch-xx-08', 'スイッチ-xx-08', True, True, 'abcd-0000008', NULL, 'abcd', 'ユーザー指定車両名xx-08', 5, 'ユーザー指定車両名xx-08', '2020/05/13 12:34:56.789','test_uid_01'),
    (129, 'test_uid_xx', 'abcd-0000009', 'switch-xx-09', 'スイッチ-xx-09', True, True, 'abcd-0000009', NULL, 'abcd', 'ユーザー指定車両名xx-09', 5, 'ユーザー指定車両名xx-09', '2020/05/13 12:34:56.789','test_uid_01'),
    (130, 'test_uid_xx', 'abcd-0000010', 'switch-xx-10', 'スイッチ-xx-10', True, True, 'abcd-0000010', NULL, 'abcd', 'ユーザー指定車両名xx-10', 5, 'ユーザー指定車両名xx-10', '2020/05/13 12:34:56.789','test_uid_01'),
    (131, 'test_uid_xx', 'abcd-0000011', 'switch-xx-11', 'スイッチ-xx-11', True, True, 'abcd-0000011', NULL, 'abcd', 'ユーザー指定車両名xx-11', 5, 'ユーザー指定車両名xx-11', '2020/05/13 12:34:56.789','test_uid_01'),
    (132, 'test_uid_xx', 'abcd-0000012', 'switch-xx-12', 'スイッチ-xx-12', True, True, 'abcd-0000012', NULL, 'abcd', 'ユーザー指定車両名xx-12', 5, 'ユーザー指定車両名xx-12', '2020/05/13 12:34:56.789','test_uid_01'),
    (133, 'test_uid_xx', 'abcd-0000013', 'switch-xx-13', 'スイッチ-xx-13', True, True, 'abcd-0000013', NULL, 'abcd', 'ユーザー指定車両名xx-13', 5, 'ユーザー指定車両名xx-13', '2020/05/13 12:34:56.789','test_uid_01'),
    (134, 'test_uid_xx', 'abcd-0000014', 'switch-xx-14', 'スイッチ-xx-14', True, True, 'abcd-0000014', NULL, 'abcd', 'ユーザー指定車両名xx-14', 5, 'ユーザー指定車両名xx-14', '2020/05/13 12:34:56.789','test_uid_01'),
    (135, 'test_uid_xx', 'abcd-0000015', 'switch-xx-15', 'スイッチ-xx-15', True, True, 'abcd-0000015', NULL, 'abcd', 'ユーザー指定車両名xx-15', 5, 'ユーザー指定車両名xx-15', '2020/05/13 12:34:56.789','test_uid_01'),
    (136, 'test_uid_xx', 'abcd-0000016', 'switch-xx-16', 'スイッチ-xx-16', True, True, 'abcd-0000016', NULL, 'abcd', 'ユーザー指定車両名xx-16', 5, 'ユーザー指定車両名xx-16', '2020/05/13 12:34:56.789','test_uid_01'),
    (137, 'test_uid_xx', 'abcd-0000017', 'switch-xx-17', 'スイッチ-xx-17', True, True, 'abcd-0000017', NULL, 'abcd', 'ユーザー指定車両名xx-17', 5, 'ユーザー指定車両名xx-17', '2020/05/13 12:34:56.789','test_uid_01'),
    (138, 'test_uid_xx', 'abcd-0000018', 'switch-xx-18', 'スイッチ-xx-18', True, True, 'abcd-0000018', NULL, 'abcd', 'ユーザー指定車両名xx-18', 5, 'ユーザー指定車両名xx-18', '2020/05/13 12:34:56.789','test_uid_01'),
    (139, 'test_uid_xx', 'abcd-0000019', 'switch-xx-19', 'スイッチ-xx-19', True, True, 'abcd-0000019', NULL, 'abcd', 'ユーザー指定車両名xx-19', 5, 'ユーザー指定車両名xx-19', '2020/05/13 12:34:56.789','test_uid_01'),
    (140, 'test_uid_xx', 'abcd-0000020', 'switch-xx-20', 'スイッチ-xx-20', True, True, 'abcd-0000020', NULL, 'abcd', 'ユーザー指定車両名xx-20', 5, 'ユーザー指定車両名xx-20', '2020/05/13 12:34:56.789','test_uid_01');
    '''
    ret = execute_insert_statement(sql)

    set_sequence_sql = '''
        SELECT setval('t_user_vehicle_user_vehicle_id_seq', (SELECT MAX(user_vehicle_id) FROM t_user_vehicle));
    '''
    execute_select_statement(set_sequence_sql)

    return ret


def init_t_drive_unit_history():
    sql: str = 'DELETE FROM t_drive_unit_history;'
    return execute_delete_statement(sql)


def add_t_drive_unit_history():
    sql: str = '''
    INSERT INTO t_drive_unit_history(
        user_vehicle_id
        , du_first_timestamp
        , du_last_timestamp
        , gigya_uid
        , du_serial_number
        , du_first_odometer
        , du_last_odometer
        , insert_timestamp
        , insert_user_id
        , update_timestamp
        , update_user_id
    )
    VALUES
    (1, '2022/05/13 12:34:56.789', '9999/12/31 23:59:59.999', 'test_uid_02', '000011', 30, 30, '2020/05/13 12:34:56.789', 'test_uid_01', '2022/05/13 12:34:56.789','test_uid_01'),
    (1, '2022/05/12 12:34:56.789', '2022/05/13 12:34:56.789', 'test_uid_02', '000022', 20, 30, '2020/05/13 12:34:56.789', 'test_uid_01', NULL, NULL),
    (1, '2022/05/11 12:34:56.789', '2022/05/12 12:34:56.789', 'test_uid_02', '000011', 10, 20, '2020/05/13 12:34:56.789', 'test_uid_01', NULL, NULL),
    (1, '2022/05/10 12:34:56.789', '2022/05/11 12:34:56.789', 'test_uid_02', '000011',  0, 10, '2020/05/13 12:34:56.789', 'test_uid_01', NULL, NULL),
    (99, '2022/05/13 12:34:56.789', '9999/12/31 23:59:59.999', 'test_uid_99', '000099', 0, 30, '2020/05/13 12:34:56.789', 'test_uid_99', '2022/05/13 12:34:56.789','test_uid_99');
    '''
    return execute_insert_statement(sql)


def init_t_maintain_history():
    sql: str = 'DELETE FROM t_maintain_history;'
    return execute_delete_statement(sql)


def add_t_maintain_history():
    sql: str = '''
    INSERT
    INTO t_maintain_history(
        maintain_history_id
        , gigya_uid
        , user_vehicle_id
        , maintain_item_code
        , model_code
        , maintain_implement_date
        , maintain_location
        , maintain_cost
        , maintain_required_time
        , maintain_memo
        , maintain_du_serial_number
        , maintain_du_last_timestamp
        , maintain_du_last_odometer
        , maintain_image_ids
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    (1,'test_uid_02',1,'00002', 'abcd','2022/05/11','メンテナンス場所_01',1000,10,'memo_タイヤ空気圧', '000011','2022/05/11 12:00:00.000', 5,'test1,test2,test3', '2020/05/13 12:34:56.789','test_uid_01'),
    (2,'test_uid_02',1,'00003', 'abcd','2022/05/11','メンテナンス場所_02',2000,20,'memo_タイヤ摩耗',   '000011','2022/05/11 12:00:00.000', 5,'test1,test2,test3', '2020/05/13 12:34:56.789','test_uid_01'),
    (3,'test_uid_02',1,'00002', 'abcd','2022/04/30','メンテナンス場所_01',1000,10,'memo_タイヤ空気圧', '000010', '2022/04/30 12:00:00.000', 4,'test1,test2,test3', '2020/05/13 12:34:56.789','test_uid_01'),
    (4,'test_uid_02',1,'00004', 'abcd','2022/05/12','メンテナンス場所_01',1000,10,'memo_チェーン動作', '000022', '2022/05/12 20:00:00.000', 4,'test1,test2,test3', '2020/05/13 12:34:56.789','test_uid_01'),
    (5,'test_uid_02',1,'00009', 'abcd','2022/05/11','メンテナンス場所_01',1000,10,'memo_定期点検',    '000022', '2022/05/11 12:00:00.000', 5,'test1,test2,test3', '2020/05/13 12:34:56.789','test_uid_01'),
    (6,'test_uid_02',1,'00009', 'abcd','2023/12/31','メンテナンス場所_01',1000,10,'memo_定期点検',    '000022', '2022/05/11 12:00:00.000', 5,'test1,test2,test3', '2020/05/13 12:34:56.789','test_uid_01'),
    (7,'test_uid_02',1,'00001', 'abcd','2022/10/11','メンテナンス場所',   9999,999,'メンテナンスメモ', '16777215','2022/10/11 12:34:56.789',123,'null,null,null','  2020/05/13 12:34:56.789','test_uid_01'),
    (8,'test_uid_03',4,'00002', 'abcd','2020/10/10','メンテナンス場所',9999,999,'メンテナンスメモ','16777215','2022/10/11 12:34:56.789',123,'null,null,null','2020/05/13 12:34:56.789','test_uid_01'),
    (9, 'test_uid_03',4,'00002','abcd','2020/10/11','メンテナンス場所2',9999,999,'メンテナンスメモ','16777215','2022/10/11 12:34:56.789',123,'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX1,XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXX2,null','2020/05/13 12:34:56.789','test_uid_01'),
    (10,'test_uid_03',4,'00002','abcd','2020/10/12','メンテナンス場所3',9999,999,'メンテナンスメモ','16777215','2022/10/11 12:34:56.789',123,'null,null,null','2020/05/13 12:34:56.789','test_uid_01'),
    (11,'test_uid_03',4,'00002','abcd','2020/10/13','メンテナンス場所4',9999,999,'メンテナンスメモ','16777215','2022/10/11 12:34:56.789',123,'null,null,null','2020/05/13 12:34:56.789','test_uid_01'),
    (12,'test_uid_03',4,'00003','abcd','2020/10/14','メンテナンス場所5',9999,999,'メンテナンスメモ','16777215','2022/10/11 12:34:56.789',123,'null,null,null','2020/05/13 12:34:56.789','test_uid_01');
    '''
    ret = execute_insert_statement(sql)

    set_sequence_sql = '''
        SELECT setval('t_maintain_history_maintain_history_id_seq', (SELECT MAX(maintain_history_id) FROM t_maintain_history));
    '''
    execute_select_statement(set_sequence_sql)

    return ret


def init_t_user_setting_maintain():
    sql: str = 'DELETE FROM t_user_setting_maintain;'
    return execute_delete_statement(sql)


def add_t_user_setting_maintain():
    sql: str = '''
    INSERT INTO t_user_setting_maintain(
        user_vehicle_id
        , gigya_uid
        , maintain_consciousness
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    (1, 'test_uid_02', '01', '2020/05/13 12:34:56.789','test_uid_01'),
    (2, 'test_uid_02', '01', '2020/05/13 12:34:56.789','test_uid_01'),
    (3, 'test_uid_02', '02', '2020/05/13 12:34:56.789','test_uid_01'),
    (4, 'test_uid_03', '03', '2020/05/13 12:34:56.789','test_uid_01');
    '''
    return execute_insert_statement(sql)


def init_t_user_setting_maintain_item():
    sql: str = 'DELETE FROM t_user_setting_maintain_item;'
    return execute_delete_statement(sql)


def add_t_user_setting_maintain_item():
    sql: str = '''
    INSERT INTO t_user_setting_maintain_item(
        user_vehicle_id
        , maintain_item_code
        , maintain_item_alert
        , maintain_item_alert_status
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    (1, '00001', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (1, '00002', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (1, '00003', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (1, '00004', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (1, '00005', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    -- (1, '00006', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    -- (1, '00007', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    -- (1, '00008', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (1, '00009', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (2, '00001', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (3, '00001', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (4, '00001', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (4, '00002', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (4, '00003', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (4, '00004', True,0, '2020/05/13 12:34:56.789','test_uid_01'),
    (4, '00005', True,0, '2020/05/13 12:34:56.789','test_uid_01');
    '''
    return execute_insert_statement(sql)


def init_t_user_shop_purchase():
    sql: str = 'DELETE FROM t_user_shop_purchase ;'
    return execute_delete_statement(sql)


def add_t_user_shop_purchase():
    sql: str = '''
    INSERT INTO t_user_shop_purchase( 
        user_vehicle_id
        , gigya_uid
        , shop_name
        , shop_tel
        , shop_location
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    (1,'test_uid_02','test_shop_02-1','0212345678','東京都世田谷区玉川2丁目2-2','2022/12/12 12:12:12.610','test_uid_05'),
    (2,'test_uid_02','test_shop_02-2','0809999999','東京都調布市仙川町','2022/12/12 12:12:12.610','test_uid_05'),
    (140,'test_uid_02','test_shop_02','0212345678','東京都世田谷区玉川2丁目2-2','2022/12/12 12:12:12.610','test_uid_05');
    '''

    return execute_insert_statement(sql)


def init_t_user_shop_regular():
    sql: str = 'DELETE FROM t_user_shop_regular;'
    return execute_delete_statement(sql)


def add_t_user_shop_regular():
    sql: str = '''
    INSERT INTO t_user_shop_regular( 
        gigya_uid
        , shop_name
        , shop_tel
        , shop_location
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    ('test_uid_03','test_shop_03','0312345678','東京都世田谷区玉川3丁目3-3','2022/12/12 12:12:12.610','test_uid_05'),
    ('test_uid_07','test_shop_07','0712345678','東京都世田谷区玉川7丁目7-7','2022/7/17 17:17:17.610','test_uid_05'),
    ('test_uid_01','test_shop_01','0312345678','東京都世田谷区玉川1丁目1-1','2022/7/17 17:17:17.610','test_uid_05');
    '''

    return execute_insert_statement(sql)


def init_t_ride_history():
    sql: str = 'DELETE FROM t_ride_history;'
    return execute_delete_statement(sql)


def add_t_ride_history():
    sql: str = '''
    INSERT INTO t_ride_history(
        ride_history_id
        , gigya_uid
        , user_vehicle_id
        , start_timestamp
        , end_timestamp
        , ride_name
        , trip_distance
        , trip_time
        , total_calorie
        , battery_consumption
        , average_speed
        , max_speed
        , max_pedaling_power
        , max_cadence
        , bookmark_flg
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    ('42022-10-06T15:30:31.000','test_uid_03',4,'2022/12/01 12:12:12.610','2022/12/01 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1212023-10-06T15:30:31.000','test_uid_01',121,'2022/12/01 12:12:12.610','2022/12/01 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1222022-10-06T15:30:31.000','test_uid_01',122,'2022/12/02 12:12:12.610','2022/12/02 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1232022-10-06T15:30:31.000','test_uid_01',123,'2022/12/03 12:12:12.610','2022/12/03 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1242022-10-06T15:30:31.000','test_uid_01',124,'2022/12/04 12:12:12.610','2022/12/04 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1252022-10-06T15:30:31.000','test_uid_01',125,'2022/12/05 12:12:12.610','2022/12/05 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1262022-10-06T15:30:31.000','test_uid_01',126,'2022/12/06 12:12:12.610','2022/12/06 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1272022-10-06T15:30:31.000','test_uid_01',127,'2022/12/07 12:12:12.610','2022/12/07 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1282022-10-06T15:30:31.000','test_uid_01',128,'2022/12/08 12:12:12.610','2022/12/08 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1292022-10-06T15:30:31.000','test_uid_01',129,'2022/12/09 12:12:12.610','2022/12/09 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1302022-10-06T15:30:31.000','test_uid_01',131,'2022/12/10 12:12:12.610','2022/12/10 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1312022-10-06T15:30:31.000','test_uid_01',132,'2022/12/11 12:12:12.610','2022/12/11 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1322022-10-06T15:30:31.000','test_uid_01',133,'2022/12/12 12:12:12.611','2022/12/12 12:12:12.611','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1332022-10-06T15:30:31.000','test_uid_01',134,'2022/12/13 12:12:12.611','2022/12/13 12:12:12.611','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1342022-10-06T15:30:31.000','test_uid_01',135,'2022/12/14 12:12:12.610','2022/12/14 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1352022-10-06T15:30:31.000','test_uid_01',136,'2022/12/15 12:12:12.610','2022/12/15 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1362022-10-06T15:30:31.000','test_uid_01',137,'2022/12/16 12:12:12.610','2022/12/16 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1372022-10-06T15:30:31.000','test_uid_01',138,'2022/12/17 12:12:12.610','2022/12/17 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1382022-10-06T15:30:31.000','test_uid_01',139,'2022/12/18 12:12:12.610','2022/12/18 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1392022-10-06T15:30:31.000','test_uid_01',130,'2022/12/19 12:12:12.610','2022/12/19 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1402022-10-06T15:30:31.000','test_uid_01',140,'2022/12/20 12:12:12.610','2022/12/20 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,True,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1202022-10-06T15:30:31.000','test_uid_01',120,'2022/12/12 12:12:12.610','2022/12/12 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1212022-10-06T15:30:31.000','test_uid_01',121,'2022/12/12 12:12:12.610','2022/12/12 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/11/17 17:17:17.610','test_uid_05'),
    ('2222022-10-06T15:30:31.000','test_uid_01',122,'2022/12/13 12:12:12.610','2022/12/13 12:12:12.610','ユーザー車両名のライド',1234.5,3600,535,72,15,20,6,126,False,'2022/11/17 17:17:17.610','test_uid_05');
    '''
    return execute_insert_statement(sql)


def init_t_ride_track():
    sql: str = 'DELETE FROM t_ride_track;'
    return execute_delete_statement(sql)


def add_t_ride_track():
    sql: str = '''
    INSERT INTO t_ride_track(
        ride_history_id
        , track_id
        , user_vehicle_id
        , latitude
        , longitude
        , insert_timestamp
        , insert_user_id
    )
    VALUES
    ('42022-10-06T15:30:31.000',1,4,35.67506,139.763328,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1222022-10-06T15:30:31.000',1,122,35.67506,139.763328,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1212022-10-06T15:30:31.000',1,122,35.67506,139.763328,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1212022-10-06T15:30:31.000',2,122,36.67506,138.763328,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1212022-10-06T15:30:31.000',3,122,37.67506,137.763328,'2022/12/12 12:12:12.610','test_uid_05'),
    ('1232022-10-06T15:30:31.000',2,121,35.66549,139.759649,'2022/11/17 17:17:17.610','test_uid_05'),
    ('2222022-10-06T15:30:31.000',1,122,35.67506,137.763328,'2022/12/12 12:12:12.610','test_uid_05'),
    ('2222022-10-06T15:30:31.000',2,122,36.67506,138.763328,'2022/12/12 12:12:12.610','test_uid_05'),
    ('2222022-10-06T15:30:31.000',3,122,37.67506,139.763328,'2022/12/12 12:12:12.610','test_uid_05');
    '''
    return execute_insert_statement(sql)

def init_t_user_setting():
    sql: str = 'DELETE FROM t_user_setting;'
    return execute_delete_statement(sql)


def add_t_user_setting():
    sql: str = '''
        INSERT INTO t_user_setting(
            gigya_uid
            , nickname
            , weight
            , birth_date
            , max_heart_rate
            , insert_timestamp
            , insert_user_id
        )
        VALUES
        ('test_uid_02', 'test_user_02', 60, '2000-01-01', 150, '2022/12/12 12:12:12.610','test_uid_05');
        '''
    return execute_insert_statement(sql)


def init_m_spot():
    sql: str = 'DELETE FROM m_spot;'
    execute_delete_statement(sql)
    sql: str = 'SELECT SETVAL (\'m_spot_spot_id_seq\', 1, false);'
    return execute_insert_statement(sql)


def add_m_spot():
    sql: str = '''
    INSERT INTO m_spot(
        spot_id
        , spot_type_code
        , spot_location
        , rechargeable_flag
        , fcdyobi1
        , fcdyobi2
        , fcdyobi3
        , fcdyobi4
        , fcdyobi5
        , etxyobi1
        , etxyobi2
        , etxyobi3
        , etxyobi4
        , etxyobi5
        , delete_flag
        , delete_timestamp
        , delete_user_id
        , insert_timestamp
        , insert_user_id
        , update_timestamp
        , update_user_id
    )
    VALUES
    (1,'00001',ST_GeomFromText('POINT(35.68617892085704 139.70299926999502)', 4326),true,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL);
    '''
    return execute_insert_statement(sql)


def init_t_route():
    sql: str = 'DELETE FROM t_route;'
    execute_delete_statement(sql)
    sql: str = 'SELECT SETVAL (\'t_route_route_id_seq\', 1, false);'
    return execute_insert_statement(sql)


def add_t_route():
    sql: str = '''
    INSERT INTO t_route(
        gigya_uid
        , user_vehicle_id
        , save_timestamp
        , origin_name
        , origin_location
        , origin_place_id
        , destination_name
        , destination_location
        , destination_place_id
        , ride_date
        , weather
        , weather_icon
        , fcdyobi1
        , fcdyobi2
        , fcdyobi3
        , fcdyobi4
        , fcdyobi5
        , etxyobi1
        , etxyobi2
        , etxyobi3
        , etxyobi4
        , etxyobi5
        , delete_flag
        , delete_timestamp
        , delete_user_id
        , insert_timestamp
        , insert_user_id
        , update_timestamp
        , update_user_id
    )
    VALUES
    ('test_uid_2',2,'2023-09-13 11:27:46.642','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),
    'ChIJdc0fopOLGGARm4DVQaWiPZ0','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0','2023-10-02','001','001',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    ('test_uid_2',2,'2023-09-12 11:27:46.642','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),
    'ChIJdc0fopOLGGARm4DVQaWiPZ0','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0','2023-10-02','001','001',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    ('test_uid_3',2,'2023-09-12 11:27:46.642','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),
    'ChIJdc0fopOLGGARm4DVQaWiPZ0','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0','2023-10-02','001','001',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    ('test_uid_4',2,'2023-09-12 11:27:46.642','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),
    'ChIJdc0fopOLGGARm4DVQaWiPZ0','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0','2023-10-02','001','001',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    ('test_uid_5',2,'2023-09-12 11:27:46.642','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),
    'ChIJdc0fopOLGGARm4DVQaWiPZ0','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0','2023-10-02','001','001',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    ('test_uid_2',2,'2023-09-12 11:27:46.642','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),
    'ChIJdc0fopOLGGARm4DVQaWiPZ0','虎ノ門ヒルズ森タワー',ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0','2023-10-02','001','001',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL);
    '''
    return execute_insert_statement(sql)


def init_t_workout():
    sql: str = 'DELETE FROM t_workout;'
    execute_delete_statement(sql)
    sql: str = 'SELECT SETVAL (\'t_workout_workout_id_seq\', 1, false);'
    return execute_insert_statement(sql)


def add_t_workout():
    sql: str = '''
    INSERT INTO t_workout(
        data_source_kind_code
        , data_source_id
        , user_vehicle_id
        , gigya_uid
        , start_timestamp
        , end_timestamp
        , workout_time
        , trip_distance
        , total_calorie
        , heartbeat_zone_1_time
        , heartbeat_zone_2_time
        , heartbeat_zone_3_time
        , heartbeat_zone_4_time
        , heartbeat_zone_5_time
        , average_heart_rate
        , average_speed
        , max_speed
        , average_pedaling_power
        , max_pedaling_power
        , average_cadence
        , max_cadence
        , weather
        , temperature
        , humidity
        , workout_mode_code
        , fcdyobi1
        , fcdyobi2
        , fcdyobi3
        , fcdyobi4
        , fcdyobi5
        , etxyobi1
        , etxyobi2
        , etxyobi3
        , etxyobi4
        , etxyobi5
        , delete_flag
        , delete_timestamp
        , delete_user_id
        , insert_timestamp
        , insert_user_id
        , update_timestamp
        , update_user_id
    )
    VALUES
    ('01', 'abcd-1234567', 1, 'test_uid', '2022-10-06T15:30:31.000', '2022-10-16T15:30:31.000', 10000, 1000, 1000, 100,
     100, 100, 100, 100, 160, 20, 40, 40, 100, 40, 100, '001', 30, 60, '01', NULL, NULL, NULL, NULL, NULL,
     NULL, NULL, NULL, NULL, NULL, false, NULL, NULL, NULL, NULL, NULL, NULL);
    '''
    return execute_insert_statement(sql)


def init_t_route_one_way():
    sql: str = 'DELETE FROM t_route_one_way;'
    execute_delete_statement(sql)
    sql: str = 'SELECT SETVAL (\'t_route_one_way_route_one_way_id_seq\', 1, false);'
    return execute_insert_statement(sql)


def add_t_route_one_way():
    sql: str = '''
    INSERT INTO t_route_one_way(
        route_id
        , route_one_way_id
        , round_trip_type_code
        , duration
        , distance
        , route_type
        , route_type_branch_no
        , fcdyobi1
        , fcdyobi2
        , fcdyobi3
        , fcdyobi4
        , fcdyobi5
        , etxyobi1
        , etxyobi2
        , etxyobi3
        , etxyobi4
        , etxyobi5
        , delete_flag
        , delete_timestamp
        , delete_user_id
        , insert_timestamp
        , insert_user_id
        , update_timestamp
        , update_user_id
    )
    VALUES
    (1,10,'11',100,100,'11',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
	(1,11,'12',110,110,'12',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (2,12,'10',120,120,'21',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (3,13,'10',123,123,'11',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (4,14,'10',123,123,'12',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (5,15,'10',123,123,'21',1,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL);
    '''
    return execute_insert_statement(sql)


def init_t_route_via_point():
    sql: str = 'DELETE FROM t_route_via_point;'
    execute_delete_statement(sql)
    sql: str = 'SELECT SETVAL (\'t_route_via_point_route_via_point_id_seq\', 1, false);'
    return execute_insert_statement(sql)


def add_t_route_via_point():
    sql: str = '''
    INSERT INTO t_route_via_point(
        route_id
        , route_one_way_id
        , route_via_point_location
        , route_via_point_place_id
        , route_via_point_type
        , fcdyobi1
        , fcdyobi2
        , fcdyobi3
        , fcdyobi4
        , fcdyobi5
        , etxyobi1
        , etxyobi2
        , etxyobi3
        , etxyobi4
        , etxyobi5
        , delete_flag
        , delete_timestamp
        , delete_user_id
        , insert_timestamp
        , insert_user_id
        , update_timestamp
        , update_user_id
    )
    VALUES
    (1,10,ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0','01',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (4,14,ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0','01',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (5,15,ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0','01',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (5,15,ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL);
    '''
    return execute_insert_statement(sql)


def init_t_bicycle_parking():
    sql: str = 'DELETE FROM t_bicycle_parking;'
    execute_delete_statement(sql)
    sql: str = 'SELECT SETVAL (\'t_bicycle_parking_bicycle_parking_id_seq\', 1, false);'
    return execute_insert_statement(sql)


def add_t_bicycle_parking():
    sql: str = '''
    INSERT INTO t_bicycle_parking(
        route_id
        , bicycle_parking_name
        , bicycle_parking_distance
        , bicycle_parking_location
        , bicycle_parking_place_id
        , fcdyobi1
        , fcdyobi2
        , fcdyobi3
        , fcdyobi4
        , fcdyobi5
        , etxyobi1
        , etxyobi2
        , etxyobi3
        , etxyobi4
        , etxyobi5
        , delete_flag
        , delete_timestamp
        , delete_user_id
        , insert_timestamp
        , insert_user_id
        , update_timestamp
        , update_user_id
    )
    VALUES
    (1,'テスト駐輪場',100,ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (4,'テスト駐輪場',100,ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (5,'テスト駐輪場',100,ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL),
    (5,'テスト駐輪場',100,ST_GeomFromText('POINT(35.667009002633066 139.7493871115867)', 4326),'ChIJdc0fopOLGGARm4DVQaWiPZ0',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,false,NULL,NULL,NULL,NULL,NULL,NULL);
    '''
    return execute_insert_statement(sql)
