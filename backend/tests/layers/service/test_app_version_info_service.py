from datetime import datetime, timedelta
import pytest
from importlib import import_module, reload
from common.error.business_error import BusinessError
from common.error.old_app_version_error import OldAppVersionError
from service.app_version_info_service import update_ios_app_version, update_android_app_version, check_app_version
from repository.app_version_repository import get_app_version_list
from common.utils.aws_utils import get_constant

import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.app_version_info_service')
update_ios_app_version = getattr(module, 'update_ios_app_version')
update_android_app_version = getattr(module, 'update_android_app_version')


class ITunesRequestResponse:
    text = '{ "resultCount":1, "results": [{"version": "1.0.1"}]}'


class ITunesNotRequestResponse:
    text = '{ "resultCount":1, "results": null}'


class ITunesMatchRequestResponse:
    text = '{ "resultCount":1, "results": [{"version": "0.1.0"}]}'


class AndroidPostEditRequestResponse:
    text = '{"id": "test"}'


class AndroidPostEditNotRequestResponse:
    text = 'null'


class AndroidGetEditRequestResponse:
    text = '{"releases": [{"name": "1.1.1", "versionCodes": ["4"]}]}'


class AndroidGetEditMatchRequestResponse:
    text = '{"releases": [{"name": "1.1.0", "versionCodes": ["3"]}]}'


class AndroidGetEditNotNameRequestResponse:
    text = '{"releases": [{"name": null, "versionCodes": ["2"]}]}'


class AndroidGetEditNotTrackRequestResponse:
    text = 'null'


class AndroidGetEditNotReleasesRequestResponse:
    text = '{"releases": null}'


class AndroidDeleteEditRequestResponse:
    text = '{}'


@pytest.mark.freeze_time("2023-12-24 12:34:56.789101")
def test_update_ios_app_version_1call_ok_01(mocker):
    # requests.getのmock化
    mocker.patch(
        'requests.get',
        return_value=ITunesRequestResponse()
    )
    reload(module)

    update_ios_app_version()
    version = get_app_version_list('ios')[0]
    assert version.get('app_version') == '1.0.1'
    assert int(version.get('update_timestamp')) == int(datetime(2023, 12, 24, 12, 34, 56, 789101).timestamp())


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_ios_app_version_1call_ng_01(mocker):
    # versionが存在しない場合

    # requests.getのmock化
    mocker.patch(
        'requests.get',
        return_value=ITunesNotRequestResponse()
    )

    update_ios_app_version()

    app_version_list = get_app_version_list('ios')
    version = app_version_list[0]
    assert version.get('app_version') == '0.1.0'
    assert version.get('expiration_timestamp') is None
    assert app_version_list[1].get('app_version') == '0.0.0'
    assert int(app_version_list[1].get('expiration_timestamp')) == 1703947400
    assert int(version.get('update_timestamp')) == 1703343600


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_ios_app_version_1call_ng_02(mocker):
    # versionとapp_versionが一致の場合

    # requests.getのmock化
    mocker.patch(
        'requests.get',
        return_value=ITunesMatchRequestResponse()
    )

    update_ios_app_version()

    app_version_list = get_app_version_list('ios')
    version = app_version_list[0]
    assert version.get('app_version') == '0.1.0'
    assert version.get('expiration_timestamp') is None
    assert app_version_list[1].get('app_version') == '0.0.0'
    assert int(app_version_list[1].get('expiration_timestamp')) == 1703947400
    assert int(version.get('update_timestamp')) == 1703343600


