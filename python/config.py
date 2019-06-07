"""Default settings and configuration for audio reactive LED strip"""
from __future__ import division
from __future__ import print_function

import copy

use_defaults = {"configuration": True,  # See notes below for detailed explanation
                "GUI_opts": True,
                "devices": True,
                "colors": True,
                "gradients": True}

effectOptions = {
                "Off": {
                        "idle_r": 1,
                        "idle_g": 1,
                        "idle_b": 1,
                },
                "Energy": {"blur": 1,  # Amount of blur to apply
                            "scale": 1,  # Width of effect on strip
                            "r_multiplier": 1.0,  # How much red
                            "mirror": True,  # Reflect output down centre of strip
                            "g_multiplier": 1.0,  # How much green
                            "b_multiplier": 1.0},  # How much blue
                "EnergyScroll": {"opacity": 0.7,
                                  "energy_on_top": False},
                "Wave": {"color_wave": "Red",  # Colour of moving bit
                          "color_flash": "White",  # Colour of flashy bit
                          "wipe_len": 7,  # Initial length before beat
                          "color_mode": "Spectral",  # Color of gradient
                          "decay": 0.9,  # How quickly the flash fades away
                          "wipe_speed": 1},  # Number of pixels added to colour bit every frame

                "Spectrum": {"blur": 1.0, "color_mode": "Spectral"},

                "Wavelength": {"roll_speed": 0,  # How fast (if at all) to cycle colour overlay across strip
                                "color_mode": "Spectral",  # Colour gradient to display
                                "mirror": False,  # Reflect output down centre of strip
                                "reverse_grad": False,  # Flip (LR) gradient
                                "reverse_roll": False,  # Reverse movement of gradient roll
                                "blur": 1.0,  # Amount of blur to apply
                                "flip_lr": False},  # Flip output left-right
                "Scroll": {"lows_color": "Red",  # Colour of low frequencies
                            "mids_color": "Green",  # Colour of mid frequencies
                            "high_color": "Blue",  # Colour of high frequencies
                            "decay": 0.995,  # How quickly the colour fades away as it moves
                            "speed": 5,  # Speed of scroll
                            "flip_lr": False,  # Reflect output down centre of strip
                            "r_multiplier": 1.0,  # How much red
                            "g_multiplier": 1.0,  # How much green
                            "b_multiplier": 1.0,  # How much blue
                            "blur": 0.2},  # Amount of blur to apply
                "Power": {"color_mode": "Spectral",  # Colour gradient to display
                           "s_count": 20,  # Initial number of sparks
                           "s_color": "White",  # Color of sparks
                           "mirror": True,  # Mirror output down central axis
                           "flip_lr": False},  # Flip output left-right
                "Single": {"color": "Purple"},  # Static color to show
                "Auto": {"timer": 500},
                "Beat": {"color": "Red",  # Colour of beat flash
                          "decay": 0.7},  # How quickly the flash fades away
                "Bars": {"resolution": 4,  # Number of "bars"
                          "color_mode": "Spectral",  # Multicolour mode to use
                          "roll_speed": 0,  # How fast (if at all) to cycle colour colours across strip
                          "mirror": False,  # Mirror down centre of strip
                          "reverse_roll": False,  # Reverse movement of gradient roll
                          "flip_lr": False},  # Flip output left-right
                "Stars": {"star_rate": 0.29,
                           "star_decay": 9,
                           "star_speed": 0.0006},
                "Mood": {"color_mode": "Spectral",  # Colour gradient to display
                          "roll_speed": 1,
                          "delay": 0.1,  # How fast (if at all) to cycle colour colours across strip
                          "fast": False,  # Fast/Slow
                          "mirror": False,  # Mirror gradient down central axis
                          "reverse": False},  # Reverse movement of gradient

                "Gradient": {"color_mode": "Spectral",  # Colour gradient to display
                              "roll_speed": 0,
                              "fast": False,  # Fast/Slow
                              "mirror": False,  # Mirror gradient down central axis
                              "reverse": False},  # Reverse movement of gradient
                "Fade": {"color_mode": "Spectral",  # Colour gradient to fade through
                          "roll_speed": 1,  # How fast (if at all) to fade through colours
                          "reverse": False},  # Reverse "direction" of fade (r->g->b or r<-g<-b)
                "Calibration": {"r": 100,
                                 "g": 100,
                                 "b": 100},

                "Sleep": {"hour": 6, "minute": 9, "minutes_fade": 30},
                "Fire": {"delay": 0.04},
                "Runner": {"color_mode": "Spectral", "times": 0.15, "add": 0.1, "divide": 4.7, "blur": 0},
                "RunnerReactive": {"color_mode": "Fruity", "times": 0.90, "add": 0.8, "divide": 18, "blur": 1}
                }

settings = {  # All settings are stored in this dict
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
            "configuration": {"UDP_IP": "wrl_1.local",
                              # IP address of the ESP8266. Must match IP in ws2812_controller.ino
                              "UDP_PORT": 7778,  # Port number used for socket communication between Python and ESP8266
                              "maxBrightness": 255,
                              # Max brightness of output (0-255) (my strip sometimes bugs out with high brightness)
                              # Other configuration
                              "N_PIXELS": 300,  # Number of pixels in the LED strip (must match ESP8266 firmware)
                              "N_FFT_BINS": 24,
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
            "effect_opts": copy.deepcopy(effectOptions)
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
        #     "effect_opts": copy.deepcopy(effectOptions)
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
        #     "effect_opts": copy.deepcopy(effectOptions)
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
