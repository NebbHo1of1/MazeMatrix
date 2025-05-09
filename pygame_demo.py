#!/usr/bin/env python3
"""
MazeMatrix - Algorithms in Action
PyGame Demo for maze generation and pathfinding visualization.
This file creates a PyGame-based version which should be more compatible with VNC.
"""

import os
import sys
import time
import pygame
import threading
import random
from maze_generator import create_maze
from pathfinding import run_algorithm

# Initialize pygame
pygame.init()

# Define colors
COLORS = {
    "wall": (44, 62, 80),        # Dark blue-gray
    "path": (236, 240, 241),     # Light gray
    "start": (46, 204, 113),     # Green
    "end": (231, 76, 60),        # Red
    "visited": {
        "DFS": (52, 152, 219),   # Blue
        "Dijkstra": (155, 89, 182),  # Purple
        "A*": (243, 156, 18),    # Orange
        "Custom A*": (26, 188, 156)  # Turquoise
    },
    "final_path": {
        "DFS": (41, 128, 185),   # Darker blue
        "Dijkstra": (142, 68, 173),  # Darker purple
        "A*": (211, 84, 0),      # Darker orange
        "Custom A*": (22, 160, 133)  # Darker turquoise
    },
    "background": (255, 255, 255),  # White
    "text": (0, 0, 0),           # Black
    "button": (189, 195, 199),   # Light gray
    "button_hover": (149, 165, 166),  # Gray
    "button_text": (0, 0, 0),    # Black
}

class Button:
    def __init__(self, x, y, width, height, text, callback):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
    
    def draw(self, screen, font):
        color = COLORS["button_hover"] if self.hovered else COLORS["button"]
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, COLORS["text"], self.rect, 1)  # Border
        
        text_surface = font.render(self.text, True, COLORS["button_text"])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
    
    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
            return True
        return False

