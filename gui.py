"""
Main GUI module for the Maze Generation and Pathfinding Visualization application.
This module integrates all components into a cohesive application.
"""

import tkinter as tk
from tkinter import ttk, messagebox, Frame, LabelFrame, StringVar, IntVar, Canvas, Scale, HORIZONTAL
import time
import threading
import random

from maze_generator import create_maze
from pathfinding import run_algorithm
from visualization import MazeVisualizer
from utils import play_sound, timed_callback

class MazeApp:
    """Main application class for the Maze Visualization application."""
    
    def __init__(self, root):
        """
        Initialize the application.
        
        Args:
            root (tk.Tk): Root window for the application.
        """
        self.root = root
        self.maze = None
        self.start = None
        self.end = None
        self.graph = None
        self.visualizers = {}
        self.algorithm_frames = {}
        self.results = {}
        self.running = False
        
        # Set default maze dimensions
        self.default_height = 21
        self.default_width = 31
        
        # Set up the GUI
        self.setup_gui()
        
        # Generate an initial maze
        self.generate_maze()
    
    def setup_gui(self):
        """Set up the GUI components."""
        # Configure the root window
        self.root.geometry("1024x768")
        self.root.configure(bg="#F0F0F0")
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create control panel
        self.setup_control_panel()
        
        # Create visualization area
        self.setup_visualization_area()
        
        # Set up style
        self.setup_styles()
        
        # Update idletasks to ensure widgets are properly initialized
        self.root.update_idletasks()
    
    def setup_styles(self):
        """Set up custom styles for the application."""
        style = ttk.Style()
        
        # Configure default styles
        style.configure("TFrame", background="#F0F0F0")
        style.configure("TLabel", background="#F0F0F0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"))
        style.configure("TCheckbutton", background="#F0F0F0", font=("Arial", 10))
        
        # Configure specific styles
        style.configure("Header.TLabel", font=("Arial", 14, "bold"))
        style.configure("Stats.TLabel", font=("Arial", 9))
        style.configure("StatsHeader.TLabel", font=("Arial", 9, "bold"))
    
    def setup_control_panel(self):
        """Set up the control panel with input fields and action buttons."""
        # Create control panel frame
        self.control_panel = ttk.LabelFrame(self.main_frame, text="Controls", padding="10")
        self.control_panel.pack(fill=tk.X, padx=10, pady=5)
        
        # Create maze dimension inputs
        dimension_frame = ttk.Frame(self.control_panel)
        dimension_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(dimension_frame, text="Height:").pack(side=tk.LEFT, padx=5)
        self.height_var = tk.StringVar(value=str(self.default_height))
        ttk.Entry(dimension_frame, textvariable=self.height_var, width=5).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(dimension_frame, text="Width:").pack(side=tk.LEFT, padx=5)
        self.width_var = tk.StringVar(value=str(self.default_width))
        ttk.Entry(dimension_frame, textvariable=self.width_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Create algorithm selection
        algo_frame = ttk.Frame(self.control_panel)
        algo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(algo_frame, text="Select Algorithms:").pack(side=tk.LEFT, padx=5)
        
        # Create checkboxes for algorithms
        self.algo_vars = {
            "DFS": tk.BooleanVar(value=True),
            "Dijkstra": tk.BooleanVar(value=True),
            "A*": tk.BooleanVar(value=True),
            "Custom A*": tk.BooleanVar(value=True)
        }
        
        for i, (algo_name, var) in enumerate(self.algo_vars.items()):
            ttk.Checkbutton(
                algo_frame,
                text=algo_name,
                variable=var,
                command=self.update_layout
            ).pack(side=tk.LEFT, padx=10)
        
        # Create action buttons
        button_frame = ttk.Frame(self.control_panel)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            button_frame,
            text="Generate Maze",
            command=self.generate_maze
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Run Algorithms",
            command=self.run_algorithms
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Stop",
            command=self.stop_algorithms
        ).pack(side=tk.LEFT, padx=5)
        
        # Animation speed slider
        speed_frame = ttk.Frame(self.control_panel)
        speed_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(speed_frame, text="Animation Speed:").pack(side=tk.LEFT, padx=5)
        
        self.speed_var = tk.IntVar(value=10)
        self.speed_slider = ttk.Scale(
            speed_frame,
            from_=1,
            to=50,
            orient=tk.HORIZONTAL,
            variable=self.speed_var,
            length=200
        )
        self.speed_slider.pack(side=tk.LEFT, padx=5)
        
        # Add a label to show the current value
        self.speed_label = ttk.Label(speed_frame, text="10 ms")
        self.speed_label.pack(side=tk.LEFT, padx=5)
        
        # Update label when slider changes
        self.speed_var.trace_add("write", self.update_speed_label)
    
    def update_speed_label(self, *args):
        """Update the speed label with the current slider value."""
        self.speed_label.config(text=f"{self.speed_var.get()} ms")
    
    def setup_visualization_area(self):
        """Set up the area for maze visualization."""
        # Create visualization frame
        self.viz_frame = ttk.Frame(self.main_frame, padding="10")
        self.viz_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Initialize with a 2x2 grid for four algorithms
        self.setup_algorithm_frames(2, 2)
    
    def setup_algorithm_frames(self, rows, cols):
        """
        Set up frames for algorithm visualization.
        
        Args:
            rows (int): Number of rows in the grid.
            cols (int): Number of columns in the grid.
        """
        # Clear existing frames
        for frame in self.algorithm_frames.values():
            frame.destroy()
        self.algorithm_frames = {}
        self.visualizers = {}
        
        # Get selected algorithms
        selected_algos = [algo for algo, var in self.algo_vars.items() if var.get()]
        
        # Calculate cell width and height for the grid
        cell_width = 100 // cols
        cell_height = 100 // rows
        
        # Create frames for each algorithm
        for i, algo in enumerate(selected_algos):
            if i >= rows * cols:
                break
                
            row = i // cols
            col = i % cols
            
            # Create a frame for the algorithm
            frame = ttk.LabelFrame(self.viz_frame, text=algo, padding="5")
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            
            # Configure row and column to expand
            self.viz_frame.rowconfigure(row, weight=1)
            self.viz_frame.columnconfigure(col, weight=1)
            
            # Create a canvas for maze visualization
            canvas = Canvas(frame, bg="white")
            canvas.pack(fill=tk.BOTH, expand=True)
            
            # Create a stats frame
            stats_frame = ttk.Frame(frame, padding="5")
            stats_frame.pack(fill=tk.X)
            
            # Add stats labels
            ttk.Label(stats_frame, text="Time:", style="StatsHeader.TLabel").grid(row=0, column=0, sticky="w")
            ttk.Label(stats_frame, text="Path Length:", style="StatsHeader.TLabel").grid(row=1, column=0, sticky="w")
            ttk.Label(stats_frame, text="Nodes Explored:", style="StatsHeader.TLabel").grid(row=2, column=0, sticky="w")
            
            time_var = StringVar(value="--")
            path_var = StringVar(value="--")
            nodes_var = StringVar(value="--")
            
            ttk.Label(stats_frame, textvariable=time_var, style="Stats.TLabel").grid(row=0, column=1, sticky="w")
            ttk.Label(stats_frame, textvariable=path_var, style="Stats.TLabel").grid(row=1, column=1, sticky="w")
            ttk.Label(stats_frame, textvariable=nodes_var, style="Stats.TLabel").grid(row=2, column=1, sticky="w")
            
            # Store frames and variables
            self.algorithm_frames[algo] = {
                "frame": frame,
                "canvas": canvas,
                "stats_frame": stats_frame,
                "time_var": time_var,
                "path_var": path_var,
                "nodes_var": nodes_var
            }
    
    def update_layout(self):
        """Update the layout based on selected algorithms."""
        selected_algos = [algo for algo, var in self.algo_vars.items() if var.get()]
        num_algos = len(selected_algos)
        
        if num_algos == 0:
            messagebox.showwarning("Warning", "Please select at least one algorithm.")
            # Re-select the first algorithm
            self.algo_vars["DFS"].set(True)
            selected_algos = ["DFS"]
            num_algos = 1
        
        # Determine grid layout based on number of selected algorithms
        if num_algos == 1:
            rows, cols = 1, 1
        elif num_algos == 2:
            rows, cols = 1, 2
        elif num_algos == 3:
            rows, cols = 1, 3
        else:  # 4 algorithms
            rows, cols = 2, 2
        
        # Update frames
        self.setup_algorithm_frames(rows, cols)
        
        # Render maze in each frame if maze exists
        if self.maze:
            self.render_maze_in_frames()
    
    def generate_maze(self):
        """Generate a new maze based on user input."""
        try:
            # Get dimensions from input fields
            height = int(self.height_var.get())
            width = int(self.width_var.get())
            
            # Validate dimensions
            if height < 5 or width < 5:
                messagebox.showerror("Error", "Maze dimensions must be at least 5x5.")
                return
            
            # Generate maze
            self.maze, self.start, self.end, self.graph = create_maze(height, width)
            
            # Play sound effect for maze generation
            play_sound("generate")
            
            # Update the visualization
            self.render_maze_in_frames()
            
            # Clear previous results
            self.results = {}
            self.clear_stats()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid integer dimensions.")
    
    def render_maze_in_frames(self):
        """Render the maze in each algorithm frame."""
        if not self.maze:
            return
        
        # Clear existing visualizers
        self.visualizers = {}
        
        # Create visualizers for each selected algorithm
        for algo, frame_data in self.algorithm_frames.items():
            canvas = frame_data["canvas"]
            
            # Determine appropriate cell size based on maze dimensions
            height, width = len(self.maze), len(self.maze[0])
            canvas_width = canvas.winfo_width() or 400  # Default if not yet rendered
            canvas_height = canvas.winfo_height() or 300  # Default if not yet rendered
            
            cell_size_w = canvas_width // width
            cell_size_h = canvas_height // height
            cell_size = min(cell_size_w, cell_size_h, 30)  # Cap at 30 pixels
            
            # Create visualizer
            visualizer = MazeVisualizer(canvas, self.maze, self.start, self.end, cell_size)
            visualizer.render_maze()
            
            # Store visualizer
            self.visualizers[algo] = visualizer
    
    def run_algorithms(self):
        """Run the selected pathfinding algorithms."""
        if not self.maze:
            messagebox.showerror("Error", "Please generate a maze first.")
            return
        
        # If already running, don't start again
        if self.running:
            return
        
        self.running = True
        
        # Clear previous results
        self.results = {}
        self.clear_stats()
        
        # Get selected algorithms
        selected_algos = [algo for algo, var in self.algo_vars.items() if var.get()]
        
        # Re-render maze for clean visualization
        self.render_maze_in_frames()
        
        # Run algorithms in separate threads
        for algo in selected_algos:
            threading.Thread(
                target=self.run_algorithm,
                args=(algo,),
                daemon=True
            ).start()
    
    def run_algorithm(self, algorithm):
        """
        Run a specific pathfinding algorithm.
        
        Args:
            algorithm (str): Name of the algorithm to run.
        """
        try:
            # Run the algorithm
            result = run_algorithm(algorithm, self.graph, self.start, self.end)
            
            # Store the result
            self.results[algorithm] = result
            
            # Update statistics
            self.update_stats(algorithm, result)
            
            # Get the animation speed
            animation_speed = self.speed_var.get()
            self.visualizers[algorithm].set_animation_speed(animation_speed)
            
            # Animate the pathfinding
            self.visualizers[algorithm].animate_pathfinding(
                result["visited"],
                result["path"],
                algorithm,
                lambda: self.add_completion_effect(algorithm)
            )
            
        except Exception as e:
            messagebox.showerror("Error", f"Error running {algorithm}: {str(e)}")
        finally:
            # Check if all algorithms have completed
            if len(self.results) == len([algo for algo, var in self.algo_vars.items() if var.get()]):
                self.running = False
    
    def add_completion_effect(self, algorithm):
        """
        Add a completion effect when an algorithm finishes.
        
        Args:
            algorithm (str): Name of the algorithm that completed.
        """
        # Play a completion sound
        play_sound("complete")
        
        # Add visual effects to the end node
        self.visualizers[algorithm].add_visual_effect(self.end, "glow")
    
    def update_stats(self, algorithm, result):
        """
        Update the statistics display for an algorithm.
        
        Args:
            algorithm (str): Name of the algorithm.
            result (dict): Result data from the algorithm.
        """
        if algorithm not in self.algorithm_frames:
            return
        
        frame_data = self.algorithm_frames[algorithm]
        
        # Update stats
        time_ms = result["time_taken"] * 1000  # Convert to milliseconds
        path_length = result["path_length"] if result["path"] else "No path found"
        nodes_explored = result["nodes_explored"]
        
        frame_data["time_var"].set(f"{time_ms:.2f} ms")
        frame_data["path_var"].set(str(path_length))
        frame_data["nodes_var"].set(str(nodes_explored))
    
    def clear_stats(self):
        """Clear the statistics display for all algorithms."""
        for frame_data in self.algorithm_frames.values():
            frame_data["time_var"].set("--")
            frame_data["path_var"].set("--")
            frame_data["nodes_var"].set("--")
    
    def stop_algorithms(self):
        """Stop all running algorithms."""
        self.running = False
        
        # Re-render maze to clear visualizations
        self.render_maze_in_frames()
        
        # Clear results
        self.results = {}
        self.clear_stats()
