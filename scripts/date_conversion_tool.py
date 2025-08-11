"""
Download from: https://www.informatik.uni-leipzig.de/~duc/amlich/AL.py

(c) 2006 Ho Ngoc Duc.
Astronomical algorithms
from the book "Astronomical Algorithms" by Jean Meeus, 1998
"""
import datetime
import math


@pyscript_compile
def jd_from_date(dd: int, mm: int, yy: int) -> int:
    # Compute the (integral) Julian day number of day dd/mm/yyyy,
    # i.e., the number of days between 1/1/4713 BC (Julian calendar) and dd/mm/yyyy.
    a = int((14 - mm) / 12.)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + int((153 * m + 2) / 5.) + 365 * y + int(y / 4.) - int(y / 100.) + int(y / 400.) - 32045
    if jd < 2299161:
        jd = dd + int((153 * m + 2) / 5.) + 365 * y + int(y / 4.) - 32083
    return jd


@pyscript_compile
def jd_to_date(jd: int) -> list[int]:  # Convert a Julian day number to day/month/year. jd is an integer.
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


@pyscript_compile
def new_moon(k: int) -> float:
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


@pyscript_compile
def sun_longitude(jdn: float) -> float:
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


@pyscript_compile
def get_sun_longitude(day_number: int, time_zone: int) -> int:
    # Compute sun position at midnight of the day with the given Julian day number.
    # The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
    # The function returns a number between 0 and 11.
    # From the day after March equinox and the 1st major term after March equinox, 0 is returned.
    # After that, return 1, 2, 3 ...
    return int(sun_longitude(day_number - 0.5 - time_zone / 24.) / math.pi * 6)


@pyscript_compile
def get_new_moon_day(k: int, time_zone: int) -> int:
    # Compute the day of the k-th new moon in the given time zone.
    # The time zone if the time difference between local time and UTC: 7.0 for UTC+7:00.
    return int(new_moon(k) + 0.5 + time_zone / 24.)


@pyscript_compile
def get_lunar_month_11(yy: int, time_zone: int) -> int:
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


@pyscript_compile
def get_leap_month_offset(a11: int, time_zone: int) -> int:
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


@pyscript_compile
def solar_to_lunar(dd: int, mm: int, yy: int, time_zone: int = 7) -> list[int]:
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


@pyscript_compile
def lunar_to_sonar(lunar_day: int, lunar_month: int, lunar_year: int, lunar_leap: int, time_zone: int = 7) -> list[int]:
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


@pyscript_compile
def get_solar_term(day_number: int, time_zone: int) -> int:
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

# Tý=0, Sửu=1, Dần=2, Mão=3, Thìn=4, Tỵ=5, Ngọ=6, Mùi=7, Thân=8, Dậu=9, Tuất=10, Hợi=11
AUSPICIOUS_DAY_START_CHI = {
    (1, 7): 0,  # Tháng 1, 7 (Dần, Thân) -> Bắt đầu từ Tý (index 0)
    (2, 8): 2,  # Tháng 2, 8 (Mão, Dậu)  -> Bắt đầu từ Dần (index 2)
    (3, 9): 4,  # Tháng 3, 9 (Thìn, Tuất) -> Bắt đầu từ Thìn (index 4)
    (4, 10): 6,  # Tháng 4, 10 (Tỵ, Hợi)  -> Bắt đầu từ Ngọ (index 6)
    (5, 11): 8,  # Tháng 5, 11 (Ngọ, Tý)  -> Bắt đầu từ Thân (index 8)
    (6, 12): 10  # Tháng 6, 12 (Mùi, Sửu)  -> Bắt đầu từ Tuất (index 10)
}
# Các sao trong chu kỳ Hoàng Đạo / Hắc Đạo
# T: Hoàng Đạo (Tốt), X: Hắc Đạo (Xấu), B: Trung bình (Không tốt không xấu)
# Thanh Long (T), Minh Đường (T), Thiên Hình (B), Chu Tước (X), Kim Quỹ (B), Kim Đường (T),
# Bạch Hổ (X), Ngọc Đường (T), Thiên Lao (B), Nguyên Vũ (X), Tư Mệnh (B), Câu Trận (X)
AUSPICIOUS_DAY_STATUS = [
    "T", "T", "B", "X", "B", "T",
    "X", "T", "B", "X", "B", "X"
]

