import math
import numpy as np

from camera import Camera

class Canvas: 
    def __init__(self, camera: Camera, pixelWidth: int, pixelHeight: int):
        self.pixelWidth = pixelWidth
        self.pixelHeight = pixelHeight
        self.camera = camera
    
    def perspectiveProject(self, worldCoordinates: np.ndarray) -> np.ndarray:
        """
        Convert a 3D world position into a 2D screen pixel.
        """
        cameraCoordinates = self.cameraSpace(worldCoordinates)
        screenCoordinates = self.screenSpace(cameraCoordinates)
        normalCoordinates = self.normalSpace(screenCoordinates)
        rasterCoordinates = self.rasterSpace(normalCoordinates, self.pixelWidth, self.pixelHeight)
        return rasterCoordinates
    
    def cameraSpace(self, worldCoordinates: np.ndarray) -> np.ndarray:
        """
        The space where 3D points are defined using the camera coordinate system.
        """
        cameraPosition = self.camera.cameraPosition
        cameraCoordinateX = worldCoordinates[0] - cameraPosition[0]
        cameraCoordinateY = worldCoordinates[1] - cameraPosition[1]
        cameraCoordinateZ = worldCoordinates[2] - cameraPosition[2]

        # ZeroDivisionError
        if cameraCoordinateZ == 0:
            cameraCoordinateZ = 1

        return np.array([cameraCoordinateX, cameraCoordinateY, cameraCoordinateZ])

    def screenSpace(self, cameraCoordinates: np.ndarray) -> np.ndarray:
        """
        The space where 2D points lie in the infinite image plane.
        """
        screenCoordinateX = cameraCoordinates[0] / cameraCoordinates[2]
        screenCoordinateY = cameraCoordinates[1] / cameraCoordinates[2]
        return np.array([screenCoordinateX, screenCoordinateY])

    def normalSpace(self, screenCoordinates: np.ndarray) -> np.ndarray:
        normalCoordinateX = 0.5 + screenCoordinates[0]
        normalCoordinateY = 0.5 + screenCoordinates[1]
        return np.array([normalCoordinateX, normalCoordinateY])

    def rasterSpace(self, normalCoordinates: np.ndarray, pixelWidth: int, pixelHeight: int) -> np.ndarray:
        # y-coordinate points down in raster images.
        rasterCoordinateX = math.floor(normalCoordinates[0] * pixelWidth)
        rasterCoordinateY = math.floor((1 - normalCoordinates[1]) * pixelHeight)
        return np.array([rasterCoordinateX, rasterCoordinateY])

    def visibleSurface(self, point: np.ndarray, normal: np.ndarray) -> bool:
        """
        The surface is visible when the distance to the camera is positive.
        """
        return np.dot(normal, np.subtract(point, self.camera.cameraPosition)) > 0
