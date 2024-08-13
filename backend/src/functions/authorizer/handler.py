from common.utils.time_utils import get_current_datetime, convert_str_to_datetime
from common.logger import Logger
from service import session_service as session

log = Logger()


def handler(event, context):
    log.info('event =>')
    log.info(event)

    _ = context
    effect = 'DENY'
    gigya_uid = None
    # session_id = event.get("authorizationToken", "")
    session_id = event.get('headers', {}).get('authorization', '')

    # t_sessionからsession_idに紐づくレコードを取得
    if session_id:
        # 現在日時を取得
        now_utc = get_current_datetime()

        t_session = session.get_t_session_by_session_id(session_id)

        # リクエスト日時 < 有効期限であることをチェック
        if t_session is not None and len(t_session) > 0:
            expire_session_timestamp = t_session[0].get('expire_session_timestamp')
            if expire_session_timestamp is not None:
                expire_session_timestamp = convert_str_to_datetime(expire_session_timestamp)

            if expire_session_timestamp is None or now_utc < expire_session_timestamp:
                effect = 'ALLOW'
                gigya_uid = t_session[0]['gigya_uid']

    log.info(f'gigya_uid => {gigya_uid}')

    if not gigya_uid:
        headers = event.get('headers')
        device_id = headers.get('device_id', '')

        gigya_uid = device_id.replace('-', '')

    if gigya_uid:
        effect = 'ALLOW'

    return {
        "principalId": "*",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": event['methodArn'],
                }
            ]
        },
        "context": {
            "gigya_uid": gigya_uid
        }
    }
