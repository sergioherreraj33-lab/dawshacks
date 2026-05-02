import pygame

from src.my_package.helpers.bridge_builder import BridgeBuilder
from src.my_package.helpers.physics_manager import PhysicsManager
from src.my_package import grid


class TimedScreen:
    def __init__(self):
        self.grid = grid.BackgroundGrid(1280, 720, 40)

        self.bridge = BridgeBuilder(self.grid)
        self.physics = PhysicsManager(self.grid)

        self.timer_options = [5, 10, 90]
        self.selected_duration = None
        self.remaining_time = 0
        self.timer_running = False
        self.start_ticks = 0

        self.font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 36)

        self.timer_rects = []
        self.start_rect = pygame.Rect(0, 0, 120, 40)
        self.start_rect.center = (1180, 50)

        self.back_rect = pygame.Rect(1180, 60, 100, 36)

        self._build_timer_rects()

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

    def handle_event(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        pos = event.pos

        if self.back_rect.collidepoint(pos):
            return "menu"

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

        if self.timer_running:
            self.bridge.handle_click(pos)
            return

        if self.physics.active and not self.timer_running:
            self.physics.drop_ball(pos)

    def _update_timer(self):
        if not self.timer_running or self.selected_duration is None:
            return

        elapsed = (pygame.time.get_ticks() - self.start_ticks) / 1000
        self.remaining_time = max(0, self.selected_duration - int(elapsed))

        if self.remaining_time <= 0:
            self.timer_running = False
            self.physics.initialize(self.bridge.beams)

    def draw(self, screen):
        if self.physics.active:
            self.physics.update()
            self.physics.draw(
                screen,
                self.bridge.beams,
                self.bridge.nodes,
                self.bridge.selected_node
            )

            pygame.draw.rect(screen, (80, 80, 120), self.back_rect)
            back_text = self.font.render("Back", True, "white")
            screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))

            info_surface = self.font.render("Click to drop a ball", True, "black")
            screen.blit(info_surface, (140, 68))
            return

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

        pygame.draw.rect(screen, (80, 80, 120), self.back_rect)
        back_text = self.font.render("Back", True, "white")
        screen.blit(back_text, back_text.get_rect(center=self.back_rect.center))

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

        for beam in self.bridge.beams:
            pygame.draw.line(screen, (255, 255, 255), beam[0], beam[1], 2)

        for node in self.bridge.nodes:
            pygame.draw.circle(screen, (0, 200, 255), node, 6)

        if self.bridge.selected_node is not None:
            pygame.draw.circle(screen, (255, 255, 0), self.bridge.selected_node, 10, 2)