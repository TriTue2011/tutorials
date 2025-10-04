# Các bản thiết kế và hướng dẫn độc đáo dành cho Home Assistant

*Tất cả các bản thiết kế (blueprint) trong tài liệu này đều được tinh chỉnh để hoạt động hiệu quả nhất với **Gemini 2.5 Flash**. Các mô hình khác có thể cần tinh chỉnh thêm để đạt kết quả như mong muốn.*

Biến Home Assistant thành trợ lý cá nhân thực thụ với bộ sưu tập blueprint và hướng dẫn bằng tiếng Việt. Mỗi kịch bản đều được thử nghiệm thực tế, có mô tả rõ ràng, ví dụ lệnh thoại và mẹo triển khai để bạn áp dụng ngay cho ngôi nhà thông minh của mình.

**[English version click here](/README.en.md)**

---

## 🧠 Voice Assist - Ghi nhớ mọi thông tin

Biến Voice Assist thành "trợ lý trí nhớ" luôn bên cạnh. Blueprint này cho phép bạn lưu trữ, cập nhật, truy xuất hoặc xoá mọi mẩu thông tin bằng giọng nói: mật khẩu Wi-Fi, vị trí đỗ xe, danh sách việc vặt... Chỉ cần hỏi, dữ liệu sẽ được đọc lại trong vài giây mà không phải mở điện thoại hay tìm kiếm thủ công.

**Ví dụ lệnh thoại:**

- Lưu lại vị trí đậu xe ở B2 R10
- Tìm lại vị trí đậu xe ở đâu?
- Ghi nhớ mật khẩu Wi-Fi khách là 123456789
- Mật khẩu Wi-Fi khách là gì?

### LLM Version

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fmemory_tool_full_llm.yaml)

### Local verion

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fmemory_tool_local.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 👀 Voice Assist - "Nhìn" thấy xung quanh

Trao cho Voice Assist khả năng truy cập các camera hoặc nguồn hình ảnh mà bạn chia sẻ. Bạn có thể yêu cầu trợ lý kiểm tra camera cụ thể, tìm thú cưng, xác nhận có người xuất hiện trước cổng hay không... tất cả đều bằng giọng nói tự nhiên và phản hồi gần như tức thì.

**Ví dụ lệnh thoại:**

- Xem các camera xem con mèo đang ở đâu
- Xem cam cổng hiện tại có người nào không

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🗓️ Voice Assist - Tạo sự kiện lịch

Sắp xếp lịch trình của bạn dễ dàng như đang trò chuyện. Blueprint này chuyển mọi lời nhắc, cuộc họp, chuyến du lịch thành sự kiện trong lịch, đồng thời kết hợp tuyệt vời với blueprint tra cứu sự kiện để nhắc bạn đúng thời điểm.

**Ví dụ lệnh thoại:**

- Tạo lịch 2h chiều mai đi cắt tóc
- Lên lịch 9h sáng mai họp trong 3 tiếng
- Thêm lịch thứ bảy này về quê
- Tạo sự kiện chủ nhật tuần sau đi chơi Phú Quốc trong 1 tuần

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcreate_calendar_event_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🤝 Tương tác 2 chiều với Zalo (Official Zalo Bot)

Kết nối Home Assistant với Official Account trên Zalo để duy trì đối thoại tự nhiên như đang chat với một trợ lý thật. Bạn có thể điều khiển thiết bị, nhờ bot gửi ảnh kèm phân tích, hoặc để bot chủ động hỏi lại khi cần thêm thông tin trước khi thực thi hành động.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fzalo_bot_webhook.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 📩 Voice Assist → Zalo (Official Bot)

Gửi nội dung đến người nhận trên Zalo chỉ bằng giọng nói. Nếu bạn nhắc tới địa điểm, blueprint tự động tạo liên kết Google Maps; với thông tin khác, đường dẫn Google Search sẽ được đính kèm để người nhận tra cứu ngay.

**Ví dụ lệnh thoại:**

- Tìm các quán ăn ngon ở Nha Trang và gửi chúng lên Zalo
- Gửi địa chỉ Hoàng thành Thăng Long kèm mô tả ngắn lên Zalo

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_zalo_bot_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🧩 Tương tác 2 chiều với Zalo (Custom Bot)

Tự xây dựng bot Zalo tùy chỉnh nhưng vẫn giữ đầy đủ khả năng hội thoại tự nhiên. Blueprint xử lý webhook, đồng bộ trạng thái và cho phép gửi/nhận đa phương tiện (ảnh, video, âm thanh, tài liệu) mà không cần tự viết lại toàn bộ logic.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fzalo_custom_bot_webhook.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 📬 Voice Assist → Zalo (Custom Bot)

