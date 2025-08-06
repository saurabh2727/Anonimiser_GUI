#!/usr/bin/env python3
"""
Modern AI Interface Module
Claude-like chat interface with dark/light mode and zoom
"""

import tkinter as tk
from tkinter import messagebox, Toplevel, filedialog, Canvas, Frame
import threading
import os
from theme_manager import theme_manager
try:
    import pyperclip
except ImportError:
    pyperclip = None


class ModernChatWidget(Frame):
    """Modern chat widget with Claude-like styling"""
    
    def __init__(self, parent, ai_config=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.ai_config = ai_config
        self.messages = []
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup the chat UI"""
        # Create scrollable canvas
        self.canvas = Canvas(self, highlightthickness=0)
        self.scrollable_frame = Frame(self.canvas)
        
        # Modern scrollbar
        self.scrollbar = theme_manager.create_modern_scrollbar(self)
        self.scrollbar.pack(side="right", fill="y")
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.canvas.yview)
        
        # Configure scrollable frame
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind scrolling events
        self.scrollable_frame.bind('<Configure>', self._on_frame_configure)
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.bind_all('<MouseWheel>', self._on_mousewheel)
    
    def _on_frame_configure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def _on_canvas_configure(self, event):
        """Reset the canvas window to encompass inner frame when required"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling"""
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def add_message(self, text, message_type="ai", image_filename=None):
        """Add a message to the chat with modern styling"""
        # Create message container with reduced spacing
        msg_container = Frame(self.scrollable_frame, bg=theme_manager.get_color("bg_chat"))
        msg_container.pack(fill="x", padx=15, pady=6)
        
        if message_type == "user":
            # User message - right aligned with modern styling
            bubble_frame = Frame(msg_container, bg=theme_manager.get_color("bg_chat"))
            bubble_frame.pack(anchor="e", padx=(150, 0))
            
            # Add image indicator if present
            if image_filename:
                img_indicator = tk.Label(bubble_frame, 
                                       text=f"📷 {image_filename}",
                                       font=theme_manager.get_font(size=10),
                                       bg=theme_manager.get_color("bg_chat"),
                                       fg=theme_manager.get_color("fg_secondary"))
                img_indicator.pack(anchor="e", pady=(0, 4))
            
            # User bubble with rounded appearance
            bubble = tk.Frame(bubble_frame, 
                            bg=theme_manager.get_color("bg_user_message"),
                            relief="flat",
                            bd=0)
            bubble.pack(anchor="e")
            
            # Inner padding for rounded effect
            padding = tk.Frame(bubble, bg=theme_manager.get_color("bg_user_message"))
            padding.pack(fill="both", expand=True, padx=16, pady=12)
            
            # Modern text widget
            text_widget = tk.Text(padding,
                                bg=theme_manager.get_color("bg_user_message"),
                                fg=theme_manager.get_color("fg_user"),
                                font=theme_manager.get_font(size=13),
                                wrap=tk.WORD,
                                relief="flat",
                                bd=0,
                                height=1,
                                width=50,
                                cursor="arrow",
                                state=tk.DISABLED)
            text_widget.pack(fill="both", expand=True)
            
            # Insert text and auto-resize
            text_widget.config(state=tk.NORMAL)
            text_widget.insert(tk.END, text)
            text_widget.config(state=tk.DISABLED)
            
            # Auto-resize height based on content
            text_widget.update_idletasks()
            lines = int(text_widget.index('end-1c').split('.')[0])
            text_widget.config(height=min(lines, 15))
            
        else:
            # AI message - left aligned with modern styling
            bubble_frame = Frame(msg_container, bg=theme_manager.get_color("bg_chat"))
            bubble_frame.pack(anchor="w", padx=(0, 150), fill="x")
            
            # AI avatar and name header
            header_frame = Frame(bubble_frame, bg=theme_manager.get_color("bg_chat"))
            header_frame.pack(fill="x", pady=(0, 6))
            
            avatar_label = tk.Label(header_frame,
                                  text="🤖",
                                  font=theme_manager.get_font(size=16),
                                  bg=theme_manager.get_color("bg_chat"),
                                  fg=theme_manager.get_color("fg_primary"))
            avatar_label.pack(side="left")
            
            # Model info for dual LLM
            model_info = ""
            if self.ai_config and hasattr(self.ai_config, 'config') and self.ai_config.config.get('dual_llm_enabled', False):
                model_info = " (Smart Routing)"
            
            name_label = tk.Label(header_frame,
                                text=f"AI Assistant{model_info}",
                                font=theme_manager.get_font(size=12, weight="bold"),
                                bg=theme_manager.get_color("bg_chat"),
                                fg=theme_manager.get_color("fg_primary"))
            name_label.pack(side="left", padx=(10, 0))
            
            # AI message bubble with rounded appearance
            bubble = tk.Frame(bubble_frame,
                            bg=theme_manager.get_color("bg_ai_message"),
                            relief="flat",
                            bd=0)
            bubble.pack(fill="x")
            
            # Inner padding for content
            padding = tk.Frame(bubble, bg=theme_manager.get_color("bg_ai_message"))
            padding.pack(fill="both", expand=True, padx=16, pady=14)
            
            # Modern text widget for AI messages
            text_widget = tk.Text(padding,
                                bg=theme_manager.get_color("bg_ai_message"),
                                fg=theme_manager.get_color("fg_ai"),
                                font=theme_manager.get_font(size=13),
                                wrap=tk.WORD,
                                relief="flat",
                                bd=0,
                                height=1,
                                cursor="arrow",
                                state=tk.DISABLED,
                                selectbackground=theme_manager.get_color("bg_user_message"))
            text_widget.pack(fill="both", expand=True)
            
            # Insert and format text
            text_widget.config(state=tk.NORMAL)
            
            # Enhanced text formatting for better readability
            formatted_text = self._format_ai_text(text)
            text_widget.insert(tk.END, formatted_text)
            
            text_widget.config(state=tk.DISABLED)
            
            # Auto-resize height based on content
            text_widget.update_idletasks()
            lines = int(text_widget.index('end-1c').split('.')[0])
            text_widget.config(height=min(lines, 60))  # 3x larger: 20 * 3 = 60
        
        # Store message for later reference
        self.messages.append({
            'text': text,
            'type': message_type,
            'image': image_filename,
            'widget': msg_container
        })
        
        # Auto-scroll to bottom
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)
    
    def _format_ai_text(self, text):
        """Format AI text for better readability"""
        import re
        
        # Improve formatting for SQL and code blocks
        formatted = text.replace('```', '\n```')
        
        # Add proper spacing after bullet points
        formatted = formatted.replace('• ', '• ')
        formatted = formatted.replace('* ', '• ')
        formatted = formatted.replace('- ', '• ')
        
        # Ensure proper line breaks for numbered lists
        formatted = re.sub(r'(\d+\.)(?!\d)', r'\n\1 ', formatted)
        
        # Format headers and sections
        formatted = re.sub(r'#{1,3}\s*([^#\n]+)', r'\n\1\n', formatted)
        
        # Clean up multiple newlines but preserve structure
        formatted = re.sub(r'\n{3,}', '\n\n', formatted)
        formatted = formatted.strip()
        
        return formatted
    
    def clear_messages(self):
        """Clear all messages"""
        for message in self.messages:
            message['widget'].destroy()
        self.messages.clear()
    
    def apply_theme(self):
        """Apply current theme to the chat widget"""
        bg_color = theme_manager.get_color("bg_chat")
        self.configure(bg=bg_color)
        self.canvas.configure(bg=bg_color)
        self.scrollable_frame.configure(bg=bg_color)
        
        # Reapply theme to existing messages
        for message in self.messages:
            if message['type'] == 'user':
                # Update user message colors
                pass
            else:
                # Update AI message colors
                pass


