# Maze Generator & Solver 🧩

A Python-based maze generator and solver with real-time visualization using Tkinter. Watch as mazes are created using recursive backtracking and then solved using depth-first search algorithms.

## ✨ Features

- **Dynamic Maze Generation** - Creates unique mazes using recursive backtracking DFS algorithm
- **Pathfinding Visualization** - Watch the solver explore the maze in real-time
- **Interactive Controls** - Adjustable maze size (5x5 to 50x50)
- **Real-Time Statistics** - Track generation steps, path length, and solving efficiency
- **Responsive Design** - Automatically resizes to fit window dimensions
- **Color-Coded Visualization**:
  - Purple: Start and end points
  - Blue: Explored cells during solving
  - Red: Final solution path
  - Black: Maze walls

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- tkinter (usually comes pre-installed with Python)

### Installation

Run in Visual Studio Code
1. Open the project folder in VS Code
2. Select a Python interpreter (bottom-right)
3. Open `firstGen.py` and click "Run Python File in Terminal" or press F5 to debug


### Quick Start
1. Click "Generate Maze" to create a random maze
2. Choose a solver and click the appropriate button:
  - "Solve Maze using DFS" — explores until it finds a path (first-found)
  - "Solve Maze using BFS" — finds the shortest path in number of steps
3. Adjust the maze size and generate new mazes
4. Use "Reset" to clear the solution and try again

## 🛠️ Technical Details

### Algorithms

**Maze Generation: Recursive Backtracking**
- Starts at a random cell and marks it as visited
- Randomly selects an unvisited neighbor and removes the wall between them
- Recursively visits the new cell
- Backtracks when no unvisited neighbors remain
- Creates perfect mazes with exactly one solution

**Pathfinding: Depth-First Search (DFS)**
- Explores as far as possible along each branch
- Backtracks when hitting dead ends
- Guarantees finding a solution if one exists
- Visualizes the exploration process in real-time

**Pathfinding: Breadth-First Search (BFS)**
- Finds the shortest path (in number of steps) on an unweighted grid
- Explores nodes by layers outward from the start until it reaches the end
- Implemented: BFS is available as an alternative solver in the app
- Useful when you want the shortest route rather than the first-found route

### Technologies
- **Python 3** - Core programming language
- **Tkinter** - GUI framework for visualization
- **Type Hints** - Enhanced code readability

### Project Structure
```
maze/
│
├── firstGen.py    # Main application file (current)
└── README.md      # Documentation
```

### Code Highlights
- Object-oriented design with `MazeCell` and `MazeVisualizer` classes
- Type annotations for better code clarity
- Efficient wall representation using dictionaries
- Dynamic canvas resizing for responsive UI
- Real-time statistics tracking

##  Statistics Display

The app tracks and displays:
- **Generation Steps** - Total cells processed during maze creation
- **Path Length** - Number of cells in the solution path
- **Cells Explored** - Total cells visited during pathfinding
- **Efficiency** - Ratio of path length to cells explored (%)

## 🔮 Future Enhancements

- [ ] Additional solving algorithms (A*, Dijkstra)
- [ ] Different maze generation algorithms (Prim's, Kruskal's)
- [ ] Export maze as image
- [ ] Save/load maze configurations
- [ ] Adjustable animation speed slider
- [ ] Compare multiple algorithms side-by-side
- [ ] 3D maze visualization

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs or issues
- Suggest new features or algorithms
- Submit pull requests
- Improve documentation

---

**Created by Alex** | Python + Tkinter Visualization Project