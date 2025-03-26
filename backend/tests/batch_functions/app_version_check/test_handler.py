from importlib import import_module, reload
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.batch_functions.app_version_check.handler')
handler = getattr(module, 'handler')


class ITunesRequestResponse:
    text = '{ "resultCount":1, "results": [{"version": "1.0.1"}]}'


class AndroidGetEditRequestResponse:
    text = '{"releases": [{"name": "1.0.1", "versionCodes": ["2"]}]}'


def test_handler_ok(mocker):
    """
    正常系 アプリバージョン情報取得バッチ処理
    Mock化
    """

    # device.service.app_version_info_service import update_ios_app_version のモック化
    mocker.patch("service.app_version_info_service.update_ios_app_version", return_value=None)

    # device.service.app_version_info_service import update_android_app_version のモック化
    mocker.patch("service.app_version_info_service.update_android_app_version", return_value=None)

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = None

    response = handler({
        'version': '0',
        'id': 'abcde',
        'detail-type': 'Scheduled Event',
        'source': 'aws.events',
        'account': '889185496976',
        'time': '2022-02-22T06:00:00Z',
        'region': 'eu-west-1',
        'resources': 'abcde',
        'detail': {}
    })

    assert response == expected_value


def test_handler(mocker):
    """
    正常系 アプリバージョン情報取得バッチ処理
    Mock化なし
    """
    # get_secretのmock化
    mocker.patch(
        "service.app_version_info_service.get_secret",
        return_value={'ApiKey': '4_KYQsYzv9qps4inqV_WLniw', 'Iss': 'https://fidm.gigya.com/jwt/'}
    )
    # requests.getのmock化

    def request_get(url: str, timeout):
        if url == 'https://itunes.apple.com/lookup?id=7':
            return ITunesRequestResponse()
        else:
            return AndroidGetEditRequestResponse()

    mocker.patch(
        'requests.get',
        side_effect=request_get
    )

    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = None

    response = handler({
        'version': '0',
        'id': 'abcde',
        'detail-type': 'Scheduled Event',
        'source': 'aws.events',
        'account': '889185496976',
        'time': '2022-02-22T06:00:00Z',
        'region': 'eu-west-1',
        'resources': 'abcde',
        'detail': {}
    })

    assert response == expected_value
