import pygame, pymunk, sys

def create_circle(space, pos):
    body = pymunk.Body(1, 100, body_type= pymunk.Body.DYNAMIC) # mass, inertia
    body.position = pos
    shape = pymunk.Circle(body, 40) # body, radius
    space.add(body, shape)
    return shape

def draw_circle(circles):
    for circle in circles:
        pos_x = int(circle.body.position.x)
        pos_y =  int(circle.body.position.y)
        pygame.draw.circle(screen, "black", (pos_x, pos_y), 80)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
space = pymunk.Space() # create a physics space with pymunk
space.gravity = (0, 900) 

circles = [] # empty array for the circles 
sticks = [] # empty array for the sticks 
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            circles.append(create_circle(space, event.pos))


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    draw_circle(circles)
    space.step(1/50) # this is the physics speed  --> 50 steps per second


    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_w]:
    #     player_pos.y -= 300 * dt
    # if keys[pygame.K_s]:
    #     player_pos.y += 300 * dt
    # if keys[pygame.K_a]:
    #     player_pos.x -= 300 * dt
    # if keys[pygame.K_d]:
    #     player_pos.x += 300 * dt

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60) / 1000

pygame.quit()