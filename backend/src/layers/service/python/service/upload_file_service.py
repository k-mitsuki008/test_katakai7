import uuid
import os
from common.logger import Logger
from common.utils.aws_utils import get_s3_url, get_constant, get_s3_bucket_key
from common.decorator.service import service

log = Logger()


@service
def get_upload_urls(gigya_uid: str, upload_file_counts: int) -> list:
    """
    アップロードファイルURL取得
    """
    bucket = get_s3_bucket_key('S3_BUCKET', code='UPLOAD')
    expires = get_constant('S3_URL_EXPIRES', 'S3_URL_EXPIRES', 900)
    path = f'{gigya_uid}/'

    upload_urls = []
    for i in range(upload_file_counts):
        file_id = str(uuid.uuid4())
        log.info(f'UPLOAD_PATH = {path + file_id}')

        url = get_s3_url(bucket, path + file_id, expires)
        upload_urls.append(
            {
                "file_id": file_id,
                "s3_url": url
            }
        )

    return upload_urls
