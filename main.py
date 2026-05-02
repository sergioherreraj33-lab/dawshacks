import pygame
from src.my_package.views.menu_screen import MenuScreen
from src.my_package.views.timed_screen import TimedScreen
from src.my_package.views.sandbox_screen import SandboxScreen

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
            current_screen = TimedScreen()
        if result == "sandbox":
            current_screen = SandboxScreen()

    current_screen.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()