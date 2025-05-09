# MazeMatrix - Algorithms in Action

An interactive desktop and web application for visualizing maze generation and pathfinding algorithms, providing dynamic and engaging learning experiences through advanced visualization techniques.

## Overview

MazeMatrix is an educational tool designed to demonstrate the differences between various pathfinding algorithms through visual representation. The application generates random mazes and allows users to watch multiple algorithms solve the same maze simultaneously, comparing their efficiency and approaches.

## Features

- **Dynamic Maze Generation**: Creates random mazes using Randomized Prim's algorithm
- **Multiple Pathfinding Algorithms**:
  - Depth-First Search (DFS)
  - Dijkstra's Algorithm
  - A* with Manhattan distance heuristic
  - Custom A* with Euclidean distance heuristic
- **Real-time Visualization**: Animated exploration and path-finding
- **Performance Statistics**: Compares algorithms based on:
  - Execution time
  - Path length
  - Nodes explored
- **Interactive Controls**:
  - Adjustable maze dimensions
  - Animation speed controls
  - Algorithm selection
- **Multiple Application Versions**:
  - Web application (Flask)
  - Desktop application (PyGame)
  - VNC-compatible version

## Getting Started

### Web Application

1. Run the web application:
   ```
   python web_app.py
   ```
2. Open your browser and navigate to http://localhost:5000

### Desktop Application

1. Run the desktop application:
   ```
   python main.py
   ```

### PyGame Demo

1. Run the PyGame demo:
   ```
   python pygame_demo.py
   ```

## Using the Application

1. **Generate a Maze**: Set the desired dimensions and click "Generate Maze"
2. **Select Algorithms**: Choose one or more pathfinding algorithms to run
3. **Run Algorithms**: Click "Run Algorithms" to start the visualization
4. **Analyze Results**: Compare the performance statistics for each algorithm
5. **Adjust Animation Speed**: Use the speed slider to control visualization pace

## Files and Components

- `web_app.py` - Flask web application entry point
- `main.py` - Desktop application entry point
- `maze_generator.py` - Maze generation algorithms
- `pathfinding.py` - Pathfinding algorithm implementations
- `visualization.py` - Visualization and animation components
- `utils.py` - Utility functions and helper methods
- `pygame_demo.py` - PyGame-based demo version
- `vnc_demo.py` - VNC-compatible demo version
- `gui.py` - GUI components for desktop application

## Technologies Used

- **Backend**: Python
- **Web Framework**: Flask
- **Visualization**: HTML5 Canvas, PyGame
- **Frontend**: JavaScript, HTML, CSS

## Educational Value

This application serves as an educational tool for understanding:
- How different pathfinding algorithms work
- Trade-offs between algorithms (speed vs. optimality)
- Maze generation techniques
- Algorithm visualization techniques

## Performance Notes

- Maximum recommended maze size: 30x30 (for optimal performance)
- Larger mazes may result in slower animation and processing
- Multiple algorithms can be run simultaneously for comparison

## Future Enhancements

- Additional maze generation algorithms
- More pathfinding algorithms
- Custom maze creation by users
- 3D maze visualization
- Additional performance metrics

---

Created as an educational demonstration tool for algorithm visualization and comparison.
