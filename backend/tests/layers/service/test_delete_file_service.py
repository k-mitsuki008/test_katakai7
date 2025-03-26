import tests.test_utils.fixtures as fixtures
from common.error.s3_access_error import S3AccessError
from importlib import import_module, reload

db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.delete_file_service')
get_file = getattr(module, 'get_file')
delete_file = getattr(module, 'delete_file')


def test_get_file_ok_01(mocker):
    # repository.maintain_history_repository.get_t_maintain_history_all のモック化
    mocker.patch(
        "repository.maintain_history_repository.get_t_maintain_history_all",
        return_value=[
            {
                "gigya_uid": "test_uid_01",
                "maintain_image_ids": "1-1,1-2,1-3",
            },
            {
                "gigya_uid": "test_uid_01",
                "maintain_image_ids": "1-4,null,1-6",
            },
            {
                "gigya_uid": "test_uid_01",
                "maintain_image_ids": "1-7,1-8,1-9",
            },
            {
                "gigya_uid": "test_uid_02",
                "maintain_image_ids": "2-7,2-8,2-9",
            },
            {
                "gigya_uid": "test_uid_02",
                "maintain_image_ids": "2-1,2-2,2-3",
            },
            {
                "gigya_uid": "test_uid_02",
                "maintain_image_ids": "2-4,2-5,2-6",
            },
            {
                "gigya_uid": "test_uid_03",
                "maintain_image_ids": "3-1,3-2,3-3",
            },
            {
                "gigya_uid": "test_uid_03",
                "maintain_image_ids": "3-4,null,3-6",
            },
            {
                "gigya_uid": "test_uid_03",
                "maintain_image_ids": "3-7,3-8,null",
            }
        ]
    )
    reload(module)

    expected_value = [
        {
            'test_uid_01': ['1-1', '1-2', '1-3', '1-4', None, '1-6', '1-7', '1-8', '1-9'],
            'test_uid_02': ['2-7', '2-8', '2-9', '2-1', '2-2', '2-3', '2-4', '2-5', '2-6'],
            'test_uid_03': ['3-1', '3-2', '3-3', '3-4', None, '3-6', '3-7', '3-8', None]
        }
    ]

    result = get_file()
    print(f'RESULT={result}')
    assert result == expected_value


def test_get_file_ok_02(mocker):
    """
    正常系：50件以上の場合は配列が分割されること
    """
    # repository.maintain_history_repository.get_t_maintain_history_all のモック化
    def maintain_history_all() -> list:
        maintain_history_data_all = []
        num = 1
        while num <= 52:
            maintain_history_data = {
                "gigya_uid": "test_uid_" + str(num),
                "maintain_image_ids": str(num) + "-1," + str(num) + "-2," + str(num) + "-3",
            }
            maintain_history_data_all.append(maintain_history_data)
            num += 1

        return maintain_history_data_all

    mocker.patch(
        "repository.maintain_history_repository.get_t_maintain_history_all",
        side_effect=maintain_history_all
    )
    reload(module)

    expected_value = [
        {
            'test_uid_1': ['1-1', '1-2', '1-3'], 'test_uid_2': ['2-1', '2-2', '2-3'], 'test_uid_3': ['3-1', '3-2', '3-3'], 'test_uid_4': ['4-1', '4-2', '4-3'], 'test_uid_5': ['5-1', '5-2', '5-3'],
            'test_uid_6': ['6-1', '6-2', '6-3'], 'test_uid_7': ['7-1', '7-2', '7-3'], 'test_uid_8': ['8-1', '8-2', '8-3'], 'test_uid_9': ['9-1', '9-2', '9-3'], 'test_uid_10': ['10-1', '10-2', '10-3'],
            'test_uid_11': ['11-1', '11-2', '11-3'], 'test_uid_12': ['12-1', '12-2', '12-3'], 'test_uid_13': ['13-1', '13-2', '13-3'], 'test_uid_14': ['14-1', '14-2', '14-3'], 'test_uid_15': ['15-1', '15-2', '15-3'],
            'test_uid_16': ['16-1', '16-2', '16-3'], 'test_uid_17': ['17-1', '17-2', '17-3'], 'test_uid_18': ['18-1', '18-2', '18-3'], 'test_uid_19': ['19-1', '19-2', '19-3'], 'test_uid_20': ['20-1', '20-2', '20-3'],
            'test_uid_21': ['21-1', '21-2', '21-3'], 'test_uid_22': ['22-1', '22-2', '22-3'],'test_uid_23': ['23-1', '23-2', '23-3'], 'test_uid_24': ['24-1', '24-2', '24-3'], 'test_uid_25': ['25-1', '25-2', '25-3'],
            'test_uid_26': ['26-1', '26-2', '26-3'], 'test_uid_27': ['27-1', '27-2', '27-3'], 'test_uid_28': ['28-1', '28-2', '28-3'], 'test_uid_29': ['29-1', '29-2', '29-3'], 'test_uid_30': ['30-1', '30-2', '30-3'],
            'test_uid_31': ['31-1', '31-2', '31-3'], 'test_uid_32': ['32-1', '32-2', '32-3'], 'test_uid_33': ['33-1', '33-2', '33-3'], 'test_uid_34': ['34-1', '34-2', '34-3'], 'test_uid_35': ['35-1', '35-2', '35-3'],
            'test_uid_36': ['36-1', '36-2', '36-3'], 'test_uid_37': ['37-1', '37-2', '37-3'], 'test_uid_38': ['38-1', '38-2', '38-3'], 'test_uid_39': ['39-1', '39-2', '39-3'], 'test_uid_40': ['40-1', '40-2', '40-3'],
            'test_uid_41': ['41-1', '41-2', '41-3'], 'test_uid_42': ['42-1', '42-2', '42-3'], 'test_uid_43': ['43-1', '43-2', '43-3'], 'test_uid_44': ['44-1', '44-2', '44-3'], 'test_uid_45': ['45-1', '45-2', '45-3'],
            'test_uid_46': ['46-1', '46-2', '46-3'], 'test_uid_47': ['47-1', '47-2', '47-3'], 'test_uid_48': ['48-1', '48-2', '48-3'], 'test_uid_49': ['49-1', '49-2', '49-3'], 'test_uid_50': ['50-1', '50-2', '50-3']
         },
        {
            'test_uid_51': ['51-1', '51-2', '51-3'], 'test_uid_52': ['52-1', '52-2', '52-3']
        }
    ]

    result = get_file()
    print(f'RESULT={result}')
    assert result == expected_value


