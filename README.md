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

1. Clone the repository
2. Open in IDE 
3. Run the application


### Quick Start
1. Click "Generate Maze" to create a random maze
2. Click "Solve Maze" to watch it find the solution
3. Adjust the maze size and generate new mazes
4. Use "Reset" to clear the solution and solve again

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

### Technologies
- **Python 3** - Core programming language
- **Tkinter** - GUI framework for visualization
- **Type Hints** - Enhanced code readability

### Project Structure
```
maze-generator-solver/
│
├── maze_visualizer.py    # Main application file
└── README.md            # Documentation
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

- [ ] Additional solving algorithms (BFS, A*, Dijkstra)
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
