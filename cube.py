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
    def __init__(self, centerPosition: np.ndarray, size: np.ndarray):
        self.centerPosition = centerPosition
        self.size = size

    def get_vertices(self) -> list[np.ndarray]:
        return self.__calculateVertices(self.centerPosition, self.size)

    def __calculateVertices(self, centerPosition: np.ndarray, size: np.ndarray) -> list[np.ndarray]:
        v0 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] - size[2] / 2])
        v1 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] - size[2] / 2])
        v2 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] - size[2] / 2])
        v3 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] - size[2] / 2])

        v4 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] + size[2] / 2])
        v5 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] - size[1] / 2, centerPosition[2] + size[2] / 2])
        v6 = np.array([centerPosition[0] - size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] + size[2] / 2])
        v7 = np.array([centerPosition[0] + size[0] / 2, centerPosition[1] + size[1] / 2, centerPosition[2] + size[2] / 2])

        return [v0, v1, v2, v3, v4, v5, v6, v7]

    def get_triangles(self) -> list[int]:
        return [
            0, 1, 2, 3, 2, 1, 
            7, 5, 6, 4, 6, 5,
            4, 0, 6, 2, 6, 0,
            5, 1, 7, 3, 7, 1,
            2, 3, 6, 7, 6, 3, 
            5, 1, 4, 0, 4, 1,
        ]