# ==============================================================================
# DỮ LIỆU NHỊ THẬP BÁT TÚ
# ==============================================================================

TWENTY_EIGHT_MANSIONS = [
    {
        "Tên Sao": "Giác Mộc Giao",
        "Ý nghĩa": "Kiết tú; khí sinh trưởng, thuận mở đầu và khởi dựng nhẹ",
        "Đánh giá": "Tốt",
        "Nên làm": "Cưới hỏi, khởi công nhẹ, dựng cột/cổng, dựng khung nhà, mở hàng nhỏ, xuất hành, ký kết vừa, cắt may",
        "Nên tránh": "An táng/cải táng, xây/sửa mộ phần"
    },
    {
        "Tên Sao": "Cang Kim Long",
        "Ý nghĩa": "Hung tú; dễ sinh tranh chấp, trắc trở đại sự",
        "Đánh giá": "Xấu",
        "Nên làm": "Gieo trồng, sắp xếp kho, việc vặt trong nhà, mua bán nhỏ",
        "Nên tránh": "Xây dựng/động thổ, cưới hỏi, an táng, khai trương lớn, ký kết quan trọng, xuất hành xa"
    },
    {
        "Tên Sao": "Đê Thổ Lạc",
        "Ý nghĩa": "Hung tú; khí nặng, bất lợi cho việc lớn",
        "Đánh giá": "Xấu",
        "Nên làm": "Nông tác, dọn dẹp, tu bổ nhỏ, giao dịch nhỏ",
        "Nên tránh": "Khởi công lớn, dựng nhà, hôn lễ, an táng, khai trương lớn, nhập trạch"
    },
    {
        "Tên Sao": "Phòng Nhật Thố",
        "Ý nghĩa": "Kiết tú; thuận lễ nghi và tạo tác chính danh",
        "Đánh giá": "Tốt",
        "Nên làm": "Tế lễ, cưới hỏi, thượng lương/dựng mái, dời chỗ ở, nhập trạch, mở hàng, cắt may",
        "Nên tránh": "Kiện tụng lớn, mua đất quy mô"
    },
    {
        "Tên Sao": "Tâm Nguyệt Hồ",
        "Ý nghĩa": "Hung tú; dễ thị phi, hao tổn",
        "Đánh giá": "Xấu",
        "Nên làm": "Lễ bái giải hạn, sửa sang nhỏ, đi việc ngắn ngày, chữa bệnh",
        "Nên tránh": "Khởi công lớn, cưới hỏi, kiện tụng, khai trương lớn"
    },
    {
        "Tên Sao": "Vĩ Hỏa Hổ",
        "Ý nghĩa": "Kiết tú; cát lợi cầu tài, mưu sự tiến",
        "Đánh giá": "Tốt",
        "Nên làm": "Cưới hỏi, sửa chữa nâng cấp nhà cửa, lát sân/ngõ, khai thông mương rãnh nhẹ, ký kết làm ăn",
        "Nên tránh": "May đo lễ phục cầu kỳ, phá dỡ lớn vô cớ"
    },
    {
        "Tên Sao": "Cơ Thủy Báo",
        "Ý nghĩa": "Kiết tú; hợp kiến tạo và thủy lợi",
        "Đánh giá": "Tốt",
        "Nên làm": "Xây dựng, đào ao/giếng, nạo vét mương rãnh, mở cửa, khai thông đường nước, thu tài",
        "Nên tránh": "Hôn lễ trọng thể, cắt may lễ phục"
    },
    {
        "Tên Sao": "Đẩu Mộc Giải",
        "Ý nghĩa": "Kiết tú; hòa thuận, việc thường dễ thành",
        "Đánh giá": "Tốt",
        "Nên làm": "Xây/sửa nhà, mở cửa, khai thông nước, cắt may, lập khế ước nhỏ, mở hàng",
        "Nên tránh": "An táng lớn, phá dỡ ồ ạt"
    },
    {
        "Tên Sao": "Ngưu Kim Ngưu",
        "Ý nghĩa": "Hung tú; trì trệ, bất lợi khai mở",
        "Đánh giá": "Xấu",
        "Nên làm": "Chăn nuôi, bảo trì thiết bị, dọn dẹp kho, kiểm tra an toàn",
        "Nên tránh": "Cưới hỏi, xây dựng, mở cửa/xả nước, nhập trạch, mua bán lớn"
    },
    {
        "Tên Sao": "Nữ Thổ Bức",
        "Ý nghĩa": "Hung tú; dễ vướng thị phi/kiện tụng",
        "Đánh giá": "Xấu",
        "Nên làm": "Học nghề/kỹ nghệ, bảo trì nhỏ, chuẩn bị giấy tờ",
        "Nên tránh": "Tang sự, tranh tụng, cắt may, mở cửa/xả nước, khởi công"
    },
    {
        "Tên Sao": "Hư Nhật Thử",
        "Ý nghĩa": "Hung tú; hư hao tản mát, kỵ khai mở",
        "Đánh giá": "Xấu",
        "Nên làm": "Tĩnh tu, sắp xếp nội bộ, bảo dưỡng nhỏ, thu hồi nợ khó",
        "Nên tránh": "Mở hàng, xuất hành, ký kết, cưới hỏi, động thổ, an táng, mở cửa/xả nước"
    },
    {
        "Tên Sao": "Nguy Nguyệt Yến",
        "Ý nghĩa": "Hung tú; tiềm ẩn rủi ro, cần thận trọng",
        "Đánh giá": "Xấu",
        "Nên làm": "Kiểm định/nghiệm thu an toàn, tô trát nhỏ, công vụ cần kiểm soát rủi ro",
        "Nên tránh": "Khởi công xây cất, an táng, hôn lễ, mở cửa/xả nước, làm việc trên cao/ra biển xa"
    },
    {
        "Tên Sao": "Thất Hỏa Trư",
        "Ý nghĩa": "Kiết tú; vượng gia trạch, cát cho cư trú",
        "Đánh giá": "Tốt",
        "Nên làm": "Cưới hỏi, dời ở, xây dựng/chống thấm, tế lễ, đào giếng, đặt bếp, nhập trạch",
        "Nên tránh": "Làm tang lớn"
    },
    {
        "Tên Sao": "Bích Thủy Dư",
        "Ý nghĩa": "Kiết tú; bền ổn, lợi kiến tạo và tàng trữ",
        "Đánh giá": "Tốt",
        "Nên làm": "Cưới hỏi, xây dựng, an táng/cải táng, đắp bờ kè, dựng tường rào, lập kho",
        "Nên tránh": "Phá dỡ không cần thiết"
    },
    {
        "Tên Sao": "Khuê Mộc Lang",
        "Ý nghĩa": "Hung tú; kỵ khai mở lớn, chỉ hợp chỉnh trang",
        "Đánh giá": "Xấu",
        "Nên làm": "Cắt may, sửa cửa/sơn sửa, thay biển hiệu nhỏ, xuất hành gần",
        "Nên tránh": "Khai trương mở lớn, đầu tư mạo hiểm, ký hợp đồng dài hạn"
    },
    {
        "Tên Sao": "Lâu Kim Cẩu",
        "Ý nghĩa": "Kiết tú; ổn cho gia sự và sửa sang",
        "Đánh giá": "Tốt",
        "Nên làm": "Cưới hỏi, sửa nhà, lát sân/ngõ, làm cổng rào, dựng chuồng trại",
        "Nên tránh": "Phá dỡ lớn, chuyển kho quy mô lớn cùng ngày"
    },
    {
        "Tên Sao": "Vị Thổ Trĩ",
        "Ý nghĩa": "Kiết tú; thuận lễ nghi và công vụ",
        "Đánh giá": "Tốt",
        "Nên làm": "Cưới hỏi, xin phép/khai báo, tuyển dụng, khởi công công trình công cộng, mở cửa hàng",
        "Nên tránh": "Đầu cơ tư lợi, cắt may lễ phục, an táng"
    },
    {
        "Tên Sao": "Mão Nhật Kê",
        "Ý nghĩa": "Hung tú; dễ rối rắm, hư hỏng",
        "Đánh giá": "Xấu",
        "Nên làm": "Tu sửa nhỏ, dọn dẹp, kiểm kê, giảng dạy/học tập",
        "Nên tránh": "Động thổ, đóng giường ghế, làm mui thuyền, khai thông hào rãnh, cưới hỏi, khai trương"
    },
    {
        "Tên Sao": "Tất Nguyệt Ô",
        "Ý nghĩa": "Kiết tú; đại cát, vạn sự hanh thông",
        "Đánh giá": "Tốt",
        "Nên làm": "Khởi công, xây nhà, cưới hỏi, an táng, trổ/dựng cửa, đào giếng/kênh mương, khai trương, xuất hành, nhập học, cất nóc, nhập trạch",
        "Nên tránh": "Đi thuyền"
    },
    {
        "Tên Sao": "Chủy Hỏa Hầu",
        "Ý nghĩa": "Hung tú; dễ phát sinh tai ương",
        "Đánh giá": "Xấu",
        "Nên làm": "Kiểm tra an toàn, thu hồi/đình chỉ việc rủi ro",
        "Nên tránh": "Xây dựng, an táng, cưới hỏi, mở hàng, xuất hành, ký kết mới"
    },
    {
        "Tên Sao": "Sâm Thủy Viên",
        "Ý nghĩa": "Kiết tú; thuận hành, hợp sửa chữa vừa phải",
        "Đánh giá": "Tốt",
        "Nên làm": "Đi công vụ xa, dựng cửa, sửa chữa nhẹ, thay lợp mái nhỏ, mua sắm dụng cụ",
        "Nên tránh": "Cưới hỏi, an táng, khởi công lớn, vay vốn lớn"
    },
    {
        "Tên Sao": "Tỉnh Mộc Hãn",
        "Ý nghĩa": "Kiết tú; cát với nông canh và kiến tạo",
        "Đánh giá": "Tốt",
        "Nên làm": "Tế lễ, gieo trồng, động thổ/kiến tạo, dựng cột trụ, trồng cây lâu năm, mở nguồn nước",
        "Nên tránh": "Cắt may lễ phục"
    },
    {
        "Tên Sao": "Quỷ Kim Dương",
        "Ý nghĩa": "Hung tú; chỉ hợp việc âm, kỵ hỷ sự",
        "Đánh giá": "Xấu",
        "Nên làm": "An táng/cải táng, tu sửa mộ phần, tảo mộ",
        "Nên tránh": "Cưới hỏi, xây dựng, xuất hành, khai trương, ký kết"
    },
    {
        "Tên Sao": "Liễu Thổ Chương",
        "Ý nghĩa": "Hung tú; dễ suy hao, dính kiện tụng",
        "Đánh giá": "Xấu",
        "Nên làm": "Dọn dẹp, thanh lý đồ cũ, kiểm tra an ninh an toàn",
        "Nên tránh": "An táng, xây dựng, mở cửa/xả nước, khai trương, khởi công, đi xa"
    },
    {
        "Tên Sao": "Tinh Nhật Mã",
        "Ý nghĩa": "Hung tú; động khí mạnh, dễ quá đà",
        "Đánh giá": "Xấu",
        "Nên làm": "Trồng trọt, tuyển dụng, tổ chức hoạt động vừa, sửa chữa vệ sinh",
        "Nên tránh": "Tang sự, mở nước lớn, phá dỡ nhiều hạng mục cùng lúc"
    },
    {
        "Tên Sao": "Trương Nguyệt Lộc",
        "Ý nghĩa": "Kiết tú; vui mừng, khai xướng rực rỡ",
        "Đánh giá": "Tốt",
        "Nên làm": "Cưới hỏi, khai trương/mở chợ, tế lễ, khởi công, ký kết, mở rộng kinh doanh",
        "Nên tránh": "Kiện tụng, phá bỏ công trình đang dùng tốt"
    },
    {
        "Tên Sao": "Dực Hỏa Xà",
        "Ý nghĩa": "Hung tú; nóng nảy, bất lợi đại sự",
        "Đánh giá": "Xấu",
        "Nên làm": "Gieo trồng, thay cây, sửa vườn, kiểm định an toàn điện/nhiệt",
        "Nên tránh": "Hôn lễ, an táng, xây dựng cao, xuất hành xa, khai trương"
    },
    {
        "Tên Sao": "Chẩn Thủy Dẫn",
        "Ý nghĩa": "Kiết tú; thuận văn thư điền thổ, mưu sự ổn định",
        "Đánh giá": "Tốt",
        "Nên làm": "Mua đất, ký nhận chức, tuyển dụng/nhập học, xây dựng, cưới hỏi, cắt may, lập kho",
        "Nên tránh": "Chuyển nhà gấp, thay đổi lớn đột ngột"
    }
]

