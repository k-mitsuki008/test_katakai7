import os
import boto3
from botocore.exceptions import ClientError

from common.error.dynamo_db_access_error import DynamoDbAccessError
from common.logger import Logger

log = Logger()


class Singleton(object):
    def __new__(cls, *args, **kargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kargs)
        return cls._instance


class DynamoDb(Singleton):
    dynamodb_resource = None
    messages = None
    constants = None

    def resource(self: any) -> any:

        if self.dynamodb_resource:
            return self.dynamodb_resource

        self.dynamodb_resource = boto3.resource(
            'dynamodb',
            region_name=os.environ.get('SECRET_MANAGER_REGION', os.environ.get('AURORA_SECRET_MANAGER_REGION'))
        )
        return self.dynamodb_resource

    def set_data(self: any) -> any:

        if self.constants and self.messages:
            return

        log.info('定数マスタ、メッセージマスタの初期化')
        self.messages = {f'{item["message_cd"]}': item["message"] for item in self.get_all('m_message')}

        self.constants = {}
        for constant in self.get_all('m_constant'):

            category_cd = constant.get('category_cd')
            code = constant.get('code')
            value = constant.get('value')

            if category_cd not in self.constants:
                self.constants[category_cd] = {}

            self.constants[category_cd][code] = value

    def get_all(self, table_name: str) -> any:
        client = self.resource()
        table = client.Table(table_name)
        try:
            res = table.scan()
        except ClientError as e:
            raise DynamoDbAccessError() from e
        return res.get('Items', {})
