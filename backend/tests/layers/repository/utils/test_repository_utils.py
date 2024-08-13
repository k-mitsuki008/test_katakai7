from repository.utils.repository_utils import create_update_set_sql


def test_create_update_set_sql():
    """
    正常系
    """
    params = {
        'key': 'value'
    }
    result = create_update_set_sql(**params)
    expect = 'key = %(key)s\n ,update_timestamp = %(now_str)s \n ,update_user_id = %(gigya_uid)s'
    assert result == expect
