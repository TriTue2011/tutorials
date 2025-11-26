# Unique Home Assistant Blueprints & Tutorials

_All blueprints in this collection are fine-tuned to work best with **Gemini 2.5 Flash**. Other models may require minor adjustments to behave as expected._

Transform Home Assistant into a fully-fledged personal teammate with this curated collection of blueprints and guides. Every scenario has been proven in real homes, backed by clear explanations, example voice prompts, and deployment tips so you can bring each idea to life right away.

**[Vietnamese version click here](/README.md)**

---

## Table of Contents

- [Voice Assist - Smart Scheduling & Timers](#voice-assist---smart-scheduling--timers)
- [Voice Assist - Memory & Information Retrieval](#voice-assist---memory--information-retrieval)
- [Voice Assist - Camera Image Analysis](#voice-assist---camera-image-analysis)
- [Voice Assist - Calendar & Event Management](#voice-assist---calendar--event-management)
- [Voice Assist - Lunar Calendar Lookup & Conversion](#voice-assist---lunar-calendar-lookup--conversion)
- [Interactive Smart Home Chatbot](#interactive-smart-home-chatbot)
- [Voice Assist - Send Messages & Images](#voice-assist---send-messages--images)
- [Voice Assist - Internet Knowledge Search](#voice-assist---internet-knowledge-search)
- [Voice Assist - YouTube Search & Playback](#voice-assist---youtube-search--playback)
- [Voice Assist - Favorite YouTube Channels](#voice-assist---favorite-youtube-channels)
- [Voice Assist - Smart Fan Control](#voice-assist---smart-fan-control)
- [Voice Assist - Device Location & Find](#voice-assist---device-location--find)
- [Voice Assist - Traffic Fine Lookup](#voice-assist---traffic-fine-lookup)
- [Automatic Traffic Fine Notifications](#automatic-traffic-fine-notifications)
- [Device State Synchronization](#device-state-synchronization)
- [Obsolete Blueprints](#obsolete-blueprints)
- [Additional Tutorials](#additional-tutorials)
  - [Custom System Instructions for Voice Assist](/home_assistant_voice_instructions.md)
  - [Play YouTube Videos from favorite channels](/home_assistant_play_favorite_youtube_channel_videos.md)
  - [Daily News Summary](/home_assistant_get_and_summary_daily_news.md)
  - [Monitor Offline/Unavailable Devices](/home_assistant_unavailable_devices.md)
  - [Auto-switch iOS Themes (Light/Dark)](/home_assistant_ios_themes.md)
  - [Find Phones & Devices Setup Guide](/home_assistant_device_location_lookup_guide_en.md)

---

**Note:** Please make sure to read each blueprint's description and follow its instructions when installing or updating.

---

## Voice Assist - Smart Scheduling & Timers

Automatically create, extend, pause, resume, or cancel **device schedules** through natural voice commands. Each schedule controls one or multiple smart devices and **automatically restores itself after Home Assistant restarts**.

**Key Features:**

- **Flexible Management:** Supports all necessary modes: `start`, `extend`, `pause`, `resume`, `cancel`, `list`.
- **Multitasking:** Manage multiple devices and independent schedules simultaneously.
- **Persistent:** Automatically restores all active schedules after a Home Assistant restart.
- **Smart:** Integrated with Voice Assist (LLMs) to naturally understand multi-language commands.

**Example Voice Commands:**

- "Set a schedule to turn off the living room fan in 15 minutes."
- "Extend the kitchen light schedule by 10 minutes."
- "Add a schedule to turn off the bedroom AC at 6 a.m."
- "What schedules are currently active?"

**Use Cases:**

- Schedule lights, fans, air conditioners, or heaters to save energy.
- Set a schedule for tasks that need to run for a specific duration, like charging an electric scooter for 2 hours.
- Easily change or cancel schedules by voice without opening the app.

For full functionality, you need to install **all 3 blueprints**:

1. **Controller Blueprint (LLM):** Processes voice commands and coordinates actions.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevices_schedules_controller_full_llm.yaml)
2. **Core Schedule Blueprint:** Responsible for creating and managing the schedules.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevices_schedules.yaml)
3. **Restore Blueprint:** Automatically restores active schedules when Home Assistant restarts.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevices_schedules_restart_handler.yaml)

---

## Voice Assist - Memory & Information Retrieval

Turn Voice Assist into your personal memory vault to store, retrieve, and manage personal or household information.

**Key Features:**

- **Versatile Storage:** Remembers everything from passwords and addresses to quick notes.
- **Flexible Retrieval:** Fetches information by an exact "key" (`get`) or searches by keyword/context (`search`).
- **Storage Scopes:** Choose to save information for just yourself (`user`), the whole `household`, or only the current `session`.
- **Auto-Expiration:** Optionally set memories to be automatically deleted after a specified number of days.

**Example Voice Commands:**

- "Remember the guest Wi-Fi password is `guestshere123`."
- "Remember I parked at B2, column D5, and forget it after one day."
- "Remind me that ABC Company's address is 123 Main Street, Anytown."
- "Search for the memory about my parking spot."
- "What is the guest Wi-Fi password?"

**Use Cases:**

- **Secure & Personal:** Store rarely used but important personal info (passport numbers, membership IDs, warranty details) with `user` scope.
- **Household Convenience:** Save shared information for the family (guest Wi-Fi password, gate code) with `household` scope.
- **Temporary Notes:** Save temporary, expiring information (parking spots, temporary addresses, a recommended book title).

_Choose the version you want to use:_

**LLM Version (Multi-language):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fmemory_tool_full_llm.yaml)

**Local Version (English only, works offline):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fmemory_tool_local.yaml)

---

## Voice Assist - Camera Image Analysis

Give Voice Assist eyes on your surroundings by allowing it to access your cameras and answer questions about what's happening.

**Key Features:**

- **Image Analysis:** Extracts content from camera snapshots to answer your questions.
- **Multi-Camera Support:** Configure multiple cameras to give Voice Assist a wider field of view.
- **Instant Responses:** Get answers almost immediately after asking.

**Example Voice Commands:**

- "Check the cameras to see where the cat is."
- "Look at the gate camera to see if anyone's there."
- "Is there a strange car in the yard?"

**Use Cases:**

- Quickly check your yard, a child's room, or your front door without opening the camera app.
- Find a pet or confirm unusual activity when you're not near a screen.

To use this feature, you need to install **both blueprints**:

1. **Snapshot Blueprint:** Takes a picture from the requested camera.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcamera_snapshot_full_llm.yaml)
2. **Analyzer Blueprint (LLM):** Sends the snapshot to the language model for analysis and response.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

---

## Voice Assist - Calendar & Event Management

Manage your personal schedule effectively using natural voice commands.

### Create Calendar Events

Plan your schedule by voice as if you were talking to an assistant. This blueprint automates creating events for reminders, meetings, and trips in your calendar.

**Key Features:**

- **Natural Language Processing:** Automatically parses dates, times, and durations from your commands.
- **Quick Event Creation:** Add events to your calendar without manual typing.
- **Seamless Integration:** Works perfectly with Google Calendars configured in Home Assistant.

**Example Voice Commands:**

- "Schedule a haircut tomorrow at 2 PM."
- "Schedule a 3-hour meeting tomorrow at 9 AM."
- "Add an event this Saturday to visit family."

**Use Cases:**

- Quickly create reminders and appointments while driving or busy.
- Add family or work events to your calendar the moment you think of them.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcreate_calendar_event_full_llm.yaml)

### Calendar Events Lookup

Ask about and get information on existing events in your calendar, such as birthdays, appointments, or anniversaries.

**Example Voice Commands:**

- "What events are happening this week?"
- "What's on the calendar for this month?"

**Use Cases:**

- Get a quick overview of your day or week without opening the calendar app.
- Ensure you don't miss any important events.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcalendar_events_lookup_full_llm.yaml)

---

## Voice Assist - Lunar Calendar Lookup & Conversion

Tools to help you accurately track and manage events based on the Lunar calendar.

### Lunar Calendar Conversion & Lookup

Instantly convert between Solar and Lunar calendars, 100% offline. Provides full traditional details like Can Chi, solar terms, auspicious/inauspicious days, and lucky hours.

**Key Features:**

- **Offline Functionality:** Extremely fast and requires no internet connection.
- **Detailed Information:** Provides comprehensive traditional lunar calendar data.
- **Event Countdown:** Shows the number of days remaining until major holidays like Lunar New Year.

**Example Voice Commands:**

- "What's the lunar date this Sunday?"
- "How many days until Tet?"
- "Is tomorrow a good or bad day?"

**Use Cases:**

- Check the lunar date for festivals, memorials, and cultural ceremonies.
- Look up auspicious/inauspicious days for important life events.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdate_lookup_and_conversion_full_llm.yaml)

### Create Lunar Calendar Events

Automatically add important events based on the Lunar calendar (memorials, anniversaries, etc.) to your calendar.

**Note:** This blueprint is designed for **manual execution** or via automation, requiring users to fill in information directly through the Home Assistant UI. It **does not support voice commands** via Voice Assist.

**Key Features:**

- **Automatic Conversion:** Calculates and creates events on the corresponding solar date each year.
- **Accurate & Convenient:** No more manual conversions or forgetting important traditional dates.

**Use Cases:**

- Ensure you never miss important family memorials or ceremonies.
- Automatically get reminders for anniversaries or birthdays that are celebrated based on the lunar calendar.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcreate_lunar_events.yaml)

---

## Interactive Smart Home Chatbot

Build a bot to chat with and control Home Assistant via Telegram or Zalo. The bot can ask clarifying questions and send/receive images.

**Key Features:**

- **Conversational AI:** The bot can ask clarifying questions before taking action.
- **Rich Media Support:** Send camera snapshots for analysis or receive files from the bot.
- **Smart Home Control:** Issue commands directly in the chat interface to control devices.

**Use Cases:**

- Control your home remotely via a chat app without opening the Home Assistant app.
- Send a photo of a plant in your garden and ask, "What plant is this and how do I care for it?".

_Install the webhook blueprint for your chosen platform. For image analysis, also install the Analyzer blueprint._

**Webhook for Telegram:**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftelegram_bot_webhook.yaml)

**Webhook for Zalo (Official Account):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fzalo_bot_webhook.yaml)

**Webhook for Zalo (Custom Bot):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fzalo_custom_bot_webhook.yaml)

**(Optional) Image Analyzer Blueprint:**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

---

## Voice Assist - Send Messages & Images

Use your voice to send text messages, photos, locations, or search results to friends and group chats via Telegram or Zalo.

**Key Features:**

- **Multi-Content Support:** Send text messages, photos from your cameras, or media files.
- **Maps & Search Integration:** Automatically attach Google Maps links for locations and Google Search links for other content.
- **Group or Private:** Supports sending messages to both private chats and groups.

**Example Voice Commands:**

- "Send a list of good restaurants in Nha Trang to the Telegram family group."
- "Send the address of the Thang Long Citadel to my wife Zalo."
- "Send the photo from the gate camera to the Telegram group."

**Use Cases:**

- Quickly share a location, image, or interesting piece of information with someone while on the go.
- Forward voice search results to others for their reference.

_Install the blueprint for the platform you want to send messages to:_

**Send to Telegram:**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_telegram_full_llm.yaml)

**Send to Zalo (Official Bot):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_zalo_bot_full_llm.yaml)

**Send to Zalo (Custom Bot):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_zalo_custom_bot_full_llm.yaml)

---

## Voice Assist - Internet Knowledge Search

Run sophisticated Google searches by voice and hear concise, summarized, and up-to-date answers.

**Key Features:**

- **Smart Summarization:** Returns a brief, direct answer instead of a long list of search results.
- **Understands Open-Ended Questions:** Handles complex questions that require information synthesis.
- **Always Current:** Fetches the latest data directly from Google's search results.

**Example Voice Commands:**

- "What's the entry score for Hanoi University of Science and Technology this year?"
- "Which AI technologies are trending this week?"

**Use Cases:**

- Quickly look up facts, events, or knowledge without sifting through websites.
- Settle everyday questions and debates instantly ("who was the main actor in movie X?").

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_google_search_full_llm.yaml)

---

## Voice Assist - YouTube Search & Playback

Search YouTube and play videos on any media device using conversation alone.

**Key Features:**

- **Semantic Search:** Finds videos based on topics, people, or events, not just keywords.
- **Automatic Playback:** Automatically selects the most relevant video and plays it on your designated device.
- **Knowledge Questions:** Answers questions by finding and playing a relevant video.

**Example Voice Commands:**

- "Find a video about the life and career of Le Duc Tho."
- "Who was the most outstanding female scientist of the 20th century? Find a video about her."

**Use Cases:**

- Find and play a tutorial for cooking or repairs while your hands are busy.
- Quickly play entertainment or music videos for the whole family.

To use this feature, you need to install **both blueprints**:

1. **Search Blueprint (LLM):** Analyzes the query and finds the right video.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_youtube_search_full_llm.yaml)
2. **Player Blueprint:** Gets the video info and plays it on the media player.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

