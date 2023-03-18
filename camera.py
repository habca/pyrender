import math
import numpy as np

import vector

class Camera:
    def __init__(self, cameraPosition: np.ndarray, cameraDirection: np.ndarray):
        self.cameraPosition = cameraPosition
        self.cameraDirection = cameraDirection
        self.screenPosition = np.array([0, 0, 1])

    def perspectiveProject(self, worldCoordinates: np.ndarray) -> np.ndarray:
        """
        Convert a 3D world position into a 2D screen pixel.
        """
        cameraCoordinates = self.cameraSpace(worldCoordinates)
        screenCoordinates = self.screenSpace(cameraCoordinates)
        normalCoordinates = self.normalSpace(screenCoordinates)
        rasterCoordinates = self.rasterSpace(normalCoordinates, 640, 480)
        return rasterCoordinates
        
    def cameraSpace(self, worldCoordinates: np.ndarray) -> np.ndarray:
        """
        The space where 3D points are defined using the camera coordinate system.
        """
        x = worldCoordinates[0] - self.cameraPosition[0]
        y = worldCoordinates[1] - self.cameraPosition[1]
        z = worldCoordinates[2] - self.cameraPosition[2]

        # cx = math.cos(self.cameraDirection[0])
        # cy = math.cos(self.cameraDirection[1])
        # cz = math.cos(self.cameraDirection[2])

        # sx = math.sin(self.cameraDirection[0])
        # sy = math.sin(self.cameraDirection[1])
        # sz = math.sin(self.cameraDirection[2])

        # cameraCoordinateX = cy*(sz*y + cz*x) - sy*z
        # cameraCoordinateY = sx*(cy*z + sy*(sz*y + cz*x)) + cx*(cz*y - sz*x)
        # cameraCoordinateZ = cx*(cy*z + sy*(sz*y + cz*x)) - sx*(cz*y - sz*x)
        cameraCoordinateX = x 
        cameraCoordinateY = y
        cameraCoordinateZ = z

        # ZeroDivisionError
        if cameraCoordinateZ == 0:
            cameraCoordinateZ = 1

        return np.array([cameraCoordinateX, cameraCoordinateY, cameraCoordinateZ])

    def screenSpace(self, cameraCoordinates: np.ndarray) -> np.ndarray:
        """
        The space where 2D points lie in the infinite image plane.
        """
        screenCoordinateX = (self.screenPosition[2]/cameraCoordinates[2])*cameraCoordinates[0] + self.screenPosition[0]
        screenCoordinateY = (self.screenPosition[2]/cameraCoordinates[2])*cameraCoordinates[1] + self.screenPosition[1]
        return np.array([screenCoordinateX, screenCoordinateY])

    def normalSpace(self, screenCoordinates: np.ndarray) -> np.ndarray:
        canvasWidth = 2
        canvasHeight = 2

        normalCoordinateX = (screenCoordinates[0] + canvasWidth/2) / canvasWidth
        normalCoordinateY = (screenCoordinates[1] + canvasHeight/2) / canvasHeight
        return np.array([normalCoordinateX, normalCoordinateY])

    def rasterSpace(self, normalCoordinates: np.ndarray, pixelWidth: int, pixelHeight: int) -> np.ndarray:
        # y-coordinate points down in raster images.
        rasterCoordinateX = math.floor(normalCoordinates[0] * pixelWidth)
        rasterCoordinateY = math.floor((1 - normalCoordinates[1]) * pixelHeight)
        return np.array([rasterCoordinateX, rasterCoordinateY])
