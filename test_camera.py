import unittest
import numpy as np

from camera import Camera

class CameraTest(unittest.TestCase):
    def test_perspective_project_origin(self):
        cameraPosition = [0,0,1]
        cameraDirection = [0,0,-1]
        worldCoordinates = [0,0,0]
        
        camera = Camera(cameraPosition, cameraDirection)
        screenCoordinates = camera.perspectiveProject(worldCoordinates)

        self.assertTrue(np.array_equal([320,240], screenCoordinates))

    def test_perspective_project(self):
        """
        When the camera direction is orthogonal to a 3D vector,
        the 2D vector should be in the centre of the image.
        """
        cameraPosition = [10, 15, 5]
        cameraDirection = [0, 0, -1]
        worldCoordinates = [10, 15, -5]

        camera = Camera(cameraPosition, cameraDirection)
        screenCoordinates = camera.perspectiveProject(worldCoordinates)

        np.testing.assert_almost_equal([320, 240], screenCoordinates)

    def test_camera_space(self):
        """ 
        When the camera position and orientation are null vectors,
        the 3D vector (1,2,0) should be projected to the 2D vector (1,2).
        """
        cameraPosition = np.array([1, 2, 3])
        cameraDirection = np.array([0, 0, 0])
        worldCoordinates = np.array([1, 2, 3])

        camera = Camera(cameraPosition, cameraDirection)
        cameraCoordinates = camera.cameraSpace(worldCoordinates)

        self.assertEqual(0, cameraCoordinates[0])
        self.assertEqual(0, cameraCoordinates[1])

    def test_screen_space(self):
        """
        The camera position should be in the origin of the camera space.
        """
        cameraPosition = np.array([0, 0, 0])
        cameraDirection = np.array([0, 0, 0])
        worldCoordinates = np.array([1, 2, 0])

        camera = Camera(cameraPosition, cameraDirection)
        cameraCoordinates = camera.cameraSpace(worldCoordinates)
        screenCoordinates = camera.screenSpace(cameraCoordinates)

        self.assertEqual(1, screenCoordinates[0])
        self.assertEqual(2, screenCoordinates[1])

if __name__ == "__main__":
    unittest.main()
