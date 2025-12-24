# Guide to Install iOS Themes for Home Assistant

This guide helps you install a beautiful set of iOS themes, automatically switch between Light/Dark modes according to time, and store local backgrounds for faster loading.

## 1. Install Necessary Components

- **HACS:** Ensure you have [HACS](https://github.com/hacs) installed.
- **Themes Configuration:** Ensure your `configuration.yaml` file includes the configuration line to load themes (if not, add it):
  ```yaml
  frontend:
    themes: !include_dir_merge_named themes
  ```

### Install via HACS:

1.  Go to **HACS** > **Frontend**.
2.  Search for and install **iOS Themes** ([basnijholt/lovelace-ios-themes](https://github.com/basnijholt/lovelace-ios-themes)).
3.  Go to **HACS** > **Integrations**.
4.  Search for and install **Spook** ([frenck/spook](https://github.com/frenck/spook)).
    - _Note:_ Spook provides the `input_select.random` feature required for this guide.

## 2. Configure Local Backgrounds

This helps backgrounds load faster from your local network instead of downloading from the internet every time you open the app.

1.  Use File Editor or VS Code to access your Home Assistant configuration directory.
2.  Navigate to the `themes/ios-themes` folder (where HACS downloaded the themes).
3.  Copy all `.jpg` image files from there.
4.  Paste them into the `www/ios-themes` folder.
    - _If the `www` folder does not exist, create it at the same level as your `configuration.yaml` file._
    - _If the `ios-themes` folder does not exist within `www`, create it._
5.  **Restart** Home Assistant to apply the changes.

## 3. Create Automatic Theme Switching (Auto Light/Dark)

### 3.1. Create Helper Entities

You can add the code to `configuration.yaml` or create them via the UI (Settings > Devices & Services > Helpers).

**YAML Code (add to configuration.yaml):**

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

### 3.2. Create Automation

This automation will automatically switch to Light mode at sunrise and Dark mode at sunset, and apply a random background daily.

```yaml
alias: "System: Auto change iOS themes"
description: "Automatically switch between Light/Dark themes and select random color"
triggers:
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

## 4. Activate Theme on Your Device

**Most Important Step:** For the automation to change your interface, you must select **Use default theme** mode in your user settings.

1.  Click on the **User Profile** icon in the bottom-left corner of the sidebar.
2.  Under **Theme**, select **Use default theme**.
