import pygame
from src.my_package.views.menu_screen import MenuScreen
from src.my_package.views.timed_screen import TimedScreen
from src.my_package.views.sandbox_screen import SandboxScreen

pygame.init()

# Create the main display and a clock to cap the frame rate.
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

# Start on the main menu screen.
current_screen = MenuScreen(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Forward events to the current screen and respond to navigation results.
        result = current_screen.handle_event(event)

        if result == "timed":
            current_screen = TimedScreen()
        if result == "sandbox":
            current_screen = SandboxScreen()
        if result == "menu":
            current_screen = MenuScreen(screen)

    # Draw the active screen and update the display.
    current_screen.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
