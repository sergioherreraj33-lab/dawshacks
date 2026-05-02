import pygame
from src.my_package import grid


class SandboxScreen:
    """A freeform sandbox mode for placing nodes and connecting beams."""

    def __init__(self):
        self.grid = grid.BackgroundGrid(1280, 720, 40)
        self.nodes = []
        self.beams = []
        self.selected_node = None

    def handle_event(self, event):
        """Handle clicks to create nodes and connect them with beams."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked_node = None

            # Detect whether an existing node was clicked.
            for node in self.nodes:
                distance = ((node[0] - pos[0]) ** 2 + (node[1] - pos[1]) ** 2) ** 0.5
                if distance < 12:
                    clicked_node = node
                    break

            if clicked_node:
                # If a node is already selected, connect it to the clicked node.
                if self.selected_node is None:
                    self.selected_node = clicked_node
                else:
                    self.beams.append((self.selected_node, clicked_node))
                    self.selected_node = None
            else:
                # Otherwise create a new node at the click position.
                self.nodes.append(pos)

    def draw(self, screen):
        """Render the sandbox grid and all placed nodes/beams."""
        screen.fill((30, 30, 30))
        self.grid.drawGrid(screen)

        for beam in self.beams:
            pygame.draw.line(screen, (255, 255, 255), beam[0], beam[1], 2)

        for node in self.nodes:
            pygame.draw.circle(screen, (0, 200, 255), node, 6)

        if self.selected_node is not None:
            pygame.draw.circle(screen, (255, 255, 0), self.selected_node, 10, 2)
