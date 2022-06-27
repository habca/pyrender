import pygame
import numpy as np

from camera import Camera
from cube import Cube

class Sovellus:
    def __init__(self):
        pygame.init()
        self.width = 640
        self.height = 480

        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 14)
        
        self.scene = Scene()
        self.camera = Camera(np.array([0, 0, 5]), np.array([0, 0, -1]))

    def suorita(self):
        ms = self.clock.tick(60)
        while True:
            self.tapahtumat(ms)
            self.render()

    def tapahtumat(self, deltaTime: int):
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.QUIT:
                exit()

    def render(self):
        self.screen.fill((255, 255, 255))

        kulma = self.scene.kuutio.eulerAngle
        kulma = kulma + np.array([0.1, 0.1, 0.1])
        self.scene.kuutio.updateEulerAngle(kulma)

        vertices = self.scene.kuutio.get_vertices()
        triangles = self.scene.kuutio.get_triangles()
        self.draw_triangles(vertices, triangles)

        pygame.display.flip()
        self.clock.tick(60)

    def draw_triangles(self, vertices: list[np.array], triangles: list[int]) -> None:
        for i in range(len(triangles) // 3):
            v0 = self.camera.perspectiveProject(vertices[triangles[i * 3]])
            v1 = self.camera.perspectiveProject(vertices[triangles[i * 3 + 1]])
            v2 = self.camera.perspectiveProject(vertices[triangles[i * 3 + 2]])
            pygame.draw.polygon(self.screen, (0, 0, 0), (v0, v1, v2), 1)

class Scene:
    def __init__(self):
        self.kuutio = Cube((0, 0, 0), (2, 2, 2))

if __name__ == "__main__":
    sovellus = Sovellus()
    sovellus.suorita()
