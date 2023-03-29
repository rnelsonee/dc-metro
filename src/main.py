import time
from config import config
from train_board import TrainBoard
from metro_api import MetroApi, MetroApiOnFireException

from secrets import secrets
import busio
import board
from digitalio import DigitalInOut, Pull
import neopixel
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

# New network
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)
status_light = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.2)
wifi = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, status_light)

# Get our username, key and desired timezone
aio_username = secrets.get("aio_username")
aio_key = secrets.get("aio_key")
location = secrets.get("timezone", None)
TIME_URL = "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s" % (aio_username, aio_key)
TIME_URL += "&fmt=%25Y-%25m-%25d+%25H%3A%25M%3A%25S.%25L+%25j+%25u+%25z+%25Z"

OFF_HOURS_ENABLED =  config.get("use_timer") and aio_username and aio_key and config.get("display_on_time") and config.get("display_off_time")

REFRESH_INTERVAL = config['refresh_interval']
STATION_CODES = config['metro_station_codes']
TRAIN_GROUPS_1 = list(zip(STATION_CODES, config['train_groups_1']))
TRAIN_GROUPS_2 = list(zip(STATION_CODES, config['train_groups_2']))
train_groups = TRAIN_GROUPS_1
WALKING_TIMES = config['walking_times']
if max(WALKING_TIMES) == 0:
    WALKING_TIMES = {}
else:
    WALKING_TIMES = dict(zip(STATION_CODES, WALKING_TIMES))

SHOW_HEADING = config['heading_visible']
DIVISOR = config['button_check_divisor']

def is_off_hours() -> bool:
    try:
        now = wifi.get(TIME_URL, timeout=1).text
        now_hour = int(now[11:13])
        now_minute = int(now[14:16])
        after_end = now_hour > OFF_HOUR or (now_hour == OFF_HOUR and now_minute > OFF_MINUTE)
        before_start = now_hour < ON_HOUR or (now_hour == ON_HOUR and now_minute < ON_MINUTE)

        if ON_HOUR < OFF_HOUR or (ON_HOUR == OFF_HOUR and ON_MINUTE < OFF_MINUTE):
            return after_end or before_start
        else:
            return after_end and before_start
    except Exception as e:
        print(e)
        return False

api = MetroApi()

def refresh_trains(train_groups: list) -> [dict]:
    try:
        trains = api.fetch_train_predictions(wifi, STATION_CODES, train_groups, WALKING_TIMES)
    except MetroApiOnFireException:
        print(config['source_api'] + ' API might be on fire. Resetting wifi ...')
        wifi.reset()
        return None
    return trains

show_heading = config['heading_visible']
train_board = TrainBoard(lambda: refresh_trains(train_groups))

if OFF_HOURS_ENABLED:
    ON_HOUR, ON_MINUTE = map(int, config['display_on_time'].split(":"))
    OFF_HOUR, OFF_MINUTE = map(int, config['display_off_time'].split(":"))

dn_button = DigitalInOut(board.BUTTON_DOWN)
dn_button.switch_to_input(pull=Pull.UP)
dn_button_unpressed = True

up_button = DigitalInOut(board.BUTTON_UP)
up_button.switch_to_input(pull=Pull.UP)
up_button_unpressed = True

# Switch modes, depending on User pressing "UP" button
# Mode      |   Train group to show
#   0       |   Show both TRAIN_GROUPS_1 & TRAIN_GROUPS_2 at once
#   1       |   Altnernate between TRAIN_GROUPS_1 & TRAIN_GROUPS_2
#   1       |   Show only TRAIN_GROUPS_1
#   2       |   Show only TRAIN_GROUPS_2
switch_mode = 0
mode_text = ['Both groups', 'Alt. groups', 'Group 1', 'Group 2']

while True:
    if OFF_HOURS_ENABLED and is_off_hours():
        train_board.turn_off_display()
    else:
        train_board.refresh()
        train_board.turn_on_display()
        if switch_mode == 0:
            train_groups = TRAIN_GROUPS_1 + TRAIN_GROUPS_2
        elif switch_mode == 1:
            train_groups = TRAIN_GROUPS_1 if train_groups == TRAIN_GROUPS_2 else TRAIN_GROUPS_2
        elif switch_mode == 2:
            train_groups = TRAIN_GROUPS_1
        else:
            train_groups = TRAIN_GROUPS_2

    counter = 0
    
    while counter < DIVISOR:
        counter += 1

        # Pressing the "DOWN" button will toggle the heading text on/off
        # to allow for one more train to show
        if dn_button.value is False and dn_button_unpressed:
            show_heading = not show_heading
            print(f'Down putton pressed, show_heading is now {show_heading}')
            train_board.alter_heading(show_heading)
       
        dn_button_unpressed = dn_button.value

        # Changes the group mode, as explained by switch_mode above
        if up_button.value is False and up_button_unpressed:
            switch_mode = (switch_mode + 1) % 4
            print(f'Up button pressed, going to mode {mode_text[switch_mode]}')
            train_board.show_banner(f'{mode_text[switch_mode]}')

        up_button_unpressed = up_button.value

        time.sleep(REFRESH_INTERVAL/DIVISOR)
