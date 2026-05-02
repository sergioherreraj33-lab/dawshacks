import math
import pygame
import pymunk
from src.my_package import grid

class TimedScreen:
    LEDGE_W = 200
    LEDGE_H = 550
    CIRCLE_RADIUS = 40
    GRAVITY = 900

    def __init__(self):
        # Initialize grid, prebuilt nodes, beams, and timer variables
        self.grid = grid.BackgroundGrid(1280, 720, 40)
        self.nodes = self._build_initial_nodes()
        self.beams = []
        self.selected_node = None

        # Timer settings
        self.timer_options = [5, 10, 90]
        self.selected_duration = None
        self.remaining_time = 0
        self.timer_running = False
        self.start_ticks = 0

        # Physics state
        self.space = None
        self.ball_shape = None
        self.ledges = []
        self.physics_active = False
        self.physics_initialized = False

        # Fonts
        self.font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 36)

        # Timer button rectangles
        self.timer_rects = []
        self.start_rect = pygame.Rect(0, 0, 120, 40)
        self.start_rect.center = (1180, 50)
        self._build_timer_rects()

    def _build_initial_nodes(self):
        num_nodes_x = 9
        num_nodes_y = 5
        spacing_x = 100
        spacing_y = 60
        bottom_gap = 50

        total_width = (num_nodes_x - 1) * spacing_x
        start_x = (self.grid.width - total_width) // 2

        total_height = (num_nodes_y - 1) * spacing_y
        start_y = (self.grid.height - bottom_gap) - total_height

        nodes = []
        for i in range(num_nodes_x):
            for j in range(num_nodes_y):
                x = start_x + (i * spacing_x)
                y = start_y + (j * spacing_y)
                nodes.append((x, y))
        return nodes

    # Helper method to create rectangles for timer options
    def _build_timer_rects(self):
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

    def _create_ledge(self, pos):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, (self.LEDGE_W, self.LEDGE_H))
        self.space.add(body, shape)
        return shape

    def _create_ball(self, pos):
        body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        body.position = pos
        shape = pymunk.Circle(body, self.CIRCLE_RADIUS)
        shape.elasticity = 0.5
        self.space.add(body, shape)
        return shape

    def _initialize_physics(self):
        if self.physics_initialized:
            return
        self.physics_initialized = True
        self.physics_active = True

        self.space = pymunk.Space()
        self.space.gravity = (0, self.GRAVITY)

        left_ledge_pos = (self.LEDGE_W / 2, self.grid.height - 180)
        right_ledge_pos = (self.grid.width - (self.LEDGE_W / 2), self.grid.height - 180)
        self.ledges = [
            self._create_ledge(left_ledge_pos),
            self._create_ledge(right_ledge_pos),
        ]

        self.ball_shape = self._create_ball((self.grid.width / 2, 80))

        for beam in self.beams:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            shape = pymunk.Segment(body, beam[0], beam[1], 2)
            shape.elasticity = 0.5
            self.space.add(body, shape)

    def _update_physics(self):
        if not self.physics_active:
            return
        self.space.step(1 / 60)

    # Event handler for mouse clicks
    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        pos = event.pos

        # Check if a timer option or start button was clicked
        if not self.timer_running:
            for idx, rect in enumerate(self.timer_rects):
                if rect.collidepoint(pos):
                    self.selected_duration = self.timer_options[idx]
                    self.remaining_time = self.selected_duration
                    return

            if self.start_rect.collidepoint(pos) and self.selected_duration:
                self.timer_running = True
                self.start_ticks = pygame.time.get_ticks()
                return

        # If timer is running, handle node and beam selection/creation
        if self.timer_running:
            clicked_node = None
            for node in self.nodes:
                distance = math.dist(node, pos)
                if distance < 12:
                    clicked_node = node
                    break

            if clicked_node:
                if self.selected_node is None:
                    self.selected_node = clicked_node
                else:
                    if clicked_node != self.selected_node:
                        self.beams.append((self.selected_node, clicked_node))
                    self.selected_node = None

    # Update the timer based on elapsed time
    def _update_timer(self):
        if not self.timer_running or self.selected_duration is None:
            return

        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.remaining_time = max(0, self.selected_duration - int(elapsed))
        if self.remaining_time <= 0:
            self.timer_running = False
            self._initialize_physics()

    def _draw_physics_scene(self, screen):
        screen.fill("white")

        for ledge in self.ledges:
            body = ledge.body
            pos_x = int(body.position.x)
            pos_y = int(body.position.y)
            draw_x = pos_x - (self.LEDGE_W / 2)
            draw_y = pos_y - (self.LEDGE_H / 2)
            pygame.draw.rect(screen, "lightgreen", (draw_x, draw_y, self.LEDGE_W, self.LEDGE_H))

        if self.ball_shape is not None:
            pos_x = int(self.ball_shape.body.position.x)
            pos_y = int(self.ball_shape.body.position.y)
            pygame.draw.circle(screen, "blue", (pos_x, pos_y), self.CIRCLE_RADIUS)

        for beam in self.beams:
            pygame.draw.line(screen, "orange", beam[0], beam[1], 2)

        for node in self.nodes:
            pygame.draw.circle(screen, "blue", node, 6)

        if self.selected_node is not None:
            pygame.draw.circle(screen, "yellow", self.selected_node, 10, 2)

    def draw(self, screen):
        if self.physics_active:
            self._update_physics()
            self._draw_physics_scene(screen)
        else:
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

            self._update_timer()

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

            for beam in self.beams:
                pygame.draw.line(screen, (255, 255, 255), beam[0], beam[1], 2)

            for node in self.nodes:
                pygame.draw.circle(screen, (0, 200, 255), node, 6)

            if self.selected_node is not None:
                pygame.draw.circle(screen, (255, 255, 0), self.selected_node, 10, 2)

    