"""
Module for pathfinding algorithms.
This module contains implementations of various pathfinding algorithms:
DFS, Dijkstra's, A*, and Custom A*.
"""

import time
import heapq
from collections import deque

def solve_maze_dfs(graph, start, end):
    """
    Solve the maze using Depth-First Search (DFS) algorithm.
    
    Args:
        graph (dict): Graph representation of the maze.
        start (tuple): Starting point (y, x).
        end (tuple): End point (y, x).
        
    Returns:
        dict: Results including path, visited nodes, and performance statistics.
    """
    start_time = time.time()
    
    visited = set()
    stack = [(start, [start])]  # (current_node, path_so_far)
    
    while stack:
        current, path = stack.pop()
        
        if current == end:
            end_time = time.time()
            return {
                "path": path,
                "visited": list(visited),
                "path_length": len(path),
                "nodes_explored": len(visited),
                "time_taken": end_time - start_time,
                "algorithm": "DFS"
            }
        
        if current not in visited:
            visited.add(current)
            
            # Get neighbors in reverse order for consistent DFS behavior
            neighbors = sorted(graph[current], reverse=True)
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
    
    # No path found
    end_time = time.time()
    return {
        "path": None,
        "visited": list(visited),
        "path_length": 0,
        "nodes_explored": len(visited),
        "time_taken": end_time - start_time,
        "algorithm": "DFS"
    }

def dijkstra(graph, start, end):
    """
    Solve the maze using Dijkstra's algorithm.
    
    Args:
        graph (dict): Graph representation of the maze.
        start (tuple): Starting point (y, x).
        end (tuple): End point (y, x).
        
    Returns:
        dict: Results including path, visited nodes, and performance statistics.
    """
    start_time = time.time()
    
    # Priority queue for Dijkstra's algorithm
    # Format: (distance, node, path)
    priority_queue = [(0, start, [start])]
    visited = set()
    
    while priority_queue:
        distance, current, path = heapq.heappop(priority_queue)
        
        if current == end:
            end_time = time.time()
            return {
                "path": path,
                "visited": list(visited),
                "path_length": len(path),
                "nodes_explored": len(visited),
                "time_taken": end_time - start_time,
                "algorithm": "Dijkstra"
            }
        
        if current not in visited:
            visited.add(current)
            
            for neighbor in graph[current]:
                if neighbor not in visited:
                    # In this implementation, all edges have a weight of 1
                    new_distance = distance + 1
                    heapq.heappush(priority_queue, (new_distance, neighbor, path + [neighbor]))
    
    # No path found
    end_time = time.time()
    return {
        "path": None,
        "visited": list(visited),
        "path_length": 0,
        "nodes_explored": len(visited),
        "time_taken": end_time - start_time,
        "algorithm": "Dijkstra"
    }

def manhattan_distance(a, b):
    """
    Calculate the Manhattan distance between two points.
    
    Args:
        a (tuple): First point (y, x).
        b (tuple): Second point (y, x).
        
    Returns:
        int: Manhattan distance between the two points.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star(graph, start, end):
    """
    Solve the maze using A* algorithm with Manhattan distance heuristic.
    
    Args:
        graph (dict): Graph representation of the maze.
        start (tuple): Starting point (y, x).
        end (tuple): End point (y, x).
        
    Returns:
        dict: Results including path, visited nodes, and performance statistics.
    """
    start_time = time.time()
    
    # Priority queue for A* algorithm
    # Format: (f_score, g_score, node, path)
    # f_score = g_score + h_score (h_score is the heuristic)
    priority_queue = [(manhattan_distance(start, end), 0, start, [start])]
    visited = set()
    
    while priority_queue:
        _, g_score, current, path = heapq.heappop(priority_queue)
        
        if current == end:
            end_time = time.time()
            return {
                "path": path,
                "visited": list(visited),
                "path_length": len(path),
                "nodes_explored": len(visited),
                "time_taken": end_time - start_time,
                "algorithm": "A*"
            }
        
        if current not in visited:
            visited.add(current)
            
            for neighbor in graph[current]:
                if neighbor not in visited:
                    new_g_score = g_score + 1
                    h_score = manhattan_distance(neighbor, end)
                    f_score = new_g_score + h_score
                    heapq.heappush(priority_queue, (f_score, new_g_score, neighbor, path + [neighbor]))
    
    # No path found
    end_time = time.time()
    return {
        "path": None,
        "visited": list(visited),
        "path_length": 0,
        "nodes_explored": len(visited),
        "time_taken": end_time - start_time,
        "algorithm": "A*"
    }

def euclidean_distance(a, b):
    """
    Calculate the Euclidean distance between two points.
    
    Args:
        a (tuple): First point (y, x).
        b (tuple): Second point (y, x).
        
    Returns:
        float: Euclidean distance between the two points.
    """
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5

def a_star_custom(graph, start, end):
    """
    Solve the maze using A* algorithm with a custom heuristic (Euclidean distance).
    
    Args:
        graph (dict): Graph representation of the maze.
        start (tuple): Starting point (y, x).
        end (tuple): End point (y, x).
        
    Returns:
        dict: Results including path, visited nodes, and performance statistics.
    """
    start_time = time.time()
    
    # Priority queue for A* algorithm with custom heuristic
    # Format: (f_score, g_score, node, path)
    priority_queue = [(euclidean_distance(start, end), 0, start, [start])]
    visited = set()
    
    while priority_queue:
        _, g_score, current, path = heapq.heappop(priority_queue)
        
        if current == end:
            end_time = time.time()
            return {
                "path": path,
                "visited": list(visited),
                "path_length": len(path),
                "nodes_explored": len(visited),
                "time_taken": end_time - start_time,
                "algorithm": "Custom A*"
            }
        
        if current not in visited:
            visited.add(current)
            
            for neighbor in graph[current]:
                if neighbor not in visited:
                    new_g_score = g_score + 1
                    h_score = euclidean_distance(neighbor, end)
                    f_score = new_g_score + h_score
                    heapq.heappush(priority_queue, (f_score, new_g_score, neighbor, path + [neighbor]))
    
    # No path found
    end_time = time.time()
    return {
        "path": None,
        "visited": list(visited),
        "path_length": 0,
        "nodes_explored": len(visited),
        "time_taken": end_time - start_time,
        "algorithm": "Custom A*"
    }

def run_algorithm(algorithm, graph, start, end):
    """
    Run the specified pathfinding algorithm.
    
    Args:
        algorithm (str): Name of the algorithm to run.
        graph (dict): Graph representation of the maze.
        start (tuple): Starting point (y, x).
        end (tuple): End point (y, x).
        
    Returns:
        dict: Results from the algorithm.
    """
    algorithms = {
        "DFS": solve_maze_dfs,
        "Dijkstra": dijkstra,
        "A*": a_star,
        "Custom A*": a_star_custom
    }
    
    if algorithm in algorithms:
        return algorithms[algorithm](graph, start, end)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")
