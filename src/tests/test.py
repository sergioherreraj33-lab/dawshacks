import pygame
import sys
import math

from src.my_package import grid

pygame.init()

#(1280, 720)
screen_w = 1400
screen_h = 900

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Bridge Builder")
clock = pygame.time.Clock()

# Array to hold nodes and beams
nodes = []

# for x in range(300, 1200, 100):
#     for y in range(450, 900, 100):
#         nodes.append((x, y))

num_nodes_x = 9
num_nodes_y = 5
spacing_x = 100
spacing_y = 60  
bottom_gap = 50

total_width = (num_nodes_x - 1) * spacing_x
start_x = (screen_w - total_width) // 2


total_height = (num_nodes_y - 1) * spacing_y
start_y = (screen_h - bottom_gap) - total_height

nodes = []
for i in range(num_nodes_x):
    for j in range(num_nodes_y):
        x = start_x + (i * spacing_x)
        y = start_y + (j * spacing_y)
        nodes.append((x, y))

beams = []
selected_node = None

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
                #Pythagorean theorem
                distance = math.dist(node, pos)
                if distance < 12:
                    clicked_node = node
                    break

            if clicked_node:
                if selected_node is None:
                    selected_node = clicked_node
                else:
                    beams.append((selected_node, clicked_node))
                    selected_node = None

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