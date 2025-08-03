#!/usr/bin/env python3
"""
AI Configuration Module
Handles AI provider configuration and API calls
"""

import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
import threading
try:
    import requests
except ImportError:
    requests = None


class AIConfig:
    """Manages AI configuration and API interactions"""
    
    def __init__(self):
        self.config = {
            'api_key': 'local',
            'api_provider': 'local_llm',  # openai, anthropic, local_llm, custom
            'base_url': 'http://localhost:11434/v1/chat/completions',
            'model': 'deepseek-coder-v2:latest'
        }
    
    def show_config_dialog(self, parent):
        """Show AI configuration dialog"""
        config_window = Toplevel(parent)
        config_window.title("AI Configuration")
        config_window.geometry("600x500")
        config_window.resizable(False, False)
        
        # Make it modal
        config_window.transient(parent)
        config_window.grab_set()
        
        # Header
        header_frame = tk.Frame(config_window, bg="#E3F2FD")
        header_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(header_frame, text="🤖 AI Configuration", font=('Arial', 16, 'bold'), bg="#E3F2FD").pack(pady=5)
        tk.Label(header_frame, text="Configure your AI provider settings", font=('Arial', 12), bg="#E3F2FD").pack()
        
        # Main form
        form_frame = tk.Frame(config_window)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # API Provider
        tk.Label(form_frame, text="API Provider:", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky="w", pady=5)
        provider_var = tk.StringVar(value=self.config['api_provider'])
        provider_combo = ttk.Combobox(form_frame, textvariable=provider_var, values=['openai', 'anthropic', 'local_llm', 'custom'], state='readonly', font=('Arial', 11))
        provider_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # API Key
        tk.Label(form_frame, text="API Key:", font=('Arial', 12, 'bold')).grid(row=1, column=0, sticky="w", pady=5)
        api_key_var = tk.StringVar(value=self.config['api_key'])
        api_key_entry = tk.Entry(form_frame, textvariable=api_key_var, show="*", width=40, font=('Arial', 11))
        api_key_entry.grid(row=1, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Show/Hide API Key
        def toggle_api_key_visibility():
            if api_key_entry['show'] == '*':
                api_key_entry.config(show='')
                show_key_btn.config(text="🙈 Hide")
            else:
                api_key_entry.config(show='*')
                show_key_btn.config(text="👁️ Show")
        
        show_key_btn = tk.Button(form_frame, text="👁️ Show", command=toggle_api_key_visibility)
        show_key_btn.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Model
        tk.Label(form_frame, text="Model:", font=('Arial', 12, 'bold')).grid(row=2, column=0, sticky="w", pady=5)
        model_var = tk.StringVar(value=self.config['model'])
        model_entry = tk.Entry(form_frame, textvariable=model_var, width=40, font=('Arial', 11))
        model_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Base URL (for custom providers)
        tk.Label(form_frame, text="Base URL (optional):", font=('Arial', 12, 'bold')).grid(row=3, column=0, sticky="w", pady=5)
        base_url_var = tk.StringVar(value=self.config['base_url'])
        base_url_entry = tk.Entry(form_frame, textvariable=base_url_var, width=40, font=('Arial', 11))
        base_url_entry.grid(row=3, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Help text
        help_frame = tk.Frame(config_window, bg="#FFF3E0")
        help_frame.pack(fill="x", padx=10, pady=5)
        
        help_text = """💡 Help:
• OpenAI: Use models like 'gpt-3.5-turbo', 'gpt-4'
• Anthropic: Use models like 'claude-3-sonnet-20240229'
• Local LLM: Use local models via Ollama (Base URL: http://localhost:11434/v1/chat/completions)
• Custom: Provide your own base URL and model name
• API keys are stored locally and never shared
• For Local LLM, API key can be any value or leave empty
• Available models: deepseek-coder-v2:latest, mistral:latest, llava:latest"""
        
        tk.Label(help_frame, text=help_text, bg="#FFF3E0", justify="left", font=('Arial', 11)).pack(padx=10, pady=10)
        
        # Configure grid weights
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Add model suggestions based on provider
        def update_model_suggestions(*_args):
            provider = provider_var.get()
            if provider == 'openai':
                model_var.set('gpt-3.5-turbo')
                base_url_entry.config(state='disabled')
                base_url_var.set('')
                api_key_entry.config(state='normal')
            elif provider == 'anthropic':
                model_var.set('claude-3-sonnet-20240229')
                base_url_entry.config(state='disabled')
                base_url_var.set('')
                api_key_entry.config(state='normal')
            elif provider == 'local_llm':
                model_var.set('deepseek-coder-v2:latest')  # Use available model
                base_url_entry.config(state='normal')
                base_url_var.set('http://localhost:11434/v1/chat/completions')
                api_key_entry.config(state='disabled')
                api_key_var.set('local')  # Dummy key for local LLM
            else:  # custom
                model_var.set('gpt-3.5-turbo')
                base_url_entry.config(state='normal')
                api_key_entry.config(state='normal')
        
        provider_var.trace_add('write', update_model_suggestions)
        update_model_suggestions()  # Initialize
        
        # Define save_config function
        def save_config():
            # Validate inputs
            api_key = api_key_var.get().strip()
            provider = provider_var.get()
            model = model_var.get().strip()
            base_url = base_url_var.get().strip()
            
            # Basic validation
            if not api_key and provider != 'local_llm':
                messagebox.showwarning("Validation Error", "API Key is required for cloud providers.")
                return
            
            if not model:
                messagebox.showwarning("Validation Error", "Model name is required.")
                return
            
            if (provider == 'custom' or provider == 'local_llm') and not base_url:
                messagebox.showwarning("Validation Error", "Base URL is required for custom and local LLM providers.")
                return
            
            # Save configuration
            self.config = {
                'api_key': api_key,
                'api_provider': provider,
                'base_url': base_url,
                'model': model
            }
            
            messagebox.showinfo("Configuration Saved", "AI configuration saved successfully!")
            config_window.destroy()
            return True
        
        # Test connection function
        def test_connection():
            test_config = {
                'api_key': api_key_var.get(),
                'api_provider': provider_var.get(),
                'base_url': base_url_var.get(),
                'model': model_var.get()
            }
            
            test_btn.config(state='disabled', text="🔄 Testing...")
            
            def run_test():
                try:
                    result = self._test_connection(test_config)
                    config_window.after(0, lambda: show_test_result(result))
                except Exception as e:
                    config_window.after(0, lambda: show_test_result(f"Test failed: {str(e)}"))
            
            def show_test_result(result):
                test_btn.config(state='normal', text="🧪 Test Connection")
                if "successfully" in result.lower():
                    messagebox.showinfo("Connection Test", result)
                else:
                    messagebox.showerror("Connection Test", result)
            
            threading.Thread(target=run_test, daemon=True).start()
        
        # Buttons
        button_frame = tk.Frame(config_window)
        button_frame.pack(fill="x", padx=20, pady=15)
        
        test_btn = tk.Button(button_frame, text="🧪 Test Connection", command=test_connection, bg="#2196F3", fg="black", font=('Arial', 11))
        test_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Button(button_frame, text="Save", command=save_config, bg="#4CAF50", fg="black", font=('Arial', 11)).pack(side=tk.RIGHT, padx=(10, 0))
        tk.Button(button_frame, text="Cancel", command=config_window.destroy, bg="#F44336", fg="black", font=('Arial', 11)).pack(side=tk.RIGHT)
        
        return config_window
    
    def _test_connection(self, config):
        """Test AI API connection"""
        if requests is None:
            return "Error: 'requests' module is required for AI features."
        
        try:
            test_prompt = "Hello, this is a connection test. Please respond with 'Connection successful'."
            response = self.call_ai_api(test_prompt, config)
            
            if response and "success" in response.lower():
                return "✅ Connection test successful!"
            elif response:
                return f"✅ Connection successful! Response: {response[:100]}..."
            else:
                return "❌ Connection failed: No response received"
                
        except Exception as e:
            return f"❌ Connection failed: {str(e)}"
    
    def call_ai_api(self, prompt, config=None):
        """Make API call to AI service"""
        if requests is None:
            raise Exception("The 'requests' module is required for AI features.")
        
        if config is None:
            config = self.config
        
        try:
            if config['api_provider'] == 'openai':
                url = config['base_url'] or 'https://api.openai.com/v1/chat/completions'
                headers = {
                    'Authorization': f'Bearer {config["api_key"]}',
                    'Content-Type': 'application/json'
                }
                data = {
                    'model': config['model'],
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 2000
                }
                
                response = requests.post(url, headers=headers, json=data, timeout=30)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
                
            elif config['api_provider'] == 'anthropic':
                url = config['base_url'] or 'https://api.anthropic.com/v1/messages'
                headers = {
                    'x-api-key': config['api_key'],
                    'Content-Type': 'application/json',
                    'anthropic-version': '2023-06-01'
                }
                data = {
                    'model': config['model'],
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 2000
                }
                
                response = requests.post(url, headers=headers, json=data, timeout=30)
                response.raise_for_status()
                return response.json()['content'][0]['text']
                
            elif config['api_provider'] == 'local_llm':
                # Ollama API call
                url = config['base_url'] or 'http://localhost:11434/v1/chat/completions'
                headers = {
                    'Content-Type': 'application/json'
                }
                
                # Limit prompt length for local LLM to prevent 500 errors
                max_prompt_length = 2000  # More aggressive limit for local models
                if len(prompt) > max_prompt_length:
                    prompt = prompt[:max_prompt_length] + "\n\n[Note: Query was truncated - showing first part only]"
                
                data = {
                    'model': config['model'],
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 1000,  # Reduced for better performance
                    'stream': False,
                    'temperature': 0.7
                }
                
                response = requests.post(url, headers=headers, json=data, timeout=120)
                response.raise_for_status()
                
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                else:
                    raise Exception("Invalid response format from local LLM")
                
            else:  # custom
                url = config['base_url']
                headers = {
                    'Authorization': f'Bearer {config["api_key"]}',
                    'Content-Type': 'application/json'
                }
                data = {
                    'model': config['model'],
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 2000
                }
                
                response = requests.post(url, headers=headers, json=data, timeout=30)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
                
        except requests.exceptions.Timeout:
            print("AI API call timed out. The request took too long to process.")
            return None
        except requests.exceptions.ConnectionError:
            print("AI API connection failed. Check if the service is running.")
            return None
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 500:
                print("AI API server error (500). The prompt might be too complex or the model is overloaded.")
                return None
            else:
                print(f"AI API HTTP error: {e}")
                return None
        except Exception as e:
            print(f"AI API call failed: {e}")
            return None
    
    def is_configured(self):
        """Check if AI is properly configured"""
        return bool(self.config['api_key'] or self.config['api_provider'] == 'local_llm')