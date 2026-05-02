import pygame
import sys

# 1. Initialize and set up the window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My Pygame Window")

# 2. Main loop
running = True

bridge_grid = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1]
]

while running:
    # Check for events (like clicking the 'X')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. Drawing section
    screen.fill((50, 50, 50))  # Fills screen with a dark grey color
  
    radius = 10
    separation = radius * 5
    
    for row in range(len(bridge_grid)): 
        for col in range(len(bridge_grid[0])):
            pygame.draw.circle(screen, (0, 255, 0), (separation, 200), radius)
            separation += radius*2

        
    pygame.display.flip()
# Clean up
pygame.quit()
sys.exit()

