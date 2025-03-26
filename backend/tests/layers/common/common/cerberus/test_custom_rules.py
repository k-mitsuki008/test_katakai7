from importlib import import_module

cur = import_module('common.cerberus.custom_rules')


def test_get_constant_ok():
    """
    観点:
    DynamoDBから想定通りの定数を取得できているか
    """

    assert cur.OPTIONAL_BATTERY_REMIND_CD['battery_remind_cd']['allowed'] == ['02', '01', '00']
    assert cur.OPTIONAL_HOME_ASSIST_MODE_NUMBER['home_assist_mode_number']['allowed'] == ['02', '05', '04', '01', '03']
    assert cur.MAINTAIN_CONSCIOUSNESS['maintain_consciousness']['allowed'] == ['01', '03', '02']
