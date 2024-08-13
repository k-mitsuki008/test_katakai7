import os
import sys

from importlib import import_module
from moto import mock_dynamodb
from common.aws.dynamodb import DynamoDb
import boto3
from decimal import Decimal

# __pycache__生成を抑止
sys.dont_write_bytecode = True

# バリデーション定義のimport時にDynamoDBアクセスが発生するため、このタイミングでDynamoDBのモックを作成、初期化する。
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
        {"category_cd": "MAINTENANCE_CONSCIOUSNESS", "code": "LOW", "value": "03"},
        {"category_cd": "MAINTENANCE_CONSCIOUSNESS", "code": "MIDDLE", "value": "02"},
        {"category_cd": "MAINTENANCE_EXPLANATION_TYPE", "code": "STRING", "value": 1},
        {"category_cd": "MAINTENANCE_EXPLANATION_TYPE", "code": "IMAGE", "value": 2},
        {"category_cd": "MAINTENANCE_VEHICLE_IMAGE_SUFFIX", "code": "SUFFIX", "value": "_top.png"},
        {"category_cd": "BATTERY_REMIND", "code": "ASSIST", "value": "02"},
        {"category_cd": "BATTERY_REMIND", "code": "LONG_LIFE", "value": "01"},
        {"category_cd": "BATTERY_REMIND", "code": "NO_NOTIFICATION", "value": "00"},
        {"category_cd": "ASSIST_MODE_NUMBER", "code": "ECO", "value": "02"},
        {"category_cd": "ASSIST_MODE_NUMBER", "code": "EXPW", "value": "05"},
        {"category_cd": "ASSIST_MODE_NUMBER", "code": "HIGH", "value": "04"},
        {"category_cd": "ASSIST_MODE_NUMBER", "code": "PLUS_ECO", "value": "01"},
        {"category_cd": "ASSIST_MODE_NUMBER", "code": "STD", "value": "03"},
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
        {'os': 'android', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '1.1.0', 'app_build_number': 3, 'update_timestamp': 1703343600},  # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
        {'os': 'android', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '0.1.0', 'app_build_number': 2, 'expiration_timestamp': 1703948300, 'update_timestamp': 1703343500},  # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
        {'os': 'android', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '0.0.1', 'app_build_number': 1, 'expiration_timestamp': 1703948200, 'update_timestamp': 1703343400},  # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
        {'os': 'ios', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '0.0.0', 'app_build_number': 0, 'expiration_timestamp': 1703947400, 'update_timestamp': 1703342600},  # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
        {'os': 'ios', 'app_name': 'yamaha_buddy_app_dev', 'app_version': '0.1.0', 'app_build_number': 1, 'update_timestamp': 1703343600}  # 2023/12/31T00:00:00+09:00, 2023/12/24T00:00:00+09:00
    ]
    table = dynamodb.Table('t_app_version')
    for item in t_app_info_list:
        table.put_item(Item=item)

    # モック化したメッセージマスタ、定数マスタを設定
    const_dynamodb.set_data()

# rootパスを取得
root_dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(f'LAMBDA_DIR_PATH = {root_dir_path + "/src"}')
sys.path.append(root_dir_path + '/src')

# Lambda Layer のパスを通す
# layers_dir_path = root_dir_path + '/src/layers'
# sys.path.append(layers_dir_path)
sys.path.append(root_dir_path + '/src/layers/common/python')
sys.path.append(root_dir_path + '/src/layers/gigya/python')
sys.path.append(root_dir_path + '/src/layers/repository/python')
sys.path.append(root_dir_path + '/src/layers/service/python')

# テスト対象関数に対してパスを通す
functions_dir_path = root_dir_path + '/src/functions'
sys.path.append(functions_dir_path)
# /src/functions/配下のdir、faileを取得
for file in os.listdir(functions_dir_path):

    file_path = os.path.join(functions_dir_path, file)
    if os.path.isdir(file_path):
        sys.path.append(file_path)

        # テスト対象のhandlerを全て登録する
        if os.path.isfile(file_path + '/handler.py') :
            _ = import_module('src.functions.' + file + '.handler')
        if os.path.isfile(file_path + '/get_handler.py') :
            _ = import_module('src.functions.' + file + '.get_handler')
        if os.path.isfile(file_path + '/post_handler.py') :
            _ = import_module('src.functions.' + file + '.post_handler')
        if os.path.isfile(file_path + '/put_handler.py') :
            _ = import_module('src.functions.' + file + '.put_handler')
        if os.path.isfile(file_path + '/delete_handler.py') :
            _ = import_module('src.functions.' + file + '.delete_handler')
        if os.path.isfile(file_path + '/err_handler.py') :
            _ = import_module('src.functions.' + file + '.err_handler')

batch_functions_dir_path = root_dir_path + '/src/batch_functions'
sys.path.append(batch_functions_dir_path)
# /src/batch_functions/配下のdir、faileを取得
for file in os.listdir(batch_functions_dir_path):

    file_path = os.path.join(batch_functions_dir_path, file)
    if os.path.isdir(file_path):
        sys.path.append(file_path)

        # テスト対象のhandlerを全て登録する
        if os.path.isfile(file_path + '/handler.py') :
            _ = import_module('src.batch_functions.' + file + '.handler')
        if os.path.isfile(file_path + '/delete_files_handler.py') :
            _ = import_module('src.batch_functions.' + file + '.delete_files_handler')
        if os.path.isfile(file_path + '/get_list_handler.py') :
            _ = import_module('src.batch_functions.' + file + '.get_list_handler')
        if os.path.isfile(file_path + '/request_notifications_handler.py') :
            _ = import_module('src.batch_functions.' + file + '.request_notifications_handler')
