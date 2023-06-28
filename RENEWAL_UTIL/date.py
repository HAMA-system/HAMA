import datetime


def convert_to_year_month(datetime_str):
    """
    datetime.datetime 형식의 문자열을 [년, 월] 형태로 변환합니다.

    매개변수:
        datetime_str (str): datetime.datetime 형식의 문자열입니다.

    반환값:
        list: [년, 월] 형태로 변환된 값입니다.
    """
    parsed_datetime = eval(datetime_str)
    year = parsed_datetime.year
    month = parsed_datetime.month
    return [year, month]