# ==============================================================================
# DỮ LIỆU THẬP NHỊ TRỰC (12 TRỰC)
# ==============================================================================

TWELVE_DAY_OFFICERS = [
    {
        "Tên Trực": "Kiến",
        "Ý nghĩa": "Khởi đầu/kiến lập; hợp việc vừa phải hơn là khai mở lớn.",
        "Đánh giá": "Trung bình",
        "Nên làm": "Xuất hành, thăm hỏi, gặp gỡ, ký kết nhỏ, cầu tài vừa",
        "Nên tránh": "Động thổ, xây cất lớn, an táng, mở kho quy mô lớn"
    },
    {
        "Tên Trực": "Trừ",
        "Ý nghĩa": "Trừ bỏ/tẩy uế; thuận loại bỏ điều xấu và làm sạch.",
        "Đánh giá": "Tốt",
        "Nên làm": "Giải hạn, dọn dẹp, tẩy uế, chữa bệnh, cắt tóc, bỏ điều cũ, xuất hành",
        "Nên tránh": "Khai trương lớn, khởi công trọng đại, chi xuất tiền lớn"
    },
    {
        "Tên Trực": "Mãn",
        "Ý nghĩa": "Viên mãn/đầy đủ; hợp thu nạp và tổng kết hơn là khởi tạo.",
        "Đánh giá": "Trung bình",
        "Nên làm": "Tế lễ, sắp xếp/nhập kho, tổng kết, nhận hàng",
        "Nên tránh": "Cưới hỏi, khởi công, mở hàng/khai trương"
    },
    {
        "Tên Trực": "Bình",
        "Ý nghĩa": "Cân bằng/yên ổn; hợp việc thường nhật, kém hợp việc lớn.",
        "Đánh giá": "Trung bình",
        "Nên làm": "Giao dịch nhỏ, gặp gỡ, học hành, khám định kỳ",
        "Nên tránh": "Khởi sự lớn, động thổ, công trình hạ tầng nặng"
    },
    {
        "Tên Trực": "Định",
        "Ý nghĩa": "Ổn định/an định; tốt để chốt việc và an vị.",
        "Đánh giá": "Tốt",
        "Nên làm": "Ký kết/khế ước, chốt kế hoạch, an vị, nhập trạch, cưới hỏi",
        "Nên tránh": "Tranh tụng, thưa kiện, xuất hành xa"
    },
    {
        "Tên Trực": "Chấp",
        "Ý nghĩa": "Giữ gìn/duy trì; thiên về duy trì bền vững, không hợp khai mở lớn.",
        "Đánh giá": "Trung bình",
        "Nên làm": "Tu sửa, xây bền vững, trồng cây lâu năm, tuyển dụng/nhận người",
        "Nên tránh": "Dời nhà, mở cửa buôn bán, xuất/nhập kho lớn, an sàng, chi tiền lớn"
    },
    {
        "Tên Trực": "Phá",
        "Ý nghĩa": "Phá bỏ/kết liễu; hợp dỡ bỏ cái cũ.",
        "Đánh giá": "Xấu",
        "Nên làm": "Phá dỡ, thanh lý, kết thúc việc cũ, trị bệnh (phá bệnh)",
        "Nên tránh": "Khởi công, khai trương, cưới hỏi, nhập trạch, ký hợp đồng mới"
    },
    {
        "Tên Trực": "Nguy",
        "Ý nghĩa": "Nguy nan/cẩn trọng; tốt khi làm việc đòi hỏi tỉ mỉ.",
        "Đánh giá": "Trung bình",
        "Nên làm": "Lễ bái, cầu an, các việc cần kiểm soát an toàn, đo đạc/thi công chi tiết",
        "Nên tránh": "Khai trương, động thổ, cưới hỏi, đi xa mạo hiểm, việc mạo hiểm sông/biển"
    },
    {
        "Tên Trực": "Thành",
        "Ý nghĩa": "Thành tựu/hoàn tất; rất thuận việc lớn và mừng.",
        "Đánh giá": "Tốt",
        "Nên làm": "Khánh thành, ký kết, khai trương, cưới hỏi, nhập trạch, nhậm chức",
        "Nên tránh": "Kiện tụng, cố ý phá dỡ"
    },
    {
        "Tên Trực": "Thu",
        "Ý nghĩa": "Thu nạp/thu hoạch; hợp gom góp cất giữ hơn là mở rộng.",
        "Đánh giá": "Trung bình",
        "Nên làm": "Thu hoạch, thu nợ, nhập kho, cất giữ",
        "Nên tránh": "Khai trương, khởi công, mở rộng mới"
    },
    {
        "Tên Trực": "Khai",
        "Ý nghĩa": "Khai mở/mở mang; đại cát cho các việc mở đầu.",
        "Đánh giá": "Tốt",
        "Nên làm": "Khai trương, khởi công nhẹ, xuất hành, đăng ký/ứng cử, nhận chức",
        "Nên tránh": "An táng; kiêng động thổ nặng, lợp mái, đào giếng"
    },
    {
        "Tên Trực": "Bế",
        "Ý nghĩa": "Đóng lại/kết thúc; kỵ khởi sự.",
        "Đánh giá": "Xấu",
        "Nên làm": "Kết thúc, đóng kho, lấp hố/đắp đập, vá sửa chỗ hư",
        "Nên tránh": "Mở hàng, khởi công, cưới hỏi, xuất hành, nhậm chức"
    }
]


