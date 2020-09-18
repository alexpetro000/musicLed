from scipy.ndimage.filters import gaussian_filter1d
import numpy as np
import config  as config
import util

from effects.effect import Effect
from effects.wavelength import Wavelength

import math


class RunnerReactive(Effect):
    def __init__(self, visualizer):
        self.effectName = "Reactive Runner"
        self.position = 0
        self.configProps = [
            ["times", "times", "slider", (0.05, 1, 0.05), 0.15],
            ["divide", "divide", "slider", (1, 15, 1), 4.7],
            ["add", "add", "slider", (0, 2, 0.1), 0.1],
            ["blur", "blur", "slider", (0, 5, 1), 0],
            ["color_mode", "Color Mode", "dropdown", config.settings["gradients"], "Spectral"]
        ]

    def visualize(self, board, y):
        # print('Beat vis called')
        output = np.array([
            [(((math.sin(i * board.effectConfig["Reactive Runner"]["times"] + (
                        self.position / board.effectConfig["Reactive Runner"]["divide"])) +
                board.effectConfig["Reactive Runner"]["add"]) * ((math.cos(i))))) for i in
             range(board.config["N_PIXELS"])],
            [(((math.sin(i * board.effectConfig["Reactive Runner"]["times"] + (
                        self.position / board.effectConfig["Reactive Runner"]["divide"])) +
                board.effectConfig["Reactive Runner"]["add"]) * ((math.cos(i))))) for i in
             range(board.config["N_PIXELS"])],
            [(((math.sin(i * board.effectConfig["Reactive Runner"]["times"] + (
                        self.position / board.effectConfig["Reactive Runner"]["divide"])) +
                board.effectConfig["Reactive Runner"]["add"]) * ((math.cos(i))))) for i in
             range(board.config["N_PIXELS"])]
        ])

        outputGradient = np.array(
            [
                board.visualizer.multicolor_modes[board.effectConfig["Reactive Runner"]["color_mode"]][0][
                :board.config["N_PIXELS"]],
                board.visualizer.multicolor_modes[board.effectConfig["Reactive Runner"]["color_mode"]][1][
                :board.config["N_PIXELS"]],
                board.visualizer.multicolor_modes[board.effectConfig["Reactive Runner"]["color_mode"]][2][
                :board.config["N_PIXELS"]],
            ]
        )

        output[0] = np.multiply(output[0], outputGradient[0])
        output[1] = np.multiply(output[1], outputGradient[1])
        output[2] = np.multiply(output[2], outputGradient[2])

        wavelength = board.visualizer.effects["Wavelength"].visualize(board, y)
        output[0] = np.multiply(output[0], ((wavelength[0] + wavelength[1] + wavelength[1]) / 3) / 10)
        output[1] = np.multiply(output[1], ((wavelength[0] + wavelength[1] + wavelength[1]) / 3) / 10)
        output[2] = np.multiply(output[2], ((wavelength[0] + wavelength[1] + wavelength[1]) / 3) / 10)

        if (board.effectConfig["Reactive Runner"]["blur"] > 0):
            output[0] = gaussian_filter1d(output[0], sigma=board.effectConfig["Reactive Runner"]["blur"])
            output[1] = gaussian_filter1d(output[1], sigma=board.effectConfig["Reactive Runner"]["blur"])
            output[2] = gaussian_filter1d(output[2], sigma=board.effectConfig["Reactive Runner"]["blur"])

        self.position += 1

        return output
