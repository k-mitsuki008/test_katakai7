import json
from importlib import import_module, reload
from tests.test_utils.utils import get_event
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('src.functions.vehicles_shop.post_handler')
post_handler = getattr(module, 'handler')


def test_handler_ok(mocker):
    """
    正常系 ユーザー購入店舗登録更新API
    """
    # 入力データ
    input_body = {
        "shop_name": "test_shop_01",
        "shop_tel": "0312345678",
        "shop_location": "東京都世田谷区玉川1丁目1-1",
    }
    user_vehicle_id = {
        "user_vehicle_id": '111',
    }
    event = get_event(
        body=input_body,
        path_parameters=user_vehicle_id,
        gigya_uid='test_uid_01',
        path='/vehicles/111/shop'
    )

    context = {}

    # service.user_vehicle_service.user_vehicle_id_is_existのモック化
    mocker.patch("service.user_vehicle_service.user_vehicle_id_is_exist", return_value=None)

    # device.service.upsert_t_user_purchaseのモック化
    mocker.patch(
        "service.user_shop_purchase_service.upsert_t_user_shop_purchase",
        return_value={
            "user_vehicle_id": 111,
            "shop_name": "test_shop_01",
            "shop_tel": "0312345678",
            "shop_location": "東京都世田谷区玉川1丁目1-1",
        }
    )

    # device.service.t_user_shop_regularのモック化
    mocker.patch(
        "service.user_shop_regular_service.insert_t_user_shop_regular",
        return_value={None}
    )

    reload(module)

    # common.rds.connect.DbConnection.connect のモック化
    mocker.patch(
        "common.rds.connect.DbConnection.connect",
        return_value={None}
    )

    # 期待しているレスポンスボディの値
    expected_value = {
        "result": True,
        "user_vehicle_id": 111,
        "shop_name": "test_shop_01",
        "shop_tel": "0312345678",
        "shop_location": "東京都世田谷区玉川1丁目1-1",
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])

    assert status_code == 200
    assert body == expected_value


def test_handler_ng_01(mocker):
    """
    準正常系 ユーザー購入店舗登録更新API
    バリデーションチェック
    購入店舗名：必須項目エラー
    電話番号：半角数字以外が入力された場合
    住所：文字数超過
    user_vehicle_id：必須項目エラー
    """
    # 入力データ
    input_body = {
        "shop_name": None,
        "shop_tel": "あいうえお",
        "shop_location": "東京都世田谷区玉川1丁目1-1東京都世田谷区玉川1丁目1-1東京都世田谷区玉川1丁目1-1\
            東京都世田谷区玉川1丁目1-1東京都世田谷区玉川1丁目1-1東京都世田谷区玉川1丁目1-1東京都世田谷区玉川1丁",
    }
    user_vehicle_id = {
        "user_vehicle_id": "",
    }
    event = get_event(
        body=input_body,
        path_parameters=user_vehicle_id,
        gigya_uid='test_uid_01',
        path='/vehicles/123/shop'
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
                  "field": "shop_location",
                  "message": "100文字以下で入力してください。",
                },
                {
                  "code": "E010",
                  "field": "shop_name",
                  "message": "購入店舗名は必須入力項目です。"
                },
                {
                  "code": "E019",
                  "field": "shop_tel",
                  "message": "半角数字で入力してください。"
                },
                {
                  "code": "E007",
                  "field": "user_vehicle_id",
                  "message": "validation error"
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
    準正常系 ユーザー購入店舗登録更新API
    バリデーションチェック
    購入店舗名：文字数超過
    電話番号：文字数超過
    user_vehicle_id：半角数字以外が入力された場合
    """
    # 入力データ
    input_body = {
        "shop_name": "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほま",
        "shop_tel": "123456789012",
        "shop_location": "東京都世田谷区玉川1丁目1-1",
    }
    user_vehicle_id = {
        "user_vehicle_id": "AAA",
    }
    event = get_event(
        body=input_body,
        path_parameters=user_vehicle_id,
        gigya_uid='test_uid_01',
        path='/vehicles/123/shop'
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
                  "field": "shop_name",
                  "message": "30文字以下で入力してください。",
                },
                {
                  "code": "E016",
                  "field": "shop_tel",
                  "message": "11文字以下で入力してください。"
                },
                {
                  "code": "E007",
                  "field": "user_vehicle_id",
                  "message": "validation error"
                },
            ]
        }
    }

    response = post_handler(event, context)
    status_code = response['statusCode']
    body = json.loads(response['body'])
    assert status_code == 422
    assert body == expected_value