@pyscript_compile
def validate_date(date: str) -> bool:
    try:
        datetime.date.fromisoformat(date)
        return True
    except ValueError:
        return False


@pyscript_compile
def split_date(date: str) -> tuple[int, int, int]:
    current_date = datetime.date.fromisoformat(date)
    return current_date.day, current_date.month, current_date.year


@pyscript_compile
def join_date(day: int, month: int, year: int) -> str:
    return datetime.date(year, month, day).isoformat()


@pyscript_compile
def get_day_of_week(day: int, month: int, year: int) -> int:
    return datetime.date(year, month, day).weekday()


@pyscript_compile
def get_twelve_day_officers(jd: int) -> dict:
    """
    Tính toán Trực của ngày dựa trên Tiết Khí (Solar Term).
    - jd: Julian Day number
    """
    st_index = get_solar_term(jd, 7)
    month_chi_list = [
        3,  # 0: Xuân Phân -> Tháng Mão
        4,  # 1: Thanh Minh -> Tháng Thìn
        4,  # 2: Cốc Vũ -> Tháng Thìn
        5,  # 3: Lập Hạ -> Tháng Tỵ
        5,  # 4: Tiểu Mãn -> Tháng Tỵ
        6,  # 5: Mang Chủng -> Tháng Ngọ
        6,  # 6: Hạ Chí -> Tháng Ngọ
        7,  # 7: Tiểu Thử -> Tháng Mùi
        7,  # 8: Đại Thử -> Tháng Mùi
        8,  # 9: Lập Thu -> Tháng Thân
        8,  # 10: Xử Thử -> Tháng Thân
        9,  # 11: Bạch Lộ -> Tháng Dậu
        9,  # 12: Thu Phân -> Tháng Dậu
        10,  # 13: Hàn Lộ -> Tháng Tuất
        10,  # 14: Sương Giáng -> Tháng Tuất
        11,  # 15: Lập Đông -> Tháng Hợi
        11,  # 16: Tiểu Tuyết -> Tháng Hợi
        0,  # 17: Đại Tuyết -> Tháng Tý
        0,  # 18: Đông Chí -> Tháng Tý
        1,  # 19: Tiểu Hàn -> Tháng Sửu
        1,  # 20: Đại Hàn -> Tháng Sửu
        2,  # 21: Lập Xuân -> Tháng Dần
        2,  # 22: Vũ Thủy -> Tháng Dần
        3  # 23: Kinh Trập -> Tháng Mão
    ]
    month_chi_index = month_chi_list[st_index]
    day_chi_index = (jd + 1) % 12
    duty_index = (day_chi_index - month_chi_index) % 12

    return TWELVE_DAY_OFFICERS[duty_index]


