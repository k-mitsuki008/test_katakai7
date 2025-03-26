import requests
import json
from datetime import datetime, timedelta
from typing import Tuple
from common.logger import Logger
from common.decorator.service import service
from common.error.business_error import BusinessError
from common.error.old_app_version_error import OldAppVersionError
from common.utils.aws_utils import get_constant, get_secret
from repository import app_version_repository as repository

log = Logger()
# リリースしたアプリのIDを指定
ITUNES_LOOKUP_APP_URI = 'https://itunes.apple.com/lookup?id={}'
# packageNameを指定
ANDROID_EDITS_URI = 'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{}/edits?key={}'
ANDROID_EDIT_URI = 'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{}/edits/{}?key={}'
# packageName、取得したeditId、トラック種別（production, internal, alpha、beta、etc...）を指定
ANDROID_EDIT_TRACK_URI = 'https://androidpublisher.googleapis.com/androidpublisher/v3/applications/{}/edits/{}/tracks/{}?key={}'


@service
def check_app_version(user_agent: dict) -> bool():
    # バージョン情報のリストを取得してチェック
    # 最新と一致ならスルー
    # 以前のバージョンと一致なら、猶予期間チェック
    # 一致するものがないなら、システムエラー
    os_name = user_agent.get('os_name', '')
    version_key = user_agent.get('app_version')
    app_info_list = _get_published_app_version_info(os_name)
    if os_name == get_constant('OS_KIND', code='ANDROID') and user_agent.get('app_build_number'):
        if _latest_android_app_version(user_agent, app_info_list[0]):
            # 最新チェック
            return True

        app_info = repository.get_app_version(get_constant('OS_KIND', code='ANDROID'), version_key)
        if app_info and _equals_android_app_version(user_agent, app_info):
            # バージョンの存在チェク、期限チェック
            if _is_expired(app_info):
                raise OldAppVersionError()
            else:
                return True

        # 正しくバージョニングされていないケース
        raise OldAppVersionError()

    elif os_name == get_constant('OS_KIND', code='IOS') and user_agent.get('app_version'):
        if _latest_ios_app_version(user_agent, app_info_list[0]):
            # 最新チェック
            return True

        app_info = repository.get_app_version(get_constant('OS_KIND', code='IOS'), version_key)
        if app_info and _equals_ios_app_version(user_agent, app_info):
            # バージョンの存在チェク、期限チェック
            if _is_expired(app_info):
                raise OldAppVersionError()
            else:
                return True

        # 正しくバージョニングされていないケース
        raise OldAppVersionError()

    else:
        raise BusinessError()


@service
def update_ios_app_version():
    version_info_list = _get_published_app_version_info(get_constant('OS_KIND', code='IOS'))
    last_app_info = version_info_list[0]
    last_app_version = last_app_info.get('app_version')

    version = _collect_ios_app_version()
    now = datetime.now()
    expiration = now + timedelta(days=int(get_constant('APP_INFO', code='EXPIRATION_DELTA', default=7)))

    log.info(f'VERSION_INFO= {last_app_version}, {version}')
    if version and last_app_version != version:
        version_info = {
            'os': get_constant('OS_KIND', code='IOS'),
            'app_version': version,
            'update_timestamp': int(now.timestamp()),
        }
        repository.put_app_version(**version_info)

        update_info = {
            'expiration_timestamp': int(expiration.timestamp())
        }
        repository.upsert_app_version(get_constant('OS_KIND', code='IOS'), last_app_info.get('app_version'), **update_info)


@service
def update_android_app_version():
    version_info_list = _get_published_app_version_info(get_constant('OS_KIND', code='ANDROID'))
    last_app_info = version_info_list[0]
    last_app_version = last_app_info.get('app_version')
    last_app_build_number = last_app_info.get('app_build_number')

    version_name, version_code = _collect_android_app_version()
    now = datetime.now()
    expiration = now + timedelta(days=int(get_constant('APP_INFO', code='EXPIRATION_DELTA', default=7)))
    log.info(f'VERSION_INFO= {last_app_version}, {version_name}, {last_app_build_number}, {version_code}')
    if version_name and version_code is not None and (last_app_version != version_name or last_app_build_number != version_code):
        version_info = {
            'os': get_constant('OS_KIND', code='ANDROID'),
            'app_version': version_name,
            'app_build_number': version_code,
            'update_timestamp': int(now.timestamp()),
        }
        repository.put_app_version(**version_info)

        update_info = {
            'expiration_timestamp': int(expiration.timestamp())
        }
        repository.upsert_app_version(get_constant('OS_KIND', code='ANDROID'), last_app_version, **update_info)


def _get_published_app_version_info(os_name: str) -> list:
    app_info_list = repository.get_app_version_list(os_name)
    if not app_info_list:
        raise BusinessError()
    return app_info_list


