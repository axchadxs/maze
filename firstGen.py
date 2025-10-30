import tkinter as tk
from tkinter import ttk
import random
from typing import List, Tuple, Dict


class MazeCell:    
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        self.walls = {'N': True, 'S': True, 'E': True, 'W': True}  # True = wall exists
        self.visited = False
        self.in_path = False
        
    def __repr__(self):
        return f"Cell({self.row}, {self.col})"


class MazeVisualizer:
    # Color scheme
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
        self.init_empty_maze()

    def init_empty_maze(self):
       
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
        
        # Size input
        size_frame = ttk.Frame(control_frame)
        size_frame.pack(side=tk.LEFT, padx=10)
        ttk.Label(size_frame, text="Maze Size:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.size_var = tk.StringVar(value="20")
        size_entry = ttk.Entry(size_frame, textvariable=self.size_var, width=6, font=("Arial", 10))
        size_entry.pack(side=tk.LEFT, padx=5)
        
        # Control buttons
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame,
            text="Generate Maze",
            command=self.generate_new_maze,
            width=20
        ).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(
            btn_frame,
            text="Solve Maze using DFS",
            command=self.solve_maze_dfs,
            width=20
        ).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(
            btn_frame,
            text="Solve Maze using BFS",
            command=self.solve_maze_bfs,
            width=20
        ).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(
            btn_frame,
            text="Reset",
            command=self.reset_maze,
            width=12
        ).pack(side=tk.LEFT, padx=3)
        
        speed_frame = ttk.Frame(control_frame)
        self.speed = 5
        
        # Statistics panel
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
        
        # Canvas for maze rendering
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH, padx=20, pady=10)
        
        self.canvas = tk.Canvas(canvas_frame, bg='white', highlightthickness=2, highlightbackground='#bdc3c7')
        self.canvas.pack(expand=True, fill=tk.BOTH)
        
        self.canvas.bind('<Configure>', lambda e: self.draw_maze())
    
    def generate_new_maze(self):
        if self.algorithm_running:
            return
        
        # Validate size input
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
        
        self.maze = [[MazeCell(r, c) for c in range(self.cols)] for r in range(self.rows)]
        
        # Generate maze instantly without animation
        self.generate_maze_instant()
        
        self.canvas.delete("all")
        self.draw_maze()
        self.update_stats_text(f"Maze generated. Size: {self.rows}x{self.cols}")
    
    def generate_maze_instant(self):
        # Generate maze using DFS without visualization (instant, non-animated)
        stack = [(0, 0)]
        self.maze[0][0].visited = True
        
        while stack:
            row, col = stack[-1]
            current = self.maze[row][col]
            
            # Define all four directions
            directions = [
                ('N', -1, 0),
                ('S', 1, 0),
                ('E', 0, 1),
                ('W', 0, -1)
            ]
            
            # Find unvisited neighbors
            neighbors = []
            for direction, dr, dc in directions:
                nr, nc = row + dr, col + dc
                if (0 <= nr < self.rows and 0 <= nc < self.cols and
                        not self.maze[nr][nc].visited):
                    neighbors.append((direction, nr, nc))
            
            if neighbors:
                # Choose random neighbor
                direction, nr, nc = random.choice(neighbors)
                
                # Remove walls
                current.walls[direction] = False
                opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
                self.maze[nr][nc].walls[opposite[direction]] = False
                
                self.maze[nr][nc].visited = True
                stack.append((nr, nc))
            else:
                stack.pop()
        
        # Reset visited flags for solving
        for row in self.maze:
            for cell in row:
                cell.visited = False
    
    def solve_maze_dfs(self):
       
        if self.algorithm_running:
            return
        
        if not self.maze:
            self.update_stats_text("Error: generate a maze first")
            return
        
        # Reset cell states
        for row in self.maze:
            for cell in row:
                cell.visited = False
                cell.in_path = False
        
        self.solve_steps = 0
        self.path_length = 0
        self.algorithm_running = True
        
        self.update_stats_text("Solving maze...")
        self.root.after(10, lambda: self.dfs_solve(self.start[0], self.start[1], []))
    
    def solve_maze_bfs(self):
        # Initialize and start BFS maze solving with animation
        if self.algorithm_running:
            return
        
        if not self.maze:
            self.update_stats_text("Error: generate a maze first")
            return
        
        # Reset cell states
        for row in self.maze:
            for cell in row:
                cell.visited = False
                cell.in_path = False
        
        self.solve_steps = 0
        self.path_length = 0
        self.algorithm_running = True
        
        self.update_stats_text("Solving maze with BFS...")
        
        # Initialize BFS queue: (row, col, path_taken)
        queue = [(self.start[0], self.start[1], [])]
        
        self.root.after(10, lambda: self.bfs_solve_step(queue))

    def bfs_solve_step(self, queue: List[Tuple[int, int, List[Tuple[int, int]]]]):
        # Process one BFS step with animation (called repeatedly via after)
        if not self.algorithm_running or not queue:
            if not queue and self.algorithm_running:
                self.algorithm_running = False
                self.update_stats_text("No solution found!")
            return
        
        # Dequeue (FIFO)
        row, col, path = queue.pop(0)
        
        current = self.maze[row][col]
        if current.visited:
            delay = max(1, 50 - self.speed * 4)
            self.root.after(delay, lambda: self.bfs_solve_step(queue))
            return
        
        # Mark visited and update path
        current.visited = True
        path = path + [(row, col)]
        self.solve_steps += 1
        
        # Check if reached goal
        if (row, col) == self.end:
            for r, c in path:
                self.maze[r][c].in_path = True
            self.path_length = len(path)
            self.algorithm_running = False
            self.draw_maze()
            
            efficiency = (self.path_length / self.solve_steps * 100) if self.solve_steps > 0 else 0
            self.update_stats_text(
                f"SOLVED with BFS! Path Length: {self.path_length} | "
                f"Cells Explored: {self.solve_steps} | "
                f"Efficiency: {efficiency:.1f}%"
            )
            return
        
        # Update display
        self.draw_maze()
        self.update_stats()
        
        # Add neighbors to queue
        if not current.walls['N'] and row - 1 >= 0 and not self.maze[row - 1][col].visited:
            queue.append((row - 1, col, path))
        if not current.walls['S'] and row + 1 < self.rows and not self.maze[row + 1][col].visited:
            queue.append((row + 1, col, path))
        if not current.walls['E'] and col + 1 < self.cols and not self.maze[row][col + 1].visited:
            queue.append((row, col + 1, path))
        if not current.walls['W'] and col - 1 >= 0 and not self.maze[row][col - 1].visited:
            queue.append((row, col - 1, path))
        
        # Continue to next step
        delay = max(1, 50 - self.speed * 4)
        self.root.after(delay, lambda: self.bfs_solve_step(queue))
    
    def dfs_solve(self, row: int, col: int, path: List[Tuple[int, int]]) -> bool:
        if not self.algorithm_running:
            return False
        
        # Check if reached destination
        if (row, col) == self.end:
            path.append((row, col))
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
        
        # Check all accessible directions (no walls)
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
        
        for dr, dc in moves:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                self.root.after(delay)
                self.root.update()
                if self.dfs_solve(nr, nc, path[:]):
                    return True
        
        return False
    
    def draw_maze(self):
        self.canvas.delete("all")
        
        # Calculate cell size to fit canvas
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
                
                # Determine cell color
                color = self.COLOR_EMPTY
                if (row, col) == self.start:
                    color = self.COLOR_START
                elif (row, col) == self.end:
                    color = self.COLOR_END
                elif cell.in_path:
                    color = self.COLOR_PATH
                elif cell.visited:
                    color = self.COLOR_VISITED
                
                # Draw cell background
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
        if solved:
            efficiency = (self.path_length / self.solve_steps * 100) if self.solve_steps > 0 else 0
            text = f"Found solution! Length: {self.path_length}, Explored {self.solve_steps} cells"
        elif self.solve_steps > 0:
            text = f"Finding path... ({self.solve_steps} cells checked)"
        else:
            text = f"Creating maze... ({self.gen_steps}/{self.rows * self.cols})"
        
        self.stats_label.config(text=text)
    
    def update_stats_text(self, text: str):
        self.stats_label.config(text=text)
    
    def reset_maze(self):
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
    root = tk.Tk()
    app = MazeVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()