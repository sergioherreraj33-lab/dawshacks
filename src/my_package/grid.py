import pygame

class BackgroundGrid:
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size

    grid_color = ( 60, 60, 60)
    grid_spacing = 40

    def drawGrid(self, surface):
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(surface, self.grid_color, (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(surface, self.grid_color, (0, y), (self.width, y))