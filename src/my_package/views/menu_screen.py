import pygame


class MenuScreen:
    """A simple menu screen for choosing between game modes."""

    def __init__(self, screen):
        self.screen = screen

        # Fonts used by the title and buttons.
        self.title_font = pygame.font.SysFont(None, 64)
        self.button_font = pygame.font.SysFont(None, 48)

        # Title text rendered once.
        self.title_surface = self.title_font.render("Mode Selection", True, "white")
        self.title_rect = self.title_surface.get_rect(
            center=(screen.get_width() // 2, 80)
        )

        # Button layout settings.
        rect_width = 300
        rect_height = 100
        spacing = 30

        # Create the timed mode selection button.
        self.rect1 = pygame.Rect(0, 0, rect_width, rect_height)
        self.rect1.center = (
            screen.get_width() // 2,
            screen.get_height() // 2 - rect_height,
        )

        # Create the sandbox mode selection button.
        self.rect2 = pygame.Rect(0, 0, rect_width, rect_height)
        self.rect2.center = (
            screen.get_width() // 2,
            self.rect1.bottom + spacing + rect_height // 2,
        )

        # Convert button labels into rendered text surfaces.
        self.text1 = self.button_font.render("Timed", True, "white")
        self.text1_rect = self.text1.get_rect(center=self.rect1.center)

        self.text2 = self.button_font.render("Sandbox", True, "white")
        self.text2_rect = self.text2.get_rect(center=self.rect2.center)

    def handle_event(self, event):
        """Return the selected mode when a button is clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect1.collidepoint(event.pos):
                return "timed"
            if self.rect2.collidepoint(event.pos):
                return "sandbox"

    def draw(self, screen):
        """Render the menu screen background, buttons, and title."""
        self.screen.fill("black")
        pygame.draw.rect(self.screen, "grey", self.rect1)
        pygame.draw.rect(self.screen, "grey", self.rect2)

        self.screen.blit(self.title_surface, self.title_rect)
        self.screen.blit(self.text1, self.text1_rect)
        self.screen.blit(self.text2, self.text2_rect)
