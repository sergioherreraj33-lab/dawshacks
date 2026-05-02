import pygame
import sys

from src.my_package import grid

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Bridge Builder")
clock = pygame.time.Clock()

# Array to hold nodes and beams
nodes = []
beams = []
# Variable to track the currently selected node for beam creation
selected_node = None

# Create a BackgroundGrid object
grid_obj = grid.BackgroundGrid(screen.get_width(), screen.get_height(), 40)

# Game will run until the user closes the window
running = True

while running:
    screen.fill((30, 30, 30))
    grid_obj.drawGrid(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #get the position of the mouse click and check if it's on an existing node
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            clicked_node = None

            for node in nodes:
                distance = ((node[0] - pos[0]) ** 2 + (node[1] - pos[1]) ** 2) ** 0.5
                if distance < 12:
                    clicked_node = node
                    break

            if clicked_node:
                if selected_node is None:
                    selected_node = clicked_node
                else:
                    beams.append((selected_node, clicked_node))
                    selected_node = None
            else:
                nodes.append(pos)

    for beam in beams:
        pygame.draw.line(screen, (255, 255, 255), beam[0], beam[1], 2)

    for node in nodes:
        pygame.draw.circle(screen, (0, 200, 255), node, 6)

    if selected_node is not None:
        pygame.draw.circle(screen, (255, 255, 0), selected_node, 10, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()