#!/usr/bin/env python3
"""
Modern GUI Demo with Claude-like Chat Interface
Demonstrates the new modern interface with dark/light mode and zoom
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from ai_config import AIConfig
from ai_interface import AIInterface
from theme_manager import theme_manager


class ModernGUIDemo:
    """Demo application showcasing the modern interface"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Modern AI Chat Interface Demo")
        self.root.geometry("900x700")
        self.root.minsize(600, 500)
        
        # Initialize AI components
        self.ai_config = AIConfig()
        self.ai_interface = AIInterface(self.ai_config, self.get_sample_sql)
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup the main demo UI"""
        # Header with theme controls
        self.create_header()
        
        # Main content
        self.create_main_content()
        
        # Footer
        self.create_footer()
    
    def create_header(self):
        """Create header with theme and zoom controls"""
        self.header = tk.Frame(self.root, height=80)
        self.header.pack(fill="x", padx=20, pady=20)
        self.header.pack_propagate(False)
        
        # Title
        title = tk.Label(self.header,
                        text="🤖 Modern AI Chat Interface",
                        font=theme_manager.get_font(size=20, weight="bold"))
        title.pack(side="left", pady=20)
        
        # Controls
        controls = tk.Frame(self.header)
        controls.pack(side="right", pady=20)
        
        # Theme toggle
        self.theme_btn = tk.Button(controls,
                                  text="🌙" if theme_manager.current_theme == "light" else "☀️",
                                  font=theme_manager.get_font(size=16),
                                  relief="flat",
                                  bd=0,
                                  padx=15,
                                  pady=10,
                                  command=self.toggle_theme)
        self.theme_btn.pack(side="right", padx=10)
        
        # Zoom controls
        zoom_frame = tk.Frame(controls)
        zoom_frame.pack(side="right", padx=20)
        
        tk.Button(zoom_frame,
                 text="🔍−",
                 font=theme_manager.get_font(size=12),
                 relief="flat",
                 bd=0,
                 padx=8,
                 pady=5,
                 command=self.zoom_out).pack(side="left", padx=2)
        
        self.zoom_label = tk.Button(zoom_frame,
                                   text=f"{int(theme_manager.zoom_level * 100)}%",
                                   font=theme_manager.get_font(size=10),
                                   relief="flat",
                                   bd=0,
                                   padx=8,
                                   pady=5,
                                   command=self.reset_zoom)
        self.zoom_label.pack(side="left", padx=2)
        
        tk.Button(zoom_frame,
                 text="🔍+",
                 font=theme_manager.get_font(size=12),
                 relief="flat",
                 bd=0,
                 padx=8,
                 pady=5,
                 command=self.zoom_in).pack(side="left", padx=2)
    
    def create_main_content(self):
        """Create main content area"""
        self.content = tk.Frame(self.root)
        self.content.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Info section
        info_frame = tk.Frame(self.content)
        info_frame.pack(fill="x", pady=(0, 20))
        
        info_text = """✨ Features Showcased:
        
🎨 Modern Claude-like chat interface with beautiful message bubbles
🌙 Dark/Light mode toggle (click the moon/sun button above)
🔍 Zoom in/out functionality for entire interface
📷 Image upload and paste support (Ctrl+Shift+V)
⌨️ Keyboard shortcuts (Ctrl+Enter to send)
🤖 AI model support: llava:latest (local), GPT-4 (OpenAI), Claude (Anthropic)"""
        
        info_label = tk.Label(info_frame,
                             text=info_text,
                             font=theme_manager.get_font(size=12),
                             justify="left",
                             relief="solid",
                             bd=1,
                             padx=20,
                             pady=15)
        info_label.pack(fill="x")
        
        # Demo buttons
        buttons_frame = tk.Frame(self.content)
        buttons_frame.pack(fill="x", pady=10)
        
        # Modern Chat Demo
        modern_chat_btn = tk.Button(buttons_frame,
                                   text="🚀 Open Modern Chat Interface",
                                   font=theme_manager.get_font(size=14, weight="bold"),
                                   relief="flat",
                                   bd=0,
                                   padx=30,
                                   pady=15,
                                   command=self.open_modern_chat)
        modern_chat_btn.pack(fill="x", pady=5)
        
        # Legacy Chat Demo
        legacy_chat_btn = tk.Button(buttons_frame,
                                   text="📜 Open Legacy Chat Interface",
                                   font=theme_manager.get_font(size=12),
                                   relief="flat",
                                   bd=0,
                                   padx=20,
                                   pady=10,
                                   command=self.open_legacy_chat)
        legacy_chat_btn.pack(fill="x", pady=5)
        
        # AI Config button
        config_btn = tk.Button(buttons_frame,
                              text="⚙️ Configure AI Settings",
                              font=theme_manager.get_font(size=12),
                              relief="flat",
                              bd=0,
                              padx=20,
                              pady=10,
                              command=self.open_ai_config)
        config_btn.pack(fill="x", pady=5)
        
        # Store button references
        self.modern_chat_btn = modern_chat_btn
        self.legacy_chat_btn = legacy_chat_btn
        self.config_btn = config_btn
        self.info_label = info_label
    
    def create_footer(self):
        """Create footer with keyboard shortcuts"""
        self.footer = tk.Frame(self.root)
        self.footer.pack(fill="x", padx=20, pady=(0, 20))
        
        shortcuts_text = """⌨️ Keyboard Shortcuts:  