class ModernInputWidget(Frame):
    """Modern input widget with Claude-like styling"""
    
    def __init__(self, parent, on_send=None, on_image_upload=None, on_image_paste=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.on_send = on_send
        self.on_image_upload = on_image_upload
        self.on_image_paste = on_image_paste
        self.current_image = {'data': None, 'filename': None}
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Setup the input UI"""
        # Main input container with border
        self.input_container = Frame(self, relief="solid", bd=1)
        self.input_container.pack(fill="x", padx=15, pady=10)
        
        # Image attachment indicator
        self.image_frame = Frame(self.input_container)
        self.image_status = tk.Label(self.image_frame, text="", font=theme_manager.get_font(size=10))
        
        # Input text area
        self.text_frame = Frame(self.input_container)
        self.text_frame.pack(fill="x", padx=15, pady=10)
        
        self.input_text = tk.Text(self.text_frame,
                                height=3,
                                wrap=tk.WORD,
                                relief="flat",
                                bd=0,
                                font=theme_manager.get_font(size=12))
        self.input_text.pack(fill="x")
        
        # Placeholder text
        self.placeholder_text = "Ask me anything..."
        self.is_placeholder_active = False
        self.add_placeholder()
        
        # Bind events
        self.input_text.bind("<FocusIn>", self.remove_placeholder)
        self.input_text.bind("<FocusOut>", self.add_placeholder)
        self.input_text.bind("<KeyRelease>", self.update_send_button)
        self.input_text.bind("<Return>", self.handle_enter_key)
        self.input_text.bind("<Shift-Return>", self.handle_shift_enter)
        
        # Bind paste shortcut for images
        self.input_text.bind("<Control-Shift-v>", lambda e: self.handle_image_paste())
        
        # Bottom toolbar
        self.toolbar = Frame(self.input_container)
        self.toolbar.pack(fill="x", padx=15, pady=(0, 10))
        
        # Left side - image buttons
        self.image_buttons = Frame(self.toolbar)
        self.image_buttons.pack(side="left")
        
        self.upload_btn = tk.Button(self.image_buttons,
                                  text="📎",
                                  font=theme_manager.get_font(size=14),
                                  relief="flat",
                                  bd=0,
                                  width=3,
                                  command=self.upload_image)
        self.upload_btn.pack(side="left", padx=(0, 5))
        
        self.paste_btn = tk.Button(self.image_buttons,
                                 text="📋",
                                 font=theme_manager.get_font(size=14),
                                 relief="flat",
                                 bd=0,
                                 width=3,
                                 command=self.paste_image)
        self.paste_btn.pack(side="left", padx=5)
        
        # Right side - send button
        self.send_btn = tk.Button(self.toolbar,
                                text="Send",
                                font=theme_manager.get_font(size=11, weight="bold"),
                                relief="flat",
                                bd=0,
                                padx=20,
                                pady=8,
                                command=self.send_message)
        self.send_btn.pack(side="right")
        
        # Bind events
        self.input_text.bind('<Control-Return>', lambda e: self.send_message())
        self.input_text.bind('<Control-Shift-V>', lambda e: self.paste_image())
        self.input_text.bind('<FocusIn>', self.remove_placeholder)
        self.input_text.bind('<FocusOut>', self.add_placeholder)
        self.input_text.bind('<KeyRelease>', self.update_send_button)
    
    def add_placeholder(self, event=None):
        """Add placeholder text"""
        current_text = self.input_text.get("1.0", tk.END).strip()
        if not current_text or current_text == self.placeholder_text:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", self.placeholder_text)
            self.input_text.config(fg=theme_manager.get_color("fg_tertiary"))
            self.is_placeholder_active = True
    
    def remove_placeholder(self, event=None):
        """Remove placeholder text"""
        if hasattr(self, 'is_placeholder_active') and self.is_placeholder_active:
            self.input_text.delete("1.0", tk.END)
            self.input_text.config(fg=theme_manager.get_color("fg_primary"))
            self.is_placeholder_active = False
    
    def handle_enter_key(self, event=None):
        """Handle Enter key press - send message"""
        if event:
            event.widget.event_generate('<Control-Return>')  # This will be ignored
            return "break"  # Prevent default newline behavior
        
        # Get text and send if not empty
        text = self.get_text()
        if text.strip():
            self.send_message()
        return "break"
    
    def handle_shift_enter(self, event=None):
        """Handle Shift+Enter - insert newline"""
        # Let the default behavior happen (insert newline)
        return None
    
    def handle_image_paste(self):
        """Handle image paste from clipboard"""
        if self.on_image_paste:
            self.on_image_paste()
    
    def update_send_button(self, event=None):
        """Update send button state"""
        has_content = bool(self.get_text().strip())
        
        if has_content:
            theme_manager.apply_theme_to_widget(self.send_btn, "primary_button")
        else:
            theme_manager.apply_theme_to_widget(self.send_btn, "button")
    
    def upload_image(self):
        """Handle image upload"""
        if self.on_image_upload:
            self.on_image_upload()
    
    def paste_image(self):
        """Handle image paste"""
        if self.on_image_paste:
            self.on_image_paste()
    
    def set_image(self, image_data, filename):
        """Set current image"""
        self.current_image['data'] = image_data
        self.current_image['filename'] = filename
        
        if image_data:
            self.image_frame.pack(fill="x", padx=15, pady=(10, 0))
            self.image_status.config(text=f"📷 {filename}", 
                                   fg=theme_manager.get_color("fg_success"))
            self.image_status.pack(side="left")
            
            # Add clear button
            clear_btn = tk.Button(self.image_frame,
                                text="✕",
                                font=theme_manager.get_font(size=10),
                                relief="flat",
                                bd=0,
                                fg=theme_manager.get_color("fg_error"),
                                command=self.clear_image)
            clear_btn.pack(side="right")
        else:
            self.image_frame.pack_forget()
    
    def clear_image(self):
        """Clear current image"""
        self.current_image['data'] = None
        self.current_image['filename'] = None
        self.image_frame.pack_forget()
    
    def send_message(self):
        """Send the message"""
        text = self.input_text.get("1.0", tk.END).strip()
        if text and text != self.placeholder_text:
            if self.on_send:
                self.on_send(text, self.current_image['data'], self.current_image['filename'])
            
            # Clear input
            self.input_text.delete("1.0", tk.END)
            self.add_placeholder()
            self.update_send_button()
            
            # Keep image for follow-up questions
            # self.clear_image()  # Uncomment if you want to clear image after sending
    
    def get_text(self):
        """Get current input text"""
        if hasattr(self, 'is_placeholder_active') and self.is_placeholder_active:
            return ""
        text = self.input_text.get("1.0", tk.END).strip()
        return text
    
    def set_text(self, text):
        """Set input text"""
        self.input_text.delete("1.0", tk.END)
        if text:
            self.input_text.insert("1.0", text)
            self.input_text.config(fg=theme_manager.get_color("fg_primary"))
        else:
            self.add_placeholder()
    
    def apply_theme(self):
        """Apply current theme"""
        bg_color = theme_manager.get_color("bg_primary")
        input_bg = theme_manager.get_color("bg_input")
        border_color = theme_manager.get_color("border_input")
        
        self.configure(bg=bg_color)
        self.input_container.configure(bg=input_bg, highlightbackground=border_color)
        self.text_frame.configure(bg=input_bg)
        self.toolbar.configure(bg=input_bg)
        self.image_frame.configure(bg=input_bg)
        self.image_buttons.configure(bg=input_bg)
        
        theme_manager.apply_theme_to_widget(self.input_text, "input")
        theme_manager.apply_theme_to_widget(self.upload_btn, "button")
        theme_manager.apply_theme_to_widget(self.paste_btn, "button")
        theme_manager.apply_theme_to_widget(self.send_btn, "button")
        theme_manager.apply_theme_to_widget(self.image_status, "default")


class ModernAIInterface:
    """Modern AI Interface with Claude-like design"""
    
    def __init__(self, ai_config, sql_getter_callback):
        self.ai_config = ai_config
        self.get_sql = sql_getter_callback
    
    def show_modern_chat(self, title, initial_content, sql_context=""):
        """Show modern chat interface"""
        # Create main window
        chat_window = Toplevel()
        chat_window.title(title)
        chat_window.geometry("1400x900")
        chat_window.minsize(1000, 700)
        
        # Center the window on screen
        chat_window.update_idletasks()
        width = chat_window.winfo_width()
        height = chat_window.winfo_height()
        screen_width = chat_window.winfo_screenwidth()
        screen_height = chat_window.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        chat_window.geometry(f"{width}x{height}+{x}+{y}")
        
        # Apply theme to window
        chat_window.configure(bg=theme_manager.get_color("bg_primary"))
        
        # Create header with theme toggle and zoom controls
        self.create_header(chat_window, title)
        
        # Main content area
        content_frame = Frame(chat_window)
        content_frame.pack(fill="both", expand=True)
        theme_manager.apply_theme_to_widget(content_frame, "default")
        
        # Chat area
        self.chat_widget = ModernChatWidget(content_frame, ai_config=self.ai_config)
        self.chat_widget.pack(fill="both", expand=True, padx=25, pady=(0, 8))
        
        # Add initial AI message
        if initial_content:
            self.chat_widget.add_message(initial_content, "ai")
        
        # Input area
        self.input_widget = ModernInputWidget(
            content_frame,
            on_send=lambda text, img_data, img_name: self.handle_message(text, img_data, img_name, sql_context),
            on_image_upload=self.handle_image_upload,
            on_image_paste=self.handle_image_paste
        )
        self.input_widget.pack(fill="x", padx=25, pady=(0, 15))
        
        # Store references for theme updates
        self.chat_window = chat_window
        
        return chat_window
    
    def create_header(self, parent, title):
        """Create modern header with controls"""
        header = Frame(parent, height=50)
        header.pack(fill="x", padx=25, pady=(15, 8))
        header.pack_propagate(False)
        theme_manager.apply_theme_to_widget(header, "header")
        
        # Title
        title_label = tk.Label(header,
                              text=title,
                              font=theme_manager.get_font(size=15, weight="bold"))
        title_label.pack(side="left", pady=12)
        theme_manager.apply_theme_to_widget(title_label, "header")
        
        # Controls frame
        controls = Frame(header)
        controls.pack(side="right", pady=8)
        theme_manager.apply_theme_to_widget(controls, "header")
        
        # Zoom controls
        zoom_frame = Frame(controls)
        zoom_frame.pack(side="left", padx=(0, 20))
        theme_manager.apply_theme_to_widget(zoom_frame, "header")
        
        zoom_out_btn = tk.Button(zoom_frame,
                               text="🔍−",
                               font=theme_manager.get_font(size=12),
                               relief="flat",
                               bd=0,
                               padx=8,
                               command=self.zoom_out)
        zoom_out_btn.pack(side="left", padx=2)
        theme_manager.apply_theme_to_widget(zoom_out_btn, "button")
        
        zoom_reset_btn = tk.Button(zoom_frame,
                                 text="100%",
                                 font=theme_manager.get_font(size=10),
                                 relief="flat",
                                 bd=0,
                                 padx=8,
                                 command=self.zoom_reset)
        zoom_reset_btn.pack(side="left", padx=2)
        theme_manager.apply_theme_to_widget(zoom_reset_btn, "button")
        
        zoom_in_btn = tk.Button(zoom_frame,
                              text="🔍+",
                              font=theme_manager.get_font(size=12),
                              relief="flat",
                              bd=0,
                              padx=8,
                              command=self.zoom_in)
        zoom_in_btn.pack(side="left", padx=2)
        theme_manager.apply_theme_to_widget(zoom_in_btn, "button")
        
        # Theme toggle
        theme_btn = tk.Button(controls,
                            text="🌙" if theme_manager.current_theme == "light" else "☀️",
                            font=theme_manager.get_font(size=14),
                            relief="flat",
                            bd=0,
                            padx=10,
                            command=self.toggle_theme)
        theme_btn.pack(side="left", padx=10)
        theme_manager.apply_theme_to_widget(theme_btn, "button")
        
        # Store references for updates
        self.zoom_reset_btn = zoom_reset_btn
        self.theme_btn = theme_btn
    
    def handle_message(self, text, image_data, image_filename, sql_context):
        """Handle user message"""
        # Add user message to chat
        self.chat_widget.add_message(text, "user", image_filename)
        
        # Show thinking indicator
        thinking_msg = self.chat_widget.add_message("Thinking...", "ai")
        
        # Get AI response in background
        def get_response():
            try:
                # Build context
                if sql_context:
                    context_prompt = f"SQL Code:\n{sql_context}\n\nQuestion: {text}"
                else:
                    context_prompt = text
                
                if image_data:
                    context_prompt += "\n\nPlease also analyze the provided image."
                
                response = self.ai_config.call_ai_api(context_prompt, image_data=image_data)
                
                if response:
                    # Remove thinking message and add real response
                    self.chat_window.after(0, lambda: self.update_last_message(response))
                else:
                    self.chat_window.after(0, lambda: self.update_last_message("Sorry, I couldn't process your request. Please check your AI configuration."))
                    
            except Exception as e:
                self.chat_window.after(0, lambda: self.update_last_message(f"Error: {str(e)}"))
        
        threading.Thread(target=get_response, daemon=True).start()
    
    def update_last_message(self, new_text):
        """Update the last AI message"""
        if self.chat_widget.messages:
            # Remove the last message (thinking...)
            last_msg = self.chat_widget.messages.pop()
            last_msg['widget'].destroy()
        
        # Add the real response
        self.chat_widget.add_message(new_text, "ai")
    
    def handle_image_upload(self):
        """Handle image upload"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            try:
                image_data = self.ai_config.process_image_for_ai(file_path)
                filename = os.path.basename(file_path)
                self.input_widget.set_image(image_data, filename)
            except Exception as e:
                messagebox.showerror("Image Error", f"Failed to process image: {str(e)}")
    
    def handle_image_paste(self):
        """Handle image paste"""
        try:
            image_data = self.ai_config.process_image_from_clipboard()
            if image_data:
                self.input_widget.set_image(image_data, "clipboard_image.png")
            else:
                messagebox.showinfo("No Image", "No image found in clipboard.")
        except Exception as e:
            messagebox.showerror("Paste Error", f"Failed to paste image: {str(e)}")
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        new_theme = theme_manager.toggle_theme()
        self.update_ui_theme()
        
        # Update theme button
        self.theme_btn.config(text="🌙" if new_theme == "light" else "☀️")
    
    def zoom_in(self):
        """Zoom in"""
        zoom_level = theme_manager.zoom_in()
        self.update_ui_fonts()
        self.zoom_reset_btn.config(text=f"{int(zoom_level * 100)}%")
    
    def zoom_out(self):
        """Zoom out"""
        zoom_level = theme_manager.zoom_out()
        self.update_ui_fonts()
        self.zoom_reset_btn.config(text=f"{int(zoom_level * 100)}%")
    
    def zoom_reset(self):
        """Reset zoom"""
        zoom_level = theme_manager.reset_zoom()
        self.update_ui_fonts()
        self.zoom_reset_btn.config(text=f"{int(zoom_level * 100)}%")
    
    def update_ui_theme(self):
        """Update UI theme"""
        try:
            # Update main window
            self.chat_window.configure(bg=theme_manager.get_color("bg_primary"))
            
            # Update all child widgets recursively
            for widget in self.chat_window.winfo_children():
                self._update_widget_theme_recursive(widget)
            
            # Update specific components
            if hasattr(self, 'chat_widget'):
                self.chat_widget.apply_theme()
            
            if hasattr(self, 'input_widget'):
                self.input_widget.apply_theme()
                
            # Force refresh of existing messages
            if hasattr(self, 'chat_widget') and hasattr(self.chat_widget, 'messages'):
                for message in self.chat_widget.messages:
                    self._update_message_theme(message['widget'])
                    
        except Exception as e:
            print(f"Error updating UI theme: {e}")
    
    def _update_widget_theme_recursive(self, widget):
        """Recursively update theme for all widgets"""
        try:
            if hasattr(widget, 'config'):
                # Apply appropriate theme based on widget type
                widget_class = widget.winfo_class()
                if widget_class in ['Frame', 'Toplevel']:
                    widget.config(bg=theme_manager.get_color("bg_primary"))
                elif widget_class == 'Label':
                    widget.config(
                        bg=theme_manager.get_color("bg_primary"),
                        fg=theme_manager.get_color("fg_primary")
                    )
                elif widget_class == 'Button':
                    theme_manager.apply_theme_to_widget(widget, "button")
                elif widget_class in ['Text', 'Entry']:
                    theme_manager.apply_theme_to_widget(widget, "input")
            
            # Recurse through children
            for child in widget.winfo_children():
                self._update_widget_theme_recursive(child)
        except Exception:
            pass
    
    def _update_message_theme(self, message_widget):
        """Update theme for a message widget"""
        try:
            self._update_widget_theme_recursive(message_widget)
        except Exception:
            pass
    
    def update_ui_fonts(self):
        """Update UI fonts for zoom"""
        try:
            # Update chat window if it exists
            if hasattr(self, 'chat_window') and self.chat_window.winfo_exists():
                # Update header fonts
                for widget in self.chat_window.winfo_children():
                    self._update_widget_fonts_recursive(widget)
                
                # Update theme and refresh
                self.update_ui_theme()
                
                # Force refresh of all messages with new font sizes
                if hasattr(self, 'chat_widget'):
                    self.chat_widget.apply_theme()
                    # Update all existing text widgets in messages
                    for message in self.chat_widget.messages:
                        self._update_message_fonts(message['widget'])
                
                if hasattr(self, 'input_widget'):
                    self.input_widget.apply_theme()
                    
        except Exception as e:
            print(f"Error updating UI fonts: {e}")
    
    def _update_widget_fonts_recursive(self, widget):
        """Recursively update fonts for all widgets"""
        try:
            if hasattr(widget, 'config'):
                if 'font' in widget.keys():
                    current_font = widget.cget('font')
                    if isinstance(current_font, tuple) and len(current_font) >= 2:
                        family, size = current_font[0], current_font[1]
                        weight = current_font[2] if len(current_font) > 2 else "normal"
                        new_font = theme_manager.get_font(family, size, weight)
                        widget.config(font=new_font)
            
            # Recurse through children
            for child in widget.winfo_children():
                self._update_widget_fonts_recursive(child)
        except Exception:
            pass
    
    def _update_message_fonts(self, message_widget):
        """Update fonts in a message widget"""
        try:
            self._update_widget_fonts_recursive(message_widget)
        except Exception:
            pass