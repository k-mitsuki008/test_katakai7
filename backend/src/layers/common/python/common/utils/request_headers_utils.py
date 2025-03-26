USER_AGENT_KEY = 'User-Agent'


def get_user_agent(headers: dict) -> dict:
    user_agent = headers.get(USER_AGENT_KEY, '')
    return _parse_user_agent(user_agent)


def _parse_user_agent(user_agent: str) -> dict:
    tmp_ua = user_agent.split(' ') if user_agent else []
    tmp_ua_app_info = tmp_ua[0].split('/') if len(tmp_ua) >= 2 else []
    tmp_ua_os_info = ' '.join(tmp_ua[1:]).split('/') if len(tmp_ua) >= 2 else []
    app_name = tmp_ua_app_info[0] if len(tmp_ua_app_info) >= 2 else ' '
    app_version = tmp_ua_app_info[1] if len(tmp_ua_app_info) >= 2 else ' '
    app_build_number = tmp_ua_app_info[2] if len(tmp_ua_app_info) >= 3 else ''
    os_name = tmp_ua_os_info[0] if len(tmp_ua_os_info) >= 2 else ' '
    os_version = '/'.join(tmp_ua_os_info[1:]) if len(tmp_ua_os_info) >= 2 else ' '

    return {
        'app_name': app_name,
        'app_version': app_version,
        'app_build_number': app_build_number,
        'os_name': os_name,
        'os_version': os_version
    }
