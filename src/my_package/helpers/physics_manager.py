import pygame
import pymunk


class PhysicsManager:
    LEDGE_W = 200
    LEDGE_H = 550
    CIRCLE_RADIUS = 40
    GRAVITY = 900

    def __init__(self, grid):
        self.grid = grid
        self.space = None
        self.circles = []
        self.ledges = []
        self.active = False
        self.initialized = False

    def create_ledge(self, pos):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, (self.LEDGE_W, self.LEDGE_H))
        self.space.add(body, shape)
        return shape

    def create_ball(self, pos):
        body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        body.position = pos

        shape = pymunk.Circle(body, self.CIRCLE_RADIUS)
        shape.elasticity = 0.5

        self.space.add(body, shape)
        return shape

    def initialize(self, beams):
        if self.initialized:
            return

        self.initialized = True
        self.active = True

        self.space = pymunk.Space()
        self.space.gravity = (0, self.GRAVITY)

        left_ledge_pos = (self.LEDGE_W / 2, self.grid.height - 180)
        right_ledge_pos = (self.grid.width - (self.LEDGE_W / 2), self.grid.height - 180)

        self.ledges = [
            self.create_ledge(left_ledge_pos),
            self.create_ledge(right_ledge_pos),
        ]

        for beam in beams:
            body = pymunk.Body(body_type=pymunk.Body.STATIC)
            shape = pymunk.Segment(body, beam[0], beam[1], 2)
            shape.elasticity = 0.5
            self.space.add(body, shape)

    def update(self):
        if self.active and self.space is not None:
            self.space.step(1 / 60)

    def drop_ball(self, pos):
        if self.space is not None:
            self.circles.append(self.create_ball(pos))

    def draw(self, screen, beams, nodes, selected_node):
        screen.fill("white")

        for ledge in self.ledges:
            body = ledge.body
            pos_x = int(body.position.x)
            pos_y = int(body.position.y)

            draw_x = pos_x - (self.LEDGE_W / 2)
            draw_y = pos_y - (self.LEDGE_H / 2)

            pygame.draw.rect(
                screen,
                "lightgreen",
                (draw_x, draw_y, self.LEDGE_W, self.LEDGE_H)
            )

        for circle in self.circles:
            pos_x = int(circle.body.position.x)
            pos_y = int(circle.body.position.y)
            pygame.draw.circle(screen, "blue", (pos_x, pos_y), self.CIRCLE_RADIUS)

        for beam in beams:
            pygame.draw.line(screen, "orange", beam[0], beam[1], 2)

        for node in nodes:
            pygame.draw.circle(screen, "blue", node, 6)

        if selected_node is not None:
            pygame.draw.circle(screen, "yellow", selected_node, 10, 2)