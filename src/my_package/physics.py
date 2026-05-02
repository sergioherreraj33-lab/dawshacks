import pygame
import pymunk
import sys

WIDTH, HEIGHT = 1280, 800
CIRCLE_RADIUS = 40
LEDGE_W = 200
LEDGE_H = 550

def create_circle(space, pos):
    body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC) 
    body.position = pos
    shape = pymunk.Circle(body, CIRCLE_RADIUS)
    shape.elasticity = 0.5 
    space.add(body, shape)
    return shape

def create_ledge(space, pos, size):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    space.add(body, shape)
    return shape

def draw_objects(screen, circles, ledges):
    # THIS IS CIRCLES 
    for circle in circles:
        pos_x = int(circle.body.position.x)
        pos_y = int(circle.body.position.y)
        pygame.draw.circle(screen, "blue", (pos_x, pos_y), CIRCLE_RADIUS)

    # THIS IS THE LEDGE 
    for ledge in ledges:
        pos_x = int(ledge.body.position.x)
        pos_y = int(ledge.body.position.y)
        
    
        draw_x = pos_x - (LEDGE_W / 2)
        draw_y = pos_y - (LEDGE_H / 2)
        pygame.draw.rect(screen, "lightgreen", (draw_x, draw_y, LEDGE_W, LEDGE_H))


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

space = pymunk.Space()
space.gravity = (0, 900) 

# empty arrays to keep the shapes for drawing
circles = []
ledges = []

left_ledge_pos = (LEDGE_W / 2, 540)
ledges.append(create_ledge(space, left_ledge_pos, (LEDGE_W, LEDGE_H)))

right_ledge_pos = (WIDTH - (LEDGE_W / 2), 540)
ledges.append(create_ledge(space, right_ledge_pos, (LEDGE_W, LEDGE_H)))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            circles.append(create_circle(space, event.pos))

    space.step(1/60)

    screen.fill("white")
        
    draw_objects(screen, circles, ledges)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()