def test_delete_file_ok(mocker):
    # common.utils.aws_utils import get_s3_objects のモック化
    def get_s3_objects_dict_list(bucket: str, key: str) -> dict:
        result = {}
        if key == 'test_uid_01':
            result = {
                'Contents': [
                    {'Key': 'test_uid_01/', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 0, 'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_01/8-1.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 4070378, 'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_01/8-2.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687, 'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_01/8-3.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,'StorageClass': 'STANDARD'}
                ]
            }
        elif key == 'test_uid_02':
            result = {
                'Contents': [
                    {'Key': 'test_uid_02/', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 0,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_02/9-1.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 4070378,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_02/9-2.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_02/9-3.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,
                     'StorageClass': 'STANDARD'}
                ]
            }
        elif key == 'test_uid_03':
            result = {
                'Contents': [
                    {'Key': 'test_uid_03/', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 0,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_03/10-1.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 4070378,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_03/10-2.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,
                     'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_03/10-3.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,
                     'StorageClass': 'STANDARD'}
                ]
            }
        return result
    mocker.patch(
        "common.utils.aws_utils.get_s3_objects",
        side_effect=get_s3_objects_dict_list
    )

    # common.utils.aws_utils import delete_s3_objects のモック化
    mocker.patch("common.utils.aws_utils.delete_s3_objects", side_effect=lambda *args, **kwargs: args)
    reload(module)

    file: dict = {
        'test_uid_01': ['1-1', '1-2', '1-3', '1-4', None, '1-6', '1-7', '1-8', '1-9'],
        'test_uid_02': ['2-7', '2-8', '2-9', '2-1', None, '2-3', '2-4', '2-5', '2-6'],
        'test_uid_03': ['3-1', '3-2', '3-3', '3-4', None, '3-6', '3-7', '3-8', None]
    }

    result_data = delete_file(**file)
    print(f'RESULT={result_data}')
    assert result_data is True


def test_get_file_ng(mocker):
    """
     異常系 メンテナンス履歴TBLを取得出来なかった場合
    """
    # repository.maintain_history_repository.get_t_maintain_history_all のモック化
    mocker.patch("repository.maintain_history_repository.get_t_maintain_history_all", return_value=None)
    reload(module)

    expected_value = None

    result = get_file()
    print(f'RESULT={result}')
    assert result == expected_value


def test_delete_file_ng_01(mocker):
    """
     異常系 gigya_uid配下のS3ファイルID一覧を取得出来なかった場合
    """
    # common.utils.aws_utils import get_s3_objects のモック化
    mocker.patch(
        "common.utils.aws_utils.get_s3_objects",
        return_value={
            'abcdef': [{'Key': 'test_uid_01/', 'Size': 0, 'StorageClass': 'STANDARD'}]
        }
    )

    # common.utils.aws_utils import delete_s3_objects のモック化
    mocker.patch("common.utils.aws_utils.delete_s3_objects", side_effect=lambda *args, **kwargs: args)
    reload(module)

    file: dict = {
        'test_uid_01': ['1-1', '1-2', '1-3', '1-4', None, '1-6', '1-7', '1-8', '1-9']
    }

    result_data = delete_file(**file)
    print(f'RESULT={result_data}')
    assert result_data is True


def test_delete_file_ng_02(mocker):
    """
     異常系 S3ファイルIDの削除処理でS3AccessErrorの場合
    """
    # common.utils.aws_utils import get_s3_objects のモック化
    def get_s3_objects_dict_list(bucket: str, key: str) -> dict:
        result = {}
        if key == 'test_uid_01':
            result = {
                'Contents': [
                    {'Key': 'test_uid_01/', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 0, 'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_01/8-1.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 4070378, 'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_01/8-2.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687, 'StorageClass': 'STANDARD'},
                    {'Key': 'test_uid_01/8-3.png', 'LastModified': 'abcde', 'ETag': 'abcde', 'Size': 1687,'StorageClass': 'STANDARD'}
                ]
            }
        return result
    mocker.patch(
        "common.utils.aws_utils.get_s3_objects",
        side_effect=get_s3_objects_dict_list
    )

    # common.utils.aws_utils import delete_s3_objects のモック化
    mocker.patch("common.utils.aws_utils.delete_s3_objects", side_effect=S3AccessError)
    reload(module)

    file: dict = {
        'test_uid_01': ['1-1', '1-2', '1-3', '1-4', None, '1-6', '1-7', '1-8', '1-9']
    }

    result_data = delete_file(**file)
    print(f'RESULT={result_data}')
    assert result_data is True
