from scipy.ndimage.filters import gaussian_filter1d
import numpy as np
import config as config
import util

from effects.effect import Effect


class EnergyScroll(Effect):
    def __init__(self, board):
        self.effectName = "EnergyScroll"
        self.scroll_output = np.copy(board.output)

    def visualize(self, board, y):
        scroll_output = self.visualize_scroll(board, y)

        y = np.copy(y)
        board.signalProcessor.gain.update(y)
        y /= board.signalProcessor.gain.value
        scale = config.settings["devices"][board.board]["effect_opts"]["Energy"]["scale"]
        # Scale by the width of the LED strip
        y *= float((config.settings["devices"][board.board]["configuration"]["N_PIXELS"] * scale) - 1)
        y = np.copy(util.interpolate(y, config.settings["devices"][board.board]["configuration"]["N_PIXELS"] // 2))
        # Map color channels according to energy in the different freq bands
        # y = np.copy(util.interpolate(y, config.settings["devices"][board.board]["configuration"]["N_PIXELS"] // 2))
        diff = y - board.visualizer.prev_spectrum
        board.visualizer.prev_spectrum = np.copy(y)
        spectrum = np.copy(board.visualizer.prev_spectrum)
        spectrum = np.array([j for i in zip(spectrum, spectrum) for j in i])
        # Color channel mappings
        r = int(np.mean(spectrum[:len(spectrum) // 3] ** scale) *
                config.settings["devices"][board.board]["effect_opts"]["Energy"]["r_multiplier"])
        g = int(np.mean(spectrum[len(spectrum) // 3: 2 * len(spectrum) // 3] ** scale) *
                config.settings["devices"][board.board]["effect_opts"]["Energy"]["g_multiplier"])
        b = int(np.mean(spectrum[2 * len(spectrum) // 3:] ** scale) *
                config.settings["devices"][board.board]["effect_opts"]["Energy"]["b_multiplier"])

        # Assign color to different frequency regions and mix with scroll
        ratio = config.settings["devices"][board.board]["effect_opts"]["EnergyScroll"]["opacity"]

        if config.settings["devices"][board.board]["effect_opts"]["EnergyScroll"]["energy_on_top"]:
            board.visualizer.output[0, :r] = 255
            board.visualizer.output[0, r:] = ratio * scroll_output[0, r:]

            board.visualizer.output[1, :g] = 255
            board.visualizer.output[1, g:] = ratio * scroll_output[1, g:]

            board.visualizer.output[2, :b] = 255
            board.visualizer.output[2, b:] = ratio * scroll_output[2, b:]
        else:
            alphaChannel = np.maximum(np.maximum(scroll_output[0], scroll_output[1]), scroll_output[2])/255

            board.visualizer.output[0, :r] = \
                ((1 - ratio * alphaChannel[:r]) * 255 + ratio * alphaChannel[:r] * scroll_output[0, :r])
            board.visualizer.output[0, r:] = ratio * scroll_output[0, r:]

            board.visualizer.output[1, :g] = \
                ((1 - ratio * alphaChannel[:g]) * 255 + ratio * alphaChannel[:g] * scroll_output[1, :g])
            board.visualizer.output[1, g:] = ratio * scroll_output[1, g:]

            board.visualizer.output[2, :b] = \
                ((1 - ratio * alphaChannel[:b]) * 255 + ratio * alphaChannel[:b] * scroll_output[2, :b])
            board.visualizer.output[2, b:] = ratio * scroll_output[2, b:]

        # Apply blur to smooth the edges
        board.visualizer.output[0, :] = gaussian_filter1d(board.visualizer.output[0, :], sigma=
        config.settings["devices"][board.board]["effect_opts"]["Energy"]["blur"])
        board.visualizer.output[1, :] = gaussian_filter1d(board.visualizer.output[1, :], sigma=
        config.settings["devices"][board.board]["effect_opts"]["Energy"]["blur"])
        board.visualizer.output[2, :] = gaussian_filter1d(board.visualizer.output[2, :], sigma=
        config.settings["devices"][board.board]["effect_opts"]["Energy"]["blur"])
        if config.settings["devices"][board.board]["effect_opts"]["Energy"]["mirror"]:
            p = np.concatenate((board.visualizer.output[:, ::-2], board.visualizer.output[:, ::2]), axis=1)
        else:
            p = board.visualizer.output

        return p

    def visualize_scroll(self, board, y):
        y = y**4.0
        # signal_processers[board.board].gain.update(y)
        # y /= signal_processers[board.board].gain.value
        # y *= 255.0

        n_pixels = config.settings["devices"][board.board]["configuration"]["N_PIXELS"]
        y = np.copy(util.interpolate(y, n_pixels // 2))
        board.signalProcessor.common_mode.update(y)
        diff = y - board.visualizer.prev_spectrum
        board.visualizer.prev_spectrum = np.copy(y)
        # split spectrum up
        # r = signal_processers[board.board].r_filt.update(y - signal_processers[board.board].common_mode.value)
        # g = np.abs(diff)
        # b = signal_processers[board.board].b_filt.update(np.copy(y))
        y = np.clip(y, 0, 1)
        lows = y[:len(y) // 6]
        mids = y[len(y) // 6: 2 * len(y) // 5]
        high = y[2 * len(y) // 5:]
        # max values
        lows_max = np.max(lows)
        mids_max = float(np.max(mids))
        high_max = float(np.max(high))
        # indexes of max values
        # map to colour gradient
        lows_val = (np.array(config.settings["colors"][config.settings["devices"][board.board]["effect_opts"]["Scroll"]["lows_color"]]) * lows_max).astype(int)
        mids_val = (np.array(config.settings["colors"][config.settings["devices"][board.board]["effect_opts"]["Scroll"]["mids_color"]]) * mids_max).astype(int)
        high_val = (np.array(config.settings["colors"][config.settings["devices"][board.board]["effect_opts"]["Scroll"]["high_color"]]) * high_max).astype(int)
        # Scrolling effect window
        speed = config.settings["devices"][board.board]["effect_opts"]["Scroll"]["speed"]
        self.scroll_output[:, speed:] = self.scroll_output[:, :-speed]  # shift

        self.scroll_output = (self.scroll_output * config.settings["devices"][board.board]["effect_opts"]["Scroll"]["decay"]).astype(int)  # decay

        self.scroll_output = gaussian_filter1d(self.scroll_output, sigma=config.settings["devices"][board.board]["effect_opts"]["Scroll"]["blur"])  # blur

        # Create new color originating at the center
        self.scroll_output[0, :speed] = lows_val[0] + mids_val[0] + high_val[0]
        self.scroll_output[1, :speed] = lows_val[1] + mids_val[1] + high_val[1]
        self.scroll_output[2, :speed] = lows_val[2] + mids_val[2] + high_val[2]

        # Update the LED strip
        #return np.concatenate((vis.prev_spectrum[:, ::-speed], vis.prev_spectrum), axis=1)

        # if config.settings["devices"][board.board]["effect_opts"]["Scroll"]["mirror"]:
        #     p = np.concatenate((self.scroll_output[:, ::-2], self.scroll_output[:, ::2]), axis=1)
        # else:

        p = self.scroll_output

        if config.settings["devices"][board.board]["effect_opts"]["Scroll"]["flip_lr"]:
            p = np.fliplr(p)

        return p

