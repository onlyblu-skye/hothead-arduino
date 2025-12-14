# Hot Head — My Physical Computing Project
Hot Head is an interactive party game that mixes the thrill of Heads Up with the tension of Hot Potato. Players must guess words, pass the “Hot Head” quickly, and hope the buzzer doesn’t go off while they’re still holding it!

> Developed as part of a university computer science course / physical computing project.

[![Hot Head Instruction Video](docs/assets/video_thumbnail.png)](docs/assets/Video_Project.mp4)

## Concept
Try to guess as many words as possible before time runs out.
When the buzzer sounds, **the player holding the Hot Head loses the round**.

### How to Play
1. To turn on the Hot Head **connect it to your power source**.
2. The display shows **HOT HEAD!** and the **glowing white button** indicates the game is ready.
3. Press **START**:
   - A **3–2–1–GO** countdown appears (with beep sounds).
4. During the round:
   - The **word** is shown on the display.
   - The **timer runs in the background** and is **not visible**.
   - When the group guesses correctly, press **the glowing green button**:
     - A short **PASS ON…** screen appears (anti-cheat delay),
     - then a **new word** is shown.
5. In the **last 5 seconds**:
   - The display **blinks red**,
   - the **timer becomes visible**,
   - and a **warning beep** plays each second.
6. When time is up:
   - The display shows **TIME IS UP!**
   - an **explosion sound** plays.
7. Start the next round by pressing **the white button** again.

Tip: 3 or more players recommended — the more chaos, the better!

## Requirements
To build this project you will need:

### Hardware
* [An Arduino Nano ESP32](https://store.arduino.cc/products/nano-esp32-with-headers)
* Arduino Nano **Grove Pad** (for easy wiring)
* Grove RGB LCD Display **16x2** (I2C)
* **2× Arcade Buttons with LEDs** (Start + Pass On)
  * [Example: 30mm illuminated arcade button (5V)](https://www.berrybase.ch/arcade-button-30mm-beleuchtet-led-5v-dc-transparent)
* Modulino **Buzzer**
* Power source (e.g. USB-C power bank / battery)
* Wires / breadboard or soldering equipment (depending on your build)
* 3D printed enclosure (“Hot Head” housing)

> Wiring diagram / photo: see **How to Build → Wiring**.

### Software
* [MicroPython](https://micropython.org/)
* [Arduino Lab for MicroPython](https://labs.arduino.cc/en/labs/micropython)
* [Arduino MicroPython Installer](https://labs.arduino.cc/en/labs/micropython-installer)

### Libraries
* [MicroPython I2C 16x2 LCD driver](https://github.com/ubidefeo/micropython-i2c-lcd)
* `modulino` (ModulinoBuzzer)
* `network` (WiFi)
* `requests` (HTTP requests)

## How to build
### Wiring
![Wiring Sketch](docs/assets/wiring.png)
<!-- TODO: Replace with the wiring sketch -->

### Uploading the code
* Copy the content of your `src` from your computer to your board
* Install the libraries listed above
* Open the main script and adjust:
   * WiFi credentials (optional)
   * Pins used for the hardware
   > You can change these in `START_BUTTON_PIN`, `START_LED_PIN`, `PASS_ON_BUTTON_PIN`, `PASS_ON_LED_PIN`, `WIFI_SSID`, `WIFI_PASSWORD`.

## Words
### WiFi setup (optional)
This project can fetch random words online via a public API.  
If no WiFi connection is available or the connection fails, the game automatically falls back to a local word list and can be played completely offline.

### Local Word List
The local fallback word list (`BASE_WORD_LIST`) can be freely customized.  
You can replace the existing words with your own vocabulary, for example:
* a different language
* themed words (movies, school subjects, locations, etc.)
* easier or harder words depending on the players

Currently, the fallback list contains **German nouns**.

#### Word API
The game uses the [Random Words API endpoint from KushCreates.com](https://random-words-api.kushcreates.com/api?language=de&category=animals&words=1).

The API allows customization of:
* **Language** (e.g. German, English, etc.)
* **Category** (e.g. animals, sports, games, …)

You can configure these options on the API website, then simply copy the generated API URL and replace the `RANDOM_NOUN_API_URL` in the code.


## Feedback and questions
If you are interested in this project and need to ask questions get in touch with us over Instagram/TikTok/etc/etc
