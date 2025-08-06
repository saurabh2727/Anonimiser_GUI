#!/usr/bin/env python3
"""
Test script for image pasting functionality
"""

import tkinter as tk
from ai_config import AIConfig
from ai_interface import AIInterface


def test_image_functionality():
    """Test the image functionality in a simple window"""
    
    # Create main window
    root = tk.Tk()
    root.title("Image Feature Test")
    root.geometry("600x400")
    
    # Initialize AI config
    ai_config = AIConfig()
    
    # Create AI interface
    ai_interface = AIInterface(ai_config, lambda: "SELECT * FROM test_table;")
    
    # Create test button to open conversation window
    def open_conversation():
        ai_interface.show_understand_result(
            "Test Conversation with Image Support",
            "This is a test conversation window with image pasting capability. You can now:\n\n" +
            "• Upload images using the 📁 Upload Image button\n" +
            "• Paste images from clipboard using 📋 Paste Image button or Ctrl+Shift+V\n" +
            "• Clear images using the ❌ Clear button\n\n" +
            "When you have an image attached, it will be sent to the AI along with your question.\n" +
            "For local LLM, make sure you're using llava:latest model for image support.\n" +
            "For OpenAI, use gpt-4 or vision models.\n" +
            "For Anthropic, Claude models support images natively.",
            "SELECT * FROM test_table WHERE id = 1;"
        )
    
    def open_modification():
        instructions = ai_interface.get_instruction_from_user(root)
        if instructions:
            if isinstance(instructions, dict):
                inst_text = instructions.get('instructions', 'No instructions')
                img_filename = instructions.get('image_filename', 'No image')
                has_image = instructions.get('image_data') is not None
                
                result_text = f"Instructions: {inst_text}\nImage: {img_filename}\nHas Image Data: {has_image}"
            else:
                result_text = f"Instructions: {instructions}"
            
            # Show result
            result_window = tk.Toplevel(root)
            result_window.title("Modification Instructions Result")
            result_window.geometry("500x300")
            
            text_widget = tk.Text(result_window, wrap=tk.WORD)
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            text_widget.insert("1.0", result_text)
    
    # Create info frame
    info_frame = tk.Frame(root, bg="#E3F2FD")
    info_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Label(info_frame, text="🖼️ Image Feature Test", font=('Arial', 16, 'bold'), bg="#E3F2FD").pack(pady=5)
    tk.Label(info_frame, text="Test the new image pasting functionality", font=('Arial', 12), bg="#E3F2FD").pack()
    
    # Buttons frame
    buttons_frame = tk.Frame(root)
    buttons_frame.pack(fill="x", padx=20, pady=20)
    
    tk.Button(buttons_frame, text="🗣️ Test Conversation with Images", 
              command=open_conversation, bg="#4CAF50", fg="black", 
              font=('Arial', 12, 'bold'), pady=10).pack(fill="x", pady=5)
    
    tk.Button(buttons_frame, text="✏️ Test Modification with Images", 
              command=open_modification, bg="#2196F3", fg="black", 
              font=('Arial', 12, 'bold'), pady=10).pack(fill="x", pady=5)
    
    # Instructions
    instructions_text = """
📷 Image Support Features:

1. **Conversation Window:**
   • Upload images using the 📁 Upload Image button
   • Paste images from clipboard using 📋 Paste Image or Ctrl+Shift+V
   • Images are sent to AI along with your questions

2. **Modification Window:**
   • Same image upload/paste functionality
   • Images can provide context for code modifications

3. **AI Model Support:**
   • Local LLM: Use llava:latest for image support
   • OpenAI: Use gpt-4 or vision models
   • Anthropic: Claude models support images
   • Other models: Text-only (images ignored)

4. **Keyboard Shortcuts:**
   • Ctrl+Enter: Send question
   • Ctrl+Shift+V: Paste image from clipboard
    """
    
    instructions_label = tk.Label(root, text=instructions_text, justify="left", 
                                 font=('Arial', 10), bg="#F5F5F5")
    instructions_label.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    test_image_functionality()