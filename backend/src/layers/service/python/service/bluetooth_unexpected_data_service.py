import datetime
import os

from common.logger import Logger
from common.decorator.service import service
from common.utils.aws_utils import get_constant, get_s3_bucket_key
from importlib import import_module
from common.error.business_error import BusinessError

module = import_module('common.utils.aws_utils')
create_s3_objects = getattr(module, 'create_s3_objects')

log = Logger()


@service
def upload_file(gigya_uid: str, ccu_id: str, **json_data):
    # バケット名,オブジェクト名を指定
    bucket = get_s3_bucket_key('S3_BUCKET', code='UNEXPECTED')
    log.info(bucket)
    try:
        time = json_data["timestamp"]
        data_time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%fZ')

    except ValueError as ex:
        raise BusinessError() from ex
    except KeyError as ex:
        raise BusinessError() from ex

    data_time_str = datetime.datetime.strftime(data_time, '%Y%m%d%H%M%S%f')[:-3]
    year = data_time_str[:4]
    month = data_time_str[4:6]
    day = data_time_str[6:8]

    file_type = get_constant('FILE_TYPE', code='UNEXPECTED')
    file_name = f'{ccu_id}_{file_type}_{data_time_str}'
    key = f'proc/{file_type}/{gigya_uid}/{ccu_id}/{year}/{month}/{day}/{file_name}.json'
    log.info(key)

    # オブジェクトを生成し、対象のバケットにjsonデータをアップロード
    create_s3_objects(bucket, key, json_data)

    return
