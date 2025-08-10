# Các bản thiết kế và hướng dẫn độc đáo dành cho Home Assistant

## MỚI RA MẮT - Bản thiết kế dùng cho Voice Assist gửi thông báo lên Zalo

* **Bản thiết kế này cho phép bạn gửi một nội dung bất kỳ đến một người nhận hoặc một nhóm trên Zalo bằng cách ra lệnh bằng giọng nói.**
  * Nếu là một địa điểm cụ thể, kịch bản sẽ tạo một liên kết tìm kiếm trên Google Maps, giúp bạn nhanh chóng định vị địa điểm và chỉ đường đến đó.
  * Nếu là nội dung khác, kịch bản sẽ tạo một liên kết tìm kiếm trên Google, giúp bạn dễ dàng tìm kiếm thêm thông tin nếu cần thiết.
  * Ví dụ bằng giọng nói:
    * Tìm các quán ăn ngon ở Nha Trang và gửi chúng lên Zalo
    * Gửi địa chỉ Hoàng thành Thăng Long lên Zalo

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_zalo_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## MỚI RA MẮT - Bản thiết kế dùng cho Voice Assist gửi thông báo lên Telegram

* **Bản thiết kế này cho phép bạn gửi một nội dung bất kỳ đến một người nhận hoặc một nhóm trên Telegram bằng cách ra lệnh bằng giọng nói.**
  * Nếu là một địa điểm cụ thể, kịch bản sẽ tạo một liên kết tìm kiếm trên Google Maps, giúp bạn nhanh chóng định vị địa điểm và chỉ đường đến đó.
  * Nếu là nội dung khác, kịch bản sẽ tạo một liên kết tìm kiếm trên Google, giúp bạn dễ dàng tìm kiếm thêm thông tin nếu cần thiết.
  * Ví dụ bằng giọng nói:
    * Tìm các quán ăn ngon khu vực Mỹ Đình và gửi chúng lên Telegram
    * Gửi địa chỉ Công viên Yên Sở lên Telegram

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_telegram_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## MỚI RA MẮT - Bản thiết kế dùng cho Voice Assist tìm kiếm thông tin trên Google

* **Bản thiết kế này cho phép bạn tìm kiếm mọi thông tin mới nhất trên Google bằng cách ra lệnh bằng giọng nói.**
  * Ví dụ bằng giọng nói:
    * Điểm chuẩn Đại học Bách khoa Hà Nội năm nay là bao nhiêu?

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_google_search_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng cho Voice Assist hẹn giờ bật tắt các thiết bị

* **Bản thiết kế này cho phép bạn hẹn giờ bật tắt một hay nhiều thiết bị sau một khoảng thời gian được chỉ định bằng cách ra lệnh bằng giọng nói.**
  * Ví dụ bằng giọng nói:
    * Tắt đèn và quạt phòng khách sau 30 phút
    * Tắt điều hòa phòng ngủ lúc 6h sáng

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_control_timer_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_control_tool.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng để gửi thông báo về điện thoại khi xe bị phạt nguội

* **Bản thiết kế này cho phép bạn theo dõi trạng thái phạt nguội của các xe do bạn chỉ định.**
* **Thông báo sẽ được gửi về điện thoại ngay khi có thông tin phạt nguội trên hệ thống của Cục Cảnh sát giao thông.**

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_notification.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng cho Voice Assist tra cứu phạt nguội của một xe bất kỳ

* **Bản thiết kế này cho phép bạn tra cứu phạt nguội của một phương tiện bất kỳ bằng cách ra lệnh bằng giọng nói.**
* **Dữ liệu được lấy trực tiếp từ Cổng thông tin điện tử Cục Cảnh sát giao thông.**
  * Ví dụ bằng giọng nói:
    * Kiểm tra phạt nguội ô tô 30G12345

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_lookup_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## MỚI CẬP NHẬT - Hướng dẫn cách tạo một bản chỉ dẫn hệ thống cho Voice Assist

* [**Hướng dẫn chi tiết**](/home_assistant_voice_instructions.md)

## Bản thiết kế dùng cho Voice Assist tìm kiếm nội dung trên YouTube

* **Bản thiết kế này cho phép bạn tìm kiếm các video nội dung bất kỳ trên YouTube và phát các video đó lên TV bằng cách ra lệnh bằng giọng nói.**
  * Ví dụ bằng giọng nói:
    * Tìm video về cuộc đời và sự nghiệp của ông Lê Đức Thọ
    * Ai là nhà khoa học nữ xuất sắc nhất thế kỷ 20? Tìm video về bà ấy

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_youtube_search_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng cho Voice Assist điều khiển tốc độ quạt

* **Bản thiết kế này cho phép bạn điều khiển tốc độ của một hay nhiều quạt bằng cách ra lệnh bằng giọng nói.**
  * Ví dụ bằng giọng nói:
    * Tăng tốc quạt phòng bếp
    * Chỉnh tốc độ quạt phòng ngủ xuống 50

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_speed_control_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng cho Voice Assist điều khiển quạt xoay

* **Bản thiết kế này cho phép bạn điều khiển xoay một hay nhiều quạt bằng cách ra lệnh bằng giọng nói.**
  * Ví dụ bằng giọng nói:
    * Cho xoay quạt phòng khách và bếp
    * Ngừng xoay quạt phòng ngủ

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_oscillation_control_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng cho Voice Assist tìm kiếm các video mới từ các kênh YouTube yêu thích

