import pygame
import numpy as np

from canvas import Canvas
from camera import Camera
from cube import Cube
import vector

class Application:
    def __init__(self):
        pygame.init()
        self.eulerAngle = [0,0,0]

        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 14)

        self.camera = Camera([0, 0, 5], [0, 0, -1])
        self.canvas = Canvas(self.camera, 640, 480)
        self.cube = Cube((0, 0, 0), (2, 2, 2))

    def run(self):
        ms = self.clock.tick(60)
        while True:
            self.events(ms)
            self.render(ms)

    def events(self, time: int):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

    def render(self, time: int):
        self.screen.fill((255, 255, 255))

        angle = np.array([0.5,0,0])
        self.eulerAngle += angle

        vertices = self.cube.get_vertices()
        triangles = self.cube.get_triangles()
        self.draw_triangles(vertices, triangles)

        pygame.display.flip()
        self.clock.tick(60)

    def draw_triangles(self, vertices: list[np.ndarray], triangles: list[int]) -> None:
        for i in range(len(triangles) // 3):
            v0 = vertices[triangles[i * 3 + 0]]
            v1 = vertices[triangles[i * 3 + 1]]
            v2 = vertices[triangles[i * 3 + 2]]
            
            v0 = vector.rotate(v0, self.cube.centerPosition, self.eulerAngle)
            v1 = vector.rotate(v1, self.cube.centerPosition, self.eulerAngle)
            v2 = vector.rotate(v2, self.cube.centerPosition, self.eulerAngle)

            # self.camera.cameraPosition[2] += 0.1

            px0 = self.canvas.perspectiveProject(v0)
            px1 = self.canvas.perspectiveProject(v1)
            px2 = self.canvas.perspectiveProject(v2)

            color = pygame.Color(255, 0, 0)
            normal = vector.normal(v0, v1, v2)
            if self.camera.visibleSurface(v0, normal):
                color = pygame.Color(0, 0, 0)
            
            pygame.draw.polygon(self.screen, color, (px0, px1, px2), 2)

if __name__ == "__main__":
    Application().run()
