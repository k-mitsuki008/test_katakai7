import os
import json
import boto3
from boto3.dynamodb.conditions import Key
from botocore.client import Config
from botocore.exceptions import ClientError

from common.error.dynamo_db_access_error import DynamoDbAccessError
from common.error.s3_access_error import S3AccessError
from common.logger import Logger
from common.aws.dynamodb import DynamoDb

log = Logger()


def get_secret() -> dict:
    # Todo: dev環境もシークレットマネージャを分けるように修正。
    if os.environ.get("SECRET_MANAGER_NAME", None):
        secret_name = os.environ["SECRET_MANAGER_NAME"]
        region_name = os.environ["SECRET_MANAGER_REGION"]
        client = boto3.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

        secret_values = json.loads(secret_value_response['SecretString'])

    else:
        aurora_secret_name = os.environ["AURORA_SECRET_MANAGER_NAME"]
        region_name = os.environ["AURORA_SECRET_MANAGER_REGION"]
        # gigya_secret_name = os.environ["GIGYA_SECRET_MANAGER_NAME"]
        # google_secret_name = os.environ["GOOGLE_SECRET_MANAGER_NAME"]

        client = boto3.client(
            service_name='secretsmanager',
            region_name=region_name
        )

        aurora_secret_value_response = client.get_secret_value(
            SecretId=aurora_secret_name
        )

        # gigya_secret_value_response = client.get_secret_value(
        #     SecretId=gigya_secret_name
        # )

        # google_secret_value_response = client.get_secret_value(
        #     SecretId=google_secret_name
        # )

        secret_values = {
            **json.loads(aurora_secret_value_response['SecretString']),
            # **json.loads(gigya_secret_value_response['SecretString']),
            # **json.loads(google_secret_value_response['SecretString'])
        }

    return secret_values


def get_s3_url(bucket: str, key: str, expires: int = 900, http_method: str = 'put_object') -> str:
    try:
        url = get_s3_client().generate_presigned_url(
            ClientMethod=http_method,
            Params={'Bucket': bucket, 'Key': key},
            ExpiresIn=expires,
        )
    except ClientError as e:
        log.error(
            f"Couldn't get a presigned URL for bucket '{bucket}' and object '{key}'")
        raise S3AccessError() from e
    log.info(f'S3_URL={url}')
    return url


def get_dynamodb(table_name: str, keys: dict) -> dict:
    const_dynamodb = DynamoDb()
    dynamodb = const_dynamodb.resource()
    table = dynamodb.Table(table_name)
    try:
        res = table.get_item(Key=keys)
    except ClientError as e:
        raise DynamoDbAccessError() from e
    return res.get('Item', {})


def get_query(table_name: str, key: str, value: str) -> dict:
    table = DynamoDb().resource().Table(table_name)
    try:
        res = table.query(
            KeyConditionExpression=Key(key).eq(value)
        )
    except ClientError as e:
        raise DynamoDbAccessError() from e
    return res.get('Items', None)


def get_dynamodb_by_secondary_index(table_name: str, index: str, key: str, value: str) -> list:
    table = DynamoDb().resource().Table(table_name)
    try:
        res = table.query(
            IndexName=index,
            KeyConditionExpression=Key(key).eq(value)
        )
    except ClientError as e:
        raise DynamoDbAccessError() from e
    return res.get('Items', [])


def upsert_dynamodb(table_name: str, keys: dict, items: dict, condition: str = 'attribute_not_exists(test)') -> dict:
    table = DynamoDb().resource().Table(table_name)
    item_list = [{'exp': f'#{k} = :{k}', 'key': k, 'value': v} for k, v in items.items()]

    exp_list = [f'#{item["key"]} = :{item["key"]}' for item in item_list]
    expression = f"set {', '.join(exp_list)}"
    names = {f'#{item["key"]}': item["key"] for item in item_list}
    values = {f':{item["key"]}': item["value"] for item in item_list}
    try:
        res = table.update_item(
            Key=keys,
            ConditionExpression=condition,
            UpdateExpression=expression,
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
            ReturnValues="ALL_NEW"
        )
    except ClientError as e:
        if e.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise DynamoDbAccessError() from e
        # ConditionExpressionの条件を満たさなければ新規追加
        return put_dynamodb(table_name, items, keys)
    return res


def put_dynamodb(table_name: str, items: dict, keys: dict = None) -> dict:
    table = DynamoDb().resource().Table(table_name)

    if keys:
        items.update(keys)

    try:
        res = table.put_item(
            Item=items,
            # ConditionExpression=f'attribute_not_exists({keys.values[0]})'
        )
    except ClientError as e:
        raise DynamoDbAccessError() from e
    return res


def get_message(message_cd: str, default: str = None) -> str:
    return DynamoDb().messages.get(message_cd, default)


def get_constant(category_cd: str, code: str = None, default: any = None) -> any:
    if code is None:
        res = DynamoDb().constants.get(category_cd, default)
    else:
        res = DynamoDb().constants.get(category_cd).get(code, default)
    return res


def get_s3_objects(bucket: str, key: str) -> dict:
    # list_objects
    try:
        objects = get_s3_client().list_objects(Bucket=bucket, Prefix=key)
    except ClientError as e:
        log.error(
            f"Couldn't get a presigned URL for bucket '{bucket}' and object '{key}'")
        raise S3AccessError() from e
    return objects


def delete_s3_objects(bucket: str, key: str) -> None:
    # delete_objects
    try:
        get_s3_client().delete_object(Bucket=bucket, Key=key)
    except ClientError as e:
        log.error(
            f"Couldn't get a presigned URL for bucket '{bucket}' and object '{key}'")
        raise S3AccessError() from e
    return


def get_s3_client():
    return boto3.client(
        's3',
        config=Config(signature_version='s3v4'),
        region_name=os.environ.get('SECRET_MANAGER_REGION', os.environ.get('AURORA_SECRET_MANAGER_REGION'))
    )


def create_s3_objects(bucket: str, key: str, json_data: dict) -> None:
    # create,put
    try:
        get_s3_client().put_object(Body=json.dumps(json_data), Bucket=bucket, Key=key)
    except ClientError as e:
        log.error(
            f"Couldn't create object for bucket '{bucket}' and object '{key}'")
        raise S3AccessError() from e
    return


def get_s3_bucket_key(category_cd: str, code: str = None) -> any:
    stage = os.environ['STAGE']
    s3_bucket_key = get_constant(category_cd, code=code).replace('{env}', stage)
    return s3_bucket_key
