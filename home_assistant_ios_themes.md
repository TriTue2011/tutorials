# Hướng dẫn cài đặt iOS Themes cho Home Assistant

Hướng dẫn này giúp bạn cài đặt bộ giao diện iOS đẹp mắt, tự động chuyển đổi Sáng/Tối theo thời gian và lưu trữ hình nền cục bộ để tải nhanh hơn.

## 1. Cài đặt các thành phần cần thiết

- **HACS:** Đảm bảo bạn đã cài đặt [HACS](https://github.com/hacs).
- **Cấu hình Themes:** Đảm bảo file `configuration.yaml` của bạn đã có dòng cấu hình để load themes (nếu chưa có, hãy thêm vào):
  ```yaml
  frontend:
    themes: !include_dir_merge_named themes
  ```

### Cài đặt qua HACS:

1.  Truy cập **HACS** > **Frontend**.
2.  Tìm kiếm và cài đặt **iOS Themes** ([basnijholt/lovelace-ios-themes](https://github.com/basnijholt/lovelace-ios-themes)).
3.  Truy cập **HACS** > **Integrations**.
4.  Tìm kiếm và cài đặt **Spook** ([frenck/spook](https://github.com/frenck/spook)).
    - _Lưu ý:_ Spook cung cấp tính năng `input_select.random` cần thiết cho hướng dẫn này.

## 2. Cấu hình hình nền cục bộ (Local Backgrounds)

Việc này giúp hình nền tải nhanh hơn từ mạng nội bộ thay vì phải tải từ internet mỗi lần mở app.

1.  Sử dụng File Editor hoặc VS Code để truy cập thư mục cấu hình Home Assistant.
2.  Tìm đến thư mục `themes/ios-themes` (nơi HACS đã tải về).
3.  Sao chép toàn bộ các file ảnh `.jpg` trong đó.
4.  Dán chúng vào thư mục `www/ios-themes`.
    - _Nếu chưa có thư mục `www`, hãy tạo mới nó ngang hàng với file `configuration.yaml`._
    - _Nếu chưa có thư mục `ios-themes` trong `www`, hãy tạo mới nó._
5.  **Khởi động lại** Home Assistant để áp dụng các thay đổi.

## 3. Tạo tính năng tự động đổi Theme (Auto Light/Dark)

### 3.1. Tạo các biến trợ giúp (Helpers)

Bạn có thể thêm code vào `configuration.yaml` hoặc tạo bằng giao diện (Settings > Devices & Services > Helpers).

**Code YAML (thêm vào configuration.yaml):**

```yaml
input_select:
  ios_themes:
    name: iOS Themes
    icon: mdi:palette
    options:
      - dark-green
      - light-green
      - dark-blue
      - light-blue
      - blue-red
      - orange
      - red

input_boolean:
  ios_themes_dark_mode:
    name: iOS Themes Dark Mode
    icon: mdi:theme-light-dark
  ios_themes_local_backgrounds:
    name: iOS Themes Local Backgrounds
    icon: mdi:cloud
    initial: on
```

### 3.2. Tạo Automation

Automation này sẽ tự động chuyển sang chế độ Sáng khi mặt trời mọc và Tối khi mặt trời lặn, đồng thời áp dụng hình nền ngẫu nhiên mỗi ngày.

```yaml
alias: "System: Auto change iOS themes"
description: "Tự động đổi theme Sáng/Tối và chọn màu ngẫu nhiên"
ttriggers:
  - trigger: sun
    event: sunrise
    id: sun_event
  - trigger: sun
    event: sunset
    id: sun_event
  - trigger: state
    entity_id:
      - input_select.ios_themes
      - input_boolean.ios_themes_dark_mode
      - input_boolean.ios_themes_local_backgrounds
    id: apply_theme
conditions: []
actions:
  - choose:
      - conditions:
          - condition: trigger
            id: sun_event
          - condition: state
            entity_id: input_select.choose_default_theme
            state: iOS Themes
        sequence:
          - action: >-
              input_boolean.turn_{{ 'on' if trigger.event == 'sunset' else 'off' }}
            target:
              entity_id: input_boolean.ios_themes_dark_mode
          - action: input_select.random
            target:
              entity_id: input_select.ios_themes
      - conditions:
          - condition: trigger
            id: apply_theme
        sequence:
          - action: frontend.set_theme
            data:
              name: >-
                {% set is_dark = is_state('input_boolean.ios_themes_dark_mode', 'on') %}
                {% set mode = 'dark' if is_dark else 'light' %}
                {% set color = states('input_select.ios_themes') %}
                {% set suffix = '-alternative' if is_state('input_boolean.ios_themes_local_backgrounds', 'on') else '' %}
                ios-{{ mode }}-mode-{{ color }}{{ suffix }}
          - action: input_select.select_option
            target:
              entity_id: input_select.choose_default_theme
            data:
              option: iOS Themes
mode: queued
max: 10
```

## 4. Kích hoạt Theme trên thiết bị

**Bước quan trọng nhất:** Để automation có thể thay đổi giao diện của bạn, bạn phải chọn chế độ **Use default theme** trong cài đặt người dùng.

1.  Nhấn vào biểu tượng **Hồ sơ người dùng (User Profile)** ở góc dưới cùng bên trái thanh menu.
2.  Tại mục **Theme**, chọn **Use default theme**.
