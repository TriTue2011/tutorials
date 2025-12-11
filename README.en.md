# Unique Home Assistant Blueprints & Tutorials

**Google has recently significantly cut back on the free Gemini API, making it almost impossible to meet the usage needs of Home Assistant. You can find [a completely free alternative solution here](https://github.com/luuquangvu/ha-addons).**

_All blueprints in this collection are fine-tuned to work best with **Gemini 2.5 Flash**. Other models may require minor adjustments to behave as expected._

Transform Home Assistant into a fully-fledged personal teammate with this curated collection of blueprints and guides. Every scenario has been proven in real homes, backed by clear explanations, example voice prompts, and deployment tips so you can bring each idea to life right away.

**[Vietnamese version click here](/README.md)**

---

## Table of Contents

- [Unique Home Assistant Blueprints \& Tutorials](#unique-home-assistant-blueprints--tutorials)
  - [Table of Contents](#table-of-contents)
  - [Voice Assist - Smart Scheduling \& Timers](#voice-assist---smart-scheduling--timers)
  - [Voice Assist - Memory \& Information Retrieval](#voice-assist---memory--information-retrieval)
  - [Voice Assist - Camera Image Analysis](#voice-assist---camera-image-analysis)
  - [Voice Assist - Calendar \& Event Management](#voice-assist---calendar--event-management)
    - [Create Calendar Events](#create-calendar-events)
    - [Calendar Events Lookup](#calendar-events-lookup)
  - [Voice Assist - Lunar Calendar Lookup \& Conversion](#voice-assist---lunar-calendar-lookup--conversion)
    - [Lunar Calendar Conversion \& Lookup](#lunar-calendar-conversion--lookup)
    - [Create Lunar Calendar Events](#create-lunar-calendar-events)
  - [Interactive Smart Home Chatbot](#interactive-smart-home-chatbot)
  - [Voice Assist - Send Messages \& Images](#voice-assist---send-messages--images)
  - [Voice Assist - Internet Knowledge Search](#voice-assist---internet-knowledge-search)
  - [Voice Assist - YouTube Search \& Playback](#voice-assist---youtube-search--playback)
  - [Voice Assist - Favorite YouTube Channels](#voice-assist---favorite-youtube-channels)
  - [Voice Assist - Smart Fan Control](#voice-assist---smart-fan-control)
  - [Voice Assist - Device Location \& Find](#voice-assist---device-location--find)
  - [Voice Assist - Traffic Fine Lookup](#voice-assist---traffic-fine-lookup)
  - [Automatic Traffic Fine Notifications](#automatic-traffic-fine-notifications)
  - [Device State Synchronization](#device-state-synchronization)
  - [Obsolete Blueprints](#obsolete-blueprints)
    - [Voice Assist - Device Control Timer (Legacy)](#voice-assist---device-control-timer-legacy)
  - [Additional Tutorials](#additional-tutorials)
    - [How to write custom system instructions for Voice Assist](#how-to-write-custom-system-instructions-for-voice-assist)
    - [Play new videos from favorite YouTube channels](#play-new-videos-from-favorite-youtube-channels)
    - [Monitor unavailable devices](#monitor-unavailable-devices)
    - [Auto-switch iOS Themes](#auto-switch-ios-themes)
    - [Device location lookup guide](#device-location-lookup-guide)

---

**Note:** Please make sure to read each blueprint's description and follow its instructions when installing or updating.

---

## Voice Assist - Smart Scheduling & Timers

Want to turn on the AC for 30 minutes and have it turn off automatically? Or dim the bedroom lights after an hour?
This blueprint transforms Voice Assist into a true time management assistant. You can use natural voice commands to **create, extend, pause, resume, or cancel** schedules for any device.

**Key Features:**

- **Natural Language Understanding:** Just say "Turn on the fan for 1 hour", no rigid syntax required.
- **Comprehensive Management:** Full support for creating, extending, pausing, resuming, and canceling schedules.
- **Reliable & Persistent:** All schedules are saved and **automatically restored** if Home Assistant restarts. No more lost timers due to power outages.
- **Versatile Control:** Supports most device types: Lights (brightness, color), Covers (open/close/position), Fans (speed/oscillation), Climate, Vacuums, Media Players, etc.
- **Smart Recognition:** Automatically identifies devices by the friendly aliases you use daily.
- **Detailed Feedback:** Ask "Are there any running schedules?" and the assistant will list devices and remaining times clearly.

**Example Voice Commands:**

- "Turn on the living room lights to 50% warm white for 2 hours."
- "Open the bedroom curtains for 15 minutes to air out the room, then close them."
- "Extend the kids' room fan timer by 30 minutes."
- "Pause the garden watering schedule."
- "Which devices are currently on a timer?"

**Use Cases:**

- **Energy Saving:** Schedule heaters, water heaters, or fans to turn off after you fall asleep.
- **Comfort:** Automatically adjust lighting and curtains based on your routine without reaching for your phone.
- **Peace of Mind:** Never worry about forgetting to turn off important devices thanks to the auto-restore feature.

For full functionality, you need to install **all 3 blueprints**:

1. **Controller Blueprint (LLM):** Processes voice commands and coordinates actions.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevices_schedules_controller_full_llm.yaml)
2. **Core Schedule Blueprint:** Responsible for creating and managing the schedules.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevices_schedules.yaml)
3. **Restore Blueprint:** Automatically restores active schedules when Home Assistant restarts.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevices_schedules_restart_handler.yaml)

---

## Voice Assist - Memory & Information Retrieval

Forget where you parked the car? Keep forgetting the Wi-Fi password for guests? Let Voice Assist become your "Second Brain".

**Key Features:**

- **Remember Everything:** From small details like "Keys are in the desk drawer" to important reminders like "The customer ID for store ABC".
- **Smart Retrieval:** No need to remember exact keywords. Just ask "Where is the car?" or "What's the wifi pass?", and the assistant will find the most relevant info.
- **Flexible Scopes:**
  - **Personal (User):** For your personal details (e.g., clothing sizes, dietary preferences).
  - **Household:** Shared with the whole family (e.g., gate code, trash schedule).
  - **Temporary (Session):** Only remembered for the current conversation.
- **Auto-Cleanup:** Set expiration dates for short-term memories (e.g., parking spot at the mall).

**Example Voice Commands:**

- "Remember the guest Wi-Fi password is `guestshere123`."
- "Save my parking spot as B2 column D5, remember for 1 day only."
- "Remind me the doctor's phone number is 0912345678."
- "Find where the car is parked."
- "What was the guest Wi-Fi password?"

**Use Cases:**

- Securely store rarely used but critical information.
- Share common household info without texting back and forth.
- Quickly note down to-dos or item locations the moment you think of them.

_Choose the version you want to use:_

**LLM Version (Multi-language):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fmemory_tool_full_llm.yaml)

**Local Version (English only, works offline):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fmemory_tool_local.yaml)

---

## Voice Assist - Camera Image Analysis

Turn your security cameras into "smart eyes" for your virtual assistant. No need to open the app and check every angle-just let Voice Assist look for you.

**Key Features:**

- **Visual Intelligence:** Voice Assist can "see" images from your cameras and describe in detail what is happening.
- **Comprehensive View:** Supports connecting multiple cameras at once (gate, yard, living room...) for a complete overview.
- **Instant Response:** Captures and analyzes the image the moment you ask.

**Example Voice Commands:**

- "Check the gate camera, is anyone standing there?"
- "Check if the cat is in the front yard or the back yard?"
- "Look to see if the garage door is closed."
- "Is there any strange car in the yard?"

**Use Cases:**

- **Security:** Quickly check the situation around the house when you hear a strange noise at night.
- **Monitoring:** Keep an eye on children or pets without being glued to your phone screen.
- **Convenience:** Quickly confirm physical states (door open/closed, lights on/off) that sensors might miss.

To use this feature, you need to install **both blueprints**:

1. **Snapshot Blueprint:** Takes a picture from the requested camera.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcamera_snapshot_full_llm.yaml)
2. **Analyzer Blueprint (LLM):** Sends the snapshot to the language model for analysis and response.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffile_content_analyzer_full_llm.yaml)

---

## Voice Assist - Calendar & Event Management

Effortlessly manage your personal schedule using natural voice commands, making organization simpler and more intuitive.

### Create Calendar Events

Organize your schedule by voice as if you're conversing with an assistant. This blueprint automates event creation for all your reminders, meetings, and trips directly into your calendar.

**Key Features:**

- **Intuitive Language Recognition:** Automatically parses dates, times, and durations from your spoken commands.
- **Rapid Event Creation:** Add events to your calendar without manual input.
- **Seamless Integration:** Works perfectly with Google Calendars already configured in Home Assistant.

**Example Voice Commands:**

- "Schedule a haircut for tomorrow at 2 PM."
- "Set up a 3-hour meeting tomorrow at 9 AM."
- "Add an event this Saturday to visit family."

**Use Cases:**

- Quickly create reminders and appointments while driving or when your hands are full.
- Add family or work events to your calendar the moment they come to mind.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcreate_calendar_event_full_llm.yaml)

### Calendar Events Lookup

Inquire about and retrieve information regarding existing events in your calendar, such as birthdays, appointments, or anniversaries.

**Example Voice Commands:**

- "What events are happening this week?"
- "What's on the calendar for this month?"

**Use Cases:**

- Get a quick overview of your day or week without needing to open your calendar app.
- Ensure you don't miss any important events.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fcalendar_events_lookup_full_llm.yaml)

---

## Voice Assist - Lunar Calendar Lookup & Conversion

Bring traditional culture into your smart home. Lookup Lunar dates, check auspicious days, or countdown to Tet right on Home Assistant.

### Lunar Calendar Conversion & Lookup

A powerful Solar-Lunar calendar conversion tool that works completely **Offline** (no internet needed), ensuring instant response speeds.

**Key Features:**

- **Fast & Private:** Processed locally, independent of external APIs.
- **In-Depth Information:** Provides full Can Chi (Year/Month/Day stems and branches), Solar Terms, and Lucky Hours.
- **Good/Bad Day Advice:** Know immediately what to do or avoid according to customs.
- **Event Countdown:** Always know exactly how many days are left until Lunar New Year or major holidays.

**Example Voice Commands:**

- "What is today's lunar date?"
- "Is this Sunday a good or bad day?"
- "How many days left until Tet?"
- "Convert November 20th solar to lunar."

**Use Cases:**

- Plan for important tasks (weddings, groundbreakings, grand openings).
- Keep track of the 1st and 15th of the lunar month for traditional observances.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdate_lookup_and_conversion_full_llm.yaml)

### Create Lunar Calendar Events

Automatically add important events based on the Lunar calendar (memorials, anniversaries, etc.) to your calendar, ensuring you never miss a traditional date.

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

Don't just command; converse with your home. Create Telegram or Zalo Bots to control your home remotely with contextual understanding and smart responses.

**Key Features:**

- **Two-Way Conversation:** The Bot doesn't just receive commands but can ask clarifying questions (e.g., "Which room do you want the AC on in?")
- **Image Recognition:** Send a photo of a broken device or an unknown plant, and the bot will analyze and respond.
- **Anywhere, Anytime Control:** Turn off lights, open gates, or check cameras directly from your familiar chat interface.

**Use Cases:**

- At work and want to check if you turned off the stove? Just message the bot.
- Send a photo of your electricity/water meter for the bot to read the index for you.

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

Driving or hands messy? Use your voice to send messages, share your location, or send camera images to loved ones via Telegram/Zalo.

**Key Features:**

- **Hands-Free Messaging:** Dictate your message, and Assistant will send it immediately.
- **Smart Sharing:** Automatically attach Google Maps links when you mention a location.
- **Image Reporting:** Command to take a photo from a security camera and send it directly to a family chat group.

**Example Voice Commands:**

- "Send a list of good restaurants in Nha Trang to the Telegram family group."
- "Send the Thang Long Citadel location via Zalo to my wife."
- "Take a photo from the gate camera and send it to the chat group."

**Use Cases:**

- Quickly inform family when you're busy and can't use your phone.
- Instantly share an interesting moment or a beautiful place you've just discovered.

_Install the blueprint for the platform you want to send messages to:_

**Send to Telegram:**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_telegram_full_llm.yaml)

**Send to Zalo (Official Bot):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_zalo_bot_full_llm.yaml)

**Send to Zalo (Custom Bot):**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fsend_to_zalo_custom_bot_full_llm.yaml)

---

## Voice Assist - Internet Knowledge Search

Don't let Assistant just toggle lights. Turn it into a living encyclopedia, ready to answer any question with up-to-date data from Google.

**Key Features:**

- **Infinite Knowledge:** Access Google's massive database to answer everything from history and geography to current news.
- **Smart Summarization:** No reading through long lists of links. Assistant synthesizes and provides concise, to-the-point answers.
- **Real-time Updates:** Know today's gold price, last night's football scores, or trending events on social media.

**Example Voice Commands:**

- "What is the entry score for Hanoi University of Science and Technology this year?"
- "Summarize the main events of the last World Cup final."
- "What is the current price of iPhone 16 Pro Max?"
- "Recipe for authentic Northern beef Pho."

**Use Cases:**

- Quickly look up information while cooking, driving, or chatting with friends.
- Answer children's questions about the world around them accurately.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_google_search_full_llm.yaml)

---

## Voice Assist - YouTube Search & Playback

Transform your TV into a smart home cinema. No remote needed, no typing required-just say what you want to watch.

**Key Features:**

- **Understands Your Intent:** Find videos by describing content ("relaxing morning music," "VinFast car review") instead of rigid keywords.
- **Smart Selection:** Automatically choose the most relevant video (high views, good quality) to play.
- **Learn & Entertain:** Find lecture videos for your kids or music videos for your parents in an instant.

**Example Voice Commands:**

- "Play some soft instrumental music for reading."
- "Find a documentary about the Battle of Dien Bien Phu."
- "Show me the latest iPhone 17 Pro Max review."

**Use Cases:**

- Help seniors and children easily watch their favorite content without complicated remote operations.
- Cook while commanding Assistant to play a recipe tutorial video.

To use this feature, you need to install **both blueprints**:

1. **Search Blueprint (LLM):** Analyzes the query and finds the right video.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fadvanced_youtube_search_full_llm.yaml)
2. **Player Blueprint:** Gets the video info and plays it on the media player.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

---

## Voice Assist - Favorite YouTube Channels

Are you a die-hard fan of "MrBeast" or "Linus Tech Tips"? This blueprint ensures you never miss the latest videos from your favorite creators.

**Key Features:**

- **Stay Updated:** Automatically check your subscribed channels for new content.
- **Instant Playback:** A command like "Are there new videos?" will automatically play the latest release on your TV.
- **Proactive Notifications:** Receive messages as soon as your favorite channels upload new content.

**Example Voice Commands:**

- "Does Outdoor Boys have anything new?"
- "Play the latest video from Gordon Ramsay."

**Use Cases:**

- Watch morning news from trusted channels with just a voice command after waking up.
- Enjoy evening entertainment with the latest travel vlogs without endless scrolling.

[**View the detailed guide**](/home_assistant_play_favorite_youtube_channel_videos_en.md)

To use this feature, you need to install **both blueprints**:

1. **Info Getter Blueprint (LLM):** Checks the channel and gets the latest video info.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fget_youtube_video_info_full_llm.yaml)
2. **Player Blueprint:** Gets the video info and plays it on the media player (can be reused from the blueprint above).
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fplay_youtube_video_full_llm.yaml)

---

## Voice Assist - Smart Fan Control

Feeling hot? Just say the word, and your fan will speed up. This blueprint helps you precisely control the airflow to your liking.

**Key Features:**

- **Flexible Adjustment:** Increase/decrease speed by a specific percentage or desired level.
- **Oscillation Control:** Turn oscillation (swing) on/off with your voice.
- **Synchronized Control:** Command a specific fan or all fans in the house simultaneously.

**Example Voice Commands:**

- "Increase the living room fan to maximum."
- "Turn on oscillation for the bedroom fan, it's too hot."
- "Reduce the dining table fan speed to 30%."

**Use Cases:**

- Adjust the airflow to suit the room's temperature without leaving your bed or sofa.
- Quickly turn off all fans when leaving the house.

_Install the blueprint for the function you want to use:_

**Fan Speed Control:**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_speed_control_full_llm.yaml)

**Fan Oscillation Control:**
[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ffan_oscillation_control_full_llm.yaml)

---

## Voice Assist - Device Location & Find

"Where's my phone?" - The classic morning question. Let Assistant help you find it instantly.

**Key Features:**

- **Indoor Positioning:** Tells you which room your phone is in (based on Bluetooth/Wi-Fi signals).
- **Trigger Ringing:** Make your phone ring loudly, even if it's on silent mode.
- **Multi-Device Support:** Find iPhones, Androids, iPads, or any device with the Home Assistant app installed.

**Example Voice Commands:**

- "Where is Dad's phone right now?"
- "Make the iPad ring, I can't find it."

**Use Cases:**

- Save time searching for misplaced items when you're rushing out the door.
- Check if your kids have safely arrived home (device connected to home network).

[**View the detailed guide**](/home_assistant_device_location_lookup_guide_en.md)

To use this feature, you need to install **both blueprints**:

1. **Location Finder Blueprint (LLM):** Processes the request and finds the device's location.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_location_lookup_full_llm.yaml)
2. **Ringing Blueprint (LLM):** Triggers the device to ring.
   [![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Fdevice_ringing_full_llm.yaml)

---

## Voice Assist - Traffic Fine Lookup

Drive with peace of mind. Check traffic violation status for any vehicle by voice, using live data from the national traffic police portal.

**Note:** This feature is only applicable to the traffic fine system in Vietnam.

**Key Features:**

- **Real-time Checks:** Instantly query the official database for traffic violations.
- **Any Vehicle:** Check fines for your car, motorbike, or even a vehicle you're considering buying.
- **Proactive Awareness:** Stay informed and avoid accumulating late fees.

**Example Voice Commands:**

- "Check traffic fines for car 30G-123.45."
- "Does motorbike 29-T1 567.89 have any fines?"

**Use Cases:**

- Periodically check your family's vehicles for fines.
- Verify a used car's history for outstanding fines before purchase.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_lookup_full_llm.yaml)

---

## Automatic Traffic Fine Notifications

Never miss an important alert. Receive instant notifications the moment a new traffic violation is recorded for your vehicle in the national police system.

**Note:** This feature is only applicable to the traffic fine system in Vietnam.

**Key Features:**

- **Continuous Monitoring:** Periodically scans the system to detect new violations automatically.
- **Instant Alerts:** Get a notification directly to Home Assistant as soon as a fine is detected.
- **Multi-Vehicle Support:** Easily configure to monitor multiple license plates for your entire family.

**Use Cases:**

- Act quickly on violations to handle them in time and avoid escalating penalties.
- Automate the management of traffic fine status for all your household vehicles.

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fluuquangvu%2Ftutorials%2Fblob%2Fmain%2Ftraffic_fine_notification.yaml)

---

## Device State Synchronization

Seamlessly synchronize the `on/off` state between multiple devices, acting like a virtual two-way staircase switch for enhanced control.

**Use Cases:**

- Control a smart bulb wirelessly from a physical switch that's not directly wired to it.
- Turning on one light can automatically activate other lights in the same area for coordinated ambiance.

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

### [How to write custom system instructions for Voice Assist](/home_assistant_voice_instructions_en.md)

### [Play new videos from favorite YouTube channels](/home_assistant_play_favorite_youtube_channel_videos_en.md)

### [Monitor unavailable devices](/home_assistant_unavailable_devices_en.md)

### [Auto-switch iOS Themes](/home_assistant_ios_themes_en.md)

### [Device location lookup guide](/home_assistant_device_location_lookup_guide_en.md)

---

**If you find these blueprints helpful, please share them with the Home Assistant community! Be sure to follow along for more unique blueprints coming soon!**
