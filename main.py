import pygame
from src.my_package.views.menu_screen import MenuScreen

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

current_screen = MenuScreen(screen)

running = True
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        result = current_screen.handle_event(event)

        if result == "timed":
            print("Load Timed Screen")

        elif result == "sandbox":
            print("Load Sandbox Screen")

    current_screen.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()