@pyscript_compile
def get_twenty_eight_mansions(jd: int) -> dict:
    """
    Tính toán và trả về thông tin sao (tú) trong Nhị Thập Bát Tú của một ngày.
    - jd: Julian Day number
    """
    # JD của ngày 01/01/2000 là 2451545.
    # Vị trí của sao Vị trong mảng TWENTY_EIGHT_MANSIONS là 16.
    jd_ref = 2451545
    mansion_ref_index = 16

    # Tính khoảng cách từ ngày tham chiếu đến ngày cần xem
    day_diff = jd - jd_ref

    current_mansion_index = (mansion_ref_index + day_diff) % 28

    return TWENTY_EIGHT_MANSIONS[current_mansion_index]


@pyscript_compile
def get_auspicious_day_status(lunar_month: int, jd: int) -> str:
    """
    Xác định ngày là Hoàng Đạo hay Hắc Đạo dựa trên quy tắc Lục Diệu.
    - lunar_month: tháng âm lịch (1-12)
    - jd: Julian Day number
    """
    chi_of_day_index = (jd + 1) % 12
    start_chi_index = -1
    for months, start_index in AUSPICIOUS_DAY_START_CHI.items():
        if lunar_month in months:
            start_chi_index = start_index
            break

    if start_chi_index == -1:
        return "Không xác định"

    offset = (chi_of_day_index - start_chi_index) % 12

    if AUSPICIOUS_DAY_STATUS[offset] == "T":
        return "Ngày Hoàng Đạo"
    elif AUSPICIOUS_DAY_STATUS[offset] == "X":
        return "Ngày Hắc Đạo"
    elif AUSPICIOUS_DAY_STATUS[offset] == "B":
        return "Ngày trung bình (Không tốt không xấu)"
    return "Không xác định"


