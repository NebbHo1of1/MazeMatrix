#!/usr/bin/env python3
"""
MazeMatrix - Algorithms in Action
Main entry point for the maze generation and pathfinding visualization application.
This file initializes the GUI and starts the application.
"""

import sys
import tkinter as tk
from gui import MazeApp
import os
import pygame

# Configure environment for VNC
os.environ['DISPLAY'] = ':1'

# Initialize pygame for sound
pygame.init()

def main():
    """Initialize and start the application."""
    root = tk.Tk()
    root.title("MazeMatrix - Algorithms in Action")
    
    # Set window size for better visibility in VNC
    root.geometry("1024x768")
    
    # Set minimum window size
    root.minsize(800, 600)
    
    # Configure window
    root.configure(background='#F0F0F0')
    
    # Initialize the application
    app = MazeApp(root)
    
    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)
