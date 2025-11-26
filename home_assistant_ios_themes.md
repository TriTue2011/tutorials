# Hướng dẫn cài đặt iOS Themes cho Home Assistant

## Cài đặt

- Truy cập **HACS** (Cài đặt [HACS](https://github.com/hacs) nếu chưa có)

- Tìm kiếm theo từ khóa `iOS Themes`

- Cài đặt **iOS Themes** (Xem chi tiết tại: [github.com/basnijholt/lovelace-ios-themes](https://github.com/basnijholt/lovelace-ios-themes))

- Cài đặt **Spook** - một tích hợp có rất nhiều tính năng hay và hữu ích (Xem chi tiết tại: [github.com/frenck/spook](https://github.com/frenck/spook)). Spook cung cấp các service cần thiết như `input_select.random` được sử dụng trong hướng dẫn này.

## Lưu ảnh nền cục bộ

- Sao chép toàn bộ tập tin `.jpg` nằm trong thư mục `themes/ios-themes` sang thư mục `www/ios-themes`. Nếu thư mục `www/ios-themes` chưa có, hãy tạo mới nó. Việc này giúp hình nền tải nhanh hơn từ mạng nội bộ thay vì tải từ internet.

## Tạo tự động đổi light/dark themes

1. Khởi tạo các biến trợ giúp

- Thêm mã sau vào `config/configuration.yaml` hoặc tạo qua giao diện UI (Helpers) để tạo một `input_select`:

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
```

- Thêm mã sau vào `config/configuration.yaml` hoặc tạo qua giao diện UI (Helpers) để tạo hai `input_boolean`:

```yaml
input_boolean:
  ios_themes_dark_mode:
    name: iOS Themes Dark Mode
    icon: mdi:theme-light-dark
  ios_themes_local_backgrounds:
    name: iOS Themes Local Backgrounds
    icon: mdi:cloud
    initial: on
```

- Tạo Automation tự động thay đổi theme vào các buổi sáng và buổi tối:

```yaml
alias: Auto change iOS themes
description: ""
triggers:
  - trigger: sun
    event: sunrise
    offset: 0
    id: Sunrise
  - trigger: sun
    event: sunset
    offset: 0
    id: Sunset
  - trigger: state
    entity_id:
      - input_select.ios_themes
      - input_boolean.ios_themes_dark_mode
      - input_boolean.ios_themes_local_backgrounds
    id: iOS Themes
conditions: []
actions:
  - choose:
      - conditions:
          - condition: trigger
            id:
              - Sunrise
        sequence:
          - action: input_boolean.turn_off
            target:
              entity_id: input_boolean.ios_themes_dark_mode
          - action: input_select.random
            target:
              entity_id: input_select.ios_themes
      - conditions:
          - condition: trigger
            id:
              - Sunset
        sequence:
          - action: input_boolean.turn_on
            target:
              entity_id: input_boolean.ios_themes_dark_mode
          - action: input_select.random
            target:
              entity_id: input_select.ios_themes
      - conditions:
          - condition: trigger
            id:
              - iOS Themes
        sequence:
          - action: frontend.set_theme
            data:
              name: >-
                {% set which = 'dark' if
                is_state('input_boolean.ios_themes_dark_mode', 'on') else
                'light' -%} {% set name = states('input_select.ios_themes') -%}
                {% set suffix = '-alternative' if
                is_state('input_boolean.ios_themes_local_backgrounds', 'on')
                else '' -%} ios-{{ which }}-mode-{{ name }}{{ suffix }}
mode: queued
max: 10
```

## Đặt thẻ iOS Themes ra ngoài giao diện (tùy chọn)

- Yêu cầu có cài đặt Mushroom ([github.com/piitaya/lovelace-mushroom](https://github.com/piitaya/lovelace-mushroom))

- Thêm thẻ vào giao diện (Lovelace Dashboard):

```yaml
square: false
type: grid
cards:
  - type: custom:mushroom-select-card
    entity: input_select.ios_themes
    secondary_info: none
    tap_action:
      action: perform-action
      perform_action: input_select.random
      target:
        entity_id: input_select.ios_themes
    icon_color: primary
  - type: tile
    entity: input_boolean.ios_themes_dark_mode
    hide_state: true
    color: primary
    vertical: true
columns: 2
```

- Mỗi khi nhấn vào thẻ `input_select`, hệ thống sẽ tự động chọn ngẫu nhiên một chủ đề mới.
