import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

current_screen = "mode select"


# Fonts
title_font = pygame.font.SysFont(None, 64)
button_font = pygame.font.SysFont(None, 48)

# Title text
title_surface = title_font.render("Mode Selection", True, "white")
title_rect = title_surface.get_rect(center=(screen.get_width() / 2, 80))

# Rectangle settings
rect_width = 300
rect_height = 100
spacing = 30

# First rectangle
rect1 = pygame.Rect(0, 0, rect_width, rect_height)
rect1.center = (screen.get_width() / 2, screen.get_height() / 2 - rect_height)

# Second rectangle
rect2 = pygame.Rect(0, 0, rect_width, rect_height)
rect2.center = (screen.get_width() / 2, rect1.bottom + spacing + rect_height / 2)

# Text for rectangles
text1 = button_font.render("Timed", True, "white")
text1_rect = text1.get_rect(center=rect1.center)

text2 = button_font.render("Sandbox", True, "white")
text2_rect = text2.get_rect(center=rect2.center)

running = True
dt = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()

            if current_screen == "mode select":
                if rect1.collidepoint(mouse_position):
                    current_screen = "Timed"

                if rect2.collidepoint(mouse_position):
                    current_screen = "Sandbox"



    screen.fill("black")

    # Draw title
    screen.blit(title_surface, title_rect)

    # Draw rectangles
    pygame.draw.rect(screen, "grey", rect1)
    pygame.draw.rect(screen, "grey", rect2)

    # Draw text
    screen.blit(text1, text1_rect)
    screen.blit(text2, text2_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()