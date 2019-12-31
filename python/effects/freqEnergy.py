from scipy.ndimage.filters import gaussian_filter1d
import numpy as np
import config as config
import util
import colorsys

from effects.effect import Effect


class FreqEnergy(Effect):
    def __init__(self, board):
        self.effectName = "FreqEnergy"

    def visualize(self, board, y):
        maxMel = np.argmax(y)
        r, g, b = colorsys.hsv_to_rgb(maxMel / len(y), 1, 1)
        # Scrolling effect window
        speed = config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["speed"]
        board.visualizer.output[:, speed:] = board.visualizer.output[:, :-speed]
        board.visualizer.output = (
                    board.visualizer.output * config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"][
                "decay"]).astype(int)
        board.visualizer.output = gaussian_filter1d(
            board.visualizer.output,
            sigma=config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["scrollBlur"]
        )

        board.visualizer.output[0, :speed] = int(r * 255)
        board.visualizer.output[1, :speed] = int(g * 255)
        board.visualizer.output[2, :speed] = int(b * 255)

        y = np.copy(y)
        board.signalProcessor.gain.update(y)
        y /= board.signalProcessor.gain.value
        scale = config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["scale"]
        # Scale by the width of the LED strip
        y *= float((config.settings["devices"][board.board]["configuration"]["N_PIXELS"] * scale) - 1)
        y = np.copy(util.interpolate(y, config.settings["devices"][board.board]["configuration"]["N_PIXELS"] // 2))

        meanOrMax = np.mean if config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["mean"] else np.max

        if config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["splitRGB"]:
            r = int(meanOrMax(y[:len(y) // 3] ** scale) *
                    config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["r_multiplier"])
            g = int(meanOrMax(y[len(y) // 3: 2 * len(y) // 3] ** scale) *
                    config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["g_multiplier"])
            b = int(meanOrMax(y[2 * len(y) // 3:] ** scale) *
                    config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["b_multiplier"])
        else:
            r = g = b = int(meanOrMax(y ** scale))

        p = np.copy(board.visualizer.output)

        p[0, r:] = 0
        p[1, g:] = 0
        p[2, b:] = 0

        # Apply blur to smooth the edges
        p[0, :] = gaussian_filter1d(p[0, :], sigma=
        config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["blur"])
        p[1, :] = gaussian_filter1d(p[1, :], sigma=
        config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["blur"])
        p[2, :] = gaussian_filter1d(p[2, :], sigma=
        config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["blur"])

        if config.settings["devices"][board.board]["effect_opts"]["FreqEnergy"]["mirror"]:
            p = np.concatenate((p[:, ::-2], p[:, ::2]), axis=1)

        return p
