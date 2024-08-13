import json
from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.users_settings_shop.post_handler')
post_handler = getattr(module, 'handler')


def test_handler_ok(mocker):
    """
    正常系 ユーザー普段利用店舗登録更新API
    """
    # 入力データ
    input_body = {
        "regular_shop_name": "test_shop_01",
        "regular_shop_tel": "0312345678",
        "regular_shop_location": "東京都世田谷区玉川1丁目1-1",
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/users/settings/shop'
    )

    context = {}

    # device.service.upsert_t_user_shop_regularのモック化
    mocker.patch(
        "service.user_shop_regular_service.upsert_t_user_shop_regular",
        return_value={
            "regular_shop_name": "test_shop_01",
            "regular_shop_tel": "0312345678",
            "regular_shop_location": "東京都世田谷区玉川1丁目1-1",
        }
    )
    reload(module)

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "regular_shop_name": "test_shop_01",
        "regular_shop_tel": "0312345678",
        "regular_shop_location": "東京都世田谷区玉川1丁目1-1",
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    正常系 ユーザー普段利用店舗登録更新API
    バリデーションチェック
    普段利用店舗名：必須項目エラー
    電話番号：半角数字以外が入力された場合
    住所：文字数超過
    """
    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 入力データ
    input_body = {
        "regular_shop_tel": "あいうえお",
        "regular_shop_location": "東京都世田谷区玉川1丁目1-1東京都世田谷区玉川1丁目1-1東京都世田谷区玉川\
            1丁目1-1東京都世田谷区玉川1丁目1-1東京都世田谷区玉川1丁目1-1東京都世田谷区玉川1丁目1-1東京都世田谷区玉川1丁",
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/users/settings/shop'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                  "code": "E016",
                  "field": "regular_shop_location",
                  "message": "100文字以下で入力してください。",
                },
                {
                  "code": "E010",
                  "field": "regular_shop_name",
                  "message": "普段利用店舗名は必須入力項目です。"
                },
                {
                  "code": "E019",
                  "field": "regular_shop_tel",
                  "message": "半角数字で入力してください。"
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value


def test_handler_ng_02(mocker):
    """
    正常系 ユーザー普段利用店舗登録更新API
    バリデーションチェック
    普段利用店舗名：文字数超過
    電話番号：文字数超過
    """
    # 入力データ
    input_body = {
        "regular_shop_name": "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほま",
        "regular_shop_tel": "123456789012",
        "regular_shop_location": "東京都世田谷区玉川1丁目1-1",
    }
    event = get_event(
        body=input_body,
        gigya_uid='test_uid_01',
        path='/users/settings/shop'
    )
    context = {}

    # 期待しているレスポンスボディの値
    expected_value = {
        "errors": {
            "code": "E005",
            "message": "validation error",
            "validationErrors": [
                {
                  "code": "E016",
                  "field": "regular_shop_name",
                  "message": "30文字以下で入力してください。",
                },
                {
                  "code": "E016",
                  "field": "regular_shop_tel",
                  "message": "11文字以下で入力してください。"
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value
