#!/usr/bin/env python3
"""
Theme Manager for Modern UI
Handles dark/light themes and modern styling like Claude
"""

import tkinter as tk
from tkinter import ttk
import json
import os


class ThemeManager:
    """Manages application themes and modern styling"""
    
    def __init__(self):
        self.current_theme = "light"
        self.zoom_level = 1.0
        self.base_font_size = 11
        self.config_file = "theme_config.json"
        
        # Load saved settings
        self.load_config()
        
        # Define modern themes inspired by Claude
        self.themes = {
            "light": {
                # Background colors
                "bg_primary": "#FFFFFF",
                "bg_secondary": "#F8F9FA",
                "bg_tertiary": "#F1F3F4",
                "bg_chat": "#FFFFFF",
                "bg_user_message": "#F1F3F4",
                "bg_ai_message": "#FFFFFF",
                "bg_code": "#F8F9FA",
                "bg_header": "#FFFFFF",
                "bg_sidebar": "#F8F9FA",
                "bg_input": "#FFFFFF",
                "bg_button": "#FFFFFF",
                "bg_button_hover": "#F1F3F4",
                "bg_button_active": "#E8EAED",
                
                # Text colors
                "fg_primary": "#1F1F1F",
                "fg_secondary": "#5F6368",
                "fg_tertiary": "#80868B",
                "fg_user": "#1F1F1F",
                "fg_ai": "#1F1F1F",
                "fg_code": "#1F1F1F",
                "fg_link": "#1976D2",
                "fg_error": "#D32F2F",
                "fg_success": "#388E3C",
                "fg_warning": "#F57C00",
                
                # Border colors
                "border_primary": "#E8EAED",
                "border_secondary": "#DADCE0",
                "border_input": "#DADCE0",
                "border_button": "#DADCE0",
                "border_focus": "#1976D2",
                
                # Special colors
                "accent_primary": "#1976D2",
                "accent_secondary": "#1565C0",
                "shadow": "#00000010",
                "selection": "#1976D220",
            },
            "dark": {
                # Background colors
                "bg_primary": "#1A1A1A",
                "bg_secondary": "#2D2D2D",
                "bg_tertiary": "#3C3C3C",
                "bg_chat": "#1A1A1A",
                "bg_user_message": "#2D2D2D",
                "bg_ai_message": "#1A1A1A",
                "bg_code": "#2D2D2D",
                "bg_header": "#1A1A1A",
                "bg_sidebar": "#2D2D2D",
                "bg_input": "#2D2D2D",
                "bg_button": "#2D2D2D",
                "bg_button_hover": "#3C3C3C",
                "bg_button_active": "#4A4A4A",
                
                # Text colors
                "fg_primary": "#E8E8E8",
                "fg_secondary": "#B3B3B3",
                "fg_tertiary": "#8C8C8C",
                "fg_user": "#E8E8E8",
                "fg_ai": "#E8E8E8",
                "fg_code": "#E8E8E8",
                "fg_link": "#64B5F6",
                "fg_error": "#F28B82",
                "fg_success": "#81C784",
                "fg_warning": "#FFB74D",
                
                # Border colors
                "border_primary": "#404040",
                "border_secondary": "#4A4A4A",
                "border_input": "#4A4A4A",
                "border_button": "#4A4A4A",
                "border_focus": "#64B5F6",
                
                # Special colors
                "accent_primary": "#64B5F6",
                "accent_secondary": "#42A5F5",
                "shadow": "#00000030",
                "selection": "#64B5F630",
            }
        }
    
    def get_color(self, color_name):
        """Get color from current theme"""
        return self.themes[self.current_theme].get(color_name, "#000000")
    
    def get_font_size(self, base_size=None):
        """Get scaled font size based on zoom level"""
        if base_size is None:
            base_size = self.base_font_size
        return int(base_size * self.zoom_level)
    
    def get_font(self, family="Segoe UI", size=None, weight="normal"):
        """Get font tuple with proper scaling"""
        if size is None:
            size = self.base_font_size
        return (family, self.get_font_size(size), weight)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.save_config()
        return self.current_theme
    
    def set_theme(self, theme_name):
        """Set specific theme"""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.save_config()
    
    def zoom_in(self):
        """Increase zoom level"""
        self.zoom_level = min(3.0, self.zoom_level + 0.1)
        self.save_config()
        return self.zoom_level
    
    def zoom_out(self):
        """Decrease zoom level"""
        self.zoom_level = max(0.5, self.zoom_level - 0.1)
        self.save_config()
        return self.zoom_level
    
    def reset_zoom(self):
        """Reset zoom to default"""
        self.zoom_level = 1.0
        self.save_config()
        return self.zoom_level
    
    def apply_theme_to_widget(self, widget, widget_type="default"):
        """Apply theme colors to a widget"""
        try:
            if widget_type == "chat_message_user":
                widget.config(
                    bg=self.get_color("bg_user_message"),
                    fg=self.get_color("fg_user"),
                    relief="flat",
                    bd=0
                )
            elif widget_type == "chat_message_ai":
                widget.config(
                    bg=self.get_color("bg_ai_message"),
                    fg=self.get_color("fg_ai"),
                    relief="flat",
                    bd=0
                )
            elif widget_type == "input":
                widget.config(
                    bg=self.get_color("bg_input"),
                    fg=self.get_color("fg_primary"),
                    insertbackground=self.get_color("fg_primary"),
                    relief="solid",
                    bd=1,
                    highlightcolor=self.get_color("border_focus"),
                    highlightbackground=self.get_color("border_input")
                )
            elif widget_type == "button":
                widget.config(
                    bg=self.get_color("bg_button"),
                    fg=self.get_color("fg_primary"),
                    relief="solid",
                    bd=1,
                    highlightbackground=self.get_color("border_button"),
                    activebackground=self.get_color("bg_button_hover"),
                    activeforeground=self.get_color("fg_primary")
                )
            elif widget_type == "primary_button":
                widget.config(
                    bg=self.get_color("accent_primary"),
                    fg="#FFFFFF",
                    relief="solid",
                    bd=0,
                    activebackground=self.get_color("accent_secondary"),
                    activeforeground="#FFFFFF"
                )
            elif widget_type == "header":
                widget.config(
                    bg=self.get_color("bg_header"),
                    fg=self.get_color("fg_primary")
                )
            elif widget_type == "sidebar":
                widget.config(
                    bg=self.get_color("bg_sidebar"),
                    fg=self.get_color("fg_primary")
                )
            else:  # default
                widget.config(
                    bg=self.get_color("bg_primary"),
                    fg=self.get_color("fg_primary")
                )
        except tk.TclError:
            # Some widgets don't support all options
            pass
    
    def create_modern_scrollbar(self, parent):
        """Create a modern styled scrollbar"""
        style = ttk.Style()
        
        # Configure scrollbar style based on theme
        if self.current_theme == "dark":
            style.configure("Modern.Vertical.TScrollbar",
                          background=self.get_color("bg_secondary"),
                          troughcolor=self.get_color("bg_primary"),
                          arrowcolor=self.get_color("fg_secondary"))
        else:
            style.configure("Modern.Vertical.TScrollbar",
                          background=self.get_color("bg_tertiary"),
                          troughcolor=self.get_color("bg_secondary"),
                          arrowcolor=self.get_color("fg_secondary"))
        
        return ttk.Scrollbar(parent, style="Modern.Vertical.TScrollbar")
    
    def create_chat_bubble(self, parent, text, message_type="ai", **kwargs):
        """Create a modern chat bubble"""
        # Container for the bubble
        bubble_container = tk.Frame(parent, bg=self.get_color("bg_chat"))
        
        # Determine alignment and colors
        if message_type == "user":
            side = "right"
            bg_color = self.get_color("bg_user_message")
            fg_color = self.get_color("fg_user")
            bubble_container.pack(fill="x", padx=(50, 10), pady=5)
        else:  # AI message
            side = "left"
            bg_color = self.get_color("bg_ai_message")
            fg_color = self.get_color("fg_ai")
            bubble_container.pack(fill="x", padx=(10, 50), pady=5)
        
        # Create the actual bubble
        bubble = tk.Frame(bubble_container, 
                         bg=bg_color,
                         relief="solid",
                         bd=1 if self.current_theme == "light" else 0)
        bubble.pack(side=side, fill="x", expand=True)
        
        # Add padding frame
        padding_frame = tk.Frame(bubble, bg=bg_color)
        padding_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Message content
        message_label = tk.Label(padding_frame,
                               text=text,
                               bg=bg_color,
                               fg=fg_color,
                               font=self.get_font(size=12),
                               wraplength=600,
                               justify="left",
                               **kwargs)
        message_label.pack(anchor="w" if message_type == "ai" else "e")
        
        return bubble_container
    
    def save_config(self):
        """Save theme configuration"""
        config = {
            "theme": self.current_theme,
            "zoom_level": self.zoom_level
        }
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception:
            pass  # Fail silently if can't save
    
    def load_config(self):
        """Load theme configuration"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.current_theme = config.get("theme", "light")
                    self.zoom_level = config.get("zoom_level", 1.0)
        except Exception:
            pass  # Use defaults if can't load


    def create_rounded_frame(self, parent, bg_color, radius=10):
        """Create a frame with simulated rounded corners"""
        # Create main container
        container = tk.Frame(parent, bg=parent.cget('bg') if hasattr(parent, 'cget') else self.get_color("bg_chat"))
        
        # Create inner frame with padding for rounded effect
        inner_frame = tk.Frame(container, bg=bg_color, relief="flat", bd=0)
        inner_frame.pack(fill="both", expand=True, padx=2, pady=2)
        
        return container, inner_frame


# Global theme manager instance
theme_manager = ThemeManager()