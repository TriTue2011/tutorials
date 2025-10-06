# Các bản thiết kế và hướng dẫn độc đáo dành cho Home Assistant

*Tất cả các bản thiết kế (blueprint) trong tài liệu này đều được tinh chỉnh để hoạt động hiệu quả nhất với **Gemini 2.5 Flash**. Các mô hình khác có thể cần điều chỉnh nhẹ để đạt kết quả tối ưu.*

Biến Home Assistant thành trợ lý cá nhân thực thụ với bộ sưu tập blueprint và hướng dẫn bằng tiếng Việt. Mỗi kịch bản đều đã được thử nghiệm thực tế, mô tả rõ ràng, kèm ví dụ lệnh thoại và mẹo triển khai để bạn áp dụng ngay cho ngôi nhà thông minh của mình.

**[English version click here](/README.en.md)**

---

## 🧠 Voice Assist - Ghi nhớ mọi thông tin

Biến Voice Assist thành "trợ lý trí nhớ" luôn túc trực. Blueprint cho phép lưu trữ, cập nhật, đọc lại hoặc xoá bất kỳ mẩu thông tin nào bằng giọng nói: mật khẩu Wi-Fi, vị trí đỗ xe, danh sách việc vặt... Chỉ cần hỏi, dữ liệu sẽ được phản hồi sau vài giây mà không phải mở điện thoại hay tìm kiếm thủ công.

**Ví dụ lệnh thoại:**

- Lưu lại vị trí đậu xe ở B2 R10
- Tìm lại vị trí đậu xe ở đâu?
- Ghi nhớ mật khẩu Wi-Fi khách là 123456789
- Mật khẩu Wi-Fi khách là gì?

### Phiên bản LLM (Đa ngôn ngữ)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fmemory_tool_full_llm.yaml)

### Phiên bản Local (Chỉ tiếng Anh)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fmemory_tool_local.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 👀 Voice Assist - "Nhìn" thấy xung quanh

Trao cho Voice Assist khả năng truy cập các camera mà bạn chia sẻ. Bạn có thể yêu cầu trợ lý kiểm tra một camera cụ thể, tìm thú cưng, xác nhận có người ngoài cổng hay không... tất cả đều qua giọng nói tự nhiên với phản hồi gần như tức thì.

**Ví dụ lệnh thoại:**

- Xem các camera xem con mèo đang ở đâu
- Xem cam cổng hiện tại có người nào không

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🗓️ Voice Assist - Tạo sự kiện lịch

Sắp xếp lịch trình bằng giọng nói như đang trò chuyện. Blueprint tự động hóa việc tạo sự kiện cho mọi lời nhắc, cuộc họp hay chuyến du lịch và kết hợp tuyệt vời với blueprint tra cứu sự kiện để nhắc việc đúng lúc.

**Ví dụ lệnh thoại:**

- Tạo lịch 2h chiều mai đi cắt tóc
- Lên lịch 9h sáng mai họp trong 3 tiếng
- Thêm lịch thứ bảy này về quê
- Tạo sự kiện chủ nhật tuần sau đi chơi Phú Quốc trong 1 tuần

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcreate_calendar_event_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🤝 Tương tác 2 chiều với Zalo (Official Zalo Bot)

Kết nối Home Assistant với Official Account trên Zalo để duy trì hội thoại tự nhiên như đang chat với một trợ lý thực thụ. Điều khiển thiết bị, gửi ảnh kèm phân tích, hoặc để bot chủ động hỏi lại khi cần thêm thông tin trước khi thực thi hành động.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fzalo_bot_webhook.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 📩 Voice Assist → Zalo (Official Bot)

Gửi nội dung tới người nhận trên Zalo chỉ bằng giọng nói. Nhắc tới địa điểm sẽ tự động kèm đường dẫn Google Maps, còn thông tin khác sẽ có thêm liên kết Google Search để người nhận tra cứu nhanh.

**Ví dụ lệnh thoại:**

- Tìm các quán ăn ngon ở Nha Trang và gửi chúng lên Zalo
- Gửi địa chỉ Hoàng thành Thăng Long kèm mô tả ngắn lên Zalo

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_zalo_bot_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🧩 Tương tác 2 chiều với Zalo (Custom Bot)

Tự xây dựng bot Zalo tuỳ chỉnh nhưng vẫn đầy đủ khả năng hội thoại thông minh. Blueprint xử lý webhook, đồng bộ trạng thái và hỗ trợ gửi/nhận đa phương tiện (ảnh, video, âm thanh, tài liệu) mà không cần tự viết lại toàn bộ logic.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fzalo_custom_bot_webhook.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 📬 Voice Assist → Zalo (Custom Bot)

