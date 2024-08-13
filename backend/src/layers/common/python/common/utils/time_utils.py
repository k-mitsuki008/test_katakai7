from datetime import datetime


def get_current_datetime():
    return datetime.now()


# def get_current_datetime(is_jst=True):
#     return datetime.now(pytz.timezone('Asia/Tokyo')) if is_jst else datetime.now()


def convert_datetime_to_str(datetime_date, str_format='%Y%m%d'):
    if datetime_date is None:
        return None

    return datetime.strftime(datetime_date, str_format)


def convert_str_to_datetime(datetime_str, str_format='%Y-%m-%d %H:%M:%S.%f'):
    return datetime.strptime(datetime_str, str_format)


def convert_to_jst(datetime_date_utc):
    datetime_str = convert_datetime_to_str(datetime_date_utc, '%Y-%m-%d %H:%M:%S.%f')
    return datetime.strptime(datetime_str + "+0900", "%Y-%m-%d %H:%M:%S.%f%z")


def replace_time(datetime_date: datetime, replace_time_str: str = "00:00:00.000000"):
    date_str = convert_datetime_to_str(datetime_date, '%Y-%m-%d')
    return datetime.strptime(f"{date_str}T{replace_time_str}", '%Y-%m-%dT%H:%M:%S.%f')
