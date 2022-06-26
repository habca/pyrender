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
        self.eulerAngle = np.array([0, 0, 0])
        self.calculateVertices()
    
    def updateEulerAngle(self, eulerAngle: np.array) -> None:
        self.eulerAngle = eulerAngle
        self.calculateVertices()

    def calculateVertices(self) -> None:
        centerPosition = self.centerPosition
        size = self.size

        self.v0 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] - size[2] / 2])
        self.v1 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] - size[2] / 2])
        self.v2 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] - size[2] / 2])
        self.v3 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] - size[2] / 2])

        self.v4 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] + size[2] / 2])
        self.v5 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] + size[2] / 2])
        self.v6 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] + size[2] / 2])
        self.v7 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] + size[2] / 2])

        self.v0 = centerPosition + RotateX(self.v0 - centerPosition, DegreesToRadians(self.eulerAngle[0]))
        self.v0 = centerPosition + RotateY(self.v0 - centerPosition, DegreesToRadians(self.eulerAngle[1]))
        self.v0 = centerPosition + RotateZ(self.v0 - centerPosition, DegreesToRadians(self.eulerAngle[2]))

        self.v1 = centerPosition + RotateX(self.v1 - centerPosition, DegreesToRadians(self.eulerAngle[0]))
        self.v1 = centerPosition + RotateY(self.v1 - centerPosition, DegreesToRadians(self.eulerAngle[1]))
        self.v1 = centerPosition + RotateZ(self.v1 - centerPosition, DegreesToRadians(self.eulerAngle[2]))

        self.v2 = centerPosition + RotateX(self.v2 - centerPosition, DegreesToRadians(self.eulerAngle[0]))
        self.v2 = centerPosition + RotateY(self.v2 - centerPosition, DegreesToRadians(self.eulerAngle[1]))
        self.v2 = centerPosition + RotateZ(self.v2 - centerPosition, DegreesToRadians(self.eulerAngle[2]))

        self.v3 = centerPosition + RotateX(self.v3 - centerPosition, DegreesToRadians(self.eulerAngle[0]))
        self.v3 = centerPosition + RotateY(self.v3 - centerPosition, DegreesToRadians(self.eulerAngle[1]))
        self.v3 = centerPosition + RotateZ(self.v3 - centerPosition, DegreesToRadians(self.eulerAngle[2]))

        self.v4 = centerPosition + RotateX(self.v4 - centerPosition, DegreesToRadians(self.eulerAngle[0]))
        self.v4 = centerPosition + RotateY(self.v4 - centerPosition, DegreesToRadians(self.eulerAngle[1]))
        self.v4 = centerPosition + RotateZ(self.v4 - centerPosition, DegreesToRadians(self.eulerAngle[2]))

        self.v5 = centerPosition + RotateX(self.v5 - centerPosition, DegreesToRadians(self.eulerAngle[0]))
        self.v5 = centerPosition + RotateY(self.v5 - centerPosition, DegreesToRadians(self.eulerAngle[1]))
        self.v5 = centerPosition + RotateZ(self.v5 - centerPosition, DegreesToRadians(self.eulerAngle[2]))

        self.v6 = centerPosition + RotateX(self.v6 - centerPosition, DegreesToRadians(self.eulerAngle[0]))
        self.v6 = centerPosition + RotateY(self.v6 - centerPosition, DegreesToRadians(self.eulerAngle[1]))
        self.v6 = centerPosition + RotateZ(self.v6 - centerPosition, DegreesToRadians(self.eulerAngle[2]))

        self.v7 = centerPosition + RotateX(self.v7 - centerPosition, DegreesToRadians(self.eulerAngle[0]))
        self.v7 = centerPosition + RotateY(self.v7 - centerPosition, DegreesToRadians(self.eulerAngle[1]))
        self.v7 = centerPosition + RotateZ(self.v7 - centerPosition, DegreesToRadians(self.eulerAngle[2]))

    def get_line_loops(self) -> list[list[np.array]]:
        return [
            [self.v0, self.v1, self.v3, self.v2, self.v0],
            [self.v4, self.v5, self.v7, self.v6, self.v4],
        ]
    
    def get_lines(self) -> list[tuple[np.array]]:
        return [
            (self.v0, self.v4),
            (self.v1, self.v5),
            (self.v2, self.v6),
            (self.v3, self.v7),
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
