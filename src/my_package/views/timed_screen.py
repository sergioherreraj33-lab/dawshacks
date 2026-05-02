import pygame
from src.my_package import grid

class TimedScreen:
    def __init__(self):
        self.grid = grid.BackgroundGrid(1280, 720, 40)

    def handle_event(self, event):
        pass

    def draw(self, screen):
        screen.fill((30, 30, 30))
        self.grid.drawGrid(screen)