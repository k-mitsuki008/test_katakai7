import datetime
import json
from typing import Tuple
import jwt
import requests
from jwt.algorithms import RSAAlgorithm

# pylint: disable=unused-import
from common.logger import Logger
from common.error.authorized_error import AuthorizedError
from common.response import get_response_element
from common.decorator.default_api import default_api
from common.cerberus.custom_rules import OPTIONAL_GIGYA_UID, REQUIRED_DEVICE_ID, REQUIRED_ID_TOKEN
from common.utils.aws_utils import get_secret, get_constant
from common.utils.request_headers_utils import get_user_agent
from service import session_service as session
from service import app_version_info_service as app_version_info

log = Logger()

# cerberusのvalidation定義
POST_SCHEMA: dict = {
    **OPTIONAL_GIGYA_UID,
    **REQUIRED_DEVICE_ID,
    # **REQUIRED_ID_TOKEN,
}


# pylint: disable=unused-argument
@default_api(schema=POST_SCHEMA, method='POST')
def handler(params: dict, headers: dict) -> Tuple[dict, int]:
    """
    ログインAPI
    """
    # gigya_secret = get_secret()
    # api_key = gigya_secret['ApiKey']
    # iss_prefix = gigya_secret['Iss']

    body = params
    device_id = body.get('device_id', '')
    # id_token = body.get('id_token')

    # gigya_uidの有効性チェックを実施
    # jwt_payload = jwt_verification(id_token, iss_prefix, api_key)
    # if jwt_payload is None:
    #     log.error(f'ValidateUserSignature error. id_token: {id_token}')
    #     raise AuthorizedError()
    # gigya_uid = jwt_payload['sub']
    gigya_uid = device_id.replace('-', '')

    log.info(f'gigya_uid => {gigya_uid}')

    # セッションIDをt_sessionに登録
    updated_data = session.login_session(gigya_uid, device_id)

    # アプリバージョンチェック
    # user_agent = get_user_agent(headers)
    # app_version_info.check_app_version(user_agent)

    result = {
        "result": True,
        "session_id": updated_data['session_id']
    }
    return get_response_element(result)


def jwt_verification(id_token, iss_prefix, api_key):
    """
    JWT検証
    """
    # 変数定義
    timeout = get_constant('TIMEOUT', code='REQUEST_TIMEOUT', default=10)
    cdc_iss_url = "https://fidm.gigya.com/jwt/"
    api_domain = "eu1.gigya.com"
    get_public_key_url = f"https://accounts.{api_domain}/accounts.getJWTPublicKey?apiKey={api_key}&V2=true"
    cdc_iss = cdc_iss_url + api_key + '/'

    # TokenヘッダからKey IDと署名アルゴリズムを取得
    jwt_header = jwt.get_unverified_header(id_token)
    key_id = jwt_header["kid"]
    jwt_algorithms = jwt_header["alg"]
    # 署名検証用の公開鍵を取得
    response = requests.get(get_public_key_url, timeout=timeout)
    jwk = None
    for key in json.loads(response.text)["keys"]:
        if key["kid"] == key_id:
            jwk = key
    public_key = RSAAlgorithm.from_jwk(json.dumps(jwk))
    # JWT検証
    try:
        json_payload = jwt.decode(
            id_token,
            public_key,
            algorithms=[jwt_algorithms],
            verify=True,
            options={
                "require_exp": True
            },
            issuer=cdc_iss
        )

        log.info(f'CLAIM={json_payload} {iss_prefix} {api_key}')
        # claim の iss が https://accounts.google.com もしくは accounts.google.com であることを確認する
        if json_payload['iss'] != f"{iss_prefix}{api_key}/":
            return None

        # ログイン日時がclaimのiat～exp期間内であることを確認する
        now = int(datetime.datetime.now().timestamp())
        iat = json_payload['iat']
        exp = json_payload['exp']
        if now < iat or exp < now:
            return None

        return json_payload
    except Exception as e:
        raise AuthorizedError() from e
