import math


class BridgeBuilder:
    """Manage the bridge build grid, node selection, and beam creation."""

    def __init__(self, grid):
        self.grid = grid
        self.nodes = self._build_initial_nodes()
        self.beams = []
        self.selected_node = None

    def _build_initial_nodes(self):
        """Create a fixed array of grid nodes for timed build mode."""
        num_nodes_x = 9
        num_nodes_y = 8
        spacing_x = 100
        spacing_y = 60
        bottom_gap = 30

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

    def handle_click(self, pos):
        """Select nodes and create beams between clicked node pairs."""
        clicked_node = None

        for node in self.nodes:
            distance = math.dist(node, pos)
            if distance < 12:
                clicked_node = node
                break

        if clicked_node:
            if self.selected_node is None:
                # First node click selects a start point.
                self.selected_node = clicked_node
            else:
                # Second click creates a beam to the previously selected node.
                if clicked_node != self.selected_node:
                    self.beams.append((self.selected_node, clicked_node))
                self.selected_node = None
