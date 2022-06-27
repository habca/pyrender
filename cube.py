import math
import numpy as np

#     v6       v7
# v2   +----v3-+
#  +---|----+  |
#  |   |    |  |
#  |   |    |  |
#  |v4 +----|--+ v5
#  +--------+
# v0        v1
class Cube:
    def __init__(self, centerPosition: np.array, size: np.array):
        self.centerPosition = centerPosition
        self.size = size
        self.vertices = []

        self.eulerAngle = np.array([45, 45, 45])
        self.calculateVertices()
    
    def updateEulerAngle(self, eulerAngle: np.array) -> None:
        self.eulerAngle = eulerAngle
        self.calculateVertices()

    def calculateVertices(self) -> None:
        centerPosition = self.centerPosition
        size = self.size

        v0 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] - size[2] / 2])
        v1 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] - size[2] / 2])
        v2 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] - size[2] / 2])
        v3 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] - size[2] / 2])

        v4 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] + size[2] / 2])
        v5 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] + size[2] / 2])
        v6 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] + size[2] / 2])
        v7 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] + size[2] / 2])

        v0 = self.calculateVertex(v0)
        v1 = self.calculateVertex(v1)
        v2 = self.calculateVertex(v2)
        v3 = self.calculateVertex(v3)
        v4 = self.calculateVertex(v4)
        v5 = self.calculateVertex(v5)
        v6 = self.calculateVertex(v6)
        v7 = self.calculateVertex(v7)

        self.vertices = [v0, v1, v2, v3, v4, v5, v6, v7]

    def calculateVertex(self, vertex: np.array) -> np.array:
        vertex = self.centerPosition + RotateX(vertex - self.centerPosition, DegreesToRadians(self.eulerAngle[0]))
        vertex = self.centerPosition + RotateY(vertex - self.centerPosition, DegreesToRadians(self.eulerAngle[1]))
        vertex = self.centerPosition + RotateZ(vertex - self.centerPosition, DegreesToRadians(self.eulerAngle[2]))
        return vertex

    def get_vertices(self) -> list[np.array]:
        return self.vertices

    def get_triangles(self) -> list[int]:
        return [
            0, 2, 1, 2, 3, 1, 
            5, 6, 4, 5, 7, 6,
            4, 2, 0, 4, 6, 2, 
            1, 3, 5, 3, 7, 5,
            1, 4, 0, 1, 5, 4, 
            2, 6, 3, 6, 7, 3,
        ]

def DegreesToRadians(degrees: float) -> float:
    return degrees * (math.pi / 180)

def RadiansToDegrees(radians: float) -> float:
    return radians * (180 / math.pi)

def RotateX(direction: np.array, radians: float) -> np.array:
    return np.array([
        direction[0],
        direction[1] * math.cos(radians) -
        direction[2] * math.sin(radians),
        direction[1] * math.sin(radians) +
        direction[2] * math.cos(radians)
    ])

def RotateY(direction: np.array, radians: float) -> np.array:
    return np.array([
        direction[0] * math.cos(radians) +
        direction[2] * math.sin(radians),
        direction[1],
        -direction[0] * math.sin(radians) +
        direction[2] * math.cos(radians)
    ])

def RotateZ(direction: np.array, radians: float) -> np.array:
    return np.array([
        direction[0] * math.cos(radians) -
        direction[1] * math.sin(radians),
        direction[0] * math.sin(radians) +
        direction[1] * math.cos(radians),
        direction[2]
    ])
