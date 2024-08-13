
from common.utils.request_headers_utils import get_user_agent


def test_get_user_agent_user_agent_ok_01():
    """
    正常系
    User-Agentあり
    """
    headers = {
        "Accept": "image/gif",
        "Accept-Language": "ja",
        "Accept-Encoding": "gzip",
        "User-Agent": "Mozilla/5.0 os_name/os_version",
        "Host": "www.xxx.zzz",
        "Connection": "Keep-Alive"
    }
    expect = {
        'app_build_number': '',
        'app_name': 'Mozilla',
        'app_version': '5.0',
        'os_name': 'os_name',
        'os_version': 'os_version'
    }
    actual = get_user_agent(headers)
    assert expect == actual


def test_get_user_agent_user_agent_ok_02():
    """
    正常系
    User-Agentなし
    """
    headers = {
        "Accept": "image/gif",
        "Accept-Language": "ja",
        "Accept-Encoding": "gzip",
        "User-Agent": "",
        "Host": "www.xxx.zzz",
        "Connection": "Keep-Alive"
    }
    expect = {
        'app_build_number': '',
        'app_name': ' ',
        'app_version': ' ',
        'os_name': ' ',
        'os_version': ' '
    }
    actual = get_user_agent(headers)
    assert expect == actual