Ctrl+Enter: Send message  |  Ctrl+Shift+V: Paste image  |  Theme: Click 🌙/☀️  |  Zoom: Use 🔍+/🔍- buttons"""
        
        self.shortcuts_label = tk.Label(self.footer,
                                       text=shortcuts_text,
                                       font=theme_manager.get_font(size=10),
                                       justify="center")
        self.shortcuts_label.pack()
    
    def get_sample_sql(self):
        """Get sample SQL for demo"""
        return """SELECT u.id, u.name, u.email, p.title, p.created_date
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.active = 1
AND p.created_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY p.created_date DESC
LIMIT 50;"""
    
    def open_modern_chat(self):
        """Open modern chat interface"""
        initial_message = """👋 Welcome to the modern AI chat interface!

This is a Claude-like interface with the following features:

🎨 **Modern Design:**
• Clean message bubbles with proper spacing
• User messages on the right, AI messages on the left
• Beautiful typography and colors

📷 **Image Support:**
• Upload images using the paper clip button
• Paste from clipboard using the clipboard button or Ctrl+Shift+V
• Images are sent to the AI for analysis

🤖 **AI Integration:**
• Works with local llava:latest for image analysis
• Supports OpenAI GPT-4 and Anthropic Claude
• Context-aware conversations

⌨️ **Keyboard Shortcuts:**
• Ctrl+Enter: Send message
• Ctrl+Shift+V: Paste image

Try asking me about the SQL query or upload an image for analysis!"""
        
        self.ai_interface.show_modern_conversation(
            "Modern AI Chat",
            initial_message,
            self.get_sample_sql()
        )
    
    def open_legacy_chat(self):
        """Open legacy chat interface"""
        self.ai_interface.show_understand_result(
            "Legacy AI Chat",
            "This is the original chat interface. It still has image support but uses the older styling.",
            self.get_sample_sql()
        )
    
    def open_ai_config(self):
        """Open AI configuration"""
        self.ai_config.show_config_dialog(self.root)
    
    def toggle_theme(self):
        """Toggle theme"""
        new_theme = theme_manager.toggle_theme()
        self.apply_theme()
        self.theme_btn.config(text="🌙" if new_theme == "light" else "☀️")
    
    def zoom_in(self):
        """Zoom in"""
        zoom_level = theme_manager.zoom_in()
        self.update_fonts()
        self.zoom_label.config(text=f"{int(zoom_level * 100)}%")
    
    def zoom_out(self):
        """Zoom out"""
        zoom_level = theme_manager.zoom_out()
        self.update_fonts()
        self.zoom_label.config(text=f"{int(zoom_level * 100)}%")
    
    def reset_zoom(self):
        """Reset zoom"""
        zoom_level = theme_manager.reset_zoom()
        self.update_fonts()
        self.zoom_label.config(text=f"{int(zoom_level * 100)}%")
    
    def apply_theme(self):
        """Apply current theme to all widgets"""
        # Main window
        self.root.configure(bg=theme_manager.get_color("bg_primary"))
        
        # Header
        theme_manager.apply_theme_to_widget(self.header, "header")
        theme_manager.apply_theme_to_widget(self.theme_btn, "button")
        
        # Content
        theme_manager.apply_theme_to_widget(self.content, "default")
        theme_manager.apply_theme_to_widget(self.info_label, "default")
        theme_manager.apply_theme_to_widget(self.modern_chat_btn, "primary_button")
        theme_manager.apply_theme_to_widget(self.legacy_chat_btn, "button")
        theme_manager.apply_theme_to_widget(self.config_btn, "button")
        
        # Footer
        theme_manager.apply_theme_to_widget(self.footer, "default")
        theme_manager.apply_theme_to_widget(self.shortcuts_label, "default")
    
    def update_fonts(self):
        """Update fonts for zoom level"""
        # This is a simplified version - in a full app you'd recursively update all widgets
        pass
    
    def run(self):
        """Run the demo application"""
        self.root.mainloop()


def main():
    """Main function"""
    try:
        app = ModernGUIDemo()
        app.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start application: {str(e)}")


if __name__ == "__main__":
    main()