import pygame
from src.my_package import grid

class SandboxScreen:
    def __init__(self):
        self.grid = grid.BackgroundGrid(1280, 720, 40)
        self.nodes = []
        self.beams = []
        self.selected_node = None

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            clicked_node = None

            for node in self.nodes:
                distance = ((node[0] - pos[0]) ** 2 + (node[1] - pos[1]) ** 2) ** 0.5
                if distance < 12:
                    clicked_node = node
                    break

            if clicked_node:
                if self.selected_node is None:
                    self.selected_node = clicked_node
                else:
                    self.beams.append((self.selected_node, clicked_node))
                    self.selected_node = None
            else:
                self.nodes.append(pos)

    def draw(self, screen):
        screen.fill((30, 30, 30))
        self.grid.drawGrid(screen)
        for beam in self.beams:
            pygame.draw.line(screen, (255, 255, 255), beam[0], beam[1], 2)
        for node in self.nodes:
            pygame.draw.circle(screen, (0, 200, 255), node, 6)
        if self.selected_node is not None:
            pygame.draw.circle(screen, (255, 255, 0), self.selected_node, 10, 2)
            