from adafruit_bitmap_font import bitmap_font

config = {
	#########################
	# Network Configuration #
	#########################

	# Wi-Fi information is kept in secrets.py

	#########################
	# Metro Configuration   #
	#########################
	
	# Choose WMATA or MetroHero
	'source_api': 'WMATA', 

	# Metro Station Codes
	# Note for the four transfer stations (Metro Center, L'Enfant Plaza, Fort Totten, Gallery Place)
	# they have two codes, since they serve multiple tracks
	'metro_station_codes': ['E06','B06'],

	# Metro Train Groups
	# The '1' direction is generally towards NE; '2' is towards the stations that are futher West or South
	# The specifics are laid out in the README.md file
	# Note the size of this array should equal the number of Metro Station Codes you set above
	'train_groups_1': ['2','2'],
	'train_groups_2': ['1','1'],

	# Walking Distance Times, ignore trains arriving in less than this time
	# Note the size of this array should equal the number of Metro Station Codes you set above
	'walking_times': [0, 0],

	# WMATA API
	'wmata_api_url': 'https://api.wmata.com/StationPrediction.svc/json/GetPrediction/',

	# MetroHero API
	'metro_hero_api_url': 'https://dcmetrohero.com/api/v1/metrorail/stations/[stationCode]/trains?includeScheduledPredictions=True',

	# How many times to retry to download data
	'metro_api_retries': 3,
	
	# How long to wait before updates, in seconds
	# And how many times to check for button presses in between
	'refresh_interval': 5, 
	'button_check_divisor': 10,
	
	# Full names mapped to abbreviations for MetroHero
	'station_mapping': {
		'Branch Avenue': 'Brnch Av',
		'Huntington': 'Hntingtn',
		'Vienna/Fairfax-GMU': 'Vienna',
		'Franconia-Springfield': 'Frnconia',
		'New Carrollton': 'NewCrltn',
		'Greenbelt': 'Grnbelt',
		'Huntington': 'Hntingtn',
		'Largo Town Center': 'Largo',
		'Twinbrook': 'Twinbrk',
		'Wiehle-Reston East': 'Wiehle',
		'No Passenger': 'No Psngr',
		'NoPssenger': 'No Psngr',
		'ssenger': 'No Psngr'
	},

	#############################
	# Off Hours Configuration   #
	#############################

	# Time of day to turn board on and off - must be 24 hour "HH:MM"
	'use_timer': False,
	'display_on_time': "07:00",
	'display_off_time': "22:30",


	#########################
	# Display Configuration #
	#########################
	'matrix_width': 64,
	'matrix_height': 32,
    
	# 0: Unrotated, matrix on left side of board
	# 180: Matrix is on the right
	'rotation': 0,

	# Train font data
	'num_trains': 4,		# Even if you show 3, this can be higher as it's just cut off
	'font': bitmap_font.load_font('lib/Metroesque.bdf'),	# Thanks to u/GJT-34 for this font
	'character_width': 5,
	'character_height': 7,
	'text_color': 0xFF7500,
	'destination_max_characters': 11,
	
	# Spacing - changes if you hide heading with UP button
	'line_spacer': 2,
	'line_spacer_no_heading': 1,
	
	'loading_destination_text': 'Loading...',
	'loading_min_text': '---',
	'loading_line_color': 0xFF00FF, # Something something Purple Line joke

	# Heading data
	'heading_visible': True,
	'heading_font': bitmap_font.load_font('lib/Heading.bdf'),
    
	# There a lot of spaces here - I made the font so [space] is 1 LED wide to fine-tune
	'heading_text': 'LN	DEST				  MIN',
	'heading_height': 6,
	'heading_color': 0xFF0000,

	# Rectangle sizing
	'bar_line_height': 7,
	'bar_line_width': 4,
	'bar_line_offset': 4,

	# Minutes information
	'min_label_characters': 3,
}