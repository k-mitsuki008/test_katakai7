import os
from common.logger import Logger
from common.decorator.service import service
from common.utils.aws_utils import get_constant, get_s3_bucket_key
from common.error.s3_access_error import S3AccessError
from repository import maintain_history_repository as repository
from itertools import groupby, islice
from importlib import import_module

module = import_module('common.utils.aws_utils')
get_s3_objects = getattr(module, 'get_s3_objects')
delete_s3_objects = getattr(module, 'delete_s3_objects')

log = Logger()


@service
def get_file():
    maintain_image_ids_dict = {}
    # メンテナンス履歴TBLからgigya_uid毎の記録画像ファイルIDの一覧を管理中ファイルID一覧として取得する。
    maintain_histories = repository.get_t_maintain_history_all()

    if not maintain_histories:
        return None

    for key, value in groupby(maintain_histories, key=lambda x: x['gigya_uid']):
        for maintain_image_ids in value:
            gigya_uid = maintain_image_ids.get("gigya_uid")
            # maintain_image_idsを,区切りのリストに変換
            maintain_image_ids["maintain_image_ids"] = [x if x != "null" else None for x in maintain_image_ids.pop("maintain_image_ids").split(',')]
            # maintain_image_ids_dictにgigya_uidがキーとして存在する場合
            # pylint: disable-next=consider-iterating-dictionary
            if gigya_uid in maintain_image_ids_dict.keys():
                # 存在するキーにmaintain_image_idsの値を追加
                for maintain_image_id in maintain_image_ids.pop("maintain_image_ids"):
                    maintain_image_ids_dict[gigya_uid].append(maintain_image_id)
            # maintain_image_ids_dictにgigya_uidがキーとして存在しない場合
            else:
                # キーにgigya_uidを追加し、maintain_image_idsの値を追加
                maintain_image_ids_dict.setdefault(gigya_uid, maintain_image_ids.pop("maintain_image_ids"))
    maintain_image_ids_list = []
    size = 50
    chunks = dict_chunks(maintain_image_ids_dict, size=size)
    for file_ids in chunks:
        maintain_image_ids_list.append(file_ids)

    return maintain_image_ids_list


def dict_chunks(data, size):
    it_data = iter(data)
    for i in range(0, len(data), size):
        yield {k: data[k] for k in islice(it_data, size)}


@service
def delete_file(**kwargs):
    # 分割した管理中ファイルID一覧内のgigya_uidの件数分ループ処理を行う。
    for keys, value in kwargs.items():
        maintain_image_ids_list = set(filter(None, value))
        # S3:アップロードファイルバケット/gigya_uid/配下のS3ファイルID一覧を取得する。
        s3_bucket_key = get_s3_bucket_key('S3_BUCKET', code='UPLOAD')
        obj = get_s3_objects(s3_bucket_key, keys)
        file_list = []
        if 'Contents' in obj:
            for file in obj['Contents']:
                idx = file['Key'][file['Key'].find('/')+1:]
                if idx:
                    file_name = idx
                    file_list.append(file_name)
            s3_file = set(file_list)
            # gigya_uidが持つ記録画像ファイルIDが、S3ファイルID一覧に存在しない場合、そのS3ファイルIDを削除する。
            delete_list = s3_file - maintain_image_ids_list
            for maintain_image_id in delete_list:
                try:
                    s3_bucket_key = get_s3_bucket_key('S3_BUCKET', code='UPLOAD')
                    delete_s3_objects(s3_bucket_key, keys + "/" + maintain_image_id)
                except S3AccessError:
                    continue
    return True
