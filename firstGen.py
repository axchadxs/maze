import tkinter as tk
from tkinter import ttk
import random
from typing import List, Tuple, Dict



class MazeCell:    
    # A single cell in the maze
    
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        # True means wall exists
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}
        self.visited = False
        self.in_path = False
        
    def __repr__(self):
        return f"Cell({self.row}, {self.col})"


class MazeVisualizer:
    # Main application class for the maze generator and solver visualization.
    # Handles the GUI, maze state, and visualization of the algorithms
    # Colors used in the maze
    COLOR_START = "#ff00ff" 
    COLOR_END = "#ff00ff"
    COLOR_VISITED = "#56b6f7"
    COLOR_PATH = "#ff0000"
    COLOR_EMPTY = "white"
    COLOR_WALL = "#2c3e50"
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Maze Generator & Solver")
        self.root.geometry("1100x750")
        self.root.configure(bg='#ecf0f1')
        
        # Maze parameters
        self.rows = 20
        self.cols = 20
        self.cell_size = 25
        self.maze: List[List[MazeCell]] = []
        self.start = (0, 0)
        self.end = (self.rows - 1, self.cols - 1)
        self.algorithm_running = False
        
        # Statistics
        self.gen_steps = 0
        self.solve_steps = 0
        self.path_length = 0
        self.start_time = 0
        
        self.setup_ui()
        # Do not auto-generate a maze on startup. Initialize a full-walled grid and draw it.
        self.init_empty_maze()

    def init_empty_maze(self):
        # Create an empty (full-walled) maze grid and draw it without starting generation
        # Ensure rows/cols are current from size_var (but don't throw errors during init)
        try:
            size = int(self.size_var.get())
            if 5 <= size <= 50:
                self.rows = self.cols = size
        except Exception:
            pass

        self.end = (self.rows - 1, self.cols - 1)
        self.gen_steps = 0
        self.solve_steps = 0
        self.path_length = 0

        # Initialize maze grid with all walls intact
        self.maze = [[MazeCell(r, c) for c in range(self.cols)] for r in range(self.rows)]

        for row in self.maze:
            for cell in row:
                cell.visited = False
                cell.in_path = False

        self.canvas.delete("all")
        self.draw_maze()
        self.update_stats_text("Ready to generate maze...")
        
    def setup_ui(self):
        
        title_frame = ttk.Frame(self.root)
        title_frame.pack(side=tk.TOP, fill=tk.X, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="Maze Generator & Solver",
            font=("Arial", 18, "bold"),
            bg='#ecf0f1',
            fg='#2c3e50'
        )
        title_label.pack()
        
        control_frame = ttk.LabelFrame(self.root, text="Controls", padding="15")
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=5)
        
        size_frame = ttk.Frame(control_frame)
        size_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(size_frame, text="Maze Size:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.size_var = tk.StringVar(value="20")
        size_entry = ttk.Entry(size_frame, textvariable=self.size_var, width=6, font=("Arial", 10))
        size_entry.pack(side=tk.LEFT, padx=5)
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame,
            text="Generate Maze",
            command=self.generate_new_maze,
            width=18
        ).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(
            btn_frame,
            text="Solve Maze",
            command=self.solve_maze_dfs,
            width=18
        ).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(
            btn_frame,
            text="Reset",
            command=self.reset_maze,
            width=12
        ).pack(side=tk.LEFT, padx=3)
        
        speed_frame = ttk.Frame(control_frame)
        self.speed = 5  # Default speed (1 slow .. 10 fast)
        
        # Stats panel
        stats_frame = ttk.LabelFrame(self.root, text="Statistics", padding="10")
        stats_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=5)
        
        self.stats_label = tk.Label(
            stats_frame,
            text="Ready to generate maze...",
            font=("Courier", 11),
            bg='white',
            fg='#2c3e50',
            anchor='w',
            padx=10,
            pady=5
        )
        self.stats_label.pack(fill=tk.X)
        
        # Canvas for maze
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=2, highlightbackground='#bdc3c7')
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        # Bind resize event
        self.canvas.bind('<Configure>', lambda e: self.draw_maze())
        
    
    def generate_new_maze(self):
        # Initialize and start maze generation.
        # Validates size input and prepares the grid for the generation algorithm
        # Prevent multiple generations running at once
        if self.algorithm_running:
            return
        
        try:
            size = int(self.size_var.get())
            if size < 5:
                self.update_stats_text("Maze size too small - minimum is 5x5")
                return
            if size > 50:
                self.update_stats_text("Size too large, maximum is 50x50")
                return
            self.rows = self.cols = size
        except ValueError:
            self.update_stats_text("Please enter a valid number for the size")
            return
        
        self.end = (self.rows - 1, self.cols - 1)
        self.gen_steps = 0
        self.solve_steps = 0
        self.path_length = 0
        
        # Initialize maze grid
        self.maze = [[MazeCell(r, c) for c in range(self.cols)] for r in range(self.rows)]
        
        self.canvas.delete("all")
        self.draw_maze()
        self.update_stats_text("Generating maze...")
        
        # Start DFS generation
        self.algorithm_running = True
        self.root.after(10, lambda: self.generate_maze_dfs(0, 0, []))
    
    def generate_maze_dfs(self, row: int, col: int, stack: List[Tuple[int, int]]):
        # Generate maze using DFS - removes walls to create paths
        
        if not self.algorithm_running:
            return
        
        # Mark current cell as visited and update progress
        current = self.maze[row][col]
        current.visited = True
        self.gen_steps += 1
        
        # Define directions: North, South, East, West
        directions = [
            ('N', -1, 0),
            ('S', 1, 0),
            ('E', 0, 1),
            ('W', 0, -1)
        ]
        
        # Get unvisited neighbors
        neighbors = []
        for direction, dr, dc in directions:
            nr, nc = row + dr, col + dc
            if (0 <= nr < self.rows and 0 <= nc < self.cols and
                    not self.maze[nr][nc].visited):
                neighbors.append((direction, nr, nc))
        
        if neighbors:
            # Choose random unvisited neighbor (randomness creates maze variety)
            direction, nr, nc = random.choice(neighbors)
            
            # Remove walls between current and chosen neighbor
            current.walls[direction] = False
            opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
            self.maze[nr][nc].walls[opposite[direction]] = False
            
            # Push current to stack and move to neighbor
            stack.append((row, col))
            
            self.draw_maze()
            self.update_stats()
            
            delay = max(1, 100 - self.speed * 9)
            self.root.after(delay, lambda: self.generate_maze_dfs(nr, nc, stack))
            
        elif stack:
            # Backtrack to previous cell
            prev_row, prev_col = stack.pop()
            delay = max(1, 100 - self.speed * 9)
            self.root.after(delay, lambda: self.generate_maze_dfs(prev_row, prev_col, stack))
            
        else:
            # Generation complete
            self.algorithm_running = False
            self.update_stats_text(f"Maze generated. Total cells: {self.gen_steps} | Size: {self.rows}x{self.cols}")
    
    def solve_maze_dfs(self):
        # Initialize and start maze solving using depth-first search.
        # Explores possible paths until it finds the end, marking the solution path
        
        # Prevent multiple solves running at once
        if self.algorithm_running:
            return
        
        # Ensure we have a maze to solve
        if not self.maze:
            self.update_stats_text("Error: generate a maze first")
            return
        
        # Reset visited flags
        for row in self.maze:
            for cell in row:
                cell.visited = False
                cell.in_path = False
        
        self.solve_steps = 0
        self.path_length = 0
        self.algorithm_running = True
        
        self.update_stats_text("Solving maze...")
        self.root.after(10, lambda: self.dfs_solve(self.start[0], self.start[1], []))
    
    def dfs_solve(self, row: int, col: int, path: List[Tuple[int, int]]) -> bool:
        
        if not self.algorithm_running:
            return False
        
        # Check if reached end
        if (row, col) == self.end:
            path.append((row, col))
            # Mark solution path
            for r, c in path:
                self.maze[r][c].in_path = True
            self.path_length = len(path)
            self.algorithm_running = False
            self.draw_maze()
            
            efficiency = (self.path_length / self.solve_steps * 100) if self.solve_steps > 0 else 0
            self.update_stats_text(
                f"SOLVED! Path Length: {self.path_length} | "
                f"Cells Explored: {self.solve_steps} | "
                f"Efficiency: {efficiency:.1f}%"
            )
            return True
        
        current = self.maze[row][col]
        if current.visited:
            return False
        
        current.visited = True
        path.append((row, col))
        self.solve_steps += 1
        
        self.draw_maze()
        self.update_stats()
        
        # Try all accessible directions (where walls are removed)
        moves = []
        if not current.walls['N']:
            moves.append((-1, 0))
        if not current.walls['S']:
            moves.append((1, 0))
        if not current.walls['E']:
            moves.append((0, 1))
        if not current.walls['W']:
            moves.append((0, -1))
        
        delay = max(1, 50 - self.speed * 4)
        
        # Explore each valid direction
        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                self.root.after(delay)
                self.root.update()
                if self.dfs_solve(nr, nc, path[:]):
                    return True
        
        return False
    
    def draw_maze(self):
        # Renders the current state of the maze on the canvas.
        # Handles dynamic resizing, cell coloring, and wall drawing
        # Clear previous drawing
        self.canvas.delete("all")
        
        # Calculate cell size to fit canvas while maintaining square cells
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width > 1 and canvas_height > 1:
            self.cell_size = min(
                (canvas_width - 20) // self.cols,
                (canvas_height - 20) // self.rows
            )
        else:
            self.cell_size = 25
        
        # Center the maze
        total_width = self.cols * self.cell_size
        total_height = self.rows * self.cell_size
        offset_x = (canvas_width - total_width) // 2
        offset_y = (canvas_height - total_height) // 2
        
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.maze[row][col]
                x = offset_x + col * self.cell_size
                y = offset_y + row * self.cell_size
                
                # Determine cell color based on state
                color = self.COLOR_EMPTY
                if (row, col) == self.start:
                    color = self.COLOR_START
                elif (row, col) == self.end:
                    color = self.COLOR_END
                elif cell.in_path:
                    color = self.COLOR_PATH
                elif cell.visited:
                    color = self.COLOR_VISITED
                
                # Draw cell
                self.canvas.create_rectangle(
                    x, y,
                    x + self.cell_size,
                    y + self.cell_size,
                    fill=color,
                    outline=''
                )
                
                # Draw walls
                wall_width = 2
                if cell.walls['N']:
                    self.canvas.create_line(
                        x, y,
                        x + self.cell_size, y,
                        fill=self.COLOR_WALL,
                        width=wall_width
                    )
                if cell.walls['S']:
                    self.canvas.create_line(
                        x, y + self.cell_size,
                        x + self.cell_size, y + self.cell_size,
                        fill=self.COLOR_WALL,
                        width=wall_width
                    )
                if cell.walls['E']:
                    self.canvas.create_line(
                        x + self.cell_size, y,
                        x + self.cell_size, y + self.cell_size,
                        fill=self.COLOR_WALL,
                        width=wall_width
                    )
                if cell.walls['W']:
                    self.canvas.create_line(
                        x, y,
                        x, y + self.cell_size,
                        fill=self.COLOR_WALL,
                        width=wall_width
                    )
    
    def update_stats(self, solved: bool = False):
        # Update statistics display during algorithm execution
        
        if solved:
            efficiency = (self.path_length / self.solve_steps * 100) if self.solve_steps > 0 else 0
            text = f"Found solution! Length: {self.path_length}, Explored {self.solve_steps} cells"
        elif self.solve_steps > 0:
            text = f"Finding path... ({self.solve_steps} cells checked)"
        else:
            text = f"Creating maze... ({self.gen_steps}/{self.rows * self.cols})"
        
        self.stats_label.config(text=text)
    
    def update_stats_text(self, text: str):
        # Update statistics label with custom text
        self.stats_label.config(text=text)
    
    def reset_maze(self):
        # Reset the maze to unsolved state
        
        if self.algorithm_running:
            self.algorithm_running = False
        
        if not self.maze:
            return
        
        for row in self.maze:
            for cell in row:
                cell.visited = False
                cell.in_path = False
        
        self.solve_steps = 0
        self.path_length = 0
        self.draw_maze()
        self.update_stats_text(f"Maze reset - ready to solve! Size: {self.rows}x{self.cols}")


def main():
    # Create and start the maze application
    # Initialize the main window
    root = tk.Tk()
    # Create the visualizer instance
    app = MazeVisualizer(root)
    # Start the event loop
    root.mainloop()

if __name__ == "__main__":
    main()