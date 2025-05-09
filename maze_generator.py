"""
MazeMatrix - Algorithms in Action
Module for maze generation using Randomized Prim's algorithm.
This module contains functions for generating mazes and converting them to a graph
representation for pathfinding.
"""

import random
from collections import deque

def generate_maze(height, width):
    """
    Generate a maze using Randomized Prim's algorithm.
    
    Args:
        height (int): Height of the maze.
        width (int): Width of the maze.
        
    Returns:
        list: 2D list representing the maze where:
              0 represents a path
              1 represents a wall
    """
    # Ensure odd dimensions for proper maze generation
    if height % 2 == 0:
        height += 1
    if width % 2 == 0:
        width += 1
    
    # Initialize maze with all walls
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Pick a random starting cell
    start_y = random.randrange(1, height, 2)
    start_x = random.randrange(1, width, 2)
    maze[start_y][start_x] = 0
    
    # Add walls of the starting cell to the wall list
    walls = []
    if start_y > 1:
        walls.append((start_y - 1, start_x))
    if start_y < height - 2:
        walls.append((start_y + 1, start_x))
    if start_x > 1:
        walls.append((start_y, start_x - 1))
    if start_x < width - 2:
        walls.append((start_y, start_x + 1))
    
    # Prim's algorithm
    while walls:
        # Pick a random wall
        wall_index = random.randint(0, len(walls) - 1)
        y, x = walls[wall_index]
        walls.pop(wall_index)
        
        # Check if the wall divides two cells
        if y % 2 == 0:  # Horizontal wall
            if x > 0 and x < width - 1:
                if maze[y - 1][x] == 1 and maze[y + 1][x] == 0:  # Upper cell is wall, lower cell is path
                    maze[y][x] = 0  # Make wall a path
                    maze[y - 1][x] = 0  # Make upper cell a path
                    
                    # Add new walls to the list
                    if y - 2 > 0:
                        walls.append((y - 2, x))
                    if x - 1 > 0:
                        walls.append((y - 1, x - 1))
                    if x + 1 < width - 1:
                        walls.append((y - 1, x + 1))
                
                elif maze[y - 1][x] == 0 and maze[y + 1][x] == 1:  # Upper cell is path, lower cell is wall
                    maze[y][x] = 0  # Make wall a path
                    maze[y + 1][x] = 0  # Make lower cell a path
                    
                    # Add new walls to the list
                    if y + 2 < height - 1:
                        walls.append((y + 2, x))
                    if x - 1 > 0:
                        walls.append((y + 1, x - 1))
                    if x + 1 < width - 1:
                        walls.append((y + 1, x + 1))
        
        else:  # Vertical wall
            if y > 0 and y < height - 1:
                if maze[y][x - 1] == 1 and maze[y][x + 1] == 0:  # Left cell is wall, right cell is path
                    maze[y][x] = 0  # Make wall a path
                    maze[y][x - 1] = 0  # Make left cell a path
                    
                    # Add new walls to the list
                    if x - 2 > 0:
                        walls.append((y, x - 2))
                    if y - 1 > 0:
                        walls.append((y - 1, x - 1))
                    if y + 1 < height - 1:
                        walls.append((y + 1, x - 1))
                
                elif maze[y][x - 1] == 0 and maze[y][x + 1] == 1:  # Left cell is path, right cell is wall
                    maze[y][x] = 0  # Make wall a path
                    maze[y][x + 1] = 0  # Make right cell a path
                    
                    # Add new walls to the list
                    if x + 2 < width - 1:
                        walls.append((y, x + 2))
                    if y - 1 > 0:
                        walls.append((y - 1, x + 1))
                    if y + 1 < height - 1:
                        walls.append((y + 1, x + 1))
    
    # Set entrance and exit
    # Entrance at top row
    for x in range(1, width - 1):
        if maze[1][x] == 0:
            maze[0][x] = 0
            start = (0, x)
            break
    
    # Exit at bottom row
    for x in range(width - 2, 0, -1):
        if maze[height - 2][x] == 0:
            maze[height - 1][x] = 0
            end = (height - 1, x)
            break
    
    return maze, start, end

def maze_to_graph(maze):
    """
    Convert a maze to a graph representation for pathfinding.
    
    Args:
        maze (list): 2D list representing the maze.
        
    Returns:
        dict: Graph representation of the maze as an adjacency list.
    """
    height = len(maze)
    width = len(maze[0])
    graph = {}
    
    # Define possible moves (4-directional)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
    
    for y in range(height):
        for x in range(width):
            if maze[y][x] == 0:  # If it's a path
                node = (y, x)
                graph[node] = []
                
                # Check adjacent cells
                for dy, dx in directions:
                    ny, nx = y + dy, x + dx
                    
                    # Check if the adjacent cell is within the maze boundaries and is a path
                    if 0 <= ny < height and 0 <= nx < width and maze[ny][nx] == 0:
                        graph[node].append((ny, nx))
    
    return graph

def create_maze(height, width):
    """
    Create a maze and prepare it for visualization and pathfinding.
    
    Args:
        height (int): Height of the maze.
        width (int): Width of the maze.
        
    Returns:
        tuple: The maze, start point, end point, and graph representation.
    """
    maze, start, end = generate_maze(height, width)
    graph = maze_to_graph(maze)
    return maze, start, end, graph
