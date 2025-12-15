"""Hot Head"""

from time import sleep, sleep_ms
from machine import I2C, Pin
from modulino import ModulinoBuzzer
from i2c_lcd import RGBDisplay
import urandom
import network
import requests

sleep(1.5)
# ============================
# GLOBAL STATE
# ============================


class GlobalState:
    """Global state of the Hot Head game."""

    def __init__(self, base_word_list):
        self.current_word = ""
        self.last_timer_text = ""
        self.game_running = False
        self.word_pool = [w.upper() for w in base_word_list]


# ============================
# CONSTANTS
# ============================

DISPLAY_WIDTH = 16

BASE_WORD_LIST = [
    "Apfel",
    "Banane",
    "Elefant",
    "Python",
    "Schokolade",
    "Berg",
    "Pizza",
    "Katze",
    "Hund",
    "Haus",
    "Baum",
    "Blume",
    "Tisch",
    "Stuhl",
    "Auto",
    "Zug",
    "Flugzeug",
    "Dozent",
    "Computer",
    "Fenster",
    "Buch",
    "Lampe",
    "Strasse",
    "Kuchen",
    "Gabel",
    "Stadt",
]

WORD_LIST = [w.upper() for w in BASE_WORD_LIST]

MIN_TIME_SEC = 15
MAX_TIME_SEC = 30

VISIBLE_COUNTDOWN_SEC = 5
NEXT_WORD_DELAY_MS = 3000

START_BUTTON_PIN = "A1"
START_LED_PIN = "A0"

PASS_ON_BUTTON_PIN = "A2"
PASS_ON_LED_PIN = "A3"

WIFI_SSID = "YOUR_WIFI_SSID"
WIFI_PASSWORD = "YOUR_WIFI_PASSWORD"
WIFI_MAX_WAIT_SEC = 8

RANDOM_NOUN_API_URL = (
    "https://random-words-api.kushcreates.com/api?language=de&category=animals&words=1"
)

state = GlobalState(BASE_WORD_LIST)


# ============================
# INITIALIZATION
# ============================

buzzer = ModulinoBuzzer()

display = RGBDisplay(I2C(1))

start_button = Pin(START_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
start_led = Pin(START_LED_PIN, Pin.OUT)

pass_on_button = Pin(PASS_ON_BUTTON_PIN, Pin.IN, Pin.PULL_UP)
pass_on_led = Pin(PASS_ON_LED_PIN, Pin.OUT)


# ============================
# HELPER FUNCTIONS
# ============================


def connect_wifi():
    """Try to connect to WiFi for a limited time and show status on the display."""
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)

    display.clear()
    display.color(255, 255, 255)
    draw("Connecting to", "WiFi...")

    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        elapsed = 0.0
        step = 0.5

        while not wlan.isconnected() and elapsed < WIFI_MAX_WAIT_SEC:
            sleep(step)
            elapsed += step

    if wlan.isconnected():
        print("WiFi connected:", wlan.ifconfig())
        display.clear()
        display.color(0, 255, 0)
        draw("WiFi connected")
        sleep(1.5)
    else:
        print("WiFi connection failed, running offline.")
        display.clear()
        display.color(255, 255, 0)
        draw("Connection failed", "running offline.")
        sleep(1.5)

    return wlan


def fetch_german_noun():
    """Retrieve a random German noun from Random Words API."""
    try:
        resp = requests.get(RANDOM_NOUN_API_URL)
        if resp.status_code == 200:
            data = resp.json()
            resp.close()

            if isinstance(data, list) and len(data) > 0:
                entry = data[0]
                word = entry.get("word")
                if word:
                    return word.upper()

        else:
            resp.close()

    except (OSError, ValueError) as exc:
        print("Noun API failed:", exc)

    return None


def center_fit(text, width=DISPLAY_WIDTH):
    """Return the text centered within the given display width."""
    t = str(text)
    if len(t) > width:
        t = t[:width]
    padding = (width - len(t)) // 2
    return " " * padding + t + " " * (width - len(t) - padding)


def draw(word, timer_text=""):
    """Render the word and optional timer text on the two-line display."""
    display.move(0, 0)
    display.write(center_fit(word))

    display.move(0, 1)
    display.write(center_fit(timer_text))


def random_word():
    """Return a German noun from API if possible, otherwise from a non-repeating fallback pool."""
    try:
        api_noun = fetch_german_noun()
        if api_noun:
            return api_noun
    except (OSError, ValueError) as e:
        print("API skipped:", e)

    if not state.word_pool:
        state.word_pool = [w.upper() for w in BASE_WORD_LIST]

    idx = urandom.getrandbits(8) % len(state.word_pool)
    return state.word_pool.pop(idx)


def random_time_sec():
    """Return a random integer representing the round duration in seconds."""
    return MIN_TIME_SEC + (urandom.getrandbits(8) % (MAX_TIME_SEC - MIN_TIME_SEC + 1))


def set_start_led(on):
    """Turn the start button LED on or off."""
    start_led.value(1 if on else 0)