---

## Voice Assist - Favorite YouTube Channels

Automatically surface the newest videos from your must-watch channels and play them on your chosen devices.

**Key Features:**

- **New Video Checks:** Automatically checks your pre-configured favorite YouTube channels for new content.
- **Play Latest Video:** Easily play the most recently uploaded video with a simple command.
- **Optional Notifications:** Can be configured to notify you the moment a new video drops.

**Example Voice Commands:**

- "Does Hoa Ban Food have a new video?"
- "Play the latest video from Sang vlog on the TV."

**Use Cases:**

- Create a "morning brief" automation that plays the latest news from your trusted channels.
- Ensure you never miss content from your favorite creators.

[**View the detailed guide**](/home_assistant_play_favorite_youtube_channel_videos.md)

To use this feature, you need to install **both blueprints**:

1. **Info Getter Blueprint (LLM):** Checks the channel and gets the latest video info.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fget_youtube_video_info_full_llm.yaml)
2. **Player Blueprint:** Gets the video info and plays it on the media player (can be reused from the blueprint above).
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

---

## Voice Assist - Smart Fan Control

Adjust the speed and oscillation of one or many fans across your home with simple voice prompts.

**Key Features:**

- **Speed Control:** Increase, decrease, or set a specific fan speed percentage.
- **Oscillation Control:** Toggle the fan's oscillation mode on or off.
- **Multi-Fan Support:** Command multiple fans at once.

