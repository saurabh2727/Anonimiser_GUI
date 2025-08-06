#!/usr/bin/env python3
"""
Enhanced SQL Masker with Dual LLM - Main Launcher
Run this to start the SQL masker with modern Claude-like AI interface
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

def main():
    """Main launcher function"""
    try:
        # Import the main GUI
        from sql_mask_gui import EnhancedSQLMaskerGUI
        
        # Create main window
        root = tk.Tk()
        
        # Set window icon if available
        try:
            root.iconbitmap('icon.ico')  # Add icon file if you have one
        except:
            pass
        
        # Center window on screen
        root.eval('tk::PlaceWindow . center')
        
        # Create and run the application
        app = EnhancedSQLMaskerGUI(root)
        
        print("🚀 Enhanced SQL Masker with Dual LLM started!")
        print("Features:")
        print("• 📝 Text/Code Analysis: deepseek-coder-v2:latest")
        print("• 🖼️ Image Analysis: llava:latest")
        print("• 🎨 Modern Claude-like interface")
        print("• 🌙 Dark/Light mode toggle")
        print("• 🔍 Zoom in/out functionality")
        print("• 🤖 Smart routing between models")
        
        root.mainloop()
        
    except ImportError as e:
        messagebox.showerror("Import Error", 
            f"Failed to import required modules:\n{str(e)}\n\n"
            f"Please ensure all dependencies are installed:\n"
            f"pip install -r requirements.txt")
        sys.exit(1)
        
    except Exception as e:
        messagebox.showerror("Application Error", 
            f"Failed to start application:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()