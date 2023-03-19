import math
import numpy as np

class Camera:
    def __init__(self, cameraPosition: np.ndarray, cameraDirection: np.ndarray):
        self.cameraPosition = cameraPosition
        self.cameraDirection = cameraDirection

    