Gửi tin nhắn tới người hoặc nhóm từ bot Zalo tùy chỉnh bằng giọng nói. Nếu bạn nhắc tới địa điểm, blueprint tự động tạo liên kết Google Maps; với thông tin khác, đường dẫn Google Search sẽ được đính kèm để người nhận tra cứu ngay.

**Ví dụ lệnh thoại:**

- Gửi danh sách quán ăn ngon ở Nha Trang lên nhóm Zalo
- Gửi địa chỉ Hoàng thành Thăng Long lên Zalo

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_zalo_custom_bot_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 💬 Tương tác 2 chiều với Telegram

Tạo bot Telegram để trò chuyện hai chiều với Home Assistant. Bạn có thể gửi lệnh điều khiển thiết bị, nhận phản hồi theo ngữ cảnh, đính kèm hình ảnh hoặc video từ camera và tiếp tục cuộc trò chuyện tự nhiên.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftelegram_bot_webhook.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## ✉️ Voice Assist → Telegram

Trao đổi thông tin với người thân hoặc nhóm Telegram chỉ bằng giọng nói. Nếu bạn nhắc tới địa điểm, blueprint tự động tạo liên kết Google Maps; với thông tin khác, đường dẫn Google Search sẽ được đính kèm để người nhận tra cứu ngay.

**Ví dụ lệnh thoại:**

- Tìm các quán ăn ngon khu vực Mỹ Đình và gửi chúng lên Telegram
- Gửi địa chỉ Công viên Yên Sở lên Telegram

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_telegram_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🔍 Voice Assist - Tìm kiếm Google nâng cao

Thực hiện các truy vấn Google phức tạp bằng giọng nói để nhận câu trả lời cập nhật nhất. Blueprint hỗ trợ đặt câu hỏi mở, lọc theo chủ đề và trả lại kết quả đã tóm tắt để bạn nắm bắt ngay điều quan trọng.

**Ví dụ lệnh thoại:**

- Điểm chuẩn Đại học Bách Khoa Hà Nội năm nay là bao nhiêu?
- Những công nghệ AI nổi bật trong tuần này là gì?

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_google_search_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## ⏱️ Voice Assist - Hẹn giờ bật/tắt thiết bị

Thiết lập bộ hẹn giờ cho bất kỳ thiết bị nào bằng giọng nói, từ đèn phòng khách đến máy điều hòa. Bạn có thể hẹn một thời điểm cụ thể hoặc đếm ngược, áp dụng đồng thời cho nhiều thiết bị mà không cần tạo automation thủ công.

**Ví dụ lệnh thoại:**

- Tắt đèn và quạt phòng khách sau 30 phút
- Tắt điều hòa phòng ngủ lúc 6 giờ sáng

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_control_timer_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_control_tool.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🚨 Thông báo phạt nguội

Theo dõi tình trạng phạt nguội của xe và nhận cảnh báo ngay khi có vi phạm mới trên hệ thống của Cục CSGT. Mọi thông báo đều được đẩy về Home Assistant để bạn xử lý kịp thời, tránh bỏ sót hạn nộp phạt.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_notification.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🛑 Voice Assist - Tra cứu phạt nguội

Tra cứu phạt nguội cho bất kỳ phương tiện nào bằng giọng nói, dữ liệu lấy trực tiếp từ Cổng thông tin điện tử CSGT. Bạn có thể kiểm tra biển số của người thân hoặc đối chiếu lại trước khi mua xe cũ.

**Ví dụ lệnh thoại:**

- Kiểm tra phạt nguội ô tô 30G12345

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_lookup_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 📺 Voice Assist - Tìm kiếm và phát video YouTube

Tìm kiếm nội dung YouTube rồi phát lên TV hoặc thiết bị Media Player chỉ bằng lời nói. Blueprint hỗ trợ tìm theo chủ đề, nhân vật, sự kiện và tự chọn video phù hợp nhất để phát ngay.

**Ví dụ lệnh thoại:**

- Tìm video về cuộc đời và sự nghiệp của ông Lê Đức Thọ
- Ai là nhà khoa học nữ xuất sắc nhất thế kỷ 20? Tìm video về bà ấy

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_youtube_search_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🌬️ Voice Assist - Điều khiển tốc độ quạt

Điều chỉnh tốc độ của một hoặc nhiều quạt trong nhà bằng giọng nói. Bạn có thể tăng/giảm theo phần trăm, đặt mức cụ thể hoặc đồng bộ nhiều phòng cùng lúc.

**Ví dụ lệnh thoại:**

- Tăng tốc quạt phòng bếp
- Chỉnh tốc độ quạt phòng ngủ xuống 50

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_speed_control_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🔄 Voice Assist - Điều khiển xoay quạt

