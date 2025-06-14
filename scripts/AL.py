"""
Download from: https://www.informatik.uni-leipzig.de/~duc/amlich/AL.py

(c) 2006 Ho Ngoc Duc.
Astronomical algorithms
from the book "Astronomical Algorithms" by Jean Meeus, 1998
"""
import datetime
import math


def jd_from_date(dd, mm, yy):
    # Compute the (integral) Julian day number of day dd/mm/yyyy,
    # i.e., the number of days between 1/1/4713 BC (Julian calendar) and dd/mm/yyyy.
    a = int((14 - mm) / 12.)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + int((153 * m + 2) / 5.) + 365 * y + int(y / 4.) - int(y / 100.) + int(y / 400.) - 32045
    if jd < 2299161:
        jd = dd + int((153 * m + 2) / 5.) + 365 * y + int(y / 4.) - 32083
    return jd


def jd_to_date(jd):  # Convert a Julian day number to day/month/year. jd is an integer.
    if jd > 2299160:  ## After 5/10/1582, Gregorian calendar
        a = jd + 32044
        b = int((4 * a + 3) / 146097.)
        c = a - int((b * 146097) / 4.)
    else:
        b = 0
        c = jd + 32082

    d = int((4 * c + 3) / 1461.)
    e = c - int((1461 * d) / 4.)
    m = int((5 * e + 2) / 153.)
    day = e - int((153 * m + 2) / 5.) + 1
    month = m + 3 - 12 * int(m / 10.)
    year = b * 100 + d - 4800 + int(m / 10.)
    return [day, month, year]


def new_moon(k):
    # Compute the time of the k-th new moon after the new moon of 1/1/1900 13:52 UCT
    # measured as the number of days since 1/1/4713 BC noon UCT, e.g., 2451545.125 is 1/1/2000 15:00 UTC.
    # Returns a floating number, e.g., 2415079.9758617813 for k=2 or 2414961.935157746 for k=-2.
    ## Time in Julian centuries from 1900 January 0.5
    t = k / 1236.85
    t2 = t * t
    t3 = t2 * t
    dr = math.pi / 180.
    jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * t2 - 0.000000155 * t3
    jd1 = jd1 + 0.00033 * math.sin((166.56 + 132.87 * t - 0.009173 * t2) * dr)
    ## Mean new moon
    m = 359.2242 + 29.10535608 * k - 0.0000333 * t2 - 0.00000347 * t3
    ## Sun's mean anomaly
    mpr = 306.0253 + 385.81691806 * k + 0.0107306 * t2 + 0.00001236 * t3
    ## Moon's mean anomaly
    f = 21.2964 + 390.67050646 * k - 0.0016528 * t2 - 0.00000239 * t3
    ## Moon's argument of latitude
    c1 = (0.1734 - 0.000393 * t) * math.sin(m * dr) + 0.0021 * math.sin(2 * dr * m)
    c1 = c1 - 0.4068 * math.sin(mpr * dr) + 0.0161 * math.sin(dr * 2 * mpr)
    c1 = c1 - 0.0004 * math.sin(dr * 3 * mpr)
    c1 = c1 + 0.0104 * math.sin(dr * 2 * f) - 0.0051 * math.sin(dr * (m + mpr))
    c1 = c1 - 0.0074 * math.sin(dr * (m - mpr)) + 0.0004 * math.sin(dr * (2 * f + m))
    c1 = c1 - 0.0004 * math.sin(dr * (2 * f - m)) - 0.0006 * math.sin(dr * (2 * f + mpr))
    c1 = c1 + 0.0010 * math.sin(dr * (2 * f - mpr)) + 0.0005 * math.sin(dr * (2 * mpr + m))
    if t < -11:
        deltat = 0.001 + 0.000839 * t + 0.0002261 * t2 - 0.00000845 * t3 - 0.000000081 * t * t3
    else:
        deltat = -0.000278 + 0.000265 * t + 0.000262 * t2
    jd_new = jd1 + c1 - deltat
    return jd_new


def sun_longitude(jdn):
    # Compute the longitude of the sun at any time.
    # Parameter: floating number jdn, the number of days since 1/1/4713 BC noon.
    t = (jdn - 2451545.0) / 36525.
    ## Time in Julian centuries
    ## from 2000-01-01 12:00:00 GMT
    t2 = t * t
    dr = math.pi / 180.  ## degree to radian
    m = 357.52910 + 35999.05030 * t - 0.0001559 * t2 - 0.00000048 * t * t2
    ## mean anomaly, degree
    l0 = 280.46645 + 36000.76983 * t + 0.0003032 * t2
    ## mean longitude, degree
    dl = (1.914600 - 0.004817 * t - 0.000014 * t2) * math.sin(dr * m)
    dl += (0.019993 - 0.000101 * t) * math.sin(dr * 2 * m) + 0.000290 * math.sin(dr * 3 * m)
    l = l0 + dl  ## true longitude, degree
    l = l * dr
    l = l - math.pi * 2 * (int(l / (math.pi * 2)))
    #### Normalize to (0, 2*math.pi)
    return l