**Example Voice Commands:**

- "Increase the kitchen fan speed."
- "Set the bedroom fan speed to 50%."
- "Start oscillation for the living room fan."

**Use Cases:**

- Adjust fan comfort level without getting up.
- Quickly change the airflow in a room to suit your needs.

_Install the blueprint for the function you want to use:_

**Fan Speed Control:**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_speed_control_full_llm.yaml)

**Fan Oscillation Control:**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_oscillation_control_full_llm.yaml)

---

## Voice Assist - Device Location & Find

Track down mobile devices or BLE tags in your home by voice and make them ring to locate them easily.

**Key Features:**

- **Location Reporting:** Reports the approximate location (by room) of the device in your home.
- **Trigger Ringing:** Makes the device ring so you can find it by sound.
- **Multi-Device Support:** Search for multiple phones or tablets at once.

**Example Voice Commands:**

- "Where are the phones right now?"
- "Find the iPad and make it ring."

**Use Cases:**

- Quickly find a misplaced phone or tablet inside the house.
- Check if your kids have left their devices at home.

[**View the detailed guide**](/home_assistant_device_location_lookup_guide_en.md)

To use this feature, you need to install **both blueprints**:

1. **Location Finder Blueprint (LLM):** Processes the request and finds the device's location.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_location_lookup_full_llm.yaml)
2. **Ringing Blueprint (LLM):** Triggers the device to ring.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_ringing_full_llm.yaml)