@pytest.mark.freeze_time("2023-12-24 12:34:56.789101")
def test_update_android_app_version_1call_ok_01(mocker):
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_API_KEY': 'test'}
    )
    # requests.getのmock化
    mocker.patch(
        'requests.get',
        return_value=AndroidGetEditRequestResponse()
    )
    # requests.postのmock化
    mocker.patch(
        'requests.post',
        return_value=AndroidPostEditRequestResponse()
    )
    # requests.deleteのmock化
    mocker.patch(
        'requests.delete',
        return_value=AndroidDeleteEditRequestResponse()
    )
    reload(module)

    update_android_app_version()
    app_version_list = get_app_version_list('android')
    expiration_time = datetime(2023, 12, 24, 12, 34, 56, 789101) + timedelta(days=int(get_constant('APP_INFO', code='EXPIRATION_DELTA', default=7)))
    assert app_version_list[0].get('app_build_number', -1) == 4
    assert app_version_list[1].get('app_build_number', -1) == 3
    assert int(app_version_list[1].get('expiration_timestamp', -1)) == int(expiration_time.timestamp())
    assert int(app_version_list[0].get('update_timestamp', -1)) == int(datetime(2023, 12, 24, 12, 34, 56, 789101).timestamp())


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_android_app_version_1call_ng_01(mocker):
    # version_nameが存在しない場合
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_API_KEY': 'test'}
    )

    mocker.patch(
        'requests.get',
        return_value=AndroidGetEditNotNameRequestResponse()
    )
    mocker.patch(
        'requests.post',
        return_value=AndroidPostEditRequestResponse()
    )
    # requests.deleteのmock化
    mocker.patch(
        'requests.delete',
        return_value=AndroidDeleteEditRequestResponse()
    )
    reload(module)

    update_android_app_version()

    app_version_list = get_app_version_list('android')

    version = app_version_list[0]
    assert version.get('app_build_number', -1) == 3
    assert version.get('expiration_timestamp') is None
    assert int(app_version_list[1].get('expiration_timestamp')) == 1703948300
    assert int(version.get('update_timestamp')) == 1703343600


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_update_android_app_version_1call_ng_02(mocker):
    # app_version,app_build_numberが一致の場合
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_API_KEY': 'test'}
    )

    mocker.patch(
        'requests.get',
        return_value=AndroidGetEditMatchRequestResponse()
    )
    mocker.patch(
        'requests.post',
        return_value=AndroidPostEditRequestResponse()
    )
    # requests.deleteのmock化
    mocker.patch(
        'requests.delete',
        return_value=AndroidDeleteEditRequestResponse()
    )
    reload(module)

    update_android_app_version()

    app_version_list = get_app_version_list('android')
    version = app_version_list[0]
    assert version.get('app_build_number', -1) == 3
    assert version.get('expiration_timestamp') is None
    assert int(app_version_list[1].get('expiration_timestamp')) == 1703948300
    assert int(version.get('update_timestamp')) == 1703343600


def test_update_android_app_version_1call_ng_03(mocker):
    # editが存在しない場合
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_API_KEY': 'test'}
    )
    # requests.getのmock化
    mocker.patch(
        'requests.get',
        return_value=AndroidGetEditRequestResponse()
    )
    # requests.postのmock化
    mocker.patch(
        'requests.post',
        return_value=AndroidPostEditNotRequestResponse()
    )
    # requests.deleteのmock化
    mocker.patch(
        'requests.delete',
        return_value=AndroidDeleteEditRequestResponse()
    )
    reload(module)

    with pytest.raises(BusinessError):
        update_android_app_version()


def test_update_android_app_version_1call_ng_04(mocker):
    # trackが存在しない場合
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_API_KEY': 'test'}
    )
    # requests.getのmock化
    mocker.patch(
        'requests.get',
        return_value=AndroidGetEditNotTrackRequestResponse()
    )
    # requests.postのmock化
    mocker.patch(
        'requests.post',
        return_value=AndroidPostEditRequestResponse()
    )
    # requests.deleteのmock化
    mocker.patch(
        'requests.delete',
        return_value=AndroidDeleteEditRequestResponse()
    )
    reload(module)

    with pytest.raises(BusinessError):
        update_android_app_version()


