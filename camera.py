import math
import numpy as np

class Camera:
    def __init__(self, cameraPosition: np.ndarray, cameraDirection: np.ndarray):
        self.cameraPosition = cameraPosition
        self.cameraDirection = cameraDirection

    def visibleSurface(self, point: np.ndarray, normal: np.ndarray) -> bool:
        """
        The surface is visible when the distance to the camera is positive.
        """
        return np.dot(normal, np.subtract(point, self.cameraPosition)) > 0