@pyscript_compile
def get_auspicious_hours(jd: int) -> str:
    chi_of_day = (jd + 1) % 12
    auspicious_hours_pattern = AUSPICIOUS_HOURS[chi_of_day % 6]
    auspicious_hours = []
    for i in range(12):
        if auspicious_hours_pattern[i] == "1":
            hour_name = CHI[i]
            start_hour = (i * 2 + 23) % 24
            end_hour = (i * 2 + 1) % 24
            start_hour = f"{start_hour - 12} p.m." if start_hour > 12 else f"{start_hour} a.m."
            end_hour = f"{end_hour - 12} p.m." if end_hour > 12 else f"{end_hour} a.m."
            hour_str = f"{hour_name} ({start_hour} - {end_hour})"
            auspicious_hours.append(hour_str)

    return ", ".join(auspicious_hours)


@pyscript_compile
def get_remaining_days(date: str) -> int:
    start_date = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
    end_date = datetime.datetime.strptime(date, "%Y-%m-%d")
    return (end_date - start_date).days


@service(supports_response="only")
def date_conversion_tool(conversion_type: str, date: str, **kwargs) -> dict:
    """
    yaml
    name: Date Conversion Tool
    description: Tool converts Solar date (Dương lịch) to Lunar date (Âm lịch) and vice versa.
    fields:
      conversion_type:
        name: Conversion Type
        description: Type of conversion ("s2l" for Solar-to-Lunar, "l2s" for Lunar-to-Solar)
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
        example: '"2022-01-01"'
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
            auspicious_hours = get_auspicious_hours(l_date[4])
            auspicious_day_status = get_auspicious_day_status(l_date[1], l_date[4])
            twelve_day_officers = get_twelve_day_officers(l_date[4])
            twenty_eight_mansions = get_twenty_eight_mansions(l_date[4])
            return dict(date=join_date(l_date[0], l_date[1], l_date[2]),
                        remaining_days=remaining_days,
                        full_date=f"{DAYS[get_day_of_week(day, month, year)]} ngày {l_date[0]} tháng {n_month} năm {cc_year}",
                        full_cc_date=f"{DAYS[get_day_of_week(day, month, year)]} ngày {cc_day} tháng {cc_month} năm {cc_year}",
                        leap_month=True if l_date[3] == 1 else False,
                        solar_term=SOLAR_TERM[get_solar_term(l_date[4] + 1, 7)],
                        auspicious_hours=auspicious_hours,
                        auspicious_day_status=auspicious_day_status,
                        auspicious_day_calculated_by_twelve_day_officers=twelve_day_officers,
                        auspicious_day_calculated_by_twenty_eight_mansions=twenty_eight_mansions)
        except Exception as error:
            return dict(error=f"Error converting Solar date {date} to Lunar date: {error}")
    elif conversion_type == "l2s":
        if day > 30:
            return dict(error="Invalid date: Lunar day must be less than or equal to 30")
        try:
            leap_month = bool(kwargs.get("leap_month", False))
            is_leap = 1 if leap_month else 0
            s_date = lunar_to_sonar(day, month, year, is_leap)
            remaining_days = get_remaining_days(join_date(s_date[0], s_date[1], s_date[2]))
            day_numer = jd_from_date(s_date[0], s_date[1], s_date[2])
            cc_day = CAN[(day_numer + 9) % 10] + " " + CHI[(day_numer + 1) % 12]
            cc_month = CAN[(year * 12 + month + 3) % 10] + " " + CHI[(month + 1) % 12]
            cc_year = CAN[(year + 6) % 10] + " " + CHI[(year + 8) % 12]
            auspicious_hours = get_auspicious_hours(day_numer)
            auspicious_day_status = get_auspicious_day_status(month, day_numer)
            twelve_day_officers = get_twelve_day_officers(day_numer)
            twenty_eight_mansions = get_twenty_eight_mansions(day_numer)
            return dict(date=join_date(s_date[0], s_date[1], s_date[2]),
                        remaining_days=remaining_days,
                        full_date=f"{DAYS[get_day_of_week(s_date[0], s_date[1], s_date[2])]} ngày {s_date[0]} tháng {s_date[1]} năm {s_date[2]}",
                        full_cc_date=f"{DAYS[get_day_of_week(s_date[0], s_date[1], s_date[2])]} ngày {cc_day} tháng {cc_month} năm {cc_year}",
                        solar_term=SOLAR_TERM[get_solar_term(day_numer + 1, 7)],
                        auspicious_hours=auspicious_hours,
                        auspicious_day_status=auspicious_day_status,
                        auspicious_day_calculated_by_twelve_day_officers=twelve_day_officers,
                        auspicious_day_calculated_by_twenty_eight_mansions=twenty_eight_mansions)
        except Exception as error:
            return dict(error=f"Error converting Lunar date {date} {kwargs} to Solar date: {error}")
    else:
        return dict(error="Failed to convert date")