* **Bản thiết kế này cho phép bạn tìm kiếm video mới ra mắt gần đây của một kênh YouTube bất kỳ mà bạn yêu thích và phát các video đó lên TV bằng cách ra lệnh bằng giọng nói.**
  * Ví dụ bằng giọng nói:
    * Hoa Ban Food có video mới không?
    * Phát video mới của Sang vlog lên TV
* [**Hướng dẫn chi tiết**](/home_assistant_play_favorite_youtube_channel_videos.md)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fget_youtube_video_info_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng cho Voice Assist định vị vị trí các thiết bị di động

* **Bản thiết kế này cho phép bạn tìm kiếm vị trí các thiết bị di động bằng cách ra lệnh bằng giọng nói.**
* **Áp dụng cho các thiết bị có cài đặt ứng dụng Home Assistant hoặc các thiết bị phát BLE như đồng hồ thông minh, smart tag.**
  * Tìm kiếm và thông báo thiết bị đang ở phòng nào, và làm cho chúng đổ chuông.
  * Sử dụng khi không nhớ để thiết bị ở đâu trong nhà.
  * Ví dụ bằng giọng nói:
    * Tìm xem iPhone đang nằm đâu?
    * Tìm cái iPad và đổ chuông nó
* [**Hướng dẫn chi tiết**](/home_assistant_device_location_lookup_guide_en.md)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_location_lookup_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_ringing_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## MỚI CẬP NHẬT - Bản thiết kế dùng cho Voice Assist tra cứu chuyển đổi lịch

* **Bản thiết kế này cho phép bạn tra cứu chuyển đổi lịch bằng cách ra lệnh bằng giọng nói.**
* **Chuyển đổi ngày Dương lịch bất kỳ sang Âm lịch và ngược lại.**
* **Các thông tin bao gồm:**
  * Thứ ngày tháng năm chuyển đổi.
  * Số ngày còn lại hoặc đã qua.
  * Tiết khí.
  * Giờ tốt.
  * Ngày tốt xấu tính theo phương pháp lục diệu.
  * Ngày tốt xấu tính theo phương pháp thập nhị trực.
  * Ngày tốt xấu tính theo phương pháp nhị thập bát tú.
* **Công cụ chuyển đổi lịch này hoạt động 100% offline tốc độ phản hồi cực nhanh.**
  * Ví dụ bằng giọng nói:
    * Chủ nhật tuần này là bao nhiêu âm?
    * Rằm trung thu vào thứ mấy?
    * Còn bao nhiêu ngày nữa đến Tết?
    * Mai ngày tốt xấu thế nào?

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdate_lookup_and_conversion_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng cho Voice Assist tra cứu các sự kiện có trong lịch

* **Bản thiết kế này cho phép bạn tra cứu tất cả các sự kiện có trong lịch bằng cách ra lệnh bằng giọng nói.**
  * Ví dụ: ngày sinh nhật, ngày giỗ chạp, lịch công việc, ...
  * Ví dụ bằng giọng nói:
    * Tuần này có lịch gì không?
    * Tháng này có sự kiện gì không?

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcalendar_events_lookup_full_llm.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng để tạo các sự kiện ngày Âm lịch vào trong lịch

* **Bản thiết kế này cho phép bạn thêm mới các sự kiện tính theo Âm lịch vào trong lịch.**
  * Ví dụ: giỗ chạp, ngày cưới hỏi, ...

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcreate_lunar_events.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Bản thiết kế dùng để đồng bộ trạng thái các thiết bị

* **Bản thiết kế này cho phép bạn đồng bộ trạng thái nhiều thiết bị khác nhau.**
* **Cách hoạt động tương tự công tắc 2 chiều cầu thang.**
* **Không giới hạn chỉ ở công tắc, bản thiết kế này cho phép đồng bộ mọi thiết bị có thể bật tắt.**

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Flink_multiple_devices.yaml)

*Vui lòng đọc kỹ mô tả của bản thiết kế.*

## Hướng dẫn theo dõi cập nhật tin tức thời sự mới nhất

* **Cách tạo một bản tóm tắt các tin tức diễn ra trong 24h qua sử dụng AI.**
* [**Hướng dẫn chi tiết**](/home_assistant_get_and_summary_daily_news.md)

## Hướng dẫn cài đặt nhận thông báo khi có thiết bị mất kết nối

* **Giám sát và cảnh báo sớm khi có bất kỳ thiết bị nào bị mất kết nối.**
* [**Hướng dẫn chi tiết**](/home_assistant_unavailable_devices.md)

## Hướng dẫn cài đặt iOS Themes

* **Giao diện Home Assistant sẽ tự động đổi ngẫu nhiên vào mỗi buổi sáng và tối.**
* [**Hướng dẫn chi tiết**](/home_assistant_ios_themes.md)

### **Nếu bạn thích những tính năng này, hãy chia sẻ chúng để nhiều người cùng biết đến, cũng như theo dõi để đón chờ thêm những tính năng mới độc đáo hơn nữa nhé**

#### ***Nếu bạn gặp lỗi trong quá trình cài đặt hay sử dụng, hoặc bạn có những ý tưởng muốn đưa chúng lên Home Assistant, nhắn cho mình nhé***

![image](images/zl.jpg)
