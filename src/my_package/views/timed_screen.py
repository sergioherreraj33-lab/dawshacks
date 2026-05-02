import pygame
from src.my_package import grid

class TimedScreen:
    def __init__(self):
        # Initialize grid, nodes, beams, and timer variables
        self.grid = grid.BackgroundGrid(1280, 720, 40)
        self.nodes = []
        self.beams = []
        self.selected_node = None

        # Timer settings
        self.timer_options = [30, 60, 90]
        self.selected_duration = None
        self.remaining_time = 0
        self.timer_running = False
        self.start_ticks = 0

        # Fonts
        self.font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 36)

        # Timer button rectangles
        self.timer_rects = []
        self.start_rect = pygame.Rect(0, 0, 120, 40)
        self.start_rect.center = (1180, 50)
        self._build_timer_rects()

    # Helper method to create rectangles for timer options
    def _build_timer_rects(self):
        rect_width = 100
        rect_height = 40
        spacing = 20
        x = 60
        y = 70

        # Create rectangles for each timer option
        self.timer_rects = []
        for _ in self.timer_options:
            rect = pygame.Rect(x, y - rect_height / 2, rect_width, rect_height)
            self.timer_rects.append(rect)
            # Update x position for the next timer option
            x += rect_width + spacing

    # Event handler for mouse clicks
    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        pos = event.pos

        # Check if a timer option or start button was clicked
        if not self.timer_running:
            # Check timer option clicks
            for idx, rect in enumerate(self.timer_rects):
                if rect.collidepoint(pos):
                    self.selected_duration = self.timer_options[idx]
                    self.remaining_time = self.selected_duration
                    return

            # Check if start button was clicked
            if self.start_rect.collidepoint(pos) and self.selected_duration:
                # Start the timer
                self.timer_running = True
                self.start_ticks = pygame.time.get_ticks()
                return

        # If timer is running, handle node and beam creation
        if self.timer_running:
            clicked_node = None
            for node in self.nodes:
                # Calculate distance from click to node to determine if a node was clicked
                distance = ((node[0] - pos[0]) ** 2 + (node[1] - pos[1]) ** 2) ** 0.5
                if distance < 12:
                    clicked_node = node
                    break

            # If a node was clicked, either select it or create a beam
            if clicked_node:
                if self.selected_node is None:
                    # Select the node for potential beam creation if another node is clicked
                    self.selected_node = clicked_node
                else:
                    # Create a beam between the selected node and the clicked node, then reset selection
                    self.beams.append((self.selected_node, clicked_node))
                    self.selected_node = None
            else:
                self.nodes.append(pos)

    # Update the timer based on elapsed time
    def _update_timer(self):
        if not self.timer_running or self.selected_duration is None:
            return

        # Calculate elapsed time and update remaining time
        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        # Ensure remaining time doesn't go negative
        self.remaining_time = max(0, self.selected_duration - int(elapsed))
        # Stop the timer if time runs out
        if self.remaining_time <= 0:
            self.timer_running = False

    def draw(self, screen):
        # Fill the background and draw the grid
        screen.fill((30, 30, 30))
        self.grid.drawGrid(screen)

        # Draw the header background
        pygame.draw.rect(screen, (20, 20, 20), (0, 0, screen.get_width(), 100))

        # Draw the title and timer options
        title_surface = self.title_font.render("Timed Challenge", True, "white")
        screen.blit(title_surface, (20, 10))



        # Draw timer option buttons with different colors based on selection
        for idx, duration in enumerate(self.timer_options):
            # Draw each timer option button, highlighting the selected one
            rect = self.timer_rects[idx]
            color = (80, 160, 80) if self.selected_duration == duration else (100, 100, 100)
            pygame.draw.rect(screen, color, rect)
            # Draw the timer duration text centered on the button
            text_surface = self.font.render(f"{duration}s", True, "white")
            screen.blit(text_surface, text_surface.get_rect(center=rect.center))
            # Draw a border around the selected timer option
        start_color = (120, 120, 220) if self.selected_duration else (70, 70, 70)
        pygame.draw.rect(screen, start_color, self.start_rect)
        start_text = self.font.render("Start", True, "white")
        screen.blit(start_text, start_text.get_rect(center=self.start_rect.center))

        self._update_timer()

        # Draw the remaining time and status message
        timer_surface = self.font.render(f"Time: {self.remaining_time}s", True, "white")
        screen.blit(timer_surface, (450, 20))

        # Display different status messages based on timer state
        if self.timer_running:
            status = "Building..."
        elif self.selected_duration and self.remaining_time == 0:
            status = "Time's up!"
        else:
            status = "Select a timer then press Start"

        # Render and display the status message
        status_surface = self.font.render(status, True, "white")
        screen.blit(status_surface, (450, 50))

        # Draw beams and nodes, highlighting the selected node if applicable
        for beam in self.beams:
            pygame.draw.line(screen, (255, 255, 255), beam[0], beam[1], 2)

        # Draw each node as a circle, and if a node is selected, draw a highlighted circle around it
        for node in self.nodes:
            pygame.draw.circle(screen, (0, 200, 255), node, 6)


        # Highlight the selected node with a yellow circle if one is selected
        if self.selected_node is not None:
            pygame.draw.circle(screen, (255, 255, 0), self.selected_node, 10, 2)

    