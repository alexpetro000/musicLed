from scipy.ndimage.filters import gaussian_filter1d
import numpy as np
import config  as config
import util


from effects.effect import Effect

class Gradient(Effect):
    nonReactive = True
    def __init__(self, visualizer):
        self.effectName = "Gradient"
        self.configProps = [
            ["color_mode", "Color Mode", "dropdown", config.settings["gradients"], "Spectral"],
            ["roll_speed", "Roll Speed", "slider", (0, 8, 1), 0],
            ["mirror", "Mirror", "checkbox", False],
            ["fast", "Fast", "checkbox", False],
            ["reverse", "Reverse", "checkbox", False]
        ]

    def visualize(self, board, y):
        output = np.array([
            board.visualizer.multicolor_modes[board.effectConfig["Gradient"]["color_mode"]][0][:board.config["N_PIXELS"]],
            board.visualizer.multicolor_modes[board.effectConfig["Gradient"]["color_mode"]][1][:board.config["N_PIXELS"]],
            board.visualizer.multicolor_modes[board.effectConfig["Gradient"]["color_mode"]][2][:board.config["N_PIXELS"]]
        ])

        board.visualizer.multicolor_modes[board.effectConfig["Gradient"]["color_mode"]] = np.roll(
            board.visualizer.multicolor_modes[board.effectConfig["Gradient"]["color_mode"]],
            board.effectConfig["Gradient"]["roll_speed"]*(-1 if board.effectConfig["Gradient"]["reverse"] else 1),
            axis=1
        )
        
        if board.effectConfig["Gradient"]["mirror"]:
            output = np.concatenate((output[:, ::-2], output[:, ::2]), axis=1)
        return output




    