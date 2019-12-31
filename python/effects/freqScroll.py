from scipy.ndimage.filters import gaussian_filter1d
import numpy as np
import config  as config
import util
import colorsys


from effects.effect import Effect


class FreqScroll(Effect):
    def __init__(self, board):        
        pass

    def visualize(self, board, y):
        y = y ** config.settings["devices"][board.board]["effect_opts"]["Scroll"]["gain"]
        maxMel = np.argmax(y)

        r, g, b = colorsys.hsv_to_rgb(maxMel / len(y), 1, 1)

        # Scrolling effect window
        speed = config.settings["devices"][board.board]["effect_opts"]["FreqScroll"]["speed"]
        board.visualizer.output[:, speed:] = board.visualizer.output[:, :-speed]
        board.visualizer.output = (board.visualizer.output * config.settings["devices"][board.board]["effect_opts"]["FreqScroll"]["decay"]).astype(int)
        board.visualizer.output = gaussian_filter1d(board.visualizer.output, sigma=config.settings["devices"][board.board]["effect_opts"]["FreqScroll"]["blur"])

        board.visualizer.output[0, :speed] = int(r * 255 * y[maxMel])
        board.visualizer.output[1, :speed] = int(g * 255 * y[maxMel])
        board.visualizer.output[2, :speed] = int(b * 255 * y[maxMel])

        p = board.visualizer.output

        p = np.concatenate((p[:, ::-2], p[:, ::2]), axis=1)

        return p

