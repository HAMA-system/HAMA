import datetime
import re


def convert_to_year_month(datetime_str):
    """
    datetime.datetime 형식의 문자열을 [년, 월] 형태로 변환합니다.
    매개변수:
        datetime_str (str): datetime.datetime 형식의 문자열
    반환값:
        list: [년, 월]
    """
    parsed_datetime = eval(datetime_str)
    year = parsed_datetime.year
    month = parsed_datetime.month
    return [year, month]


def convert_to_string(date):
    """
    주어진 datetime 객체를 '월.일' 형식의 문자열로 변환합니다.
    매개변수:
        date (datetime.datetime): datetime 객체
    반환값:
        str: '월.일' 형식의 문자열
    """
    month = date.month
    day = date.day
    string_date = f"{month}.{day}"
    return string_date


def is_관리비_or_위탁료(적요):
    if "관리비" in 적요:
        return "관리비"
    elif "위탁운영료" in 적요:
        return "위탁료"
    else:
        return False


def parse_month_part(data, total, current, view_data):
    month_parts = re.findall(r"\(([^()]*?월[^()]*?)\)", data)
    month_list = []
    try:
        for month_part in month_parts:
            if "월" in month_part in month_part:
                month_range = re.findall(r"\d+", month_part)
                if len(month_range) > 0:
                    if "~" in month_part:
                        range_part = re.search(r"(\d+)\s*~\s*(\d+)", month_part)
                        if range_part:
                            start, end = range_part.group(1), range_part.group(2)
                            month_list.extend(range(int(start), int(end) + 1))
                    elif "," in month_part:
                        for word in month_part.split(" "):
                            if "월" in word:
                                month_list.extend(map(int, re.findall(r"\d+", word)))
                    else:
                        month_list.extend(map(int, month_range))
        if len(month_list) == 0:
            print(
                "\033[95m"
                + "["
                + str(current + 1)
                + "/"
                + str(total)
                + "] 오류 - "
                + data
                + "\033[0m"
            )
        else:
            print(
                "[" + str(current + 1) + "/" + str(total) + "] 성공 - ",
                view_data[1],
                view_data[2],
                is_관리비_or_위탁료(view_data[3]),
                month_list,
            )

    except:
        print(
            "\033[95m" + "[" + str(current + 1) + "/" + str(total) + "] 오류 -" + data,
            month_parts,
            month_range,
            +"\033[0m",
        )

    return month_list