def test_update_android_app_version_1call_ng_05(mocker):
    # releasesが存在しない場合
    # get_secretのmock化
    mocker.patch(
        'common.utils.aws_utils.get_secret',
        return_value={'GOOGLE_API_KEY': 'test'}
    )
    # requests.getのmock化
    mocker.patch(
        'requests.get',
        return_value=AndroidGetEditNotReleasesRequestResponse()
    )
    # requests.postのmock化
    mocker.patch(
        'requests.post',
        return_value=AndroidPostEditRequestResponse()
    )
    # requests.deleteのmock化
    mocker.patch(
        'requests.delete',
        return_value=AndroidDeleteEditRequestResponse()
    )
    reload(module)

    with pytest.raises(BusinessError):
        update_android_app_version()


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_ios_ok_01(mocker):
    """
    正常系 アプリバージョンチェック（ios）
    ・app_version が最新
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': 'ios',
        'app_build_number': 0,
        'app_version': '0.1.0',
        'expiration_timestamp': 1675868399
    }])
    reload(module)

    expected_value = True

    result = check_app_version({
        'os_name': 'ios',
        'app_build_number': 0,
        'app_version': '0.1.0',
        'expiration_timestamp': 1675868399
    })
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_ios_ok_02(mocker):
    """
    正常系 アプリバージョンチェック（ios）
    ・app_version が古い
    ・現在日時が expiration_timestamp よりも未来
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': 'ios',
        'app_build_number': 1,
        'app_version': '1.1.1',
        'expiration_timestamp': 1675868399
    }])
    reload(module)

    expected_value = True

    result = check_app_version({
        'os_name': 'ios',
        'app_build_number': 1,
        'app_version': '0.0.0',
        'expiration_timestamp': 1675868399
    })
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_android_ok_01(mocker):
    """
    正常系 アプリバージョンチェック（android）
    ・app_build_number が最新
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': 'android',
        'app_build_number': 1,
        'app_version': '0',
        'expiration_timestamp': 1675868399
    }])
    reload(module)

    expected_value = True

    result = check_app_version({
        'os_name': 'android',
        'app_build_number': 1,
        'app_version': '0',
        'expiration_timestamp': 1675868399
    })
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_android_ok_02(mocker):
    """
    正常系 アプリバージョンチェック（android）
    ・app_build_number が古い
    ・expiration_timestamp が現在日時よりも未来
    ※app_build_number の最新は"1"であるが、
    　検証で古いバージョンと比較する必要あるため、最新を"2"としている
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': 'android',
        'app_build_number': 2,
        'app_version': '1',
        'expiration_timestamp': 2000000000
    }, {
        'os': 'android',
        'app_build_number': 1,
        'app_version': '0',
        'expiration_timestamp': 1800000000
    }])
    mocker.patch("repository.app_version_repository.get_app_version", return_value={
        'os': 'android',
        'app_build_number': 1,
        'app_version': '0',
        'expiration_timestamp': 1800000000
    })
    reload(module)

    expected_value = True

    result = check_app_version({
        'os_name': 'android',
        'app_build_number': 1,
        'app_version': '0',
        'expiration_timestamp': 1800000000
    })
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_android_ok_03(mocker):
    """
    正常系 アプリバージョンチェック（android）
    ・app_version が古い
    ・現在日時が expiration_timestamp よりも未来
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': 'android',
        'app_build_number': 2,
        'app_version': '0.1.0',
        'expiration_timestamp': 1675868399
    }])
    reload(module)

    expected_value = True

    result = check_app_version({
        'os_name': 'android',
        'app_build_number': 2,
        'app_version': '0.1.0',
        'expiration_timestamp': 1000000000
    })
    assert result == expected_value


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_ios_ng_01(mocker):
    """
    異常系 アプリバージョンチェック（ios）
    アプリバージョンエラー
    ・app_version が古い
    ・現在日時が expiration_timestamp よりも過去
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': 'ios',
        'app_build_number': 2,
        'app_version': '0.1.0',
        'expiration_timestamp': 1000000000,
    }, {
        'os': 'ios',
        'app_build_number': 1,
        'app_version': '0.0.0',
        'expiration_timestamp': 1000000000,
    }])
    mocker.patch("repository.app_version_repository.get_app_version", return_value={
        'os': 'ios',
        'app_build_number': 1,
        'app_version': '0.0.0',
        'expiration_timestamp': 1000000000,
    })
    reload(module)

    # OldAppVersionErrorのraiseを確認
    with pytest.raises(OldAppVersionError):
        check_app_version({
            'os_name': 'ios',
            'app_build_number': 1,
            'app_version': '0.0.0',
            'expiration_timestamp': 1675868399,
        })


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_ios_ng_02(mocker):
    """
    異常系 アプリバージョンチェック（ios）
    アプリバージョンエラー
    ・app_version が存在しない
    ・現在日時が expiration_timestamp よりも過去
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': 'ios',
        'app_build_number': 1,
        'app_version': '0.0.0',
        'expiration_timestamp': 1000000000,
    }])
    mocker.patch("repository.app_version_repository.get_app_version", return_value={
        'os': 'ios',
        'app_build_number': 1,
        'app_version': '0.1',
        'expiration_timestamp': 1000000000,
    })
    reload(module)

    # OldAppVersionErrorのraiseを確認
    with pytest.raises(OldAppVersionError):
        check_app_version({
            'os_name': 'ios',
            'app_build_number': 1,
            'app_version': '0.0.-1',
            'expiration_timestamp': 1675868399,
        })


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_android_ng_01(mocker):
    """
    異常系 アプリバージョンチェック（android）
    アプリバージョンエラー
    ・app_build_number が古い
    ・現在日時が expiration_timestamp よりも過去
    ※app_build_number の最新は"1"であるが、
    　検証で古いバージョンと比較する必要あるため、最新を"2"としている
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': 'android',
        'app_build_number': 2,
        'app_version': '1.0.0',
        'expiration_timestamp': 1000000000,
    }, {
        'os': 'android',
        'app_build_number': 1,
        'app_version': '0.0.1',
        'expiration_timestamp': 1000000000,
    }])
    mocker.patch("repository.app_version_repository.get_app_version", return_value={
        'os': 'android',
        'app_build_number': 1,
        'app_version': '0.0.1',
        'expiration_timestamp': 1000000000,
    })
    reload(module)

    # OldAppVersionErrorのraiseを確認
    with pytest.raises(OldAppVersionError):
        check_app_version({
            'os_name': 'android',
            'app_build_number': 1,
            'app_version': '0',
            'expiration_timestamp': 1675868399,
        })


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_android_ng_02(mocker):
    """
    異常系 アプリバージョンチェック（android）
    アプリバージョンエラー
    ・app_build_number が存在しない
    ・現在日時が expiration_timestamp よりも過去
    ※app_build_number の最新は"1"であるが、
    　検証で古いバージョンと比較する必要あるため、最新を"2"としている
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': 'android',
        'app_build_number': None,
        'app_version': '1.0.0',
        'expiration_timestamp': 1000000000,
    }])
    mocker.patch("repository.app_version_repository.get_app_version", return_value={
        'os': 'android',
        'app_build_number': None,
        'app_version': '0.0.1',
        'expiration_timestamp': 1000000000,
    })
    reload(module)

    # OldAppVersionErrorのraiseを確認
    with pytest.raises(OldAppVersionError):
        check_app_version({
            'os_name': 'android',
            'app_build_number': 1,
            'app_version': '0',
            'expiration_timestamp': 1675868399,
        })


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_ng_01(mocker):
    """
    異常系 アプリバージョンチェック
    業務エラー
    ・os が存在しない
    ・app_build_number が存在しない
    ・app_version が存在しない
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[{
        'os': None,
        'app_build_number': None,
        'app_version': None,
    }])
    reload(module)

    # BusinessErrorのraiseを確認
    with pytest.raises(BusinessError):
        check_app_version({
            'os_name': 'android',
            'app_build_number': None,
            'app_version': None,
        })


@pytest.mark.freeze_time("2022-05-13 12:34:56.789101")
def test_check_app_version_ng_02(mocker):
    """
    異常系 アプリバージョンチェック
    業務エラー
    ・t_app_versionテーブルにレコードが存在しない
    """
    # repository.app_version_repository.get_app_version のモック化
    mocker.patch("repository.app_version_repository.get_app_version_list", return_value=[])
    reload(module)

    # BusinessErrorのraiseを確認
    with pytest.raises(BusinessError):
        check_app_version({
            'os_name': None
        })
