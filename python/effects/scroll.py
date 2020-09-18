from scipy.ndimage.filters import gaussian_filter1d
import numpy as np
import config  as config
import util
import colorsys


from effects.effect import Effect

class Scroll(Effect):
    def __init__(self, visualizer):
        self.effectName = "Scroll"
        self.configProps = [
            ["lows_color", "Lows Color", "dropdown", config.settings["colors"], "Red"],
            ["mids_color", "Mids Color", "dropdown", config.settings["colors"], "Green"],
            ["high_color", "Highs Color", "dropdown", config.settings["colors"], "Blue"],
            ["blur", "Blur", "float_slider", (0.95, 1, 0.005), 0.2],
            ["flip_lr", "Flip LR", "checkbox", False],
            ["decay", "Decay", "float_slider", (0.75, 1.0, 0.0005), 0.995],
            ["speed", "Speed", "slider", (3, 10, 1), 9],
            ["gain", "Gain", "float_slider", (0.5, 6.0, 0.001), 3.0],
            # ["r_multiplier", "How much red", "float_slider", (0.01, 1.0, 0.01), 1.0],
            # ["g_multiplier", "How much green", "float_slider", (0.01, 1.0, 0.01), 1.0],
            # ["b_multiplier", "How much blue", "float_slider", (0.01, 1.0, 0.01), 1.0],
        ]

    def visualize(self, board, y):
        y = y**config.settings["devices"][board.board]["effect_opts"]["Scroll"]["gain"]

        y = np.clip(y, 0, 1)
        lows = y[:len(y) // 6]
        mids = y[len(y) // 6: 2 * len(y) // 5]
        high = y[2 * len(y) // 5:]
        # max values
        lows_max = np.max(lows)  # *config.settings["devices"][board.board]["effect_opts"]["Scroll"]["lows_multiplier"])
        mids_max = np.max(mids)  # *config.settings["devices"][board.board]["effect_opts"]["Scroll"]["mids_multiplier"])
        high_max = np.max(high)  # *config.settings["devices"][board.board]["effect_opts"]["Scroll"]["high_multiplier"])
        # indexes of max values
        # map to colour gradient
        lows_val = (np.array(config.settings["colors"][config.settings["devices"][board.board]["effect_opts"]["Scroll"]["lows_color"]]) * lows_max).astype(int)
        mids_val = (np.array(config.settings["colors"][config.settings["devices"][board.board]["effect_opts"]["Scroll"]["mids_color"]]) * mids_max).astype(int)
        high_val = (np.array(config.settings["colors"][config.settings["devices"][board.board]["effect_opts"]["Scroll"]["high_color"]]) * high_max).astype(int)
        # Scrolling effect window
        speed = config.settings["devices"][board.board]["effect_opts"]["Scroll"]["speed"]
        board.visualizer.output[:, speed:] = board.visualizer.output[:, :-speed]
        board.visualizer.output = (board.visualizer.output * config.settings["devices"][board.board]["effect_opts"]["Scroll"]["decay"]).astype(int)
        board.visualizer.output = gaussian_filter1d(board.visualizer.output, sigma=config.settings["devices"][board.board]["effect_opts"]["Scroll"]["blur"])
        # Create new color originating at the center
        board.visualizer.output[0, :speed] = lows_val[0] + mids_val[0] + high_val[0]
        board.visualizer.output[1, :speed] = lows_val[1] + mids_val[1] + high_val[1]
        board.visualizer.output[2, :speed] = lows_val[2] + mids_val[2] + high_val[2]

        if config.settings["devices"][board.board]["effect_opts"]["Scroll"]["flip_lr"]:
            p = np.fliplr(board.visualizer.output)
        else:
            p = board.visualizer.output

        p = np.concatenate((p[:, ::-2], p[:, ::2]), axis=1)

        return p

