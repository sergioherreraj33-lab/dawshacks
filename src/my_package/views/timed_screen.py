import pygame

from src.my_package.helpers.bridge_builder import BridgeBuilder
from src.my_package.helpers.physics_manager import PhysicsManager
from src.my_package import grid


class TimedScreen:
    """A screen where the player builds a bridge under a timer and then drops a ball."""

    def __init__(self):
        # Create the grid background used in build mode.
        self.grid = grid.BackgroundGrid(1280, 720, 40)

        # BridgeBuilder handles node placement and beam creation.
        self.bridge = BridgeBuilder(self.grid)

        # PhysicsManager handles the ball drop and physics simulation.
        self.physics = PhysicsManager(self.grid)

        # Timer options for the timed build phase.
        self.timer_options = [5, 10, 90]
        self.selected_duration = None
        self.remaining_time = 0
        self.timer_running = False
        self.start_ticks = 0

        # Fonts for on-screen UI text.
        self.font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 36)

        # Button rectangles used in the timer UI.
        self.timer_rects = []
        self.start_rect = pygame.Rect(0, 0, 120, 40)
        self.start_rect.center = (1180, 50)

        # Back button in the top-right corner.
        self.back_rect = pygame.Rect(1180, 60, 100, 36)

        # Build the timer selection buttons.
        self._build_timer_rects()

    def _build_timer_rects(self):
        """Create rectangles for the timer option buttons."""
        rect_width = 100
        rect_height = 40
        spacing = 20
        x = 60
        y = 70

        self.timer_rects = []
        for _ in self.timer_options:
            rect = pygame.Rect(x, y - rect_height / 2, rect_width, rect_height)
            self.timer_rects.append(rect)
            x += rect_width + spacing

    def handle_event(self, event):
        """Handle all mouse clicks on the timed screen."""
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        pos = event.pos

        # Back button returns to the main menu.
        if self.back_rect.collidepoint(pos):
            return "menu"

        # If the timer has not started yet, allow selection of options.
        if not self.timer_running:
            for idx, rect in enumerate(self.timer_rects):
                if rect.collidepoint(pos):
                    self.selected_duration = self.timer_options[idx]
                    self.remaining_time = self.selected_duration
                    return

            # Start the build timer if the start button is clicked.
            if self.start_rect.collidepoint(pos) and self.selected_duration:
                self.timer_running = True
                self.start_ticks = pygame.time.get_ticks()
                return

        # While the build timer is running, forward clicks to the bridge builder.
        if self.timer_running:
            self.bridge.handle_click(pos)
            return

        # After the build phase, clicking drops a physics ball.
        if self.physics.active and not self.timer_running:
            self.physics.drop_ball(pos)

    def _update_timer(self):
        """Update the countdown and initialize physics when it expires."""
        if not self.timer_running or self.selected_duration is None:
            return

        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.remaining_time = max(0, self.selected_duration - int(elapsed))

        if self.remaining_time <= 0:
            self.timer_running = False
            self.physics.initialize(self.bridge.beams)

    def draw(self, screen):
        """Draw either the build screen or the physics screen, depending on state."""
        if self.physics.active:
            # Physics mode: update the simulation and draw its objects.
            self.physics.update()
            self.physics.draw(
                screen,
                self.bridge.beams,
                self.bridge.nodes,
                self.bridge.selected_node,
            )

            # Draw back button during physics mode.
            pygame.draw.rect(screen, (80, 80, 120), self.back_rect)
            back_text = self.font.render("Back", True, "white")
            screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))

            # Hint for the user to drop the ball.
            info_surface = self.font.render("Click to drop a ball", True, "black")
            screen.blit(info_surface, (140, 68))
            return

        # Build mode: draw grid and UI controls.
        screen.fill((30, 30, 30))
        self.grid.drawGrid(screen)

        pygame.draw.rect(screen, "gray", (0, 0, screen.get_width(), 100))

        title_surface = self.title_font.render("Timed Challenge", True, "white")
        screen.blit(title_surface, (20, 10))

        for idx, duration in enumerate(self.timer_options):
            rect = self.timer_rects[idx]
            color = (80, 160, 80) if self.selected_duration == duration else (100, 100, 100)
            pygame.draw.rect(screen, color, rect)

            text_surface = self.font.render(f"{duration}s", True, "white")
            screen.blit(text_surface, text_surface.get_rect(center=rect.center))

        start_color = (120, 120, 220) if self.selected_duration else (70, 70, 70)
        pygame.draw.rect(screen, start_color, self.start_rect)

        start_text = self.font.render("Start", True, "white")
        screen.blit(start_text, start_text.get_rect(center=self.start_rect.center))

        # Update the timer countdown.
        self._update_timer()

        # Draw the back button during build mode as well.
        pygame.draw.rect(screen, (80, 80, 120), self.back_rect)
        back_text = self.font.render("Back", True, "white")
        screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))

        # Draw timer and status text.
        timer_surface = self.font.render(f"Time: {self.remaining_time}s", True, "white")
        screen.blit(timer_surface, (450, 20))

        if self.timer_running:
            status = "Building..."
        elif self.selected_duration and self.remaining_time == 0:
            status = "Time's up!"
        else:
            status = "Select a timer then press Start"

        status_surface = self.font.render(status, True, "white")
        screen.blit(status_surface, (450, 50))

        # Draw the current bridge beams and nodes.
        for beam in self.bridge.beams:
            pygame.draw.line(screen, (255, 255, 255), beam[0], beam[1], 2)

        for node in self.bridge.nodes:
            pygame.draw.circle(screen, (0, 200, 255), node, 6)

        # Highlight the currently selected node if present.
        if self.bridge.selected_node is not None:
            pygame.draw.circle(screen, (255, 255, 0), self.bridge.selected_node, 10, 2)
