#!/usr/bin/env python3

from __future__ import division
from __future__ import print_function

import time
from threading import Thread

import config
import lib.api as api
import lib.devices as devices
import lib.bottle as bottle
import lib.microphone as microphone
from lib.dsp import DSP
from visualizer import Visualizer

import socket


class Board:
    def __init__(self, b):
        self.board = b
        self.config = config.settings["devices"][self.board]["configuration"]

        self.visualizer = Visualizer(self)

        config.settings["devices"][self.board]["effect_opts"] = {}

        for effectName, effect in self.visualizer.effects.items():
            config.settings["devices"][self.board]["effect_opts"][effectName] = {}
            for prop in effect.configProps:
                config.settings["devices"][self.board]["effect_opts"][effectName][prop[0]] = prop[-1]

        self.effectConfig = config.settings["devices"][self.board]["effect_opts"]

        self.signalProcessor = DSP(self)

        self.esp = devices.ESP8266(self.config["UDP_IP"], self.config["UDP_PORT"])


laserSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def microphone_update(audio_samples):

    # Get processed audio data for each device
    audio_datas = {}
    for b in boards:
        audio_datas[b] = boards[b].signalProcessor.update(audio_samples)

    outputs = {}

    for b in boards:
        # Get visualization output for each board
        audio_input = audio_datas[b]["vol"] > config.settings["configuration"]["MIN_VOLUME_THRESHOLD"]
        outputs[b] = boards[b].visualizer.get_vis(audio_datas[b]["mel"], audio_input)

        if (boards[b].config["current_effect"] in config.settings["devices"][b]["effect_opts"] and "delay" in
                config.settings["devices"][b]["effect_opts"][boards[b].config["current_effect"]]):
            time.sleep(config.settings["devices"][b]["effect_opts"][boards[b].config["current_effect"]]["delay"])

        outputs[b][0] = outputs[b][0] * config.settings["brightness"]
        outputs[b][1] = outputs[b][1] * config.settings["brightness"]
        outputs[b][2] = outputs[b][2] * config.settings["brightness"]

        boards[b].esp.show(outputs[b])


boards = {}
for board in config.settings["devices"]:
    boards[board] = Board(board)

api.setBoards(boards)
api.setConfig(config)


def do_stream():
    microphone.start_stream(microphone_update)


def do_api():
    bottle.run(host='0.0.0.0', port=8082)


if __name__ == "__main__":
    apiThread = Thread(target=do_api, daemon=True)
    apiThread.start()

    streamThread = Thread(target=do_stream, daemon=True)
    streamThread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        microphone.stop_stream()
        time.sleep(3)

print('exit')
