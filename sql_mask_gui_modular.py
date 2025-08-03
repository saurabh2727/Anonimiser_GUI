#!/usr/bin/env python3
"""
Enhanced SQL Masker Tool - Modular Version
A GUI application for masking sensitive information in SQL queries with AI assistance
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import threading
import os
import sys

# Import our custom modules
try:
    from ai_config import AIConfig
    from ai_interface import AIInterface
    from sql_masker import SQLMasker, NameGenerator, SQLAnalyzer
    from syntax_highlighter import HighlightedText, SQLSyntaxHighlighter
except ImportError as e:
    messagebox.showerror("Import Error", f"Failed to import modules: {e}")
    sys.exit(1)

# Try to import optional dependencies
try:
    import pyperclip
except ImportError:
    pyperclip = None

try:
    import difflib
except ImportError:
    difflib = None


class EnhancedSQLMaskerGUI:
    """Main GUI application for SQL masking with AI assistance"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("SQL Masker Tool")
        self.root.geometry("1400x900")
        
        # Initialize core components
        self.ai_config = AIConfig()
        self.sql_masker = SQLMasker(ai_config=self.ai_config)
        self.ai_interface = AIInterface(self.ai_config, self._get_current_sql)
        
        # Application state
        self.ai_enabled = False
        self.ai_masking_enabled = False
        self.current_mappings = {}
        
        # GUI components will be created in setup
        self.input_text = None
        self.masked_text = None
        self.mapping_text = None
        
        # Setup GUI
        self._setup_layout()
        
        # Initialize syntax highlighting after GUI is ready
        self.root.after(100, self._setup_highlighting)
    
    def _setup_layout(self):
        """Setup the main GUI layout"""
        # Main container
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Control panel
        self._create_control_panel(main_frame)
        
        # Main content area with notebook tabs
        self._create_main_content(main_frame)
        
        # Status bar
        self._create_status_bar()
    
    def _create_control_panel(self, parent):
        """Create the control panel with buttons"""
        control_frame = tk.Frame(parent, bg="#F0F8FF", relief="raised", bd=1)
        control_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        title_label = tk.Label(control_frame, text="Enhanced SQL Masker Tool", 
                              font=('Arial', 16, 'bold'), bg="#F0F8FF", fg="#2E4BC6")
        title_label.pack(pady=10)
        
        # Button frame
        button_frame = tk.Frame(control_frame, bg="#F0F8FF")
        button_frame.pack(pady=(0, 10))
        
        # Row 1: File operations
        file_frame = tk.Frame(button_frame, bg="#F0F8FF")
        file_frame.pack(pady=2)
        
        tk.Button(file_frame, text="Load File", command=self.load_file, 
                 bg="#4CAF50", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(file_frame, text="Save Mapping", command=self.save_mapping, 
                 bg="#2196F3", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(file_frame, text="Load Mapping", command=self.load_mapping, 
                 bg="#FF9800", fg="black").pack(side=tk.LEFT, padx=2)
        
        # Row 2: Masking operations
        mask_frame = tk.Frame(button_frame, bg="#F0F8FF")
        mask_frame.pack(pady=2)
        
        tk.Button(mask_frame, text="Analyze SQL", command=self.analyze_sql, 
                 bg="#9C27B0", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(mask_frame, text="Edit Mappings", command=self.show_mapping_editor, 
                 bg="#607D8B", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(mask_frame, text="Mask SQL", command=self.mask_sql, 
                 bg="#F44336", fg="black").pack(side=tk.LEFT, padx=2)
        tk.Button(mask_frame, text="Unmask SQL", command=self.unmask_sql, 
                 bg="#795548", fg="black").pack(side=tk.LEFT, padx=2)
        
        # Row 3: AI and utilities
        ai_frame = tk.Frame(button_frame, bg="#F0F8FF")
        ai_frame.pack(pady=2)
        
        self.ai_toggle_btn = tk.Button(ai_frame, text="Enable AI Features", 
                                      command=self.toggle_ai_features, bg="#E91E63", fg="black")
        self.ai_toggle_btn.pack(side=tk.LEFT, padx=2)
        
        self.ai_masking_btn = tk.Button(ai_frame, text="AI Masking: OFF", 
                                       command=self.toggle_ai_masking, state='disabled',
                                       bg="#9E9E9E", fg="black")
        self.ai_masking_btn.pack(side=tk.LEFT, padx=2)
        
        self.ai_config_btn = tk.Button(ai_frame, text="AI Config", 
                                      command=self.show_ai_config, state='disabled', 
                                      bg="#FFC107", fg="black")
        self.ai_config_btn.pack(side=tk.LEFT, padx=2)
        
        self.ai_understand_btn = tk.Button(ai_frame, text="Understand Code", 
                                          command=self.ai_understand_code, state='disabled', 
                                          bg="#4CAF50", fg="black")
        self.ai_understand_btn.pack(side=tk.LEFT, padx=2)
        
        self.ai_modify_btn = tk.Button(ai_frame, text="AI Modify", 
                                      command=self.ai_modify_code, state='disabled', 
                                      bg="#FF5722", fg="black")
        self.ai_modify_btn.pack(side=tk.LEFT, padx=2)
        
        tk.Button(ai_frame, text="Show Diff", command=self.show_diff, 
                 bg="#3F51B5", fg="black").pack(side=tk.LEFT, padx=2)
    
    def _create_main_content(self, parent):
        """Create the main content area with tabs"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill="both", expand=True)
        
        # SQL Editor tab
        self._create_sql_editor_tab()
        
        # Mappings tab
        self._create_mappings_tab()
        
        # Help tab
        self._create_help_tab()
    
    def _create_sql_editor_tab(self):
        """Create the SQL editor tab"""
        sql_frame = tk.Frame(self.notebook)
        self.notebook.add(sql_frame, text="📝 SQL Editor")
        
        # Create paned window for resizable sections
        paned = tk.PanedWindow(sql_frame, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        paned.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left side: Input and Masked SQL
        left_frame = tk.Frame(paned)
        paned.add(left_frame, minsize=400)
        
        # Input SQL section
        input_frame = tk.LabelFrame(left_frame, text="Original SQL", font=('Arial', 10, 'bold'))
        input_frame.pack(fill="both", expand=True, pady=(0, 5))
        
        # Add zoom controls for input text
        input_controls = tk.Frame(input_frame)
        input_controls.pack(fill="x", padx=5, pady=2)
        
        self.input_font_size = 10
        
        def zoom_input_in():
            if self.input_font_size < 20:
                self.input_font_size += 1
                self.input_text.config(font=('Consolas', self.input_font_size))
        
        def zoom_input_out():
            if self.input_font_size > 8:
                self.input_font_size -= 1
                self.input_text.config(font=('Consolas', self.input_font_size))
        
        tk.Button(input_controls, text="🔍+", command=zoom_input_in, bg="#2196F3", fg="black", 
                 font=('Arial', 8)).pack(side=tk.RIGHT, padx=1)
        tk.Button(input_controls, text="🔍-", command=zoom_input_out, bg="#2196F3", fg="black",
                 font=('Arial', 8)).pack(side=tk.RIGHT, padx=1)
        tk.Label(input_controls, text="Zoom:", font=('Arial', 8)).pack(side=tk.RIGHT, padx=2)
        
        # Text area with scrollbar
        text_container = tk.Frame(input_frame)
        text_container.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.input_text = HighlightedText(text_container, wrap=tk.WORD, font=('Consolas', 10))
        input_scrollbar = tk.Scrollbar(text_container, orient=tk.VERTICAL, command=self.input_text.yview)
        self.input_text.configure(yscrollcommand=input_scrollbar.set)
        self.input_text.pack(side=tk.LEFT, fill="both", expand=True)
        input_scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Masked SQL section
        masked_frame = tk.LabelFrame(left_frame, text="Masked SQL", font=('Arial', 10, 'bold'))
        masked_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        # Add zoom controls for masked text
        masked_controls = tk.Frame(masked_frame)
        masked_controls.pack(fill="x", padx=5, pady=2)
        
        self.masked_font_size = 10
        
        def zoom_masked_in():
            if self.masked_font_size < 20:
                self.masked_font_size += 1
                self.masked_text.config(font=('Consolas', self.masked_font_size))
        
        def zoom_masked_out():
            if self.masked_font_size > 8:
                self.masked_font_size -= 1
                self.masked_text.config(font=('Consolas', self.masked_font_size))
        
        tk.Button(masked_controls, text="🔍+", command=zoom_masked_in, bg="#2196F3", fg="black", 
                 font=('Arial', 8)).pack(side=tk.RIGHT, padx=1)
        tk.Button(masked_controls, text="🔍-", command=zoom_masked_out, bg="#2196F3", fg="black",
                 font=('Arial', 8)).pack(side=tk.RIGHT, padx=1)
        tk.Label(masked_controls, text="Zoom:", font=('Arial', 8)).pack(side=tk.RIGHT, padx=2)
        
        # Text area with scrollbar
        masked_container = tk.Frame(masked_frame)
        masked_container.pack(fill="both", expand=True, padx=5, pady=2)
        
        self.masked_text = HighlightedText(masked_container, wrap=tk.WORD, font=('Consolas', 10))
        masked_scrollbar = tk.Scrollbar(masked_container, orient=tk.VERTICAL, command=self.masked_text.yview)
        self.masked_text.configure(yscrollcommand=masked_scrollbar.set, state='disabled')
        self.masked_text.pack(side=tk.LEFT, fill="both", expand=True)
        masked_scrollbar.pack(side=tk.RIGHT, fill="y")
        
        # Right side: Mappings
        right_frame = tk.Frame(paned)
        paned.add(right_frame, minsize=300)
        
        mapping_frame = tk.LabelFrame(right_frame, text="🗺️ Mappings", font=('Arial', 10, 'bold'))
        mapping_frame.pack(fill="both", expand=True)
        
        self.mapping_text = scrolledtext.ScrolledText(mapping_frame, wrap=tk.WORD, 
                                                     font=('Consolas', 9), state='disabled')
        self.mapping_text.pack(fill="both", expand=True)
    
    def _create_mappings_tab(self):
        """Create the mappings management tab"""
        mappings_frame = tk.Frame(self.notebook)
        self.notebook.add(mappings_frame, text="Mappings Manager")
        
        # TODO: Implement detailed mappings management interface
        tk.Label(mappings_frame, text="Detailed mappings management interface", 
                font=('Arial', 12), fg="gray").pack(expand=True)
    
    def _create_help_tab(self):
        """Create the help tab"""
        help_frame = tk.Frame(self.notebook)
        self.notebook.add(help_frame, text="Help")
        
        help_text = """
Enhanced SQL Masker Tool - Help

OVERVIEW:
This tool helps you anonymize SQL queries by replacing sensitive table names, 
column names, and string values with placeholder names.

BASIC WORKFLOW:
1. Enter or load your SQL code in the "Original SQL" section
2. Click "Analyze SQL" to identify entities that can be masked
3. Use "Edit Mappings" to customize the anonymization mappings
4. Click "Mask SQL" to generate the anonymized version
5. Save your mappings for reuse with similar queries

AI FEATURES:
• Enable AI Features: Activate AI-powered analysis and modification
• AI Masking: Toggle between random and semantic AI-generated mappings
• AI Config: Configure your AI provider (OpenAI, Anthropic, Local LLM)
• Understand Code: Get AI explanations of your SQL code
• AI Modify: Use natural language to modify SQL queries

AI MASKING MODES:
• Traditional: Random string generation (e.g., 'customer' → 'TxR8kPq3')
• AI-Enhanced: Semantic preservation (e.g., 'customer_table' → 'client_data')

KEYBOARD SHORTCUTS:
• Ctrl+O: Load file
• Ctrl+S: Save mappings
• F5: Analyze SQL
• F6: Mask SQL
• F7: Unmask SQL
• Ctrl+Plus: Zoom in text
• Ctrl+Minus: Zoom out text
• Ctrl+0: Reset zoom

SUPPORTED AI PROVIDERS:
• OpenAI (GPT models)
• Anthropic (Claude models)  
• Local LLM (Ollama/compatible)
• Custom API endpoints

TIPS:
• Use masked SQL for sharing with external parties
• Save mappings to maintain consistency across related queries
• The AI conversation feature allows follow-up questions about your SQL
• Local LLM option provides privacy for sensitive queries
        """
        
        help_display = scrolledtext.ScrolledText(help_frame, wrap=tk.WORD, font=('Arial', 10))
        help_display.pack(fill="both", expand=True, padx=10, pady=10)
        help_display.insert("1.0", help_text)
        help_display.configure(state='disabled')
    
    def _create_status_bar(self):
        """Create status bar"""
        self.status_bar = tk.Frame(self.root, relief=tk.SUNKEN, bd=1)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = tk.Label(self.status_bar, text="Ready", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # AI status indicator
        self.ai_status_label = tk.Label(self.status_bar, text="AI: Disabled", anchor=tk.E, fg="red")
        self.ai_status_label.pack(side=tk.RIGHT, padx=5)
    
    def _setup_highlighting(self):
        """Setup syntax highlighting for text widgets"""
        try:
            # Initial highlighting
            self.input_text.highlight_now()
            self.masked_text.highlight_now()
        except Exception as e:
            print(f"Error setting up highlighting: {e}")
    
    def _get_current_sql(self):
        """Get current SQL from input text widget"""
        return self.input_text.get("1.0", tk.END).strip()
    
    def _extract_sql_summary(self, sql):
        """Extract key information from large SQL queries for AI analysis"""
        import re
        
        lines = sql.split('\n')
        line_count = len(lines)
        
        # Determine query type
        sql_upper = sql.upper()
        if 'WITH ' in sql_upper and 'SELECT ' in sql_upper:
            query_type = "Complex CTE Query"
        elif sql_upper.count('SELECT') > 1:
            query_type = "Query with Subqueries"
        elif 'UNION' in sql_upper:
            query_type = "Union Query"
        elif sql_upper.startswith('SELECT'):
            query_type = "Select Query"
        elif sql_upper.startswith('INSERT'):
            query_type = "Insert Query"
        elif sql_upper.startswith('UPDATE'):
            query_type = "Update Query"
        else:
            query_type = "Complex Query"
        
        # Extract table names (basic extraction)
        table_pattern = r'(?:FROM|JOIN|UPDATE|INSERT\s+INTO)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        tables = list(set(re.findall(table_pattern, sql, re.IGNORECASE)))
        
        # Count CTEs
        cte_count = sql_upper.count('WITH ') + sql_upper.count('),\n')
        
        return {
            'type': query_type,
            'tables': tables,
            'cte_count': cte_count,
            'lines': line_count
        }
    
    def _update_status(self, message):
        """Update status bar message"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    # Core functionality methods
    def load_file(self):
        """Load SQL file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Select SQL File",
                filetypes=[("SQL files", "*.sql"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert("1.0", content)
                self.input_text.highlight_now()
                
                self._update_status(f"Loaded: {os.path.basename(file_path)}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def analyze_sql(self):
        """Analyze SQL and generate mappings"""
        try:
            sql = self._get_current_sql()
            if not sql:
                messagebox.showwarning("No SQL", "Please enter SQL code first.")
                return
            
            self._update_status("Analyzing SQL...")
            
            # Analyze SQL and generate mappings
            entities = self.sql_masker.analyze_sql(sql)
            self.sql_masker.generate_mappings(entities)
            
            # Update mappings display
            self._update_mappings_display()
            
            self._update_status("SQL analysis complete")
            
            # Show analysis results
            total_entities = sum(len(v) for v in entities.values())
            messagebox.showinfo("Analysis Complete", 
                              f"Found {total_entities} entities:\n"
                              f"• Tables: {len(entities['tables'])}\n"
                              f"• Columns: {len(entities['columns'])}\n"
                              f"• Strings: {len(entities['strings'])}\n"
                              f"• Functions: {len(entities['functions'])}\n"
                              f"• Aliases: {len(entities['aliases'])}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze SQL: {str(e)}")
            self._update_status("Analysis failed")
    
    def mask_sql(self):
        """Apply masking to SQL"""
        try:
            sql = self._get_current_sql()
            if not sql:
                messagebox.showwarning("No SQL", "Please enter SQL code first.")
                return
            
            self._update_status("Analyzing and masking SQL...")
            
            # Check if we have existing mappings, if not, analyze first
            current_mappings = self.sql_masker.get_all_mappings()
            if not any(current_mappings.values()):
                # No mappings exist, analyze SQL first
                entities = self.sql_masker.analyze_sql(sql)
                self.sql_masker.generate_mappings(entities)
                self._update_mappings_display()
            
            # Apply masking
            masked_sql = self.sql_masker.mask_sql(sql)
            
            # Update masked text display
            self.masked_text.configure(state='normal')
            self.masked_text.delete("1.0", tk.END)
            self.masked_text.insert("1.0", masked_sql)
            self.masked_text.highlight_now(highlight_masked=True, 
                                          mapping_dict=self.sql_masker.get_all_mappings())
            self.masked_text.configure(state='disabled')
            
            self._update_status("SQL masked successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to mask SQL: {str(e)}")
            self._update_status("Masking failed")
    
    def unmask_sql(self):
        """Remove masking from SQL"""
        try:
            masked_sql = self.masked_text.get("1.0", tk.END).strip()
            if not masked_sql:
                messagebox.showwarning("No Masked SQL", "No masked SQL to unmask.")
                return
            
            self._update_status("Unmasking SQL...")
            
            # Apply unmasking
            unmasked_sql = self.sql_masker.unmask_sql(masked_sql)
            
            # Show result in a popup
            self._show_popup_result("Unmasked SQL", unmasked_sql)
            
            self._update_status("SQL unmasked successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to unmask SQL: {str(e)}")
            self._update_status("Unmasking failed")
    
    def show_mapping_editor(self):
        """Show mapping editor window"""
        # TODO: Implement mapping editor
        messagebox.showinfo("Mapping Editor", "Mapping editor interface to be implemented")
    
    def save_mapping(self):
        """Save current mappings to file"""
        try:
            mappings = self.sql_masker.get_all_mappings()
            if not any(mappings.values()):
                messagebox.showwarning("No Mappings", "No mappings to save. Analyze SQL first.")
                return
            
            file_path = filedialog.asksaveasfilename(
                title="Save Mappings",
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(mappings, file, indent=2)
                
                self._update_status(f"Mappings saved: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Mappings saved successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save mappings: {str(e)}")
    
    def load_mapping(self):
        """Load mappings from file"""
        try:
            file_path = filedialog.askopenfilename(
                title="Load Mappings",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as file:
                    mappings = json.load(file)
                
                self.sql_masker.set_mappings(mappings)
                self._update_mappings_display()
                
                self._update_status(f"Mappings loaded: {os.path.basename(file_path)}")
                messagebox.showinfo("Success", "Mappings loaded successfully!")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load mappings: {str(e)}")
    
    def show_diff(self):
        """Show difference between original and masked SQL"""
        try:
            original = self._get_current_sql()
            masked = self.masked_text.get("1.0", tk.END).strip()
            
            if not original or not masked:
                messagebox.showwarning("Insufficient Data", "Need both original and masked SQL to show diff.")
                return
            
            if difflib:
                diff = difflib.unified_diff(
                    original.splitlines(keepends=True),
                    masked.splitlines(keepends=True),
                    fromfile='Original SQL',
                    tofile='Masked SQL',
                    lineterm=''
                )
                diff_text = ''.join(diff)
            else:
                diff_text = f"Original SQL:\n{original}\n\n{'='*50}\n\nMasked SQL:\n{masked}"
            
            self._show_popup_result("SQL Diff", diff_text)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate diff: {str(e)}")
    
    # AI-related methods
    def toggle_ai_features(self):
        """Toggle AI features on/off"""
        self.ai_enabled = not self.ai_enabled
        
        if self.ai_enabled:
            self.ai_toggle_btn.config(text="Disable AI Features", bg="#4CAF50", fg="black")
            self.ai_config_btn.config(state='normal')
            self.ai_masking_btn.config(state='normal')
            self.ai_status_label.config(text="AI: Enabled", fg="green")
            
            if not self.ai_config.is_configured():
                messagebox.showinfo("AI Configuration Required", 
                                  "Please configure AI settings to use AI features.")
                self.show_ai_config()
                # After config dialog, check again
                if self.ai_config.is_configured():
                    self.ai_understand_btn.config(state='normal')
                    self.ai_modify_btn.config(state='normal')
                    messagebox.showinfo("AI Features", "AI features enabled!")
            else:
                self.ai_understand_btn.config(state='normal')
                self.ai_modify_btn.config(state='normal')
                messagebox.showinfo("AI Features", "AI features enabled!")
        else:
            self.ai_toggle_btn.config(text="Enable AI Features", bg="#E91E63", fg="black")
            self.ai_config_btn.config(state='disabled')
            self.ai_masking_btn.config(state='disabled')
            self.ai_understand_btn.config(state='disabled')
            self.ai_modify_btn.config(state='disabled')
            self.ai_status_label.config(text="AI: Disabled", fg="red")
            
            # Also disable AI masking when AI features are disabled
            if self.ai_masking_enabled:
                self.toggle_ai_masking()
            
            messagebox.showinfo("AI Features", "AI features disabled.")
    
    def toggle_ai_masking(self):
        """Toggle AI-enhanced masking on/off"""
        if not self.ai_enabled or not self.ai_config.is_configured():
            messagebox.showwarning("AI Not Available", 
                                 "Please enable and configure AI features first.")
            return
        
        self.ai_masking_enabled = not self.ai_masking_enabled
        
        if self.ai_masking_enabled:
            # Enable AI-enhanced masking
            self.sql_masker.naming_mode = 'ai_enhanced'
            self.ai_masking_btn.config(text="AI Masking: ON", bg="#4CAF50", fg="black")
            messagebox.showinfo("AI Masking", 
                              "AI-enhanced masking enabled! The next masking operation will use "
                              "semantic mappings instead of random names.")
        else:
            # Disable AI-enhanced masking (back to traditional)
            self.sql_masker.naming_mode = 'business_like'
            self.ai_masking_btn.config(text="AI Masking: OFF", bg="#9E9E9E", fg="black")
            messagebox.showinfo("AI Masking", 
                              "AI-enhanced masking disabled. Using traditional random masking.")
    
    def show_ai_config(self):
        """Show AI configuration dialog"""
        if self.ai_enabled:
            config_window = self.ai_config.show_config_dialog(self.root)
            
            # Wait for config window to close, then update button states
            def check_config():
                if self.ai_config.is_configured():
                    self.ai_understand_btn.config(state='normal')
                    self.ai_modify_btn.config(state='normal')
                else:
                    self.ai_understand_btn.config(state='disabled')
                    self.ai_modify_btn.config(state='disabled')
            
            # Set up callback for when window closes (both via X button and Save button)
            def on_window_close():
                config_window.destroy()
                check_config()
            
            config_window.protocol("WM_DELETE_WINDOW", on_window_close)
            
            # Wait for the window to be destroyed, then check config
            config_window.wait_window()
            check_config()
    
    def ai_understand_code(self):
        """Use AI to understand and explain SQL code"""
        if not self.ai_config.is_configured():
            messagebox.showwarning("AI Not Configured", "Please configure AI settings first.")
            self.show_ai_config()
            return
        
        sql = self._get_current_sql()
        if not sql:
            messagebox.showwarning("No SQL", "Please enter SQL code first.")
            return
        
        # Choose data type
        data_choice = self.ai_interface.choose_data_for_ai("Understanding Code - Choose Data", self.root)
        if not data_choice:
            return
        
        # Get appropriate SQL version
        if data_choice == 'masked':
            masked_sql = self.masked_text.get("1.0", tk.END).strip()
            if not masked_sql:
                response = messagebox.askyesno("No Masked Data", 
                                            "No masked SQL available. Would you like to mask the SQL first?")
                if response:
                    self.analyze_sql()
                    self.mask_sql()
                    return
                else:
                    return
            analysis_sql = masked_sql
        else:
            analysis_sql = sql
        
        # Create progress window
        progress_window = self.ai_interface.create_progress_window("Understanding SQL Code...", self.root)
        
        def analyze_code():
            try:
                # Handle very large SQL queries with smart analysis
                if len(analysis_sql) > 2000:
                    # Extract key information for large queries
                    sql_summary = self._extract_sql_summary(analysis_sql)
                    prompt = f"""Analyze this complex SQL query based on its structure:

Query Type: {sql_summary['type']}
Main Tables: {', '.join(sql_summary['tables'][:5])}
CTEs/Subqueries: {sql_summary['cte_count']} found
Total Lines: {sql_summary['lines']}

First 800 characters:
{analysis_sql[:800]}...

Provide optimization suggestions for this type of query."""
                else:
                    # Use normal analysis for smaller queries
                    prompt = f"""Analyze this SQL query and provide:
1. Main purpose
2. Tables and joins used
3. Key filters and logic
4. Potential improvements

SQL:
{analysis_sql}"""
                
                response = self.ai_config.call_ai_api(prompt)
                
                if response:
                    progress_window.after(0, lambda: show_result(response))
                else:
                    progress_window.after(0, lambda: show_error("AI Error", 
                                        "Failed to get AI response. Please check your configuration."))
                    
            except Exception as e:
                progress_window.after(0, lambda: show_error("Error", f"AI analysis failed: {str(e)}"))
        
        def show_result(response):
            progress_window.destroy()
            self.ai_interface.show_understand_result("SQL Code Understanding", response, analysis_sql)
        
        def show_error(title, message):
            progress_window.destroy()
            messagebox.showerror(title, message)
        
        threading.Thread(target=analyze_code, daemon=True).start()
    
    def ai_modify_code(self):
        """Use AI to modify SQL code based on instructions"""
        if not self.ai_config.is_configured():
            messagebox.showwarning("AI Not Configured", "Please configure AI settings first.")
            self.show_ai_config()
            return
        
        sql = self._get_current_sql()
        if not sql:
            messagebox.showwarning("No SQL", "Please enter SQL code first.")
            return
        
        # Get modification instructions
        instructions = self.ai_interface.get_instruction_from_user(self.root)
        if not instructions:
            return
        
        # Choose data type
        data_choice = self.ai_interface.choose_data_for_ai("Modifying Code - Choose Data", self.root)
        if not data_choice:
            return
        
        # Get appropriate SQL version
        if data_choice == 'masked':
            masked_sql = self.masked_text.get("1.0", tk.END).strip()
            if not masked_sql:
                response = messagebox.askyesno("No Masked Data", 
                                            "No masked SQL available. Would you like to mask the SQL first?")
                if response:
                    self.analyze_sql()
                    self.mask_sql()
                    return
                else:
                    return
            modify_sql = masked_sql
        else:
            modify_sql = sql
        
        # Create progress window
        progress_window = self.ai_interface.create_progress_window("Modifying SQL Code...", self.root)
        
        def modify_code():
            try:
                # Handle large SQL modifications more intelligently
                if len(modify_sql) > 2000:
                    # For very large queries, provide general guidance
                    sql_summary = self._extract_sql_summary(modify_sql)
                    prompt = f"""For this {sql_summary['type']} with {sql_summary['lines']} lines:

Instructions: {instructions}

Query involves tables: {', '.join(sql_summary['tables'][:3])}
First 600 characters:
{modify_sql[:600]}...

Provide general guidance on how to {instructions.lower()} for this type of query."""
                else:
                    # Normal modification for smaller queries
                    prompt = f"""Modify this SQL according to: {instructions}

SQL:
{modify_sql}

Provide the modified SQL with brief explanation."""
                
                response = self.ai_config.call_ai_api(prompt)
                
                if response:
                    progress_window.after(0, lambda: show_result(response))
                else:
                    progress_window.after(0, lambda: show_error("AI Error", 
                                        "Failed to get AI response. Please check your configuration."))
                    
            except Exception as e:
                progress_window.after(0, lambda: show_error("Error", f"AI modification failed: {str(e)}"))
        
        def show_result(response):
            progress_window.destroy()
            self.ai_interface.show_modification_result(response, data_choice)
        
        def show_error(title, message):
            progress_window.destroy()
            messagebox.showerror(title, message)
        
        threading.Thread(target=modify_code, daemon=True).start()
    
    # Zoom methods
    def _zoom_in(self):
        """Zoom in on text areas"""
        if self.input_font_size < 20:
            self.input_font_size += 1
            self.input_text.config(font=('Consolas', self.input_font_size))
        
        if self.masked_font_size < 20:
            self.masked_font_size += 1
            self.masked_text.config(font=('Consolas', self.masked_font_size))
    
    def _zoom_out(self):
        """Zoom out on text areas"""
        if self.input_font_size > 8:
            self.input_font_size -= 1
            self.input_text.config(font=('Consolas', self.input_font_size))
        
        if self.masked_font_size > 8:
            self.masked_font_size -= 1
            self.masked_text.config(font=('Consolas', self.masked_font_size))
    
    def _reset_zoom(self):
        """Reset zoom to default size"""
        self.input_font_size = 10
        self.masked_font_size = 10
        self.input_text.config(font=('Consolas', 10))
        self.masked_text.config(font=('Consolas', 10))
    
    # Helper methods
    def _update_mappings_display(self):
        """Update the mappings display"""
        try:
            mappings = self.sql_masker.get_all_mappings()
            
            display_text = ""
            for category, mapping in mappings.items():
                if mapping:
                    display_text += f"\n=== {category.upper()} ===\n"
                    for original, masked in mapping.items():
                        display_text += f"{original} → {masked}\n"
            
            if not display_text:
                display_text = "No mappings generated yet.\nClick 'Analyze SQL' to generate mappings."
            
            self.mapping_text.configure(state='normal')
            self.mapping_text.delete("1.0", tk.END)
            self.mapping_text.insert("1.0", display_text)
            self.mapping_text.configure(state='disabled')
            
        except Exception as e:
            print(f"Error updating mappings display: {e}")
    
    def _show_popup_result(self, title, content):
        """Show result in a popup window"""
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("800x600")
        
        text_widget = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=('Consolas', 10))
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", content)
        text_widget.configure(state='disabled')
        
        # Copy button
        def copy_content():
            if pyperclip:
                pyperclip.copy(content)
                messagebox.showinfo("Copied", "Content copied to clipboard!")
            else:
                messagebox.showinfo("Copy", "pyperclip not available. Content printed to console.")
                print(content)
        
        button_frame = tk.Frame(popup)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(button_frame, text="📋 Copy", command=copy_content, 
                 bg="#607D8B", fg="black").pack(side=tk.LEFT)
        tk.Button(button_frame, text="❌ Close", command=popup.destroy, 
                 bg="#F44336", fg="black").pack(side=tk.RIGHT)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = EnhancedSQLMaskerGUI(root)
    
    # Setup keyboard shortcuts
    root.bind('<Control-o>', lambda e: app.load_file())
    root.bind('<Control-s>', lambda e: app.save_mapping())
    root.bind('<F5>', lambda e: app.analyze_sql())
    root.bind('<F6>', lambda e: app.mask_sql())
    root.bind('<F7>', lambda e: app.unmask_sql())
    
    # Zoom shortcuts
    root.bind('<Control-plus>', lambda e: app._zoom_in())
    root.bind('<Control-equal>', lambda e: app._zoom_in())  # Handle + without shift
    root.bind('<Control-minus>', lambda e: app._zoom_out())
    root.bind('<Control-0>', lambda e: app._reset_zoom())
    
    root.mainloop()


if __name__ == "__main__":
    main()