def _equals_android_app_version(user_agent: dict, app_info: dict) -> bool():
    # ビルド番号チェック
    app_build_number = user_agent.get('app_build_number')
    app_build_number = int(app_build_number) if app_build_number else None
    published_build_number = app_info.get('app_build_number')
    published_build_number = int(published_build_number) if published_build_number else None
    if app_build_number and published_build_number and app_build_number == published_build_number:
        return True

    return False


def _latest_android_app_version(user_agent: dict, app_info: dict) -> bool():
    # ビルド番号チェック
    app_build_number = user_agent.get('app_build_number')
    app_build_number = int(app_build_number) if app_build_number else None
    published_build_number = app_info.get('app_build_number')
    published_build_number = int(published_build_number) if published_build_number else None
    if app_build_number and published_build_number and app_build_number >= published_build_number:
        return True

    return False


def _equals_ios_app_version(user_agent: dict, app_info: dict) -> bool():
    # ビルド番号チェック
    app_version = user_agent.get('app_version').split('.') if user_agent.get('app_version') else []
    app_major_version = int(app_version[0]) if len(app_version) > 0 else -1
    app_minor_version = int(app_version[1]) if len(app_version) > 1 else -1
    app_patch_version = int(app_version[2]) if len(app_version) > 2 else -1
    published_app_version = app_info.get('app_version').split('.') if app_info.get('app_version') else []
    published_app_major_version = int(published_app_version[0]) if len(published_app_version) > 0 else -1
    published_app_minor_version = int(published_app_version[1]) if len(published_app_version) > 1 else -1
    published_app_patch_version = int(published_app_version[2]) if len(published_app_version) > 2 else -1
    if app_major_version == published_app_major_version and app_minor_version == published_app_minor_version and app_patch_version == published_app_patch_version:
        return True

    return False


def _latest_ios_app_version(user_agent: dict, app_info: dict) -> bool():
    # ビルド番号チェック
    app_version = user_agent.get('app_version').split('.') if user_agent.get('app_version') else []
    app_major_version = int(app_version[0]) if len(app_version) > 0 else -1
    app_minor_version = int(app_version[1]) if len(app_version) > 1 else -1
    app_patch_version = int(app_version[2]) if len(app_version) > 2 else -1
    published_app_version = app_info.get('app_version').split('.') if app_info.get('app_version') else []
    published_app_major_version = int(published_app_version[0]) if len(published_app_version) > 0 else -1
    published_app_minor_version = int(published_app_version[1]) if len(published_app_version) > 1 else -1
    published_app_patch_version = int(published_app_version[2]) if len(published_app_version) > 2 else -1
    if app_major_version > published_app_major_version or\
            app_major_version >= published_app_major_version and app_minor_version > published_app_minor_version or\
            app_major_version >= published_app_major_version and app_minor_version >= published_app_minor_version and app_patch_version >= published_app_patch_version:
        return True

    return False


def _is_expired(app_info):
    # 更新期限チェック
    now = datetime.now().timestamp()
    expiration_timestamp = app_info.get('expiration_timestamp')
    if now < expiration_timestamp:
        return False

    return True


def _collect_ios_app_version() -> str:
    timeout = get_constant('TIMEOUT', code='REQUEST_TIMEOUT', default=10)
    # itunes lookup api使って、バージョン情報を取得する。
    version = ''
    app_id = get_constant('APP_INFO', 'IOS_APP_ID')
    url = ITUNES_LOOKUP_APP_URI.format(app_id)
    response = requests.get(url, timeout=timeout)
    results = json.loads(response.text).get('results', {})
    if results:
        version = results[0].get('version', '')

    return version


def _collect_android_app_version() -> Tuple[str, int]:

    timeout = get_constant('TIMEOUT', code='REQUEST_TIMEOUT', default=10)
    package_name = get_constant('APP_INFO', 'ANDROID_PKG_NAME')
    track = get_constant('APP_INFO', 'ANDROID_TRACK')
    # TODO: 認証情報はSecretManagerで管理の想定
    secrets = get_secret()
    api_key = secrets.get('GOOGLE_API_KEY')
    edit_uri = ANDROID_EDITS_URI.format(package_name, api_key)
    edit_response = requests.post(edit_uri, timeout=timeout)
    edit = json.loads(edit_response.text)
    if not edit:
        raise BusinessError()
    edit_id = edit.get('id')
    track_uri = ANDROID_EDIT_TRACK_URI.format(package_name, edit_id, track, api_key)
    track_response = requests.get(track_uri, timeout=timeout)
    track = json.loads(track_response.text)
    if not track:
        raise BusinessError()
    releases = track.get('releases', [])
    if not releases:
        raise BusinessError()
    # TODO releasesの先頭を最新としているが、これで問題ないかは要検証。versionCodesも同様。
    version_name = releases[0].get('name', '')
    version_code = releases[0].get('versionCodes')[0]

    # edit_idを無効化
    delete_edit_uri = ANDROID_EDIT_URI.format(package_name, edit_id, api_key)
    requests.delete(delete_edit_uri, timeout=timeout)

    return version_name, int(version_code)
