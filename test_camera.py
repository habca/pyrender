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
        worldPoint = np.array([x, y, z])

        camera = Camera(cameraPosition)
        (hit, _, _) = camera.projection(worldPoint)
        
        self.assertEqual(expected, hit)

    def test_rotate_orbit_zero_angle(self):
        cameraPosition = np.array([0,0,3])
        camera = Camera(cameraPosition)
        camera.rotate_orbit(0, 0)

        np.testing.assert_almost_equal([0,0,3], camera.cameraPosition)

    """
    def test_rotate_orbit_full_circle(self):
        cameraPosition = np.array([0,0,3])
        camera = Camera(cameraPosition)
        camera.rotate_orbit(360, 360)

        np.testing.assert_almost_equal([0,0,3], camera.cameraPosition)

    def test_rotate_orbit_between_axis(self):
        cameraPosition = np.array([0,0,3])
        camera = Camera(cameraPosition)
        camera.rotate_orbit(-90, 0)

        np.testing.assert_almost_equal([0,3,0], camera.cameraPosition)

        cameraPosition = np.array([0,0,3])
        camera = Camera(cameraPosition)
        camera.rotate_orbit(0, 90)

        np.testing.assert_almost_equal([3,0,0], camera.cameraPosition)
    """

if __name__ == "__main__":
    unittest.main()
