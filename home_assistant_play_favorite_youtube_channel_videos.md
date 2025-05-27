# Hướng dẫn chi tiết cài đặt Voice Assist phát video Youtube lên Smart TV

> **Tính năng này cho phép bạn sử dụng HA Voice Assist mở một video mới ra mắt gần đây của một kênh YouTube bất kỳ mà bạn yêu thích.**

> **Chỉ hỗ trợ các LLM của Google hay OpenAI.**

> *Với Google cần sử dụng Gemini 2.0 Flash hoặc Gemini 2.5 Flash trở lên.*

> **Tính năng này không hỗ trợ tìm những video cũ từ một kênh.**

> **Tính năng này không hỗ trợ tìm một video bất kỳ trong YouTube.**

> **Yêu cầu cần có một Smart TV đã tích hợp lên Home Assistant**

## Bước 1: Lấy thông tin danh sách video từ các kênh Youtube yêu thích

### Cài đặt tích hợp Feedparser

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&repository=feedparser&owner=custom-components)

> Sau khi cài đặt xong cần khởi động lại Home Assistant.

### Lấy ID kênh Youtube

> Mở Google tìm kiếm theo từ khóa: Get YouTube Channel ID, chọn một trang bất kỳ.

> Nhập đường dẫn kênh YouTube mà bạn yêu thích để lấy ID của kênh.

![image](images/20250527_FdZbGj.png)

> Sau khi có ID của kênh YouTube, thêm sensor như sau vào tập tin cấu hình configuration.yaml của Home Assistant.

```
sensor:
  - platform: feedparser
    name: FAVORITE_CHANNEL_NAME YouTube Channel
    feed_url: https://www.youtube.com/feeds/videos.xml?channel_id=XXXXXX
    scan_interval:
      minutes: 30
    inclusions:
      - title
      - link
      - author
      - published
      - media_thumbnail
      - yt_videoid
    date_format: "%Y-%m-%dT%H:%M:%S%z"
```

>> Trong đó FAVORITE_CHANNEL_NAME để thành tên kênh YouTube bạn đang muốn thêm.

>> XXXXXX là ID của kênh.

>> Lưu ý cụm từ **YouTube Channel** trong tên sẽ là cố định gán cho mọi kênh muốn thêm.

> Ví dụ bên dưới một kênh mình rất thích xem, kênh Hoa Ban Food.

```
sensor:
  - platform: feedparser
    name: Hoa Ban Food YouTube Channel
    feed_url: https://www.youtube.com/feeds/videos.xml?channel_id=UCBhgBmuPFbLLxnejr09lnAQ
    scan_interval:
      minutes: 30
    inclusions:
      - title
      - link
      - author
      - published
      - media_thumbnail
      - yt_videoid
    date_format: "%Y-%m-%dT%H:%M:%S%z"
```

> Lặp lại các bước trên với những kênh YouTube khác bạn muốn thêm nữa.

> Sau khi thêm xong khởi động lại Home Assistant.

> Sau khi khởi động lại, chia sẻ sensor các kênh YouTube mới tạo đó với Assist.

![image](images/20250527_tiJyrT.png)

## Bước 2: Thêm kịch bản cho Assist

### Cài đặt Blueprint sau

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fget_youtube_video_info_full_llm.yaml)

> Sau khi thêm blueprint, tạo một kịch bản mới từ blueprint này. **Giữ tên kịch bản mặc định không thay đổi.**

> Sau khi tạo xong, chia sẻ kịch bản đó với Assist.

![image](images/20250527_jR4Saw.png)

### Cài đặt Blueprint tiếp theo

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

> Sau khi thêm blueprint, tạo một kịch bản mới từ blueprint này. Chỉ định một Smart TV sẽ phát video lên khi gọi Assist. **Giữ tên kịch bản mặc định không thay đổi.**

![image](images/20250527_JC5AOg.png)

> Sau khi tạo xong, chia sẻ kịch bản đó với Assist.

![image](images/20250527_oMWjtW.png)

> **Vậy là xong. Bây giờ bạn có thể thử với một số mẫu câu lệnh như sau, hoặc tùy trí tưởng tượng của bạn:**

>> Hôm nay có video YouTube nào mới không?
>> -> Assist trả lời -> Mở video XXX nhé (XXX chỉ cần là 1 phần nhỏ trong tiêu đề của video).

>> Gần đây [Tên Kênh] có video nào mới không? Hãy phát nó lên TV ngay bây giờ.

>> Tuần này [Tên Kênh] và [Tên Kênh] có video mới không? -> Assist trả lời -> Mở video XXX nhé.

> **Nếu bạn thích tính năng này, hãy theo dõi để đón chờ thêm những tính năng mới hay ho hơn nữa nhé.**