def get_sun_longitude(day_number, time_zone):
    # Compute sun position at midnight of the day with the given Julian day number.
    # The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
    # The function returns a number between 0 and 11.
    # From the day after March equinox and the 1st major term after March equinox, 0 is returned.
    # After that, return 1, 2, 3 ...
    return int(sun_longitude(day_number - 0.5 - time_zone / 24.) / math.pi * 6)


def get_new_moon_day(k, time_zone):
    # Compute the day of the k-th new moon in the given time zone.
    # The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
    return int(new_moon(k) + 0.5 + time_zone / 24.)


def get_lunar_month_11(yy, time_zone):
    # Find the day that starts the lunar month 11 of the given year for the given time zone.

    # off = jd_from_date(31, 12, yy) - 2415021.076998695
    off = jd_from_date(31, 12, yy) - 2415021.
    k = int(off / 29.530588853)
    nm = get_new_moon_day(k, time_zone)
    sun_long = get_sun_longitude(nm, time_zone)
    #### sun longitude at local midnight
    if sun_long >= 9:
        nm = get_new_moon_day(k - 1, time_zone)
    return nm


def get_leap_month_offset(a11, time_zone):
    # Find the index of the leap month after the month starting on the day a11.
    k = int((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    i = 1  ## start with month following lunar month 11
    arc = get_sun_longitude(get_new_moon_day(k + i, time_zone), time_zone)
    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(get_new_moon_day(k + i, time_zone), time_zone)
        if not (arc != last and i < 14):
            break
    return i - 1


def solar_to_lunar(dd, mm, yy, time_zone=7):
    # Convert solar date dd/mm/yyyy to the corresponding lunar date.
    day_number = jd_from_date(dd, mm, yy)
    k = int((day_number - 2415021.076998695) / 29.530588853)
    month_start = get_new_moon_day(k + 1, time_zone)
    if month_start > day_number:
        month_start = get_new_moon_day(k, time_zone)
    a11 = get_lunar_month_11(yy, time_zone)
    b11 = a11
    if a11 >= month_start:
        lunar_year = yy
        a11 = get_lunar_month_11(yy - 1, time_zone)
    else:
        lunar_year = yy + 1
        b11 = get_lunar_month_11(yy + 1, time_zone)
    lunar_day = day_number - month_start + 1
    diff = int((month_start - a11) / 29.)
    lunar_leap = 0
    lunar_month = diff + 11
    if b11 - a11 > 365:
        leap_month_diff = get_leap_month_offset(a11, time_zone)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
            if diff == leap_month_diff:
                lunar_leap = 1
    if lunar_month > 12:
        lunar_month = lunar_month - 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1
    return [lunar_day, lunar_month, lunar_year, lunar_leap, day_number]


def lunar_to_sonar(lunar_day, lunar_month, lunar_year, lunar_leap, time_zone=7):
    # Convert a lunar date to the corresponding solar date.
    if lunar_month < 11:
        a11 = get_lunar_month_11(lunar_year - 1, time_zone)
        b11 = get_lunar_month_11(lunar_year, time_zone)
    else:
        a11 = get_lunar_month_11(lunar_year, time_zone)
        b11 = get_lunar_month_11(lunar_year + 1, time_zone)
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    off = lunar_month - 11
    if off < 0:
        off += 12
    if b11 - a11 > 365:
        leap_off = get_leap_month_offset(a11, time_zone)
        leap_month = leap_off - 2
        if leap_month < 0:
            leap_month += 12
        if lunar_leap != 0 and lunar_month != leap_month:
            return [0, 0, 0]
        elif lunar_leap != 0 or off >= leap_off:
            off += 1
    month_start = get_new_moon_day(k + off, time_zone)
    return jd_to_date(month_start + lunar_day - 1)


def get_solar_term(day_number, time_zone):
    return int((sun_longitude(day_number - 0.5 - time_zone / 24.0) / math.pi) * 12)


"""
Code xử lý truy vấn và trả về kết quả
"""

DAYS = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]

MONTHS = ["Giêng", "Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy", "Tám", "Chín", "Mười", "Mười Một", "Chạp"]

CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"]

CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"]

AUSPICIOUS_HOURS = ["110100101100", "001101001011", "110011010010", "101100110100", "001011001101", "010010110011"]

SOLAR_TERM = ["Xuân Phân", "Thanh Minh", "Cốc Vũ", "Lập Hạ", "Tiểu Mãn", "Mang Chủng",
              "Hạ Chí", "Tiểu Thử", "Đại Thử", "Lập Thu", "Xử Thử", "Bạch Lộ",
              "Thu Phân", "Hàn Lộ", "Sương Giáng", "Lập Đông", "Tiểu Tuyết", "Đại Tuyết",
              "Đông Chí", "Tiểu Hàn", "Đại Hàn", "Lập Xuân", "Vũ Thủy", "Kinh Trập"]


def validate_date(date):
    try:
        datetime.date.fromisoformat(date)
        return True
    except ValueError:
        return False


def split_date(date):
    current_date = datetime.date.fromisoformat(date)
    return current_date.day, current_date.month, current_date.year


def join_date(day, month, year):
    return datetime.date(year, month, day).isoformat()


def get_day_of_week(day, month, year):
    return datetime.date(year, month, day).weekday()


def get_auspicious_hours(jd: int) -> str:
    chi_of_day = (jd + 1) % 12
    auspicious_hours_pattern = AUSPICIOUS_HOURS[chi_of_day % 6]
    auspicious_hours = []
    for i in range(12):
        if auspicious_hours_pattern[i] == '1':
            hour_name = CHI[i]
            start_hour = (i * 2 + 23) % 24
            end_hour = (i * 2 + 1) % 24
            start_hour = f"{start_hour - 12} p.m." if start_hour > 12 else f"{start_hour} a.m."
            end_hour = f"{end_hour - 12} p.m." if end_hour > 12 else f"{end_hour} a.m."
            hour_str = f"{hour_name} ({start_hour} - {end_hour})"
            auspicious_hours.append(hour_str)

    return ", ".join(auspicious_hours)


def get_remaining_days(date):
    start_date = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    end_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    return (end_date - start_date).days


@service(supports_response="only")  # pyright: ignore[reportUndefinedVariable]
def date_conversion_tool(conversion_type: str, date: str, **kwargs) -> dict:
    """
    yaml
    name: Date Conversion Tool
    description: Tool converts Solar date (Dương lịch) to Lunar date (Âm lịch) and vice versa.
    fields:
      conversion_type:
        name: Conversion Type
        description: Type of conversion ('s2l' for Solar-to-Lunar, 'l2s' for Lunar-to-Solar)
        example: s2l
        required: true
        selector:
          select:
            options:
              - label: Solar (Dương lịch) to Lunar (Âm lịch)
                value: s2l
              - label: Lunar (Âm lịch) to Solar (Dương lịch)
                value: l2s
      date:
        name: Date
        description: Format date YYYY-MM-DD
        example: "'2025-06-15'"
        required: true
        selector:
          date: {}
      leap_month:
        name: Leap Month
        description: Is it a Lunar leap month? (Only for Lunar-to-Solar)
        example: false
        selector:
          boolean: {}
    """
    if not all([conversion_type, date]):
        return dict(error="Missing one of required arguments: conversion_type, date")

    if conversion_type not in ["s2l", "l2s"]:
        return dict(error="Wrong Conversion Type: conversion_type must be s2l or l2s")

    if not validate_date(date):
        return dict(error="Invalid date format: YYYY-MM-DD")

    day, month, year = split_date(date)
    if conversion_type == "s2l":
        try:
            l_date = solar_to_lunar(day, month, year)
            remaining_days = get_remaining_days(date)
            n_month = MONTHS[l_date[1] - 1] + (" nhuận" if l_date[3] == 1 else "")
            cc_day = CAN[(l_date[4] + 9) % 10] + " " + CHI[(l_date[4] + 1) % 12]
            cc_month = CAN[(l_date[2] * 12 + l_date[1] + 3) % 10] + " " + CHI[(l_date[1] + 1) % 12]
            cc_year = CAN[(l_date[2] + 6) % 10] + " " + CHI[(l_date[2] + 8) % 12]
            return dict(date=join_date(l_date[0], l_date[1], l_date[2]),
                        remaining_days=remaining_days,
                        full_date=f"{DAYS[get_day_of_week(day, month, year)]} ngày {l_date[0]} tháng {n_month} năm {cc_year}",
                        full_cc_date=f"{DAYS[get_day_of_week(day, month, year)]} ngày {cc_day} tháng {cc_month} năm {cc_year}",
                        leap_month=True if l_date[3] == 1 else False,
                        solar_term=SOLAR_TERM[get_solar_term(l_date[4] + 1, 7)],
                        auspicious_hours=get_auspicious_hours(l_date[4]))
        except Exception as e:
            return dict(error=f"Error converting Solar {date} to Lunar: {e}")
    elif conversion_type == "l2s":
        if day > 30:
            return dict(error="Invalid date: Lunar day must be less than or equal to 30")
        try:
            leap_month = False
            for k, v in kwargs.items():
                if k == "leap_month":
                    leap_month = bool(v)
                    break
            is_leap = 1 if leap_month else 0
            s_date = lunar_to_sonar(day, month, year, is_leap)
            remaining_days = get_remaining_days(join_date(s_date[0], s_date[1], s_date[2]))
            return dict(date=join_date(s_date[0], s_date[1], s_date[2]),
                        remaining_days=remaining_days,
                        full_date=f"{DAYS[get_day_of_week(s_date[0], s_date[1], s_date[2])]} ngày {s_date[0]} tháng {s_date[1]} năm {s_date[2]}")
        except Exception as e:
            return dict(error=f"Error converting Lunar {date} {kwargs} to Solar: {e}")
    else:
        return dict(error="Failed to convert date")
