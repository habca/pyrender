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

        for start, end in self.scene.kuutio.get_lines():
            start = tuple(self.camera.perspectiveProject(start))
            end = tuple(self.camera.perspectiveProject(end))
            pygame.draw.line(self.screen, (0, 0, 0), start, end)

        for line_loop in self.scene.kuutio.get_line_loops():
            points = []
            for start in line_loop:
                start = tuple(self.camera.perspectiveProject(start))
                points.append(start)
            pygame.draw.polygon(self.screen, (0, 0, 0), points, 1)

        pygame.display.flip()
        self.clock.tick(60)

class Scene:
    def __init__(self):
        self.kuutio = Cube((0, 0, 0), (2, 2, 2))

if __name__ == "__main__":
    sovellus = Sovellus()
    sovellus.suorita()
