import pygame, pymunk, sys

# --- PHYSICS CREATION FUNCTIONS ---

def create_circle(space, pos):
    # mass, moment of inertia (how hard it is to spin)
    body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC) 
    body.position = pos
    shape = pymunk.Circle(body, 40) # Radius 40
    shape.elasticity = 0.8  # Makes it bouncy
    shape.friction = 0.5
    space.add(body, shape)
    return shape

def create_ledge(space, pos, size):
    # Static bodies don't move and don't need mass
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = 0.8
    shape.friction = 0.5
    space.add(body, shape)
    return shape

# --- DRAWING FUNCTIONS ---

def draw_objects(circles, ledges):
    # Draw Circles
    for circle in circles:
        pos_x = int(circle.body.position.x)
        pos_y = int(circle.body.position.y)
        # Match radius to physics (40)
        pygame.draw.circle(screen, "black", (pos_x, pos_y), 40)

    # Draw Ledges
    for ledge in ledges:
        pos_x = int(ledge.body.position.x)
        pos_y = int(ledge.body.position.y)
        # size was (400, 50). We subtract half to center the rect.
        pygame.draw.rect(screen, "black", (pos_x - 200, pos_y - 25, 400, 50))

# --- MAIN SETUP ---

pygame.init()
width, height = 1280, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# Pymunk Space
space = pymunk.Space()
space.gravity = (0, 900) 

# Lists to hold our objects
circles = []
ledges = []

# Create the Ledges (400x50)
# Left Ledge: centered at x=200 so it starts at 0
ledges.append(create_ledge(space, (200, 540), (400, 50)))
ledges.append(create_ledge(space, (1720, 540), (400, 50)))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            circles.append(create_circle(space, event.pos))

    space.step(1/50)

    screen.fill("white")
    draw_objects(circles, ledges)
    
    pygame.display.flip()
    clock.tick(60)