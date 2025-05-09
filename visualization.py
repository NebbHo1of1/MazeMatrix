"""
Module for visualizing mazes and pathfinding algorithms.
This module contains functions for rendering mazes, animating pathfinding,
and creating visual effects.
"""

import time
import tkinter as tk
from tkinter import Canvas
import random

# Define colors for visualization
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
    "background": "#34495E"      # Dark slate
}

class MazeVisualizer:
    """Class for visualizing mazes and pathfinding algorithms."""
    
    def __init__(self, canvas, maze, start, end, cell_size=20):
        """
        Initialize the MazeVisualizer.
        
        Args:
            canvas (tk.Canvas): Canvas widget to draw on.
            maze (list): 2D list representing the maze.
            start (tuple): Starting point (y, x).
            end (tuple): End point (y, x).
            cell_size (int): Size of each cell in pixels.
        """
        self.canvas = canvas
        self.maze = maze
        self.start = start
        self.end = end
        self.cell_size = cell_size
        self.height = len(maze)
        self.width = len(maze[0])
        self.canvas_objects = {}
        self.animation_speed = 10  # ms between animation frames
        
    def render_maze(self):
        """
        Render the maze on the canvas.
        
        Returns:
            None
        """
        # Clear canvas
        self.canvas.delete("all")
        self.canvas_objects = {}
        
        # Create a background
        self.canvas.configure(bg=COLORS["background"])
        
        # Get canvas dimensions to ensure proper scaling
        canvas_width = self.canvas.winfo_width() or 400
        canvas_height = self.canvas.winfo_height() or 300
        
        # Calculate optimal cell size to fit the canvas
        max_cell_width = canvas_width / self.width
        max_cell_height = canvas_height / self.height
        self.cell_size = min(max_cell_width, max_cell_height, 30)  # Cap at 30 pixels
        
        # Draw maze cells
        for y in range(self.height):
            for x in range(self.width):
                x1, y1 = x * self.cell_size, y * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                # Determine the cell type
                if (y, x) == self.start:
                    color = COLORS["start"]
                    # Add a distinctive start marker
                    cell_id = self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color,
                        outline="white",
                        width=1,
                        tags=f"cell_{y}_{x}"
                    )
                    # Add an arrow or symbol to indicate start
                    if self.cell_size >= 10:  # Only add details if cells are big enough
                        self.canvas.create_polygon(
                            x1 + self.cell_size/2, y1 + self.cell_size/4,
                            x1 + self.cell_size*3/4, y1 + self.cell_size*3/4,
                            x1 + self.cell_size/4, y1 + self.cell_size*3/4,
                            fill="white",
                            tags=f"start_symbol_{y}_{x}"
                        )
                elif (y, x) == self.end:
                    color = COLORS["end"]
                    # Add a distinctive end marker
                    cell_id = self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color,
                        outline="white",
                        width=1,
                        tags=f"cell_{y}_{x}"
                    )
                    # Add a square to indicate end
                    if self.cell_size >= 10:  # Only add details if cells are big enough
                        self.canvas.create_rectangle(
                            x1 + self.cell_size/4, y1 + self.cell_size/4,
                            x1 + self.cell_size*3/4, y1 + self.cell_size*3/4,
                            fill="white",
                            tags=f"end_symbol_{y}_{x}"
                        )
                elif self.maze[y][x] == 1:  # Wall
                    color = COLORS["wall"]
                    # Add texture to walls
                    cell_id = self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color,
                        outline="#1C2E40",
                        width=1,
                        tags=f"cell_{y}_{x}"
                    )
                    # Add texture lines if cells are big enough
                    if self.cell_size >= 8:
                        self.canvas.create_line(
                            x1, y1, x2, y2,
                            fill="#1C2E40",
                            width=0.5,
                            tags=f"wall_texture1_{y}_{x}"
                        )
                        self.canvas.create_line(
                            x1, y2, x2, y1,
                            fill="#1C2E40",
                            width=0.5,
                            tags=f"wall_texture2_{y}_{x}"
                        )
                else:  # Path
                    color = COLORS["path"]
                    cell_id = self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        fill=color,
                        outline="#DCE0E1",
                        width=0.5,
                        tags=f"cell_{y}_{x}"
                    )
                
                self.canvas_objects[(y, x)] = cell_id
        
        # Update canvas dimensions to fit the maze
        total_width = self.width * self.cell_size
        total_height = self.height * self.cell_size
        self.canvas.config(scrollregion=(0, 0, total_width, total_height))
        
    def animate_pathfinding(self, visited, path, algorithm, callback=None):
        """
        Animate the pathfinding process.
        
        Args:
            visited (list): List of visited nodes in order.
            path (list): Final path from start to end.
            algorithm (str): Name of the algorithm being visualized.
            callback (function): Function to call when animation completes.
            
        Returns:
            None
        """
        # Skip start and end in visited list to preserve their colors
        visited_filtered = [node for node in visited if node != self.start and node != self.end]
        
        # Create a recursive function to animate step by step
        def animate_step(idx=0, phase="visited"):
            if phase == "visited" and idx < len(visited_filtered):
                node = visited_filtered[idx]
                y, x = node
                self.canvas.itemconfig(
                    self.canvas_objects[(y, x)],
                    fill=COLORS["visited"][algorithm]
                )
                self.canvas.update_idletasks()
                self.canvas.after(self.animation_speed, animate_step, idx + 1, phase)
            
            elif phase == "visited" and idx >= len(visited_filtered):
                # Move to the path phase
                self.canvas.after(self.animation_speed * 3, animate_step, 0, "path")
            
            elif phase == "path" and idx < len(path) and path is not None:
                # Skip start and end in path to preserve their colors
                if idx > 0 and idx < len(path) - 1:  # Skip start and end
                    node = path[idx]
                    y, x = node
                    self.canvas.itemconfig(
                        self.canvas_objects[(y, x)],
                        fill=COLORS["final_path"][algorithm]
                    )
                self.canvas.update_idletasks()
                self.canvas.after(self.animation_speed * 2, animate_step, idx + 1, phase)
            
            elif phase == "path" and (idx >= len(path) or path is None):
                # Animation complete
                if callback:
                    callback()
        
        # Start the animation
        animate_step()
    
    def set_animation_speed(self, speed):
        """
        Set the animation speed.
        
        Args:
            speed (int): Animation speed in milliseconds between frames.
            
        Returns:
            None
        """
        self.animation_speed = speed
    
    def adjust_cell_size(self, new_size):
        """
        Adjust the cell size and re-render the maze.
        
        Args:
            new_size (int): New cell size in pixels.
            
        Returns:
            None
        """
        self.cell_size = new_size
        self.render_maze()
    
    def add_visual_effect(self, node, effect_type="pulse"):
        """
        Add a visual effect to a specific node.
        
        Args:
            node (tuple): The node (y, x) to apply the effect to.
            effect_type (str): Type of effect ("pulse", "glow", etc.).
            
        Returns:
            None
        """
        y, x = node
        if (y, x) not in self.canvas_objects:
            return
        
        cell_id = self.canvas_objects[(y, x)]
        
        if effect_type == "pulse":
            # Create a pulsing effect
            def pulse(count=0, growing=True):
                if count > 10:  # End the effect after a few pulses
                    return
                
                # Get current fill color
                color = self.canvas.itemcget(cell_id, "fill")
                
                # Create a temporary overlay for the pulse effect
                x1, y1, x2, y2 = self.canvas.coords(cell_id)
                shrink = self.cell_size * 0.2 if growing else 0
                
                overlay_id = self.canvas.create_rectangle(
                    x1 + shrink, y1 + shrink,
                    x2 - shrink, y2 - shrink,
                    fill=color,
                    outline=COLORS["background"],
                    width=2
                )
                
                # Schedule next pulse and remove overlay
                self.canvas.after(100, lambda: self.canvas.delete(overlay_id))
                self.canvas.after(200, pulse, count + 1, not growing)
            
            pulse()
        
        elif effect_type == "glow":
            # Create a glow effect
            x1, y1, x2, y2 = self.canvas.coords(cell_id)
            
            # Add a glow outline
            glow_id = self.canvas.create_rectangle(
                x1 - 2, y1 - 2, x2 + 2, y2 + 2,
                outline="#FFD700",  # Gold color
                width=2
            )
            
            # Fade out the glow
            def fade_glow(alpha=1.0):
                if alpha <= 0:
                    self.canvas.delete(glow_id)
                    return
                
                # Adjust opacity by changing the outline color
                alpha_hex = int(alpha * 255)
                self.canvas.itemconfig(
                    glow_id,
                    outline=f"#FFD700{alpha_hex:02X}"
                )
                
                self.canvas.after(50, fade_glow, alpha - 0.1)
            
            self.canvas.after(500, fade_glow)
