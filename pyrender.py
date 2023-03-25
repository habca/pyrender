import pygame
import numpy as np

from canvas import Canvas
from camera import Camera
from cube import Cube
from controller import Controller
import vector

class Application:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 14)

        self.controller = Controller()
        self.camera = Camera([0, 0, 3])
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.controller.mouse_button_down(pygame.mouse.get_pos())
            if event.type == pygame.MOUSEBUTTONUP:
                self.controller.mouse_button_up()
            if event.type == pygame.MOUSEMOTION:
                self.controller.mouse_motion(pygame.mouse.get_pos(), time)

    def render(self, time: int):
        self.screen.fill((255, 255, 255))

        vertices = self.cube.get_vertices()
        triangles = self.cube.get_triangles()
        
        (rx, ry) = self.controller.get_frame_update()
        self.camera.rotate_orbit(rx, ry)
        self.draw_triangles(vertices, triangles)

        pygame.display.flip()
        self.clock.tick(60)

    def draw_triangles(self, vertices: list[np.ndarray], triangles: list[int]) -> None:
        for i in range(len(triangles) // 3):
            v0 = vertices[triangles[i * 3 + 0]]
            v1 = vertices[triangles[i * 3 + 1]]
            v2 = vertices[triangles[i * 3 + 2]]

            (_, _, px0) = self.camera.projection(v0)
            (_, _, px1) = self.camera.projection(v1)
            (_, _, px2) = self.camera.projection(v2)

            color = pygame.Color(255, 0, 0)
            normal = vector.normal(v0, v1, v2)
            if self.camera.visible_surface(v0, normal):
                color = pygame.Color(0, 0, 0)
            
            pygame.draw.polygon(self.screen, color, (px0, px1, px2), 2)

if __name__ == "__main__":
    Application().run()
