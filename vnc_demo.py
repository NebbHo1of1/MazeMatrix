#!/usr/bin/env python3
"""
MazeMatrix - Algorithms in Action
VNC-compatible demo for maze generation and pathfinding visualization.
This file creates a simpler, more VNC-friendly version of the application.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, Canvas, Frame, Button, Label
import random
import time
import pygame
from maze_generator import create_maze
from pathfinding import run_algorithm
import threading

# Configure environment for VNC
os.environ['DISPLAY'] = ':1'

# Initialize pygame for sound effects
pygame.init()
pygame.mixer.init()

# Define colors
COLORS = {
    "wall": "#2C3E50",           # Dark blue-gray
    "path": "#ECF0F1",           # Light gray
    "start": "#2ECC71",          # Green
    "end": "#E74C3C",            # Red
    "visited": {
        "DFS": "#3498DB",        # Blue
        "Dijkstra": "#9B59B6",   # Purple
        "A*": "#F39C12",         # Orange
        "Custom A*": "#1ABC9C"   # Turquoise
    },
    "final_path": {
        "DFS": "#2980B9",        # Darker blue
        "Dijkstra": "#8E44AD",   # Darker purple
        "A*": "#D35400",         # Darker orange
        "Custom A*": "#16A085"   # Darker turquoise
    },
    "background": "#FFFFFF"      # White background for better visibility
}

class VNCMazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MazeMatrix - Algorithms in Action")
        self.root.geometry("900x700")
        self.root.configure(background="#F0F0F0")
        
        # Default maze size
        self.maze_height = 15
        self.maze_width = 15
        
        # Initialize variables
        self.maze = None
        self.start = None
        self.end = None
        self.graph = None
        self.running = False
        self.animation_speed = 50  # ms between frames
        
        # Setup UI components
        self.setup_ui()
        
        # Generate initial maze
        self.generate_maze()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Top control panel
        control_frame = ttk.Frame(main_frame, padding=5)
        control_frame.pack(fill=tk.X, pady=5)
        
        # Maze size controls
        ttk.Label(control_frame, text="Height:").pack(side=tk.LEFT, padx=5)
        self.height_entry = ttk.Entry(control_frame, width=5)
        self.height_entry.insert(0, str(self.maze_height))
        self.height_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(control_frame, text="Width:").pack(side=tk.LEFT, padx=5)
        self.width_entry = ttk.Entry(control_frame, width=5)
        self.width_entry.insert(0, str(self.maze_width))
        self.width_entry.pack(side=tk.LEFT, padx=5)
        
        # Generate button
        self.generate_btn = ttk.Button(control_frame, text="Generate Maze", command=self.generate_maze)
        self.generate_btn.pack(side=tk.LEFT, padx=10)
        
        # Algorithm selection
        algo_frame = ttk.Frame(main_frame, padding=5)
        algo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(algo_frame, text="Select Algorithm:").pack(side=tk.LEFT, padx=5)
        
        self.algo_var = tk.StringVar(value="DFS")
        algorithms = ["DFS", "Dijkstra", "A*", "Custom A*"]
        
        for algo in algorithms:
            ttk.Radiobutton(
                algo_frame, 
                text=algo, 
                value=algo, 
                variable=self.algo_var
            ).pack(side=tk.LEFT, padx=10)
        
        # Run button
        self.run_btn = ttk.Button(algo_frame, text="Run Algorithm", command=self.run_algorithm)
        self.run_btn.pack(side=tk.LEFT, padx=10)
        
        # Canvas for maze visualization
        self.canvas_frame = ttk.Frame(main_frame, padding=5, borderwidth=2, relief="groove")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Statistics panel
        self.stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding=10)
        self.stats_frame.pack(fill=tk.X, pady=10)
        
        stats_grid = ttk.Frame(self.stats_frame)
        stats_grid.pack(fill=tk.X)
        
        # Add stats labels
        ttk.Label(stats_grid, text="Time:").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(stats_grid, text="Path Length:").grid(row=1, column=0, sticky="w", padx=5)
        ttk.Label(stats_grid, text="Nodes Explored:").grid(row=2, column=0, sticky="w", padx=5)
        
        self.time_label = ttk.Label(stats_grid, text="--")
        self.time_label.grid(row=0, column=1, sticky="w", padx=5)
        
        self.path_label = ttk.Label(stats_grid, text="--")
        self.path_label.grid(row=1, column=1, sticky="w", padx=5)
        
        self.nodes_label = ttk.Label(stats_grid, text="--")
        self.nodes_label.grid(row=2, column=1, sticky="w", padx=5)
        
        # Legend
        legend_frame = ttk.LabelFrame(main_frame, text="Legend", padding=10)
        legend_frame.pack(fill=tk.X, pady=5)
        
        self.create_legend(legend_frame)
    
    def create_legend(self, parent):
        legend_grid = ttk.Frame(parent)
        legend_grid.pack()
        
        # Function to create a colored square
        def color_square(color):
            canvas = Canvas(legend_grid, width=20, height=20, bg=color, bd=1, relief="raised")
            return canvas
        
        # Create legend items
        items = [
            ("Wall", COLORS["wall"]),
            ("Path", COLORS["path"]),
            ("Start", COLORS["start"]),
            ("End", COLORS["end"]),
            ("Visited", COLORS["visited"]["DFS"]),
            ("Final Path", COLORS["final_path"]["DFS"])
        ]
        
        for i, (text, color) in enumerate(items):
            color_square(color).grid(row=i//3, column=(i%3)*2, padx=5, pady=2)
            ttk.Label(legend_grid, text=text).grid(row=i//3, column=(i%3)*2+1, sticky="w", padx=5, pady=2)
    
    def generate_maze(self):
        try:
            # Get dimensions
            height = int(self.height_entry.get())
            width = int(self.width_entry.get())
            
            # Validate dimensions
            if height < 5 or width < 5:
                print("Maze dimensions must be at least 5x5")
                return
            
            # Update stored dimensions
            self.maze_height = height
            self.maze_width = width
            
            # Generate maze
            self.maze, self.start, self.end, self.graph = create_maze(height, width)
            
            # Clear stats
            self.clear_stats()
            
            # Print sound message instead of playing (to avoid issues)
            print("Playing sound: generate")
            
            # Render maze
            self.render_maze()
            
        except ValueError:
            print("Please enter valid integers for maze dimensions")
    
    def render_maze(self):
        # Clear canvas
        self.canvas.delete("all")
        self.cell_objects = {}
        
        if not self.maze:
            return
        
        # Get canvas dimensions
        canvas_width = self.canvas.winfo_width() or 400
        canvas_height = self.canvas.winfo_height() or 300
        
        # Calculate cell size
        maze_height = len(self.maze)
        maze_width = len(self.maze[0])
        
        cell_width = max(5, min(canvas_width // maze_width, 30))
        cell_height = max(5, min(canvas_height // maze_height, 30))
        cell_size = min(cell_width, cell_height)
        
        # Draw maze cells
        for y in range(maze_height):
            for x in range(maze_width):
                x1, y1 = x * cell_size, y * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                
                # Determine cell color
                if (y, x) == self.start:
                    color = COLORS["start"]
                elif (y, x) == self.end:
                    color = COLORS["end"]
                elif self.maze[y][x] == 1:  # Wall
                    color = COLORS["wall"]
                else:  # Path
                    color = COLORS["path"]
                
                # Create rectangle
                cell_id = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#000000",
                    width=1,
                )
                
                # Store reference to cell
                self.cell_objects[(y, x)] = cell_id
        
        # Update canvas size
        total_width = maze_width * cell_size
        total_height = maze_height * cell_size
        self.canvas.config(width=total_width, height=total_height)
    
    def run_algorithm(self):
        if not self.maze or not self.graph:
            print("Please generate a maze first")
            return
        
        if self.running:
            return
        
        self.running = True
        
        # Clear previous visualization
        self.render_maze()
        self.clear_stats()
        
        # Get selected algorithm
        algorithm = self.algo_var.get()
        
        # Run algorithm in a thread
        threading.Thread(
            target=self._run_algorithm_thread,
            args=(algorithm,),
            daemon=True
        ).start()
    
    def _run_algorithm_thread(self, algorithm):
        try:
            # Run the algorithm
            result = run_algorithm(algorithm, self.graph, self.start, self.end)
            
            # Update statistics
            self.update_stats(result)
            
            # Visualize result
            self.visualize_result(result, algorithm)
        except Exception as e:
            print(f"Error running {algorithm}: {str(e)}")
        finally:
            self.running = False
    
    def visualize_result(self, result, algorithm):
        visited = result["visited"]
        path = result["path"]
        
        # Skip start and end points to preserve their colors
        visited_filtered = [node for node in visited if node != self.start and node != self.end]
        
        # Animate the visited nodes
        for i, node in enumerate(visited_filtered):
            if not self.running:
                break
                
            y, x = node
            self.canvas.itemconfig(
                self.cell_objects.get((y, x), None),
                fill=COLORS["visited"][algorithm]
            )
            
            # Update every few steps to avoid freezing
            if i % 10 == 0:
                self.canvas.update()
                time.sleep(0.01)
        
        # Wait a moment before showing path
        time.sleep(0.5)
        
        # Animate the path
        if path:
            # Skip start and end points
            path_filtered = path[1:-1] if len(path) > 2 else []
            
            for node in path_filtered:
                if not self.running:
                    break
                    
                y, x = node
                self.canvas.itemconfig(
                    self.cell_objects.get((y, x), None),
                    fill=COLORS["final_path"][algorithm]
                )
                
                self.canvas.update()
                time.sleep(0.05)
        
        print("Playing sound: complete")
    
    def update_stats(self, result):
        time_ms = result["time_taken"] * 1000
        path_length = result["path_length"] if result["path"] else "No path found"
        nodes_explored = result["nodes_explored"]
        
        self.time_label.config(text=f"{time_ms:.2f} ms")
        self.path_label.config(text=str(path_length))
        self.nodes_label.config(text=str(nodes_explored))
    
    def clear_stats(self):
        self.time_label.config(text="--")
        self.path_label.config(text="--")
        self.nodes_label.config(text="--")

def main():
    # Create root window
    root = tk.Tk()
    
    # Create app
    app = VNCMazeApp(root)
    
    # Start main event loop
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