---

## Voice Assist - Traffic Fine Lookup

Check for traffic fines for any vehicle by voice, using live data from the national traffic police portal.

**Note:** This feature is only applicable to the traffic fine system in Vietnam.

**Example Voice Commands:**

- "Check traffic fines for the car 30G-123.45."
- "Does the motorbike 29-T1 567.89 have any fines?"

**Use Cases:**

- Periodically check your family's vehicles for fines.
- Check a used car for outstanding fines before purchasing.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_lookup_full_llm.yaml)

---

## Automatic Traffic Fine Notifications

Get an alert as soon as a new traffic violation is recorded for your vehicle in the national police system.

**Note:** This feature is only applicable to the traffic fine system in Vietnam.

**Key Features:**

- **Automatic Checks:** Periodically scans the system for new violations.
- **Instant Notifications:** Sends a notification to Home Assistant as soon as a fine is detected.
- **Multi-Vehicle Support:** Easily configure to monitor multiple license plates.

**Use Cases:**

- Stay informed about violations early to handle them in time and avoid late fees.
- Automatically manage the fine status for all family vehicles.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_notification.yaml)

---

## Device State Synchronization

Synchronize the `on/off` state between multiple devices, acting like a virtual two-way staircase switch.

**Use Cases:**

- A physical switch can control a smart bulb that it's not directly wired to.
- Turning on one light can trigger other lights in the same area to turn on as well.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Flink_multiple_devices.yaml)

---

## Obsolete Blueprints

### Voice Assist - Device Control Timer (Legacy)

**Use the new [Voice Assist - Smart Scheduling & Timers](#voice-assist---smart-scheduling--timers) for more features.**

To use this, you need to install **both blueprints**:

1. **Controller Blueprint (LLM):**
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_control_timer_full_llm.yaml)
2. **Timer Tool Blueprint:**
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_control_tool.yaml)

---

## Additional Tutorials

- [**How to write custom system instructions for Voice Assist**](/home_assistant_voice_instructions.md)
- [**Play new videos from favorite YouTube channels**](/home_assistant_play_favorite_youtube_channel_videos.md)
- [**Get and summarize daily news with AI**](/home_assistant_get_and_summary_daily_news.md)
- [**Monitor unavailable devices**](/home_assistant_unavailable_devices.md)
- [**Auto-switch iOS Themes**](/home_assistant_ios_themes.md)
- [**Device location lookup guide**](/home_assistant_device_location_lookup_guide_en.md)

---

**If you find these blueprints helpful, please share them with the Home Assistant community! Be sure to follow along for more unique blueprints coming soon!**
