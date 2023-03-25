import unittest
from ddt import ddt, data, unpack
import numpy as np

from camera import Camera

@ddt
class CameraTest(unittest.TestCase):
    @data(
        (-1, -1, 0.0001, False),
        (1, -1, 0.0001, False),
        (-1, 1, 0.0001, False),
        (1, 1, 0.0001, False),

        (-1, -1, 0, True),
        (1, -1, 0, True),
        (-1, 1, 0, True),
        (1, 1, 0, True),

        (-1.0001, -1.0001, 0, False),
        (1.0001, -1.0001, 0, False),
        (-1.0001, 1.0001, 0, False),
        (1.0001, 1.0001, 0, False),

        (-1.0001, -1.0001, -0.0001, True),
        (1.0001, -1.0001, -0.0001, True),
        (-1.0001, 1.0001, -0.0001, True),
        (1.0001, 1.0001, -0.0001, True),
    )
    @unpack
    def test_projection(self, x: float, y: float, z: float, expected: bool):
        cameraPosition = np.array([0,0,1])
        cameraDirection = np.array([0,0,-1])
        worldPoint = np.array([x, y, z])

        camera = Camera(cameraPosition)
        (hit, _, _) = camera.projection(worldPoint)
        
        self.assertEqual(expected, hit)

if __name__ == "__main__":
    unittest.main()
