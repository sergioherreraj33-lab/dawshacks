import tkinter as tk

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Click to Connect Points")
        
        # Create canvas
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Track previous point
        self.last_x = None
        self.last_y = None
        
        # Bind left click
        self.canvas.bind("<Button-1>", self.add_point)

    def add_point(self, event):
        # Current click coordinates
        x, y = event.x, event.y
        
        # Draw a small dot for the point
        self.canvas.create_oval(x-3, y-3, x+3, y+3, fill="black")
        
        # If there's a previous point, connect them
        if self.last_x is not None:
            self.canvas.create_line(self.last_x, self.last_y, x, y, fill="blue", width=2)
            
        # Update last known point
        self.last_x, self.last_y = x, y

if __name__ == "__main__":
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()