Gửi tin nhắn tới cá nhân hoặc nhóm thông qua bot Zalo tuỳ chỉnh bằng giọng nói. Nhắc đến địa điểm sẽ tự sinh liên kết Google Maps, các nội dung khác kèm thêm đường dẫn Google Search để người nhận kiểm tra ngay lập tức.

**Ví dụ lệnh thoại:**

- Gửi danh sách quán ăn ngon ở Nha Trang lên nhóm Zalo gia đình
- Gửi địa chỉ Hoàng thành Thăng Long cho Zalo của vợ anh

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_zalo_custom_bot_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 💬 Tương tác 2 chiều với Telegram

Tạo bot Telegram trò chuyện hai chiều với Home Assistant. Bạn có thể gửi lệnh điều khiển, nhận phản hồi theo ngữ cảnh, đính kèm hình ảnh hoặc video từ camera và tiếp tục hội thoại liền mạch.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftelegram_bot_webhook.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## ✉️ Voice Assist → Telegram

Trao đổi thông tin với bạn bè hoặc nhóm Telegram bằng giọng nói. Địa điểm sẽ tự động chuyển thành liên kết Google Maps, còn thông tin khác đi kèm đường dẫn Google Search giúp người nhận kiểm tra chi tiết ngay.

**Ví dụ lệnh thoại:**

- Tìm các quán ăn ngon khu vực Mỹ Đình và gửi chúng lên Telegram
- Gửi địa chỉ Công viên Yên Sở lên Telegram

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_telegram_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🔍 Voice Assist - Tìm kiếm Google nâng cao

Thực hiện mọi truy vấn Google bằng giọng nói và nhận câu trả lời cập nhật nhất. Blueprint hỗ trợ câu hỏi mở, lọc theo chủ đề và trả kết quả đã tóm tắt để bạn nắm bắt thông tin quan trọng ngay.

**Ví dụ lệnh thoại:**

- Điểm chuẩn Đại học Bách Khoa Hà Nội năm nay là bao nhiêu?
- Những công nghệ AI nổi bật trong tuần này là gì?

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_google_search_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## ⏱️ Voice Assist - Hẹn giờ bật/tắt thiết bị

Thiết lập hẹn giờ cho bất kỳ thiết bị nào bằng giọng nói, từ đèn phòng khách đến máy điều hòa. Bạn có thể đặt thời điểm cụ thể, đếm ngược hoặc áp dụng cho nhiều thiết bị cùng lúc mà không cần tự viết automation.

**Ví dụ lệnh thoại:**

- Tắt đèn và quạt phòng khách sau 30 phút
- Tắt điều hòa phòng ngủ lúc 6 giờ sáng

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_control_timer_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_control_tool.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🚨 Thông báo phạt nguội

Theo dõi tình trạng phạt nguội của xe và nhận cảnh báo ngay khi có vi phạm mới trên hệ thống của Cục CSGT. Mọi thông báo được đẩy thẳng vào Home Assistant để bạn xử lý kịp thời, tránh bỏ lỡ hạn nộp phạt.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_notification.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🛑 Voice Assist - Tra cứu phạt nguội

Tra cứu phạt nguội của bất kỳ phương tiện nào bằng giọng nói với dữ liệu lấy trực tiếp từ Cổng thông tin điện tử CSGT. Tiện lợi để kiểm tra xe của gia đình hoặc đối chiếu trước khi mua xe cũ.

**Ví dụ lệnh thoại:**

- Kiểm tra phạt nguội ô tô 30G12345

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_lookup_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 📺 Voice Assist - Tìm kiếm và phát video YouTube

Tìm kiếm nội dung YouTube rồi phát trên TV hoặc thiết bị media bằng giọng nói. Blueprint hỗ trợ tìm theo chủ đề, nhân vật, sự kiện và chọn video phù hợp nhất để phát ngay.

**Ví dụ lệnh thoại:**

- Tìm video về cuộc đời và sự nghiệp của ông Lê Đức Thọ
- Ai là nhà khoa học nữ xuất sắc nhất thế kỷ 20? Tìm video về bà ấy

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_youtube_search_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🌬️ Voice Assist - Điều khiển tốc độ quạt

Điều chỉnh tốc độ cho một hoặc nhiều quạt trong nhà bằng giọng nói. Bạn có thể tăng/giảm theo phần trăm, đặt mức cụ thể hoặc đồng bộ nhiều phòng cùng lúc.

**Ví dụ lệnh thoại:**

- Tăng tốc quạt phòng bếp
- Chỉnh tốc độ quạt phòng ngủ xuống 50

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_speed_control_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🔄 Voice Assist - Điều khiển xoay quạt

