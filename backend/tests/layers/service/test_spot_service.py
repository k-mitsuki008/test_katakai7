from importlib import import_module, reload

module = import_module('service.spot_service')
get_spot = getattr(module, 'get_spot')


def test_get_spot_ok_01(mocker):
    """
    正常系
    """

    # repository.spot_repository.get_m_spotのモック化
    mocker.patch(
        "repository.spot_repository.get_m_spot",
        return_value=[
            {
                'spot_id': 1,
                'spot_place_id': None,
                'spot_type_code': '00001',
                'spot_location': '{"type":"Point","coordinates":[35.686178921,139.70299927]}',
                'rechargeable_flag': True
            }
        ]
    )

    reload(module)

    # 期待している返却値
    expected_value = [
        {
            "spot_id": 1,
            'spot_place_id': None,
            "spot_type_code": "00001",
            "latitude": 35.686178921,
            "longitude": 139.70299927,
            "rechargeable_flag": True
        }
    ]

    latitude, longitude, radius = 35.68617892085704, 139.70299926999502, 10
    result = get_spot(latitude, longitude, radius)
    assert result == expected_value


def test_get_spot_ok_02(mocker):
    """
    正常系 取得結果が0件の場合
    """

    # repository.spot_repository.get_m_spotのモック化
    mocker.patch(
        "repository.spot_repository.get_m_spot",
        return_value=[]
    )

    reload(module)

    # 期待している返却値
    expected_value = []

    latitude, longitude, radius = 30.68617892085704, 130.70299926999502, 10
    result = get_spot(latitude, longitude, radius)
    assert result == expected_value
