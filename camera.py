import math
import numpy as np

import vector

class Camera:
    def __init__(self, cameraPosition: np.ndarray, cameraDirection: np.ndarray):
        self.cameraPosition = cameraPosition
        self.cameraDirection = cameraDirection

    def dimensions(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        forward = np.array(self.cameraDirection)
        up = np.array([0,1,0])
        right = np.cross(forward, up)
        right = vector.normalize(right)
        up = np.cross(right, forward)
        up = vector.normalize(up)
        center = np.add(self.cameraPosition, forward)

        return (forward, right, up, center)
    
    def boundaries(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        (forward, right, up, center) = self.dimensions()

        v0 = center - right - up
        v1 = center + right - up
        v2 = center - right + up
        v3 = center + right + up

        return (v0, v1, v2, v3)

    def projection(self, worldPosition: np.ndarray
        ) -> tuple[bool, float, np.ndarray]:
        
        ray_origin = np.array(worldPosition)
        ray_direction = np.subtract(self.cameraPosition, worldPosition)
        ray_direction = vector.normalize(ray_direction)

        (forward, right, up, center) = self.dimensions()
        (v0, v1, v2, v3) = self.boundaries()

        # Reverse triangle vertices for ray casting because
        # otherwise triangle normals point towards the camera.
        (hit, hitDistance, hitPoint) = vector.intersect_quad(
            ray_origin, ray_direction, v0, v2, v1, v3
        )

        # There is neither intersection nor distance.
        if not hit: return (hit, hitDistance, hitPoint)

        # Forward vector should zero out on projection.
        normalized = np.subtract(hitPoint, center)

        normal_width = (1 + np.dot(right, normalized)) / 2 # [0,1]
        normal_height = (1 + np.dot(up, normalized)) / 2 # [0,1]

        pixel_width = 640
        pixel_height = 480

        pixel_x = math.floor(normal_width * pixel_width)
        pixel_y = math.floor((1 - normal_height) * pixel_height)

        hitPoint = np.array([pixel_x, pixel_y])

        return (hit, hitDistance, hitPoint)

    def visible_surface(self, point: np.ndarray, normal: np.ndarray) -> bool:
        """
        The surface is visible when the distance along camera vision is positive.
        """
        return np.dot(normal, np.subtract(point, self.cameraPosition)) > 0
