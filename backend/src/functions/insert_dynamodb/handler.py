import json
import boto3
import logging


# ログレベル
logging.getLogger().setLevel(logging.INFO)

dynamodbClient = boto3.client('dynamodb')
dynamodbResource = boto3.resource('dynamodb')

# テストイベントに下記を入力
# {
#   "file_name": "対象ファイル名",
#   "table_name": "対象テーブル名"
# }


def handler(event, context):  # pragma: no cover

    print(event)
    file_name = event.get('file_name')
    table_name = event.get('table_name')

    # レコード追加
    json_open = open(file_name, 'r')
    json_load = json.load(json_open)

    try:
        for item in json_load["Items"]:
            print(item)
            dynamodbClient.put_item(
                Item=item,
                TableName=table_name
            )
    except Exception as e:
        print(e)

    return {
        'statusCode': 200,
        'body': json.dumps('Uploaded to DynamoDB Table')
    }
