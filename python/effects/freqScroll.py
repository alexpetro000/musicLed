from scipy.ndimage.filters import gaussian_filter1d
import numpy as np
import config  as config
import util
import colorsys


from effects.effect import Effect


class FreqScroll(Effect):
    def __init__(self, visualizer):
        self.effectName = "FreqScroll"
        self.configProps = [
        ]

    def visualize(self, board, y):
        y = y ** config.settings["devices"][board.board]["effect_opts"]["Scroll"]["gain"]
        maxMel = np.argmax(y)

        r, g, b = colorsys.hsv_to_rgb(maxMel / len(y), 1, 1)

        # Scrolling effect window
        speed = config.settings["devices"][board.board]["effect_opts"]["Scroll"]["speed"]
        board.visualizer.output[:, speed:] = board.visualizer.output[:, :-speed]
        board.visualizer.output = (board.visualizer.output * config.settings["devices"][board.board]["effect_opts"]["Scroll"]["decay"]).astype(int)
        board.visualizer.output = gaussian_filter1d(board.visualizer.output, sigma=config.settings["devices"][board.board]["effect_opts"]["Scroll"]["blur"])

        board.visualizer.output[0, :speed] = int(r * 255 * y[maxMel])
        board.visualizer.output[1, :speed] = int(g * 255 * y[maxMel])
        board.visualizer.output[2, :speed] = int(b * 255 * y[maxMel])

        if config.settings["devices"][board.board]["effect_opts"]["Scroll"]["flip_lr"]:
            p = np.fliplr(board.visualizer.output)
        else:
            p = board.visualizer.output

        if config.settings["devices"][board.board]["effect_opts"]["Scroll"]["mirror"]:
            p = np.concatenate((p[:, ::-2], p[:, ::2]), axis=1)
        else:
            p = p[:, ::]

        return p

