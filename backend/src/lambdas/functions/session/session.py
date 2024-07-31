import boto3
import hashlib
import time
import os
import json
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from layer import response_get


def lambda_handler(event, context):

    body = json.loads(event["body"])
    user_table_name = os.environ["USERTABLE"]
    session_table_name = os.environ["SESSIONTABLE"]
    user_id = body["user_id"]
    password = body["password"]

    dynamodb = boto3.resource("dynamodb")
    user_table = dynamodb.Table(user_table_name)
    session_table = dynamodb.Table(session_table_name)

    try:
        response = user_table.scan(
            FilterExpression=boto3.dynamodb.conditions.Attr("mail_address").eq(user_id)
        )
        Items = response.get("Items", None)
        if Items:
            del_flg = Items[0]["del_flg"]
            if del_flg == "1":
                return response_get.message_none_error(404)
            current_password = Items[0]["password"]
            if current_password == password:
                mail_address = Items[0]["mail_address"]
                client_id = Items[0]["client_id"]
                password_forced_change_flg = Items[0]["password_forced_change_flg"]
                timestamp = int(time.time())
                expiration_time = timestamp + 60 * 15
                session_id = hashlib.md5(f"{timestamp}{mail_address}".encode()).hexdigest()
                current_time = datetime.now(ZoneInfo("Asia/Tokyo"))
                create_session_timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
                expire_session_timestamp = (current_time + timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                session_request = {
                    "user_id": user_id,
                    "session_id": session_id,
                    "create_session_timestamp": create_session_timestamp,
                    "expire_session_timestamp": expire_session_timestamp,
                    "expiration_time": expiration_time,
                    "client_id": client_id,
                    "insert_datetime": create_session_timestamp,
                    "update_datetime": create_session_timestamp
                }
                session_table.put_item(Item=session_request)

                return {
                    "headers": {
                        "Access-Control-Allow-Origin": "*"
                    },
                    "body": json.dumps({
                        "statusCode": 200,
                        "result": 0,
                        "session_id": session_id,
                        "password_forced_change_flg": password_forced_change_flg
                    })
                }
            else:
                return response_get.unauthorized()
        else:
            return response_get.unauthorized()
    except Exception:
        return response_get.message_none_error(500)
