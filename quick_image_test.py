#!/usr/bin/env python3
"""
Quick Image Test
Test image functionality after fixing configuration
"""

from ai_config import AIConfig
import tkinter as tk
from tkinter import filedialog, messagebox


def test_image_with_ai():
    """Test image processing with current AI configuration"""
    print("🧪 Testing Image Processing with AI...")
    
    # Initialize AI config
    ai_config = AIConfig()
    
    # Check if model supports images
    model = ai_config.config['model'].lower()
    provider = ai_config.config['api_provider']
    
    supports_images = False
    if provider == 'local_llm' and 'llava' in model:
        supports_images = True
    elif provider == 'openai' and ('gpt-4' in model or 'vision' in model):
        supports_images = True
    elif provider == 'anthropic':
        supports_images = True
    
    if not supports_images:
        print(f"❌ Current model ({ai_config.config['model']}) doesn't support images!")
        print("Please run: python debug_image_issue.py for solutions")
        return
    
    print(f"✅ Model {ai_config.config['model']} should support images")
    
    # Create simple GUI for testing
    root = tk.Tk()
    root.title("Image Test")
    root.geometry("400x300")
    
    result_text = tk.Text(root, wrap=tk.WORD, height=15)
    result_text.pack(fill="both", expand=True, padx=10, pady=10)
    
    def test_with_file():
        """Test with uploaded image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image to Test",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                result_text.delete(1.0, tk.END)
                result_text.insert(tk.END, "Processing image...\n\n")
                root.update()
                
                # Process image
                image_data = ai_config.process_image_for_ai(file_path)
                result_text.insert(tk.END, f"✅ Image processed successfully!\n")
                result_text.insert(tk.END, f"📁 File: {file_path}\n")
                result_text.insert(tk.END, f"📊 Data size: {len(image_data)} characters\n\n")
                
                # Test AI call
                result_text.insert(tk.END, "Sending to AI...\n")
                root.update()
                
                response = ai_config.call_ai_api("What do you see in this image?", image_data=image_data)
                
                if response:
                    result_text.insert(tk.END, f"🤖 AI Response:\n{response}\n")
                else:
                    result_text.insert(tk.END, "❌ No response from AI\n")
                    
            except Exception as e:
                result_text.insert(tk.END, f"❌ Error: {str(e)}\n")
    
    def test_clipboard():
        """Test with clipboard image"""
        try:
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "Checking clipboard...\n\n")
            root.update()
            
            image_data = ai_config.process_image_from_clipboard()
            
            if image_data:
                result_text.insert(tk.END, "✅ Image found in clipboard!\n")
                result_text.insert(tk.END, f"📊 Data size: {len(image_data)} characters\n\n")
                
                # Test AI call
                result_text.insert(tk.END, "Sending to AI...\n")
                root.update()
                
                response = ai_config.call_ai_api("What do you see in this image?", image_data=image_data)
                
                if response:
                    result_text.insert(tk.END, f"🤖 AI Response:\n{response}\n")
                else:
                    result_text.insert(tk.END, "❌ No response from AI\n")
            else:
                result_text.insert(tk.END, "❌ No image found in clipboard\n")
                result_text.insert(tk.END, "Copy an image to clipboard first, then try again\n")
                
        except Exception as e:
            result_text.insert(tk.END, f"❌ Error: {str(e)}\n")
    
    # Buttons
    btn_frame = tk.Frame(root)
    btn_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Button(btn_frame, text="📁 Test with Image File", command=test_with_file, 
              bg="#4CAF50", fg="white", font=('Arial', 10, 'bold')).pack(side="left", padx=5)
    
    tk.Button(btn_frame, text="📋 Test Clipboard Image", command=test_clipboard,
              bg="#2196F3", fg="white", font=('Arial', 10, 'bold')).pack(side="left", padx=5)
    
    # Initial message
    result_text.insert(1.0, f"""🧪 Image Test Ready!

Configuration:
• Provider: {ai_config.config['api_provider']}
• Model: {ai_config.config['model']}
• Supports Images: {'✅ Yes' if supports_images else '❌ No'}

Instructions:
1. Click "📁 Test with Image File" to test with an image file
2. Or copy an image to clipboard and click "📋 Test Clipboard Image"
3. The AI should describe what it sees in the image

""")
    
    root.mainloop()


if __name__ == "__main__":
    test_image_with_ai()