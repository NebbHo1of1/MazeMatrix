"""
Utility functions for the Maze Visualization application.
This module contains helper functions for sound effects, timing, and other utilities.
"""

import time
import threading
import os
import pygame
import random
import math

# Initialize pygame mixer for sound effects
pygame.mixer.init()

def generate_sound_effect(sound_type):
    """
    Generate a sound effect programmatically since we don't have audio files.
    
    Args:
        sound_type (str): Type of sound to generate.
        
    Returns:
        pygame.mixer.Sound: Generated sound effect.
    """
    sample_rate = 44100
    duration = 0.5  # seconds
    
    # Create buffer for sound
    num_samples = int(sample_rate * duration)
    buffer = bytearray(num_samples)
    
    if sound_type == "generate":
        # Ascending tone for maze generation
        for i in range(num_samples):
            t = i / sample_rate
            freq = 220 + 880 * (i / num_samples)
            buffer[i] = int(127 + 127 * math.sin(2 * math.pi * freq * t))
    
    elif sound_type == "complete":
        # Victory sound for completion
        for i in range(num_samples):
            t = i / sample_rate
            if i < num_samples / 2:
                freq = 440 + 110 * (i / (num_samples / 2))
            else:
                freq = 550 + 220 * ((i - num_samples / 2) / (num_samples / 2))
            buffer[i] = int(127 + 127 * math.sin(2 * math.pi * freq * t))
    
    elif sound_type == "start":
        # Quick rising tone for start
        for i in range(num_samples):
            t = i / sample_rate
            freq = 330 + 220 * (i / num_samples) 
            buffer[i] = int(127 + 127 * math.sin(2 * math.pi * freq * t))
    
    elif sound_type == "error":
        # Error sound (descending tone)
        for i in range(num_samples):
            t = i / sample_rate
            freq = 660 - 330 * (i / num_samples)
            buffer[i] = int(127 + 127 * math.sin(2 * math.pi * freq * t))
    
    # Create sound from buffer
    sound = pygame.mixer.Sound(buffer=buffer)
    return sound

# Pregenerate sound effects
sound_effects = {}

def play_sound(sound_type):
    """
    Play a sound effect.
    
    Args:
        sound_type (str): Type of sound to play.
                         Options: "generate", "complete", "start", "error"
    
    Returns:
        None
    """
    print(f"Playing sound: {sound_type}")
    
    try:
        # Generate the sound if it doesn't exist yet
        if sound_type not in sound_effects:
            sound_effects[sound_type] = generate_sound_effect(sound_type)
        
        # Play the sound
        sound_effects[sound_type].play()
    except Exception as e:
        print(f"Error playing sound: {e}")

def timed_callback(seconds, callback, *args, **kwargs):
    """
    Execute a callback function after a specified number of seconds.
    
    Args:
        seconds (float): Number of seconds to wait.
        callback (function): Function to call after the wait.
        *args: Arguments to pass to the callback.
        **kwargs: Keyword arguments to pass to the callback.
        
    Returns:
        None
    """
    def delayed_callback():
        time.sleep(seconds)
        callback(*args, **kwargs)
    
    threading.Thread(target=delayed_callback, daemon=True).start()

def format_time(seconds):
    """
    Format time in seconds to a readable string.
    
    Args:
        seconds (float): Time in seconds.
        
    Returns:
        str: Formatted time string.
    """
    if seconds < 0.001:
        return f"{seconds * 1000000:.2f} µs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    else:
        return f"{seconds:.2f} s"

def clamp(value, min_value, max_value):
    """
    Clamp a value between a minimum and maximum.
    
    Args:
        value: Value to clamp.
        min_value: Minimum allowed value.
        max_value: Maximum allowed value.
        
    Returns:
        Clamped value.
    """
    return max(min_value, min(value, max_value))