Bật/tắt chế độ xoay của nhiều quạt cùng lúc bằng giọng nói. Phù hợp khi bạn muốn luân phiên hướng gió giữa các khu vực hoặc cố định quạt vào một điểm cụ thể.

**Ví dụ lệnh thoại:**

- Cho quay quạt phòng khách và bếp
- Ngừng xoay quạt phòng ngủ

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_oscillation_control_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 📡 Voice Assist - Phát video mới từ kênh YouTube yêu thích

Tự động tìm video mới nhất từ các kênh bạn theo dõi và phát ngay trên thiết bị mong muốn. Blueprint cũng báo cho bạn biết khi có video mới để không bỏ lỡ nội dung yêu thích.

**Ví dụ lệnh thoại:**

- Hoa Ban Food có video mới không?
- Phát video mới của Sang vlog lên TV

[**Hướng dẫn chi tiết**](/home_assistant_play_favorite_youtube_channel_videos.md)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fget_youtube_video_info_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 📍 Voice Assist - Tìm vị trí thiết bị di động

Định vị điện thoại, máy tính bảng, smartwatch hoặc thẻ BLE trong nhà bằng giọng nói. Trợ lý sẽ thông báo vị trí gần nhất, đồng thời có thể kích hoạt chuông để bạn tìm thiết bị nhanh chóng.

**Ví dụ lệnh thoại:**

- Tìm xem mấy cái điện thoại đang nằm đâu?
- Tìm cái iPad cho nó đổ chuông

[**Hướng dẫn chi tiết**](/home_assistant_device_location_lookup_guide_en.md)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_location_lookup_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_ringing_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🌙 Voice Assist - Tra cứu & chuyển đổi lịch Âm

Chuyển đổi nhanh giữa lịch Dương và lịch Âm, hoạt động 100% offline với tốc độ phản hồi cực nhanh. Blueprint cung cấp đầy đủ Can Chi, tiết khí, ngày tốt/xấu, giờ hoàng đạo và số ngày còn lại đến sự kiện quan trọng.

**Ví dụ lệnh thoại:**

- Chủ nhật tuần này là bao nhiêu âm?
- Rằm Trung Thu vào thứ mấy?
- Còn bao nhiêu ngày nữa đến Tết?
- Mai ngày tốt xấu thế nào?

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdate_lookup_and_conversion_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 📆 Voice Assist - Tra cứu sự kiện trong lịch

Tra cứu nhanh mọi sự kiện đã có trong lịch như sinh nhật, giỗ chạp, lịch làm việc hoặc nhắc nhở cá nhân. Kết quả được đọc rõ ràng kèm thời gian giúp bạn chủ động sắp xếp.

**Ví dụ lệnh thoại:**

- Tuần này có lịch gì không?
- Tháng này có sự kiện gì không?

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcalendar_events_lookup_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🗓️ Tạo sự kiện theo lịch Âm

Tự động thêm các sự kiện tính theo lịch Âm (giỗ, kỷ niệm, cưới hỏi...) vào lịch Dương của bạn với độ chính xác cao. Không còn phải tự quy đổi hay sợ quên những ngày truyền thống quan trọng.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcreate_lunar_events.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 🔗 Đồng bộ trạng thái nhiều thiết bị

Đồng bộ trạng thái bật/tắt giữa nhiều thiết bị giống như công tắc cầu thang hai chiều. Hoạt động được với bất kỳ thiết bị có thể bật/tắt, giúp các công tắc, cảm biến hoặc automation luôn nhất quán.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Flink_multiple_devices.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo các bước trong đó nhé.*

---

## 📘 Hướng dẫn / Tutorials

- [**Hướng dẫn cách tạo một bản chỉ dẫn hệ thống cho Voice Assist**](/home_assistant_voice_instructions.md)
- [**Hướng dẫn phát video mới từ kênh YouTube yêu thích**](/home_assistant_play_favorite_youtube_channel_videos.md)
- [**Hướng dẫn theo dõi cập nhật tin tức thời sự mới nhất**](/home_assistant_get_and_summary_daily_news.md)
- [**Hướng dẫn cài đặt nhận thông báo khi có thiết bị mất kết nối**](/home_assistant_unavailable_devices.md)
- [**Hướng dẫn cài đặt iOS Themes**](/home_assistant_ios_themes.md)
- [**Hướng dẫn tra cứu vị trí thiết bị di động**](/home_assistant_device_location_lookup_guide_en.md)

---

**Nếu bạn thấy những tính năng này hữu ích, hãy chia sẻ để nhiều người cùng biết và theo dõi để cập nhật thêm những blueprint độc đáo trong tương lai nhé!**
