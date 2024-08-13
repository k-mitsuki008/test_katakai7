
from datetime import datetime
from importlib import import_module, reload
import pytest

from common.error.not_expected_error import NotExpectedError
import tests.test_utils.fixtures as fixtures
db_setup = fixtures.db_setup
dynamodb_setup = fixtures.dynamodb_setup

module = import_module('service.device_service')
upsert_device = getattr(module, 'upsert_device')


def test_upsert_device_ok(mocker):
    """
    正常系 デバイストークン登録更新
    """
    # repository.device_repository.upsert_t_device のモック化
    mocker.patch("repository.device_repository.upsert_t_device", return_value=1)
    # repository.device_repository.update_other_device_token のモック化
    mocker.patch("repository.device_repository.update_other_device_token", return_value=1)
    # repository.device_repository.get_t_device のモック化
    mocker.patch("repository.device_repository.get_t_device", return_value={
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX",
        "device_token": "740f4707"
    })
    reload(module)

    # 期待している返却値
    expected_value = {
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX",
        "device_token": "740f4707"
    }

    rec = {
        "gigya_uid": "test_uid_01",
        "device_id": "RRRRRRRR-RRRR-4RRR-rRRR-RRRRRRRRRXXX",
        "device_token": "740f4707"
    }
    result = upsert_device(**rec)

    assert result == expected_value
