#!/usr/bin/env python3
"""
Test Dual LLM Functionality
Tests the smart routing between text and vision models
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from ai_config import AIConfig
from ai_interface import AIInterface
import threading


class DualLLMTester:
    """Test application for dual LLM functionality"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 Dual LLM Tester")
        self.root.geometry("800x700")
        
        self.ai_config = AIConfig()
        self.ai_interface = AIInterface(self.ai_config, self.get_sample_sql)
        
        self.setup_ui()
        self.check_dual_llm_status()
    
    def setup_ui(self):
        """Setup the test UI"""
        # Header
        header = tk.Frame(self.root, bg="#E3F2FD", height=80)
        header.pack(fill="x", padx=10, pady=10)
        header.pack_propagate(False)
        
        tk.Label(header, text="🚀 Dual LLM Tester", 
                font=('Arial', 18, 'bold'), bg="#E3F2FD").pack(pady=20)
        
        # Status frame
        self.status_frame = tk.Frame(self.root, bg="#F5F5F5")
        self.status_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = tk.Label(self.status_frame, text="Checking configuration...", 
                                   font=('Arial', 12), bg="#F5F5F5")
        self.status_label.pack(pady=10)
        
        # Test controls
        controls_frame = tk.Frame(self.root)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Configuration button
        tk.Button(controls_frame, text="⚙️ Configure Dual LLM", 
                 command=self.open_config, bg="#2196F3", fg="white",
                 font=('Arial', 12, 'bold'), pady=10).pack(fill="x", pady=5)
        
        # Test buttons
        tk.Button(controls_frame, text="📝 Test Text Model (Code/SQL)", 
                 command=self.test_text_model, bg="#4CAF50", fg="white",
                 font=('Arial', 12, 'bold'), pady=10).pack(fill="x", pady=5)
        
        tk.Button(controls_frame, text="🖼️ Test Vision Model (Upload Image)", 
                 command=self.test_vision_model, bg="#FF9800", fg="white",
                 font=('Arial', 12, 'bold'), pady=10).pack(fill="x", pady=5)
        
        tk.Button(controls_frame, text="📋 Test Vision Model (Clipboard)", 
                 command=self.test_vision_clipboard, bg="#9C27B0", fg="white",
                 font=('Arial', 12, 'bold'), pady=10).pack(fill="x", pady=5)
        
        tk.Button(controls_frame, text="🎯 Open Modern Chat Interface", 
                 command=self.open_modern_chat, bg="#E91E63", fg="white",
                 font=('Arial', 12, 'bold'), pady=10).pack(fill="x", pady=5)
        
        # Results area
        results_frame = tk.Frame(self.root)
        results_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tk.Label(results_frame, text="Test Results:", font=('Arial', 12, 'bold')).pack(anchor="w")
        
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, font=('Arial', 10))
        scrollbar = tk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Instructions
        instructions = """📋 Instructions:

1. Click "Configure Dual LLM" to enable dual model support
2. Set Text Model to: deepseek-coder-v2:latest
3. Set Vision Model to: llava:latest  
4. Enable the "Dual LLM" checkbox
5. Test each model individually with the buttons above
6. Try the modern chat interface with both text and images

🎯 Expected Behavior:
• Text questions → deepseek-coder-v2:latest
• Image questions → llava:latest
• Automatic smart routing based on content"""
        
        self.log_result(instructions)
    
    def check_dual_llm_status(self):
        """Check and display dual LLM status"""
        config = self.ai_config.config
        
        dual_enabled = config.get('dual_llm_enabled', False)
        text_model = config.get('text_model', 'Not set')
        vision_model = config.get('vision_model', 'Not set')
        
        if dual_enabled:
            status = f"✅ Dual LLM ENABLED\n📝 Text: {text_model}\n🖼️ Vision: {vision_model}"
            self.status_label.config(text=status, fg="green")
        else:
            status = f"❌ Dual LLM DISABLED\n🔧 Single model: {config.get('model', 'Not set')}"
            self.status_label.config(text=status, fg="red")
    
    def log_result(self, message):
        """Log a result to the text area"""
        self.results_text.insert(tk.END, f"{message}\n\n")
        self.results_text.see(tk.END)
        self.root.update()
    
    def get_sample_sql(self):
        """Get sample SQL for testing"""
        return """SELECT u.id, u.name, u.email, COUNT(p.id) as post_count
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
WHERE u.active = 1
GROUP BY u.id, u.name, u.email
ORDER BY post_count DESC
LIMIT 10;"""
    
    def open_config(self):
        """Open AI configuration dialog"""
        self.ai_config.show_config_dialog(self.root)
        # Refresh status after config
        self.root.after(1000, self.check_dual_llm_status)
    
    def test_text_model(self):
        """Test the text model with a code question"""
        self.log_result("🧪 Testing Text Model...")
        self.log_result("Question: Explain this SQL query and suggest optimizations")
        
        def run_test():
            try:
                prompt = f"Explain this SQL query and suggest optimizations:\n\n{self.get_sample_sql()}"
                response = self.ai_config.call_ai_api(prompt)
                
                if response:
                    self.root.after(0, lambda: self.log_result(f"✅ Text Model Response:\n{response}"))
                else:
                    self.root.after(0, lambda: self.log_result("❌ No response from text model"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_result(f"❌ Text model error: {str(e)}"))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def test_vision_model(self):
        """Test the vision model with an uploaded image"""
        file_path = filedialog.askopenfilename(
            title="Select Image for Vision Test",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        self.log_result("🧪 Testing Vision Model...")
        self.log_result(f"Image: {file_path}")
        self.log_result("Question: What do you see in this image?")
        
        def run_test():
            try:
                # Process image
                image_data = self.ai_config.process_image_for_ai(file_path)
                
                # Call AI with image
                response = self.ai_config.call_ai_api("What do you see in this image? Describe it in detail.", image_data=image_data)
                
                if response:
                    self.root.after(0, lambda: self.log_result(f"✅ Vision Model Response:\n{response}"))
                else:
                    self.root.after(0, lambda: self.log_result("❌ No response from vision model"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_result(f"❌ Vision model error: {str(e)}"))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def test_vision_clipboard(self):
        """Test vision model with clipboard image"""
        self.log_result("🧪 Testing Vision Model (Clipboard)...")
        self.log_result("Checking clipboard for images...")
        
        def run_test():
            try:
                # Get image from clipboard
                image_data = self.ai_config.process_image_from_clipboard()
                
                if not image_data:
                    self.root.after(0, lambda: self.log_result("❌ No image found in clipboard"))
                    return
                
                self.root.after(0, lambda: self.log_result("✅ Image found in clipboard!"))
                self.root.after(0, lambda: self.log_result("Question: What do you see in this image?"))
                
                # Call AI with image
                response = self.ai_config.call_ai_api("What do you see in this image? Describe it in detail.", image_data=image_data)
                
                if response:
                    self.root.after(0, lambda: self.log_result(f"✅ Vision Model Response:\n{response}"))
                else:
                    self.root.after(0, lambda: self.log_result("❌ No response from vision model"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.log_result(f"❌ Vision model error: {str(e)}"))
        
        threading.Thread(target=run_test, daemon=True).start()
    
    def open_modern_chat(self):
        """Open the modern chat interface for interactive testing"""
        self.ai_interface.show_modern_conversation(
            "Dual LLM Chat Test",
            """🚀 Welcome to Dual LLM Testing!

This chat interface now uses SMART ROUTING:

📝 **Text Questions** → deepseek-coder-v2:latest
• Ask about SQL, code, or general text questions
• Example: "Explain this SQL query"

🖼️ **Image Questions** → llava:latest  
• Upload or paste images for analysis
• Example: Upload a screenshot and ask "What's in this image?"

🎯 **Test Both:**
1. Ask a code question (no image)
2. Upload an image and ask about it
3. Notice how different models respond!

Try it now!""",
            self.get_sample_sql()
        )
    
    def run(self):
        """Run the tester"""
        self.root.mainloop()


def main():
    """Main function"""
    try:
        tester = DualLLMTester()
        tester.run()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start dual LLM tester: {str(e)}")


if __name__ == "__main__":
    main()