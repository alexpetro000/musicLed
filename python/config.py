"""Default settings and configuration for audio reactive LED strip"""
from __future__ import division
from __future__ import print_function

import copy

use_defaults = {"configuration": True,  # See notes below for detailed explanation
                "GUI_opts": True,
                "devices": True,
                "colors": True,
                "gradients": True
                }

settings = {
    "sync": True,
    "brightness": 0.3,

    "configuration": {  # Program configuration
        'USE_GUI': False,  # Whether to display the GUI
        'MIC_RATE': 48000,  # Sampling frequency of the microphone in Hz
        'FPS': 60,  # Desired refresh rate of the visualization (frames per second)
        'maxBrightness': 255,  # Max brightness sent to LED strip
        'N_ROLLING_HISTORY': 1,  # Number of past audio frames to include in the rolling window
        'MIN_VOLUME_THRESHOLD': 0.0001,  # No music visualization displayed if recorded audio volume below threshold

    },

    # All devices and their respective settings. Indexed by name, call each one what you want.
    "devices": {
        "5m strip": {
            "configuration": {"UDP_IP": "192.168.1.11",
                              # IP address of the ESP8266. Must match IP in ws2812_controller.ino
                              "UDP_PORT": 19446,  # Port number used for socket communication between Python and ESP8266
                              "maxBrightness": 255,
                              # Max brightness of output (0-255) (my strip sometimes bugs out with high brightness)
                              # Other configuration
                              "N_PIXELS": 300,  # Number of pixels in the LED strip (must match ESP8266 firmware)
                              "N_FFT_BINS": 56,
                              # Number of frequency bins to use when transforming audio to frequency domain
                              "MIN_FREQUENCY": 20,
                              # Frequencies below this value will be removed during audio processing
                              "MAX_FREQUENCY": 18000,
                              # Frequencies above this value will be removed during audio processing
                              "current_effect": "EnergyScroll"
                              # Currently selected effect for this board, used as default when program launches
                              },

            # Configurable options for this board's effects go in this dictionary.
            # Usage: config.settings["devices"][name]["effect_opts"][effect][option]
        },
        # "2m strip": {
        #     "configuration": {"UDP_IP": "wrl_2.local",
        #                       # IP address of the ESP8266. Must match IP in ws2812_controller.ino
        #                       "UDP_PORT": 7778,  # Port number used for socket communication between Python and ESP8266
        #                       "maxBrightness": 255,
        #                       # Max brightness of output (0-255) (my strip sometimes bugs out with high brightness)
        #                       # Other configuration
        #                       "N_PIXELS": 74,  # Number of pixels in the LED strip (must match ESP8266 firmware)
        #                       "N_FFT_BINS": 24,
        #                       # Number of frequency bins to use when transforming audio to frequency domain
        #                       "MIN_FREQUENCY": 20,
        #                       # Frequencies below this value will be removed during audio processing
        #                       "MAX_FREQUENCY": 18000,
        #                       # Frequencies above this value will be removed during audio processing
        #                       "current_effect": "Stars"
        #                       # Currently selected effect for this board, used as default when program launches
        #                       },
        #
        #     # Configurable options for this board's effects go in this dictionary.
        #     # Usage: config.settings["devices"][name]["effect_opts"][effect][option]
        # },
        #
        # "Light panel": {
        #     "configuration": {"UDP_IP": "wrl_3.local",
        #                       # IP address of the ESP8266. Must match IP in ws2812_controller.ino
        #                       "UDP_PORT": 7778,  # Port number used for socket communication between Python and ESP8266
        #                       "maxBrightness": 255,
        #                       # Max brightness of output (0-255) (my strip sometimes bugs out with high brightness)
        #                       # Other configuration
        #                       "N_PIXELS": 74,  # Number of pixels in the LED strip (must match ESP8266 firmware)
        #                       "N_FFT_BINS": 24,
        #                       # Number of frequency bins to use when transforming audio to frequency domain
        #                       "MIN_FREQUENCY": 20,
        #                       # Frequencies below this value will be removed during audio processing
        #                       "MAX_FREQUENCY": 18000,
        #                       # Frequencies above this value will be removed during audio processing
        #                       "current_effect": "Stars"
        #                       # Currently selected effect for this board, used as default when program launches
        #                       },
        #
        #     # Configurable options for this board's effects go in this dictionary.
        #     # Usage: config.settings["devices"][name]["effect_opts"][effect][option]
        # },

    },

    # Collection of different colours in RGB format
    "colors": {"Red": (255, 0, 0),
               "Orange": (255, 40, 0),
               "Yellow": (255, 255, 0),
               "Green": (0, 255, 0),
               "Blue": (0, 0, 255),
               "Light blue": (1, 247, 161),
               "Purple": (80, 5, 252),
               "Pink": (255, 0, 178),
               "White": (255, 255, 255)},

    # Multicolour gradients. Colours must be in list above
    "gradients": {"Spectral": ["Red", "Orange", "Yellow", "Green", "Light blue", "Blue", "Purple", "Pink"],
                  "Dancefloor": ["Red", "Pink", "Purple", "Blue"],
                  "Sunset": ["Red", "Orange", "Yellow"],
                  "Ocean": ["Green", "Light blue", "Blue"],
                  "Jungle": ["Green", "Red", "Orange"],
                  "Sunny": ["Yellow", "Light blue", "Orange", "Blue"],
                  "Fruity": ["Orange", "Blue"],
                  "Peach": ["Orange", "Pink"],
                  "Rust": ["Orange", "Red"]
                  }

}

for board in settings["devices"]:
    # Cheeky lil fix in case the user sets an odd number of LEDs
    if settings["devices"][board]["configuration"]["N_PIXELS"] % 2:
        settings["devices"][board]["configuration"]["N_PIXELS"] -= 1