def set_pass_on_led(on):
    """Turn the pass-on button LED on or off."""
    pass_on_led.value(1 if on else 0)


def is_button_pressed(button_pin):
    """Return True if the given button pin is currently pressed."""
    return button_pin.value() == 0


def wait_for_button_release(button_pin):
    """Block until the given button is released."""
    while button_pin.value() == 0:
        sleep(0.02)


def buzzer_tone(freq):
    """Play a tone with the Modulino buzzer."""
    buzzer.tone(freq)


def buzzer_off():
    """Stop any sound on the Modulino buzzer."""
    buzzer.no_tone()


# ============================
# SOUND EFFECTS
# ============================


def play_start_countdown_sound(is_final=False):
    """Play a single countdown beep (short for 3-2-1, long for GO)."""
    if is_final:
        freq = 1500
        duration_ms = 500
    else:
        freq = 1000
        duration_ms = 200

    buzzer.tone(freq)
    sleep_ms(duration_ms)
    buzzer.no_tone()


def play_final_warning_beep():
    """Play a short warning beep during the last seconds before time is up."""
    buzzer.tone(1800)
    sleep_ms(120)
    buzzer.no_tone()


def play_explosion_sound():
    """Play explosion-style sound at the end of the round."""
    for freq in range(5000, 200, -30):
        buzzer.tone(freq)
        sleep_ms(6)

    for _ in range(20):
        rand_freq = urandom.randrange(200, 2000)
        buzzer.tone(rand_freq)
        sleep_ms(8)

    for freq in range(300, 200, -5):
        buzzer.tone(freq)
        sleep_ms(12)

    buzzer.no_tone()


# ============================
# PASS-ON BUTTON HANDLING
# ============================


def change_word():
    """Show PASS ON, then switch to a new random word after a short delay."""
    if not state.game_running:
        return

    buzzer_off()

    set_pass_on_led(False)
    sleep(0.1)
    set_pass_on_led(True)

    display.clear()
    display.color(255, 255, 255)
    draw("PASS ON...", "")

    steps = max(1, NEXT_WORD_DELAY_MS // 50)
    for _ in range(steps):
        sleep(0.05)

    state.current_word = random_word()
    display.clear()
    draw(state.current_word, "")


# ============================
# UI SCREENS
# ============================


def show_idle_screen():
    """Display the idle title screen of the game."""
    display.clear()
    display.color(255, 255, 255)
    draw("HOT HEAD!", "")

    set_start_led(True)
    set_pass_on_led(False)


def wait_for_start_button():
    """Block until the start button is pressed."""
    while True:
        if is_button_pressed(start_button):
            wait_for_button_release(start_button)
            return
        sleep(0.02)


def pre_countdown():
    """Show a 3-2-1-GO countdown animation before the round starts."""
    set_start_led(False)
    set_pass_on_led(True)
    display.clear()

    for n in [3, 2, 1]:
        display.color(0, 255, 0)
        draw("Get ready!", str(n))

        play_start_countdown_sound(is_final=False)
        sleep(0.8)

    display.color(255, 255, 255)
    draw("GO!", "")

    play_start_countdown_sound(is_final=True)
    sleep(0.5)


# ============================
# MAIN ROUND (WORD + TIMER)
# ============================


def run_round():
    """Run a single game round including word display and countdown timer."""
    state.game_running = True

    state.current_word = random_word()
    total_seconds = random_time_sec()
    state.last_timer_text = ""

    display.clear()
    display.color(255, 255, 255)
    draw(state.current_word, "")
    sleep(1)

    remaining_sec = total_seconds

    while remaining_sec > 0 and state.game_running:
        minutes = remaining_sec // 60
        seconds = remaining_sec % 60
        state.last_timer_text = f"{minutes:02d}:{seconds:02d}"

        if remaining_sec <= VISIBLE_COUNTDOWN_SEC:
            draw(state.current_word, state.last_timer_text)
        else:
            draw(state.current_word, "")

        for i in range(10):
            if remaining_sec <= VISIBLE_COUNTDOWN_SEC:
                if i == 0:
                    play_final_warning_beep()

                if i < 5:
                    display.color(255, 0, 0)
                else:
                    display.color(255, 255, 255)
            else:
                display.color(255, 255, 255)

            if is_button_pressed(pass_on_button):
                buzzer_off()
                wait_for_button_release(pass_on_button)
                change_word()

            sleep(0.1)

        remaining_sec -= 1

    state.game_running = False
    display.color(255, 0, 0)
    draw("TIME IS UP!", "00:00")
    play_explosion_sound()

    set_pass_on_led(False)
    sleep(2.0)


# ============================
# MAIN LOOP
# ============================


def main():
    """Run the main game loop handling WiFi, idle screen, start, round, and reset."""
    show_idle_screen()

    while True:
        wait_for_start_button()

        try:
            connect_wifi()
        except OSError as exc:
            print("WiFi skipped:", exc)

        pre_countdown()
        run_round()
        show_idle_screen()


# ============================
# RUN
# ============================

main()
