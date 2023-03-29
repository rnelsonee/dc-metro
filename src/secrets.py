from config import config

# This file is required by the Matrix Portal library to properly
# initialize the WiFi chip on the board.

secrets = {
    # Network configuration
    'ssid': 'YOUR_SSID_HERE',
    'password': 'YOUR_WIFI_PASSWORD_HERE',

    # WMATA / MetroHero API Key
	'wmata_api_key': 'YOUR_API_KEY_HERE',
	'metro_hero_api_key': '',

    # adafruit io settings, necessary for determining current time to sleep
    # An account is free to set up, instructions below
    # https://learn.adafruit.com/adafruit-magtag/getting-the-date-time
    'aio_username': 'USERNAME',
    'aio_key': 'KEY',
    'timezone': 'America/New_York',
}