class PyGameMazeApp:
    def __init__(self):
        # Set up display
        self.screen_width = 1024
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("MazeMatrix - Algorithms in Action")
        
        # Set up clock
        self.clock = pygame.time.Clock()
        
        # Set up fonts
        self.font = pygame.font.SysFont('Arial', 16)
        self.title_font = pygame.font.SysFont('Arial', 20, bold=True)
        
        # Default maze size
        self.maze_height = 15
        self.maze_width = 15
        
        # Initialize maze variables
        self.maze = None
        self.start = None
        self.end = None
        self.graph = None
        self.cell_size = 20
        
        # Initialize algorithm variables
        self.selected_algorithm = "DFS"
        self.algorithms = ["DFS", "Dijkstra", "A*", "Custom A*"]
        self.running = False
        self.result = None
        
        # Create UI elements
        self.create_ui_elements()
        
        # Generate initial maze
        self.generate_maze()
        
        # Running flag
        self.running = False
    
    def create_ui_elements(self):
        # Create buttons
        self.buttons = []
        
        # Generate maze button
        self.buttons.append(Button(
            20, 20, 150, 30, 
            "Generate Maze", 
            self.generate_maze
        ))
        
        # Run algorithm button
        self.buttons.append(Button(
            20, 60, 150, 30, 
            "Run Algorithm", 
            self.run_algorithm
        ))
        
        # Algorithm selection buttons
        y_pos = 120
        for algorithm in self.algorithms:
            self.buttons.append(Button(
                20, y_pos, 150, 30,
                algorithm,
                lambda a=algorithm: self.set_algorithm(a)
            ))
            y_pos += 40
        
        # Size adjustment buttons
        self.buttons.append(Button(
            20, 300, 70, 30,
            "Size -",
            lambda: self.adjust_maze_size(-5)
        ))
        
        self.buttons.append(Button(
            100, 300, 70, 30,
            "Size +",
            lambda: self.adjust_maze_size(5)
        ))
    
    def set_algorithm(self, algorithm):
        self.selected_algorithm = algorithm
        print(f"Selected algorithm: {algorithm}")
    
    def adjust_maze_size(self, change):
        new_height = max(5, min(50, self.maze_height + change))
        new_width = max(5, min(50, self.maze_width + change))
        
        if new_height != self.maze_height or new_width != self.maze_width:
            self.maze_height = new_height
            self.maze_width = new_width
            self.generate_maze()
    
    def generate_maze(self):
        try:
            # Generate maze
            self.maze, self.start, self.end, self.graph = create_maze(self.maze_height, self.maze_width)
            
            # Clear result
            self.result = None
            
            # Print sound message
            print("Playing sound: generate")
            
            # Calculate optimal cell size
            maze_area = pygame.Rect(200, 20, self.screen_width - 220, self.screen_height - 40)
            max_cell_width = maze_area.width / self.maze_width
            max_cell_height = maze_area.height / self.maze_height
            self.cell_size = min(max_cell_width, max_cell_height, 30)
            
        except Exception as e:
            print(f"Error generating maze: {str(e)}")
    
    def run_algorithm(self):
        if not self.maze or not self.graph:
            print("Please generate a maze first")
            return
        
        if self.running:
            return
        
        self.running = True
        
        # Run algorithm in a thread
        threading.Thread(
            target=self._run_algorithm_thread,
            args=(self.selected_algorithm,),
            daemon=True
        ).start()
    
    def _run_algorithm_thread(self, algorithm):
        try:
            # Run the algorithm
            self.result = run_algorithm(algorithm, self.graph, self.start, self.end)
            print(f"Algorithm completed: {algorithm}")
            print(f"Time taken: {self.result['time_taken']*1000:.2f} ms")
            print(f"Path length: {self.result['path_length']}")
            print(f"Nodes explored: {self.result['nodes_explored']}")
            print("Playing sound: complete")
        except Exception as e:
            print(f"Error running {algorithm}: {str(e)}")
        finally:
            self.running = False
    
    def draw_maze(self):
        if not self.maze:
            return
        
        # Calculate maze area
        maze_area = pygame.Rect(200, 20, self.screen_width - 220, self.screen_height - 40)
        
        # Draw maze background
        pygame.draw.rect(self.screen, COLORS["background"], maze_area)
        pygame.draw.rect(self.screen, COLORS["text"], maze_area, 1)
        
        # Calculate start position to center the maze
        start_x = maze_area.x + (maze_area.width - self.maze_width * self.cell_size) / 2
        start_y = maze_area.y + (maze_area.height - self.maze_height * self.cell_size) / 2
        
        # Draw maze cells
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                x_pos = start_x + x * self.cell_size
                y_pos = start_y + y * self.cell_size
                
                # Create rectangle
                rect = pygame.Rect(x_pos, y_pos, self.cell_size, self.cell_size)
                
                # Determine cell color
                if (y, x) == self.start:
                    color = COLORS["start"]
                elif (y, x) == self.end:
                    color = COLORS["end"]
                elif self.maze[y][x] == 1:  # Wall
                    color = COLORS["wall"]
                else:  # Path
                    color = COLORS["path"]
                    
                    # If we have results, color visited and path cells
                    if self.result:
                        # Check if this cell was visited
                        if (y, x) in self.result["visited"] and (y, x) != self.start and (y, x) != self.end:
                            color = COLORS["visited"][self.selected_algorithm]
                            
                            # Check if this cell is in the final path
                            if self.result["path"] and (y, x) in self.result["path"] and (y, x) != self.start and (y, x) != self.end:
                                color = COLORS["final_path"][self.selected_algorithm]
                
                # Draw cell
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Border
                
                # Add symbols for start and end
                if (y, x) == self.start and self.cell_size >= 10:
                    # Draw triangle for start
                    pygame.draw.polygon(
                        self.screen,
                        (255, 255, 255),
                        [
                            (x_pos + self.cell_size/2, y_pos + self.cell_size/4),
                            (x_pos + self.cell_size*3/4, y_pos + self.cell_size*3/4),
                            (x_pos + self.cell_size/4, y_pos + self.cell_size*3/4)
                        ]
                    )
                elif (y, x) == self.end and self.cell_size >= 10:
                    # Draw square for end
                    pygame.draw.rect(
                        self.screen,
                        (255, 255, 255),
                        pygame.Rect(
                            x_pos + self.cell_size/4,
                            y_pos + self.cell_size/4,
                            self.cell_size/2,
                            self.cell_size/2
                        )
                    )
    
    def draw_stats(self):
        # Draw statistics if we have results
        if self.result:
            stats_area = pygame.Rect(20, 350, 160, 120)
            pygame.draw.rect(self.screen, COLORS["background"], stats_area)
            pygame.draw.rect(self.screen, COLORS["text"], stats_area, 1)
            
            title = self.title_font.render("Statistics", True, COLORS["text"])
            self.screen.blit(title, (stats_area.x + 10, stats_area.y + 10))
            
            time_taken = self.font.render(
                f"Time: {self.result['time_taken']*1000:.2f} ms", 
                True, 
                COLORS["text"]
            )
            self.screen.blit(time_taken, (stats_area.x + 10, stats_area.y + 40))
            
            path_length = self.font.render(
                f"Path: {self.result['path_length']}", 
                True, 
                COLORS["text"]
            )
            self.screen.blit(path_length, (stats_area.x + 10, stats_area.y + 60))
            
            nodes = self.font.render(
                f"Nodes: {self.result['nodes_explored']}", 
                True, 
                COLORS["text"]
            )
            self.screen.blit(nodes, (stats_area.x + 10, stats_area.y + 80))
    
    def draw_legend(self):
        # Draw legend
        legend_area = pygame.Rect(20, 480, 160, 200)
        pygame.draw.rect(self.screen, COLORS["background"], legend_area)
        pygame.draw.rect(self.screen, COLORS["text"], legend_area, 1)
        
        title = self.title_font.render("Legend", True, COLORS["text"])
        self.screen.blit(title, (legend_area.x + 10, legend_area.y + 10))
        
        items = [
            ("Wall", COLORS["wall"]),
            ("Path", COLORS["path"]),
            ("Start", COLORS["start"]),
            ("End", COLORS["end"]),
            ("Visited", COLORS["visited"][self.selected_algorithm]),
            ("Final Path", COLORS["final_path"][self.selected_algorithm])
        ]
        
        for i, (text, color) in enumerate(items):
            # Draw color square
            square = pygame.Rect(
                legend_area.x + 10, 
                legend_area.y + 40 + i * 25,
                15, 
                15
            )
            pygame.draw.rect(self.screen, color, square)
            pygame.draw.rect(self.screen, COLORS["text"], square, 1)
            
            # Draw text
            label = self.font.render(text, True, COLORS["text"])
            self.screen.blit(label, (legend_area.x + 35, legend_area.y + 40 + i * 25))
    
    def draw_ui(self):
        # Clear screen
        self.screen.fill((240, 240, 240))
        
        # Draw buttons
        for button in self.buttons:
            button.draw(self.screen, self.font)
        
        # Draw maze size text
        size_text = self.font.render(
            f"Maze Size: {self.maze_height}x{self.maze_width}", 
            True, 
            COLORS["text"]
        )
        self.screen.blit(size_text, (20, 340))
        
        # Draw current algorithm text
        algo_text = self.font.render(
            f"Algorithm: {self.selected_algorithm}", 
            True, 
            COLORS["text"]
        )
        self.screen.blit(algo_text, (20, 100))
        
        # Draw maze
        self.draw_maze()
        
        # Draw statistics
        self.draw_stats()
        
        # Draw legend
        self.draw_legend()
        
        # Update display
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.MOUSEMOTION:
                for button in self.buttons:
                    button.check_hover(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    for button in self.buttons:
                        button.check_click(event.pos)
        
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw_ui()
            self.clock.tick(30)
        
        pygame.quit()

def main():
    app = PyGameMazeApp()
    app.run()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
