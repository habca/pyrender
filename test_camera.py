import unittest
from ddt import ddt, data, unpack
import numpy as np

from camera import Camera

@ddt
class CameraTest(unittest.TestCase):
    @data(
        ([0,0,1], [-1, -1, 0.0001], False),
        ([0,0,1], [1, -1, 0.0001], False),
        ([0,0,1], [-1, 1, 0.0001], False),
        ([0,0,1], [1, 1, 0.0001], False),

        ([0,0,1], [-1, -1, 0], False),
        ([0,0,1], [1, -1, 0], False),
        ([0,0,1], [-1, 1, 0], False),
        ([0,0,1], [1, 1, 0], False),

        ([0,0,1], [-1.0001, -1.0001, 0], False),
        ([0,0,1], [1.0001, -1.0001, 0], False),
        ([0,0,1], [-1.0001, 1.0001, 0], False),
        ([0,0,1], [1.0001, 1.0001, 0], False),

        ([0,0,1], [-1.0001, -1.0001, -0.0001], True),
        ([0,0,1], [1.0001, -1.0001, -0.0001], True),
        ([0,0,1], [-1.0001, 1.0001, -0.0001], True),
        ([0,0,1], [1.0001, 1.0001, -0.0001], True),

        ([0,0,1], [-1, -1, -0.0001], True),
        ([0,0,1], [1, -1, -0.0001], True),
        ([0,0,1], [-1, 1, -0.0001], True),
        ([0,0,1], [1, 1, -0.0001], True),

        ([0, 0, 3.16], [-1, -1, 1], True),
        ([0, 0, 3.16], [-1, 1, 1], True),
        ([0, 0, 3.16], [1, -1, 1], True),
    )
    @unpack
    def test_projection(self, cameraPosition: np.ndarray, worldPosition: np.ndarray, expected: bool):
        cameraPosition = np.array(cameraPosition)
        worldPosition = np.array(worldPosition)

        camera = Camera(cameraPosition)
        (hit, _, _) = camera.projection(worldPosition)
        
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