Bật/tắt chế độ xoay cho nhiều quạt cùng lúc bằng giọng nói. Hoàn hảo khi bạn muốn luân phiên hướng gió giữa các khu vực hoặc cố định quạt vào một điểm cụ thể.

**Ví dụ lệnh thoại:**

- Cho quay quạt phòng khách và bếp
- Ngừng xoay quạt phòng ngủ

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_oscillation_control_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 📡 Voice Assist - Phát video mới từ kênh YouTube yêu thích

Tự động phát hiện video mới nhất từ các kênh bạn theo dõi và phát ngay trên thiết bị mong muốn. Blueprint cũng có thể gửi thông báo khi có nội dung mới để bạn không bỏ lỡ video yêu thích.

**Ví dụ lệnh thoại:**

- Hoa Ban Food có video mới không?
- Phát video mới của Sang vlog lên TV

[**Hướng dẫn chi tiết**](/home_assistant_play_favorite_youtube_channel_videos.md)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fget_youtube_video_info_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 📍 Voice Assist - Tìm vị trí thiết bị di động

Định vị điện thoại, máy tính bảng, smartwatch hoặc thẻ BLE trong nhà bằng giọng nói. Trợ lý sẽ thông báo vị trí gần nhất và có thể kích hoạt chuông để bạn tìm thiết bị nhanh chóng.

**Ví dụ lệnh thoại:**

- Tìm xem mấy cái điện thoại đang ở đâu?
- Tìm cái iPad và để chuông nó

[**Hướng dẫn chi tiết**](/home_assistant_device_location_lookup_guide_en.md)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_location_lookup_full_llm.yaml)

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_ringing_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🌙 Voice Assist - Tra cứu & chuyển đổi lịch Âm

Chuyển đổi tức thì giữa lịch Dương và lịch Âm, hoạt động 100% offline với tốc độ phản hồi cực nhanh. Blueprint cung cấp đầy đủ Can Chi, tiết khí, ngày tốt/xấu, giờ hòang đạo và số ngày còn lại tới các sự kiện quan trọng.

**Ví dụ lệnh thoại:**

- Chủ nhật tuần này là bao nhiêu âm?
- Rằm Trung Thu vào thứ mấy?
- Còn bao nhiêu ngày nữa đến Tết?
- Mai ngày tốt xấu thế nào?

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdate_lookup_and_conversion_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 📆 Voice Assist - Tra cứu sự kiện trong lịch

Kiểm tra nhanh các sự kiện đã có trong lịch như sinh nhật, giỗ chạp, lịch làm việc hay nhắc nhở cá nhân. Voice Assist sẽ đọc lại rõ ràng kèm thời gian để bạn chủ động sắp xếp.

**Ví dụ lệnh thoại:**

- Tuần này có lịch gì không?
- Tháng này có sự kiện gì không?

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcalendar_events_lookup_full_llm.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🗓️ Tạo sự kiện theo lịch Âm

Tự động thêm các sự kiện tính theo lịch Âm (giỗ, kỷ niệm, cưới hỏi...) vào lịch Dương của bạn với độ chính xác cao. Không còn phải tự quy đổi hay sợ quên những ngày truyền thống quan trọng.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcreate_lunar_events.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 🔗 Đồng bộ trạng thái nhiều thiết bị

Đồng bộ trạng thái bật/tắt giữa nhiều thiết bị giống như công tắc cầu thang hai chiều. Hoạt động với bất kỳ thiết bị có thể bật/tắt, giúp công tắc, cảm biến hoặc automation luôn ăn khớp với nhau.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Flink_multiple_devices.yaml)

*Hãy đọc kỹ mô tả của blueprint và làm theo hướng dẫn trong đó nhé.*

---

## 📘 Hướng dẫn / Tutorials

- [**Hướng dẫn cách tạo một bản chỉ dẫn hệ thống cho Voice Assist**](/home_assistant_voice_instructions.md)
- [**Hướng dẫn phát video mới từ kênh YouTube yêu thích**](/home_assistant_play_favorite_youtube_channel_videos.md)
- [**Hướng dẫn theo dõi cập nhật tin tức thời sự mới nhất**](/home_assistant_get_and_summary_daily_news.md)
- [**Hướng dẫn cài đặt nhận thông báo khi có thiết bị mất kết nối**](/home_assistant_unavailable_devices.md)
- [**Hướng dẫn cài đặt iOS Themes**](/home_assistant_ios_themes.md)
- [**Hướng dẫn tra cứu vị trí thiết bị di động**](/home_assistant_device_location_lookup_guide_en.md)

---

**Nếu bạn thấy những blueprint này hữu ích, hãy chia sẻ để cộng đồng Home Assistant cùng trải nghiệm - và nhớ theo dõi để không bỏ lỡ các kịch bản độc đáo sắp ra mắt nhé!**
