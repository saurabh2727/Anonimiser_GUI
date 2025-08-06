#!/usr/bin/env python3
"""
AI Interface Module
Handles AI interaction windows and conversational features
"""

import tkinter as tk
from tkinter import messagebox, Toplevel, scrolledtext, filedialog
import threading
import os
from theme_manager import theme_manager
from modern_ai_interface import ModernAIInterface
try:
    import pyperclip
except ImportError:
    pyperclip = None


class AIInterface:
    """Manages AI interaction windows and conversations"""
    
    def __init__(self, ai_config, sql_getter_callback):
        self.ai_config = ai_config
        self.get_sql = sql_getter_callback  # Callback to get SQL from main app
        self.modern_interface = ModernAIInterface(ai_config, sql_getter_callback)
    
    def show_modern_conversation(self, title, content, sql_context=""):
        """Show modern Claude-like conversation interface"""
        return self.modern_interface.show_modern_chat(title, content, sql_context)
    
    def show_understand_result(self, title, content, sql_context=""):
        """Show AI analysis result with conversation capability (legacy)"""
        result_window = Toplevel()
        result_window.title(title)
        result_window.geometry("1000x800")
        result_window.resizable(True, True)
        
        # Header
        header_frame = tk.Frame(result_window, bg="#E8F5E8")
        header_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(header_frame, text=f"🤖 {title}", font=('Arial', 14, 'bold'), bg="#E8F5E8").pack(pady=5)
        
        # Create main container with PanedWindow for resizable sections
        main_paned = tk.PanedWindow(result_window, orient=tk.VERTICAL, sashrelief=tk.RAISED)
        main_paned.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Top frame for AI response
        top_frame = tk.Frame(main_paned)
        main_paned.add(top_frame, minsize=200)
        
        # AI Response label
        tk.Label(top_frame, text="AI Analysis:", font=('Arial', 11, 'bold')).pack(anchor="w", padx=5, pady=2)
        
        # Content (AI response)
        ai_text_widget = scrolledtext.ScrolledText(top_frame, wrap=tk.WORD, font=('Arial', 10), height=15)
        ai_text_widget.pack(fill="both", expand=True, padx=5, pady=2)
        ai_text_widget.insert("1.0", content)
        ai_text_widget.configure(state='disabled')
        
        # Bottom frame for conversation
        bottom_frame = tk.Frame(main_paned)
        main_paned.add(bottom_frame, minsize=200)
        
        # Conversation label
        tk.Label(bottom_frame, text="💬 Continue Conversation:", font=('Arial', 11, 'bold')).pack(anchor="w", padx=5, pady=2)
        
        # Conversation history
        conversation_text = scrolledtext.ScrolledText(bottom_frame, wrap=tk.WORD, font=('Arial', 9), height=10, bg="#F5F5F5")
        conversation_text.pack(fill="both", expand=True, padx=5, pady=2)
        conversation_text.configure(state='disabled')
        
        # Input frame for new questions
        input_frame = tk.Frame(bottom_frame)
        input_frame.pack(fill="x", padx=5, pady=5)
        
        # Question input
        question_label = tk.Label(input_frame, text="Ask about this SQL:", font=('Arial', 9))
        question_label.pack(anchor="w")
        
        # Image status frame
        image_frame = tk.Frame(input_frame)
        image_frame.pack(fill="x", pady=2)
        
        image_status_label = tk.Label(image_frame, text="", font=('Arial', 8), fg="green")
        image_status_label.pack(side=tk.LEFT)
        
        # Image buttons frame
        image_btn_frame = tk.Frame(image_frame)
        image_btn_frame.pack(side=tk.RIGHT)
        
        question_entry = tk.Text(input_frame, height=3, font=('Arial', 10))
        question_entry.pack(fill="x", pady=2)
        
        # Store current image data
        current_image_data = {'data': None, 'filename': None}
        
        # Image handling functions
        def upload_image():
            """Upload image from file"""
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
                    current_image_data['data'] = image_data
                    current_image_data['filename'] = os.path.basename(file_path)
                    image_status_label.config(text=f"📷 Image: {current_image_data['filename']}")
                    question_label.config(text="Ask about this SQL and/or the image:")
                except Exception as e:
                    messagebox.showerror("Image Error", f"Failed to process image: {str(e)}")
        
        def paste_image():
            """Paste image from clipboard"""
            try:
                image_data = self.ai_config.process_image_from_clipboard()
                if image_data:
                    current_image_data['data'] = image_data
                    current_image_data['filename'] = "clipboard_image.png"
                    image_status_label.config(text="📷 Image: pasted from clipboard")
                    question_label.config(text="Ask about this SQL and/or the image:")
                else:
                    messagebox.showinfo("No Image", "No image found in clipboard.")
            except Exception as e:
                messagebox.showerror("Paste Error", f"Failed to paste image: {str(e)}")
        
        def clear_image():
            """Clear current image"""
            current_image_data['data'] = None
            current_image_data['filename'] = None
            image_status_label.config(text="")
            question_label.config(text="Ask about this SQL:")
        
        # Add image buttons
        upload_btn = tk.Button(image_btn_frame, text="📁 Upload Image", command=upload_image, 
                              bg="#2196F3", fg="black", font=('Arial', 8))
        upload_btn.pack(side=tk.LEFT, padx=2)
        
        paste_btn = tk.Button(image_btn_frame, text="📋 Paste Image", command=paste_image,
                             bg="#FF9800", fg="black", font=('Arial', 8))
        paste_btn.pack(side=tk.LEFT, padx=2)
        
        clear_btn = tk.Button(image_btn_frame, text="❌ Clear", command=clear_image,
                             bg="#F44336", fg="black", font=('Arial', 8))
        clear_btn.pack(side=tk.LEFT, padx=2)
        
        # Store conversation history and SQL context
        conversation_history = []
        if not sql_context:
            sql_context = self.get_sql() if self.get_sql else ""
        
        def ask_question():
            question = question_entry.get("1.0", tk.END).strip()
            if not question:
                messagebox.showwarning("Empty Question", "Please enter a question about the SQL.")
                return
            
            # Check if we have an image
            has_image = current_image_data['data'] is not None
            image_info = f" (with image: {current_image_data['filename']})" if has_image else ""
            
            # Add question to conversation
            conversation_text.configure(state='normal')
            conversation_text.insert(tk.END, f"\n🙋 You: {question}{image_info}\n")
            conversation_text.configure(state='disabled')
            conversation_text.see(tk.END)
            
            # Clear input but keep image for potential follow-up questions
            question_entry.delete("1.0", tk.END)
            
            # Disable ask button during processing
            ask_btn.config(state='disabled', text="Thinking...")
            
            def get_ai_response():
                try:
                    # Build conversation context
                    context_prompt = f"SQL Code:\n{sql_context}\n\nPrevious Analysis:\n{content}\n\n"
                    if conversation_history:
                        context_prompt += "Previous Questions and Answers:\n"
                        for i, (q, a) in enumerate(conversation_history):
                            context_prompt += f"Q{i+1}: {q}\nA{i+1}: {a}\n\n"
                    
                    if has_image:
                        prompt = f"""{context_prompt}New Question: {question}

Please answer this specific question about the SQL code and/or analyze the provided image. Be concise and focused on the question asked."""
                    else:
                        prompt = f"""{context_prompt}New Question: {question}

Please answer this specific question about the SQL code. Be concise and focused on the question asked."""
                    
                    # Pass image data if available
                    response = self.ai_config.call_ai_api(prompt, image_data=current_image_data['data'] if has_image else None)
                    
                    if response:
                        # Add to conversation history
                        conversation_history.append((question, response))
                        
                        # Update UI in main thread
                        result_window.after(0, lambda: update_conversation(response))
                    else:
                        result_window.after(0, lambda: show_error("Failed to get AI response. Please check your configuration."))
                        
                except Exception as e:
                    result_window.after(0, lambda err=e: show_error(f"Error: {str(err)}"))
            
            def update_conversation(response):
                conversation_text.configure(state='normal')
                conversation_text.insert(tk.END, f"AI: {response}\n{'-'*50}\n")
                conversation_text.configure(state='disabled')
                conversation_text.see(tk.END)
                ask_btn.config(state='normal', text="💬 Ask")
            
            def show_error(error_msg):
                conversation_text.configure(state='normal')
                conversation_text.insert(tk.END, f"❌ Error: {error_msg}\n{'-'*50}\n")
                conversation_text.configure(state='disabled')
                conversation_text.see(tk.END)
                ask_btn.config(state='normal', text="💬 Ask")
            
            # Run AI call in background thread
            threading.Thread(target=get_ai_response, daemon=True).start()
        
        # Question buttons
        question_btn_frame = tk.Frame(input_frame)
        question_btn_frame.pack(fill="x", pady=2)
        
        ask_btn = tk.Button(question_btn_frame, text="💬 Ask", command=ask_question, bg="#4CAF50", fg="black")
        ask_btn.pack(side=tk.LEFT, padx=2)
        
        # Quick question buttons
        def quick_question(q):
            question_entry.delete("1.0", tk.END)
            question_entry.insert("1.0", q)
        
        quick_questions = [
            "What tables are being used?",
            "Explain the joins in this query",
            "What filters are applied?",
            "How can I optimize this query?",
            "What does this query return?"
        ]
        
        for i, q in enumerate(quick_questions):
            btn = tk.Button(question_btn_frame, text=f"Q{i+1}", command=lambda quest=q: quick_question(quest), 
                          bg="#2196F3", fg="black", font=('Arial', 8))
            btn.pack(side=tk.LEFT, padx=1)
        
        # Buttons frame
        button_frame = tk.Frame(result_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        def copy_result():
            # Copy both analysis and conversation
            full_content = f"AI Analysis:\n{content}\n\n"
            if conversation_history:
                full_content += "Conversation:\n"
                for q, a in conversation_history:
                    full_content += f"Q: {q}\nA: {a}\n\n"
            
            if pyperclip:
                pyperclip.copy(full_content)
                copy_btn.config(text="✅ Copied!")
                result_window.after(2000, lambda: copy_btn.config(text="📋 Copy All"))
            else:
                messagebox.showinfo("Copy", "pyperclip module not available. Content printed to console.")
                print(full_content)
        
        copy_btn = tk.Button(button_frame, text="📋 Copy All", command=copy_result, bg="#607D8B", fg="black")
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="❌ Close", command=result_window.destroy, bg="#F44336", fg="black").pack(side=tk.RIGHT, padx=5)
        
        # Bind keyboard shortcuts
        def on_enter(event):
            if event.state & 0x4:  # Ctrl+Enter
                ask_question()
                return "break"
        
        def on_paste_image(event):
            if event.state & 0x4:  # Ctrl+Shift+V
                paste_image()
                return "break"
        
        question_entry.bind("<Control-Return>", on_enter)
        question_entry.bind("<Control-Shift-V>", on_paste_image)
        
        # Add help text for shortcuts
        help_text = tk.Label(input_frame, text="💡 Ctrl+Enter: Ask question, Ctrl+Shift+V: Paste image", 
                            font=('Arial', 8), fg="gray")
        help_text.pack(anchor="w", pady=2)
        
        return result_window
    
    def show_modification_result(self, response, data_choice):
        """Show AI modification result with option to apply changes"""
        result_window = Toplevel()
        result_window.title("AI Code Modification Result")
        result_window.geometry("1000x800")
        
        # Header
        header_frame = tk.Frame(result_window, bg="#E8F5E8")
        header_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(header_frame, text="✏️ Modified SQL Code", font=('Arial', 14, 'bold'), bg="#E8F5E8").pack(pady=5)
        
        # Content
        text_widget = scrolledtext.ScrolledText(result_window, wrap=tk.WORD, font=('Consolas', 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=5)
        text_widget.insert("1.0", response)
        text_widget.configure(state='disabled')
        
        # Buttons
        button_frame = tk.Frame(result_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        def copy_result():
            if pyperclip:
                pyperclip.copy(response)
                copy_btn.config(text="✅ Copied!")
                result_window.after(2000, lambda: copy_btn.config(text="📋 Copy"))
            else:
                messagebox.showinfo("Copy", "pyperclip module not available. Content printed to console.")
                print(response)
        
        def apply_changes():
            # This would need to be implemented by the main app
            messagebox.showinfo("Apply Changes", "This feature would apply the changes to your SQL. Implementation depends on the main application.")
        
        copy_btn = tk.Button(button_frame, text="📋 Copy", command=copy_result, bg="#607D8B", fg="black")
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="✅ Apply Changes", command=apply_changes, bg="#4CAF50", fg="black").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="❌ Close", command=result_window.destroy, bg="#F44336", fg="black").pack(side=tk.RIGHT, padx=5)
        
        return result_window
    
    def create_progress_window(self, message, parent=None):
        """Create a progress window for AI operations"""
        progress_window = Toplevel(parent) if parent else Toplevel()
        progress_window.title("AI Processing")
        progress_window.geometry("400x150")
        progress_window.resizable(False, False)
        
        # Center the window
        progress_window.transient(parent if parent else None)
        progress_window.grab_set()
        
        # Content
        frame = tk.Frame(progress_window, bg="#F0F8FF")
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(frame, text="🤖 AI Processing", font=('Arial', 14, 'bold'), bg="#F0F8FF").pack(pady=10)
        tk.Label(frame, text=message, font=('Arial', 10), bg="#F0F8FF", wraplength=350).pack(pady=5)
        
        # Progress bar (indeterminate)
        try:
            from tkinter import ttk
            progress_bar = ttk.Progressbar(frame, mode='indeterminate')
            progress_bar.pack(pady=10, fill="x")
            progress_bar.start(10)
        except ImportError:
            tk.Label(frame, text="Processing...", font=('Arial', 10), bg="#F0F8FF").pack(pady=10)
        
        return progress_window
    
    def get_instruction_from_user(self, parent=None):
        """Get modification instructions from user"""
        instruction_window = Toplevel(parent) if parent else Toplevel()
        instruction_window.title("AI Code Modification Instructions")
        instruction_window.geometry("650x500")
        instruction_window.resizable(True, True)
        
        # Make it modal
        if parent:
            instruction_window.transient(parent)
            instruction_window.grab_set()
        
        # Header
        header_frame = tk.Frame(instruction_window, bg="#E8F5E8")
        header_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(header_frame, text="✏️ Modify SQL Code", font=('Arial', 14, 'bold'), bg="#E8F5E8").pack(pady=5)
        tk.Label(header_frame, text="Describe how you want to modify the SQL code", bg="#E8F5E8").pack()
        
        # Instructions input
        tk.Label(instruction_window, text="Instructions:", font=('Arial', 12, 'bold')).pack(anchor="w", padx=20, pady=(10, 5))
        
        # Image support for modification instructions
        image_mod_frame = tk.Frame(instruction_window)
        image_mod_frame.pack(fill="x", padx=20, pady=2)
        
        image_mod_status = tk.Label(image_mod_frame, text="", font=('Arial', 8), fg="green")
        image_mod_status.pack(side=tk.LEFT)
        
        # Store image data for modification
        mod_image_data = {'data': None, 'filename': None}
        
        def upload_mod_image():
            file_path = filedialog.askopenfilename(
                title="Select Image",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"), ("All files", "*.*")]
            )
            if file_path:
                try:
                    image_data = self.ai_config.process_image_for_ai(file_path)
                    mod_image_data['data'] = image_data
                    mod_image_data['filename'] = os.path.basename(file_path)
                    image_mod_status.config(text=f"📷 Image: {mod_image_data['filename']}")
                except Exception as e:
                    messagebox.showerror("Image Error", f"Failed to process image: {str(e)}")
        
        def paste_mod_image():
            try:
                image_data = self.ai_config.process_image_from_clipboard()
                if image_data:
                    mod_image_data['data'] = image_data
                    mod_image_data['filename'] = "clipboard_image.png"
                    image_mod_status.config(text="📷 Image: pasted from clipboard")
                else:
                    messagebox.showinfo("No Image", "No image found in clipboard.")
            except Exception as e:
                messagebox.showerror("Paste Error", f"Failed to paste image: {str(e)}")
        
        def clear_mod_image():
            mod_image_data['data'] = None
            mod_image_data['filename'] = None
            image_mod_status.config(text="")
        
        # Image buttons for modification
        image_mod_btn_frame = tk.Frame(image_mod_frame)
        image_mod_btn_frame.pack(side=tk.RIGHT)
        
        tk.Button(image_mod_btn_frame, text="📁 Upload", command=upload_mod_image, 
                 bg="#2196F3", fg="black", font=('Arial', 8)).pack(side=tk.LEFT, padx=1)
        tk.Button(image_mod_btn_frame, text="📋 Paste", command=paste_mod_image,
                 bg="#FF9800", fg="black", font=('Arial', 8)).pack(side=tk.LEFT, padx=1)
        tk.Button(image_mod_btn_frame, text="❌", command=clear_mod_image,
                 bg="#F44336", fg="black", font=('Arial', 8)).pack(side=tk.LEFT, padx=1)
        
        # Create frame for text with scrollbar
        text_frame = tk.Frame(instruction_window)
        text_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        instructions_text = tk.Text(text_frame, wrap=tk.WORD, font=('Arial', 11), height=12)
        text_scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=instructions_text.yview)
        instructions_text.configure(yscrollcommand=text_scrollbar.set)
        
        instructions_text.pack(side=tk.LEFT, fill="both", expand=True)
        text_scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Add some example text
        example_text = """Enter your modification instructions here. For example:

• Add a WHERE clause to filter records from last 30 days
• Join with another table called 'users'
• Add ORDER BY clause to sort by date descending
• Convert this to a stored procedure
• Optimize this query for better performance
• Add error handling to this query"""
        
        instructions_text.insert("1.0", example_text)
        instructions_text.tag_add("example", "1.0", "end")
        instructions_text.tag_config("example", foreground="gray")
        
        # Clear example text on first click
        def clear_example(event):
            if instructions_text.get("1.0", "2.0").startswith("Enter your"):
                instructions_text.delete("1.0", "end")
                instructions_text.tag_remove("example", "1.0", "end")
        
        instructions_text.bind("<FocusIn>", clear_example)
        
        # Result storage
        result = {'instructions': None, 'image_data': None, 'image_filename': None}
        
        # Buttons
        button_frame = tk.Frame(instruction_window)
        button_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        def submit_instructions():
            instructions = instructions_text.get("1.0", tk.END).strip()
            if not instructions or instructions.startswith("Enter your"):
                messagebox.showwarning("No Instructions", "Please enter modification instructions.")
                return
            
            # Include image data in result if available
            result['instructions'] = instructions
            result['image_data'] = mod_image_data['data']
            result['image_filename'] = mod_image_data['filename']
            instruction_window.destroy()
        
        # Add zoom controls for the text area
        zoom_frame = tk.Frame(button_frame)
        zoom_frame.pack(side=tk.LEFT)
        
        current_font_size = [11]  # Use list for mutable reference
        
        def zoom_in():
            if current_font_size[0] < 20:
                current_font_size[0] += 1
                instructions_text.config(font=('Arial', current_font_size[0]))
        
        def zoom_out():
            if current_font_size[0] > 8:
                current_font_size[0] -= 1
                instructions_text.config(font=('Arial', current_font_size[0]))
        
        tk.Button(zoom_frame, text="🔍+", command=zoom_in, bg="#2196F3", fg="black", 
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=2)
        tk.Button(zoom_frame, text="🔍-", command=zoom_out, bg="#2196F3", fg="black",
                 font=('Arial', 10)).pack(side=tk.LEFT, padx=2)
        
        # Submit and Cancel buttons
        tk.Button(button_frame, text="✅ Submit", command=submit_instructions, 
                 bg="#4CAF50", fg="black", font=('Arial', 11, 'bold')).pack(side=tk.RIGHT, padx=(10, 0))
        tk.Button(button_frame, text="❌ Cancel", command=instruction_window.destroy, 
                 bg="#F44336", fg="black", font=('Arial', 11, 'bold')).pack(side=tk.RIGHT)
        
        # Wait for window to close
        instruction_window.wait_window()
        
        return result
    
    def choose_data_for_ai(self, title="Choose Data to Send", parent=None):
        """Let user choose which data to send to AI"""
        choice_window = Toplevel(parent) if parent else Toplevel()
        choice_window.title(title)
        choice_window.geometry("450x300")
        choice_window.resizable(False, False)
        
        # Make it modal
        if parent:
            choice_window.transient(parent)
            choice_window.grab_set()
        
        # Header
        header_frame = tk.Frame(choice_window, bg="#E3F2FD")
        header_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(header_frame, text="🔒 Data Privacy Choice", font=('Arial', 14, 'bold'), bg="#E3F2FD").pack(pady=5)
        tk.Label(header_frame, text="Choose which version to send to AI", bg="#E3F2FD").pack()
        
        # Options
        options_frame = tk.Frame(choice_window)
        options_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        choice_var = tk.StringVar(value="original")
        
        tk.Radiobutton(options_frame, text="📄 Original SQL (with real names)", 
                      variable=choice_var, value="original", font=('Arial', 10)).pack(anchor="w", pady=5)
        
        tk.Radiobutton(options_frame, text="🎭 Masked SQL (anonymized names)", 
                      variable=choice_var, value="masked", font=('Arial', 10)).pack(anchor="w", pady=5)
        
        # Warning
        warning_frame = tk.Frame(choice_window, bg="#FFF3CD")
        warning_frame.pack(fill="x", padx=10, pady=5)
        
        warning_text = "⚠️ Consider privacy: Original SQL may contain sensitive table/column names"
        tk.Label(warning_frame, text=warning_text, bg="#FFF3CD", font=('Arial', 9), wraplength=350).pack(padx=10, pady=8)
        
        # Result storage
        result = {'choice': None}
        
        # Buttons
        button_frame = tk.Frame(choice_window)
        button_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        def confirm_choice():
            result['choice'] = choice_var.get()
            choice_window.destroy()
        
        tk.Button(button_frame, text="✅ Apply", command=confirm_choice, bg="#4CAF50", fg="black", 
                 font=('Arial', 10, 'bold')).pack(side=tk.RIGHT, padx=(10, 0))
        tk.Button(button_frame, text="❌ Cancel", command=choice_window.destroy, bg="#F44336", fg="black",
                 font=('Arial', 10, 'bold')).pack(side=tk.RIGHT)
        
        # Wait for window to close
        choice_window.wait_window()
        
        return result['choice']