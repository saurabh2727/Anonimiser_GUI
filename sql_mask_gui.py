import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel, ttk
import re
import json
import sqlparse
from sql_metadata import Parser
import pyperclip
import difflib
from sqlparse.keywords import KEYWORDS
from sqlparse.tokens import Keyword, Name, String, Whitespace, Comment, Punctuation
from sqlparse.sql import IdentifierList, Identifier, Function
import os
from datetime import datetime
import random
try:
    import requests
except ImportError:
    requests = None
import threading

class RealisticNameGenerator:
    """Generate realistic fake names for database objects"""
    
    def __init__(self):
        # Realistic table name components
        self.business_entities = [
            'users', 'customers', 'clients', 'accounts', 'profiles', 'members',
            'orders', 'transactions', 'payments', 'invoices', 'receipts', 'purchases',
            'products', 'items', 'inventory', 'catalog', 'categories', 'brands',
            'employees', 'staff', 'departments', 'roles', 'permissions', 'teams',
            'projects', 'tasks', 'activities', 'events', 'sessions', 'logs',
            'reports', 'analytics', 'metrics', 'statistics', 'summaries',
            'contacts', 'addresses', 'locations', 'regions', 'stores', 'branches',
            'reviews', 'ratings', 'feedback', 'comments', 'messages', 'notifications',
            'campaigns', 'promotions', 'discounts', 'offers', 'coupons',
            'documents', 'files', 'attachments', 'media', 'images', 'videos'
        ]
        
        # Realistic column name patterns
        self.column_patterns = {
            # ID patterns
            'id_patterns': ['id', 'uuid', 'key', 'ref', 'identifier'],
            # Name patterns  
            'name_patterns': ['name', 'title', 'label', 'description', 'caption'],
            # Date/time patterns
            'date_patterns': ['date', 'time', 'timestamp', 'created_at', 'updated_at', 'modified_date'],
            # Status patterns
            'status_patterns': ['status', 'state', 'flag', 'active', 'enabled', 'visible'],
            # Contact patterns
            'contact_patterns': ['email', 'phone', 'address', 'city', 'country', 'postal_code'],
            # Financial patterns
            'financial_patterns': ['amount', 'price', 'cost', 'total', 'subtotal', 'tax', 'discount'],
            # Measurement patterns
            'measure_patterns': ['count', 'quantity', 'weight', 'height', 'width', 'length', 'size']
        }
        
        # String content templates
        self.string_templates = [
            "'example_data'", "'sample_value'", "'test_content'", "'demo_text'",
            "'placeholder'", "'mock_data'", "'dummy_value'", "'generic_text'"
        ]
        
        # Function name patterns
        self.function_prefixes = ['get', 'calc', 'process', 'validate', 'format', 'parse', 'convert']
        self.function_suffixes = ['data', 'value', 'result', 'info', 'details', 'summary']
        
        # Used names tracking
        self.used_names = set()
    
    def generate_table_name(self, original_name=""):
        """Generate a realistic table name"""
        # Try to infer type from original name
        original_lower = original_name.lower()
        
        # Look for patterns in original name
        if any(word in original_lower for word in ['user', 'customer', 'client', 'account']):
            candidates = ['users', 'customers', 'accounts', 'profiles', 'members']
        elif any(word in original_lower for word in ['order', 'transaction', 'payment', 'purchase']):
            candidates = ['orders', 'transactions', 'payments', 'purchases', 'invoices']
        elif any(word in original_lower for word in ['product', 'item', 'inventory', 'catalog']):
            candidates = ['products', 'items', 'inventory', 'catalog', 'categories']
        elif any(word in original_lower for word in ['employee', 'staff', 'team', 'department']):
            candidates = ['employees', 'staff', 'departments', 'teams', 'roles']
        else:
            candidates = self.business_entities
        
        # Find unused name
        for name in candidates:
            if name not in self.used_names:
                self.used_names.add(name)
                return name
        
        # Fallback with suffix
        base_name = random.choice(candidates)
        counter = 1
        while f"{base_name}_{counter}" in self.used_names:
            counter += 1
        
        final_name = f"{base_name}_{counter}"
        self.used_names.add(final_name)
        return final_name
    
    def generate_column_name(self, original_name=""):
        """Generate a realistic column name"""
        original_lower = original_name.lower()
        
        # Match patterns from original name
        for pattern_type, patterns in self.column_patterns.items():
            for pattern in patterns:
                if pattern in original_lower:
                    # Find similar pattern
                    category_patterns = self.column_patterns[pattern_type]
                    for candidate in category_patterns:
                        if candidate not in self.used_names:
                            self.used_names.add(candidate)
                            return candidate
        
        # Check for common suffixes/prefixes
        if original_lower.endswith('_id') or original_lower.endswith('id'):
            candidates = ['record_id', 'item_id', 'ref_id', 'entity_id']
        elif original_lower.startswith('is_') or original_lower.startswith('has_'):
            candidates = ['is_active', 'is_enabled', 'has_data', 'is_valid']
        elif '_date' in original_lower or '_time' in original_lower:
            candidates = ['created_date', 'modified_date', 'process_time', 'event_date']
        else:
            # General column names
            candidates = ['data_value', 'content', 'description', 'details', 'info', 
                         'reference', 'category', 'type', 'status', 'priority']
        
        # Find unused name
        for name in candidates:
            if name not in self.used_names:
                self.used_names.add(name)
                return name
        
        # Fallback
        base_name = random.choice(candidates)
        counter = 1
        while f"{base_name}_{counter}" in self.used_names:
            counter += 1
        
        final_name = f"{base_name}_{counter}"
        self.used_names.add(final_name)
        return final_name
    
    def generate_schema_name(self, original_name=""):
        """Generate a realistic schema name"""
        schemas = ['public', 'main', 'core', 'app', 'data', 'reporting', 'staging', 'prod']
        
        for schema in schemas:
            if schema not in self.used_names:
                self.used_names.add(schema)
                return schema
        
        # Fallback
        counter = 1
        while f"schema_{counter}" in self.used_names:
            counter += 1
        
        final_name = f"schema_{counter}"
        self.used_names.add(final_name)
        return final_name
    
    def generate_function_name(self, original_name=""):
        """Generate a realistic function name"""
        prefix = random.choice(self.function_prefixes)
        suffix = random.choice(self.function_suffixes)
        
        candidates = [f"{prefix}_{suffix}", f"{prefix}{suffix.title()}", f"fn_{prefix}_{suffix}"]
        
        for name in candidates:
            if name not in self.used_names:
                self.used_names.add(name)
                return name
        
        # Fallback
        counter = 1
        base_name = f"{prefix}_{suffix}"
        while f"{base_name}_{counter}" in self.used_names:
            counter += 1
        
        final_name = f"{base_name}_{counter}"
        self.used_names.add(final_name)
        return final_name
    
    def generate_string_value(self, original_value=""):
        """Generate a realistic string value"""
        # Keep the same quote style
        if original_value.startswith("'"):
            return random.choice(self.string_templates)
        elif original_value.startswith('"'):
            return random.choice(self.string_templates).replace("'", '"')
        else:
            return random.choice(self.string_templates)

class SyntaxHighlighter:
    """Add syntax highlighting to text widgets"""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.setup_tags()
    
    def setup_tags(self):
        """Configure text tags for syntax highlighting"""
        # SQL Keywords - Blue
        self.text_widget.tag_configure("keyword", foreground="#0066CC", font=("Consolas", 10, "bold"))
        
        # Strings - Green
        self.text_widget.tag_configure("string", foreground="#009900", font=("Consolas", 10))
        
        # Comments - Gray
        self.text_widget.tag_configure("comment", foreground="#666666", font=("Consolas", 10, "italic"))
        
        # Numbers - Orange
        self.text_widget.tag_configure("number", foreground="#FF6600", font=("Consolas", 10))
        
        # Masked items - Red background
        self.text_widget.tag_configure("masked", background="#FFE6E6", foreground="#CC0000", font=("Consolas", 10, "bold"))
        
        # Original items - Green background  
        self.text_widget.tag_configure("original", background="#E6FFE6", foreground="#006600", font=("Consolas", 10, "bold"))
        
        # Operators - Purple
        self.text_widget.tag_configure("operator", foreground="#9900CC", font=("Consolas", 10, "bold"))
        
        # Functions - Dark Blue
        self.text_widget.tag_configure("function", foreground="#0066FF", font=("Consolas", 10, "bold"))
    
    def highlight_sql(self, content, highlight_masked=False, mapping_dict=None):
        """Apply syntax highlighting to SQL content"""
        # Store cursor position
        try:
            cursor_pos = self.text_widget.index(tk.INSERT)
        except:
            cursor_pos = "1.0"
        
        # Clear existing content and tags
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, content)
        
        # Parse SQL with error handling
        try:
            if content.strip():  # Only parse if there's content
                parsed = sqlparse.parse(content)
                
                for statement in parsed:
                    self._highlight_tokens(statement, "1.0", highlight_masked, mapping_dict)
                    
        except Exception as e:
            print(f"Highlighting error: {e}")
        
        # Restore cursor position
        try:
            self.text_widget.mark_set(tk.INSERT, cursor_pos)
        except:
            pass
    
    def _highlight_tokens(self, statement, start_pos, highlight_masked=False, mapping_dict=None):
        """Recursively highlight tokens"""
        current_pos = start_pos
        
        for token in statement.tokens:
            token_str = str(token)
            token_start = self.text_widget.search(token_str, current_pos, tk.END)
            
            if not token_start:
                continue
            
            # Calculate end position
            lines = token_str.count('\n')
            if lines > 0:
                last_line_len = len(token_str.split('\n')[-1])
                token_end = f"{int(token_start.split('.')[0]) + lines}.{last_line_len}"
            else:
                token_end = f"{token_start.split('.')[0]}.{int(token_start.split('.')[1]) + len(token_str)}"
            
            # Apply highlighting based on token type
            if token.is_group:
                self._highlight_tokens(token, token_start, highlight_masked, mapping_dict)
            else:
                self._apply_token_highlighting(token, token_start, token_end, highlight_masked, mapping_dict)
            
            current_pos = token_end
    
    def _apply_token_highlighting(self, token, start_pos, end_pos, highlight_masked, mapping_dict):
        """Apply highlighting to individual token"""
        token_str = str(token).strip()
        token_type = token.ttype
        
        # Skip empty tokens
        if not token_str:
            return
        
        # Check if this token is masked/original
        if highlight_masked and mapping_dict:
            # Check if it's a masked value
            for original, mapping in mapping_dict.items():
                if mapping["enabled"] and token_str == mapping["mask"]:
                    self.text_widget.tag_add("masked", start_pos, end_pos)
                    return
                elif token_str == original:
                    self.text_widget.tag_add("original", start_pos, end_pos)
                    return
        
        # SQL Keywords
        if (token_type in Keyword or 
            (token_type is None and token_str.upper() in KEYWORDS)):
            self.text_widget.tag_add("keyword", start_pos, end_pos)
        
        # Strings
        elif token_type in String or token_str.startswith(("'", '"')):
            self.text_widget.tag_add("string", start_pos, end_pos)
        
        # Comments
        elif token_type in Comment:
            self.text_widget.tag_add("comment", start_pos, end_pos)
        
        # Numbers
        elif token_type in (sqlparse.tokens.Literal.Number.Integer, 
                           sqlparse.tokens.Literal.Number.Float):
            self.text_widget.tag_add("number", start_pos, end_pos)
        
        # Operators
        elif token_str in ('=', '!=', '<>', '<', '>', '<=', '>=', '+', '-', '*', '/', '%'):
            self.text_widget.tag_add("operator", start_pos, end_pos)
        
        # Functions (tokens ending with parentheses)
        elif token_str.endswith('(') or (token_type in Name and 
                                        len(token_str) > 2 and 
                                        not token_str.isupper()):
            self.text_widget.tag_add("function", start_pos, end_pos)

class EnhancedSQLMaskerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced SQL Masker with Realistic Names & Syntax Highlighting")
        self.root.geometry("1800x1000")

        self.catalog_map = {}
        self.schema_map = {}
        self.table_map = {}
        self.column_map = {}
        self.string_map = {}
        self.function_map = {}
        self.alias_map = {}

        # Initialize realistic name generator
        self.name_generator = RealisticNameGenerator()
        
        # AI Configuration
        self.ai_enabled = False
        self.ai_config = {
            'api_key': '',
            'api_provider': 'openai',  # openai, anthropic, custom
            'base_url': '',
            'model': 'gpt-3.5-turbo'
        }

        # Enhanced SQL keywords including more comprehensive coverage
        self.sql_keywords = set(kw.lower() for kw in KEYWORDS.keys())
        
        # Add comprehensive SQL keywords for better recognition
        additional_keywords = {
            # Control flow
            'else', 'elseif', 'elsif', 'if', 'then', 'case', 'when', 'end', 'loop',
            'begin', 'declare', 'while', 'for', 'repeat', 'until', 'continue', 'break',
            
            # Window functions
            'over', 'partition', 'rows', 'range', 'unbounded', 'preceding', 'following',
            'current', 'row', 'first_value', 'last_value', 'lead', 'lag', 'rank',
            'dense_rank', 'row_number', 'ntile', 'percent_rank', 'cume_dist',
            
            # CTEs and advanced constructs
            'with', 'recursive', 'lateral', 'pivot', 'unpivot', 'cross', 'apply',
            
            # Data types
            'varchar', 'char', 'text', 'int', 'integer', 'bigint', 'smallint', 'tinyint',
            'decimal', 'numeric', 'float', 'double', 'real', 'date', 'datetime', 'timestamp',
            'time', 'year', 'boolean', 'bool', 'binary', 'varbinary', 'blob', 'clob',
            'json', 'xml', 'uuid', 'serial', 'auto_increment',
            
            # Common functions (to avoid masking)
            'count', 'sum', 'avg', 'min', 'max', 'abs', 'ceil', 'floor', 'round',
            'upper', 'lower', 'trim', 'ltrim', 'rtrim', 'substring', 'substr', 'length',
            'concat', 'replace', 'coalesce', 'isnull', 'nullif', 'cast', 'convert',
            'extract', 'datepart', 'datediff', 'dateadd', 'now', 'current_timestamp',
            'current_date', 'current_time', 'getdate', 'sysdate',
            
            # Database-specific keywords
            'limit', 'offset', 'top', 'fetch', 'next', 'only', 'ties',
            'returning', 'output', 'merge', 'upsert', 'conflict', 'nothing',
            'exclude', 'include', 'using', 'matched', 'except', 'intersect',
            
            # Stored procedures and functions
            'procedure', 'function', 'returns', 'return', 'out', 'inout', 'ref',
            'cursor', 'open', 'fetch', 'close', 'deallocate', 'execute', 'exec',
            'call', 'raise', 'raiserror', 'throw', 'try', 'catch', 'finally',
            
            # Constraints and indexes
            'constraint', 'primary', 'foreign', 'unique', 'check', 'default',
            'index', 'clustered', 'nonclustered', 'spatial', 'fulltext',
            
            # Transactions
            'transaction', 'commit', 'rollback', 'savepoint', 'isolation', 'level',
            'read', 'write', 'uncommitted', 'committed', 'repeatable', 'serializable',
            
            # Administrative
            'grant', 'revoke', 'deny', 'role', 'user', 'schema', 'database',
            'backup', 'restore', 'checkpoint', 'analyze', 'vacuum', 'reindex'
        }
        
        self.sql_keywords.update(additional_keywords)

        self.copy_buttons = []
        self.highlighters = {}
        self._setup_layout()

    def _setup_layout(self):
        self.root.grid_rowconfigure([1, 3, 5, 7, 9], weight=1)
        self.root.grid_rowconfigure(11, weight=0)  # AI buttons row
        self.root.grid_columnconfigure(0, weight=4)
        self.root.grid_columnconfigure(1, weight=1)

        self._create_text_section("Original SQL (Sensitive):", 0, 'input_text')
        self._create_text_section("Masked SQL (Safe for AI):", 2, 'masked_text')
        self._create_text_section("Paste AI-Modified (Masked) SQL:", 4, 'ai_text')
        self._create_text_section("Final SQL (Restored with original names):", 6, 'unmasked_text')
        self._create_text_section("Diff Viewer:", 8, 'diff_text', readonly=True)

        self.mapping_text = scrolledtext.ScrolledText(self.root, width=50, state='disabled', font=('Consolas', 9))
        self.mapping_text.grid(row=1, column=1, rowspan=7, sticky="nsew", padx=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")
        for i in range(9): btn_frame.columnconfigure(i, weight=1)

        tk.Button(btn_frame, text="Mask SQL", command=self.prepare_masking, bg="#4CAF50", fg="black").grid(row=0, column=0, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Unmask SQL", command=self.unmask_sql, bg="#2196F3", fg="black").grid(row=0, column=1, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Show Diff", command=self.show_diff, bg="#FF9800", fg="black").grid(row=0, column=2, padx=5, sticky="ew")
        tk.Button(btn_frame, text="View Mapping", command=self.update_mapping_display).grid(row=0, column=3, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Load SQL File", command=self.load_file).grid(row=0, column=4, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Test SQL", command=self.test_sql_parsing).grid(row=0, column=5, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Save Mapping", command=self.save_mapping).grid(row=0, column=6, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Load Mapping", command=self.load_mapping).grid(row=0, column=7, padx=5, sticky="ew")
        # New button for naming mode toggle
        tk.Button(btn_frame, text="Realistic Names", command=self.toggle_naming_mode, bg="#9C27B0", fg="black").grid(row=0, column=8, padx=5, sticky="ew")
        
        # Naming mode flag
        self.use_realistic_names = True
        
        # Add AI buttons row
        ai_frame = tk.Frame(self.root)
        ai_frame.grid(row=11, column=0, columnspan=2, pady=5, sticky="ew")
        for i in range(4): ai_frame.columnconfigure(i, weight=1)
        
        self.ai_toggle_btn = tk.Button(ai_frame, text="🤖 Enable AI Features", command=self.toggle_ai_features, bg="#9E9E9E", fg="black")
        self.ai_toggle_btn.grid(row=0, column=0, padx=5, sticky="ew")
        
        self.ai_config_btn = tk.Button(ai_frame, text="⚙️ AI Config", command=self.show_ai_config, state='disabled')
        self.ai_config_btn.grid(row=0, column=1, padx=5, sticky="ew")
        
        self.ai_understand_btn = tk.Button(ai_frame, text="🧠 Understand Code", command=self.ai_understand_code, state='disabled', bg="#4CAF50", fg="black")
        self.ai_understand_btn.grid(row=0, column=2, padx=5, sticky="ew")
        
        self.ai_modify_btn = tk.Button(ai_frame, text="✏️ Modify Code", command=self.ai_modify_code, state='disabled', bg="#2196F3", fg="black")
        self.ai_modify_btn.grid(row=0, column=3, padx=5, sticky="ew")

    def _create_text_section(self, label_text, row, attr_name, readonly=False):
        label = tk.Label(self.root, text=label_text, font=('Arial', 10, 'bold'))
        label.grid(row=row, column=0, sticky="w", padx=10, pady=(10, 0))
        
        # Create text widget with syntax highlighting support
        text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=8, font=('Consolas', 10))
        text_widget.grid(row=row+1, column=0, sticky="nsew", padx=10, pady=5)
        
        # Ensure text widget is properly configured for input
        text_widget.configure(
            insertbackground='black',  # Cursor color
            selectbackground='#0078d4',  # Selection color
            selectforeground='white',
            bg='white',
            fg='black'
        )
        
        if readonly:
            text_widget.configure(state='disabled', bg='#f0f0f0')
        else:
            # Ensure normal state for input
            text_widget.configure(state='normal')
        
        # Initialize syntax highlighter
        highlighter = SyntaxHighlighter(text_widget)
        self.highlighters[attr_name] = highlighter
        
        setattr(self, attr_name, text_widget)
        self._add_copy_button(text_widget, row+2, 0)
        
        # Bind text change events for real-time highlighting (with delay to avoid interference)
        if not readonly:
            # Use a longer delay to avoid interfering with typing
            text_widget.bind('<KeyRelease>', lambda e, attr=attr_name: self._on_text_change_delayed(attr))
            text_widget.bind('<FocusIn>', lambda e, attr=attr_name: self._on_focus_in(attr))
            text_widget.bind('<FocusOut>', lambda e, attr=attr_name: self._apply_highlighting(attr))

    def _on_text_change(self, attr_name):
        """Handle text changes for syntax highlighting"""
        self.root.after(500, lambda: self._apply_highlighting(attr_name))
    
    def _on_text_change_delayed(self, attr_name):
        """Handle text changes with longer delay to avoid typing interference"""
        # Cancel any pending highlighting
        if hasattr(self, '_highlight_timer'):
            try:
                self.root.after_cancel(self._highlight_timer)
            except:
                pass
        # Schedule highlighting with longer delay
        self._highlight_timer = self.root.after(1500, lambda: self._apply_highlighting(attr_name))
    
    def _on_focus_in(self, attr_name):
        """Handle focus in event"""
        # Cancel highlighting when user starts typing
        if hasattr(self, '_highlight_timer'):
            try:
                self.root.after_cancel(self._highlight_timer)
            except:
                pass

    def _delayed_highlight(self, attr_name):
        """Apply highlighting after a short delay"""
        self.root.after(100, lambda: self._apply_highlighting(attr_name))

    def _apply_highlighting(self, attr_name):
        """Apply syntax highlighting to text widget"""
        try:
            text_widget = getattr(self, attr_name)
            content = text_widget.get("1.0", tk.END)
            
            if content.strip():
                # Use simple regex-based highlighting to avoid interfering with input
                self._apply_simple_highlighting(text_widget, content, attr_name)
                
        except Exception as e:
            print(f"Highlighting error for {attr_name}: {e}")
    
    def _apply_simple_highlighting(self, text_widget, content, attr_name):
        """Apply simple regex-based highlighting that won't interfere with typing"""
        try:
            # Store current cursor position and selection
            try:
                cursor_pos = text_widget.index(tk.INSERT)
                has_selection = False
                sel_start = sel_end = None
                try:
                    sel_start = text_widget.index(tk.SEL_FIRST)
                    sel_end = text_widget.index(tk.SEL_LAST)
                    has_selection = True
                except:
                    pass
            except:
                cursor_pos = "1.0"
                has_selection = False
            
            # Clear existing tags
            for tag in ['keyword', 'string', 'comment', 'number', 'masked', 'original']:
                text_widget.tag_delete(tag)
            
            # Apply basic highlighting using regex
            import re
            
            # SQL Keywords (simple approach)
            keyword_pattern = r'\b(?:SELECT|FROM|WHERE|INSERT|UPDATE|DELETE|CREATE|TABLE|INDEX|ALTER|DROP|JOIN|INNER|LEFT|RIGHT|OUTER|ON|GROUP|BY|ORDER|HAVING|UNION|DISTINCT|COUNT|SUM|AVG|MIN|MAX|AND|OR|NOT|IN|LIKE|BETWEEN|IS|NULL|AS|CASE|WHEN|THEN|ELSE|END)\b'
            for match in re.finditer(keyword_pattern, content, re.IGNORECASE):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                text_widget.tag_add('keyword', start_idx, end_idx)
            
            # String literals
            string_pattern = r"'[^']*'|\"[^\"]*\""
            for match in re.finditer(string_pattern, content):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                text_widget.tag_add('string', start_idx, end_idx)
            
            # Comments
            comment_pattern = r'--.*?$|/\*.*?\*/'
            for match in re.finditer(comment_pattern, content, re.MULTILINE | re.DOTALL):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                text_widget.tag_add('comment', start_idx, end_idx)
            
            # Restore cursor position and selection
            try:
                text_widget.mark_set(tk.INSERT, cursor_pos)
                if has_selection:
                    text_widget.tag_add(tk.SEL, sel_start, sel_end)
            except:
                pass
                
        except Exception as e:
            print(f"Simple highlighting error: {e}")

    def toggle_naming_mode(self):
        """Toggle between realistic and generic naming"""
        self.use_realistic_names = not self.use_realistic_names
        
        # Update button text
        button_text = "Realistic Names" if self.use_realistic_names else "Generic Names"
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button) and "Names" in child['text']:
                        child.config(text=button_text)
                        break
        
        mode = "realistic" if self.use_realistic_names else "generic"
        messagebox.showinfo("Naming Mode", f"Switched to {mode} naming mode.\nThis will affect new masking operations.")

    def _add_copy_button(self, text_widget, row, col):
        btn = tk.Button(self.root, text="Copy", bg="#607D8B", fg="black")
        btn.grid(row=row, column=col, sticky="e", padx=10, pady=(0, 10))
        btn.configure(command=lambda b=btn, w=text_widget: self.copy_text(w, b))
        self.copy_buttons.append(btn)

    def copy_text(self, widget, button):
        # Check if widget is already in normal state
        current_state = widget.cget('state')
        
        # Temporarily enable if disabled
        if current_state == 'disabled':
            widget.configure(state='normal')
        
        content = widget.get("1.0", tk.END)
        
        # Restore original state
        if current_state == 'disabled':
            widget.configure(state='disabled')
        
        pyperclip.copy(content.strip())
        original_text = button['text']
        button.config(text="✅")
        button.after(2000, lambda: button.config(text=original_text))

    def is_sql_keyword_or_function(self, token_str):
        """Enhanced check for SQL keywords and common functions"""
        if not token_str or len(token_str.strip()) == 0:
            return False
        
        clean_token = token_str.strip().lower()
        
        # Check against SQL keywords
        if clean_token in self.sql_keywords:
            return True
            
        # Additional runtime checks for common patterns
        builtin_patterns = [
            # Statistical functions
            'stddev', 'variance', 'var_pop', 'var_samp', 'stddev_pop', 'stddev_samp',
            # Date/time keywords
            'epoch', 'dow', 'doy', 'week', 'quarter', 'millennium', 'century', 'decade',
            # Window function keywords
            'within', 'preceding', 'following', 'unbounded', 'current',
            # Advanced functions
            'percentile_cont', 'percentile_disc', 'cume_dist', 'percent_rank',
            'first_value', 'last_value', 'nth_value',
            # JSON functions
            'json_build_object', 'json_agg', 'json_object_agg',
            # String functions
            'string_agg', 'array_agg', 'array_to_string',
            # Math functions
            'greatest', 'least', 'coalesce', 'nullif'
        ]
        
        return clean_token in builtin_patterns

    def normalize_string_quotes(self, string_literal):
        """Normalize quotes in string literals for consistent matching"""
        if not string_literal:
            return string_literal
        
        # Remove outer quotes and normalize
        stripped = string_literal.strip()
        if (stripped.startswith("'") and stripped.endswith("'")) or \
           (stripped.startswith('"') and stripped.endswith('"')):
            return stripped[1:-1]  # Return content without quotes
        return stripped

    def extract_tables(self, sql):
        """Enhanced table extraction with error handling and markdown cleanup"""
        try:
            # Clean the SQL first - remove markdown code blocks if present
            clean_sql = self._clean_sql_from_markdown(sql)
            
            parser = Parser(clean_sql)
            tables = parser.tables or []
            
            # Additional parsing for complex queries
            parsed = sqlparse.parse(clean_sql)
            additional_tables = []
            
            for statement in parsed:
                for token in statement.flatten():
                    if token.ttype is Name and not self.is_sql_keyword_or_function(str(token)):
                        # Check if this could be a table name by context
                        token_str = str(token)
                        if '.' in token_str and token_str not in tables:
                            additional_tables.append(token_str)
            
            return list(set(tables + additional_tables))
        except Exception as e:
            print(f"Warning: Table extraction error: {e}")
            return []

    def extract_columns(self, sql):
        """Enhanced column extraction with error handling and better filtering"""
        try:
            # Clean the SQL first - remove markdown code blocks if present
            clean_sql = self._clean_sql_from_markdown(sql)
            
            parser = Parser(clean_sql)
            columns = parser.columns or []
            
            # Additional parsing for complex queries
            parsed = sqlparse.parse(clean_sql)
            additional_columns = []
            
            for statement in parsed:
                for token in statement.flatten():
                    if (token.ttype is Name and 
                        not self.is_sql_keyword_or_function(str(token)) and
                        str(token) != '*' and
                        len(str(token).strip()) > 1):
                        
                        token_str = str(token).strip()
                        
                        # Skip if it's a qualified name (contains dots)
                        if '.' in token_str:
                            continue
                            
                        # Skip if it looks like a schema or database name
                        if any(token_str in getattr(self, attr, {}) for attr in 
                               ['catalog_map', 'schema_map', 'table_map']):
                            continue
                        
                        # Skip common alias patterns
                        if len(token_str) <= 3 and token_str.isalpha():
                            continue
                            
                        if token_str not in columns:
                            additional_columns.append(token_str)
            
            # Remove duplicates and filter out qualified references
            all_columns = list(set(columns + additional_columns))
            filtered_columns = [col for col in all_columns if '.' not in col and 
                              not self.is_sql_keyword_or_function(col)]
            
            return filtered_columns
        except Exception as e:
            print(f"Warning: Column extraction error: {e}")
            return []

    def extract_strings(self, sql):
        """Enhanced string extraction with better regex and normalization"""
        # Clean the SQL first - remove markdown code blocks if present
        clean_sql = self._clean_sql_from_markdown(sql)
        
        # Only extract actual SQL string literals
        patterns = [
            r"'(?:[^'\\]|\\.)*'",     # Single quoted strings (with escape handling)
            r'"(?:[^"\\]|\\.)*"',     # Double quoted strings (with escape handling)
        ]
        
        strings = []
        for pattern in patterns:
            matches = re.findall(pattern, clean_sql)
            strings.extend(matches)
        
        # Filter out very long strings (likely not real SQL strings)
        filtered_strings = [s for s in strings if len(s) < 200]
        
        return list(set(filtered_strings))

    def extract_functions(self, sql):
        """Extract user-defined functions (not built-in SQL functions)"""
        functions = []
        try:
            parsed = sqlparse.parse(sql)
            
            for statement in parsed:
                for token in statement.flatten():
                    if isinstance(token.parent, Function):
                        func_name = str(token).strip('(')
                        if (not self.is_sql_keyword_or_function(func_name) and 
                            func_name not in functions):
                            functions.append(func_name)
        except Exception as e:
            print(f"Warning: Function extraction error: {e}")
        
        return functions

    def extract_aliases(self, sql):
        """Extract table and column aliases with better filtering and conflict prevention"""
        aliases = []
        try:
            parsed = sqlparse.parse(sql)
            
            # Common short aliases that are typically table aliases
            common_table_aliases = set()
            
            for statement in parsed:
                for token in statement.flatten():
                    if isinstance(token.parent, Identifier):
                        if hasattr(token.parent, 'get_alias'):
                            alias = token.parent.get_alias()
                            if (alias and 
                                not self.is_sql_keyword_or_function(alias) and
                                len(alias.strip()) > 0):
                                
                                # Filter out aliases that are actually column names
                                if len(alias) <= 4 and alias.isalpha():
                                    common_table_aliases.add(alias)
                                elif len(alias) > 4:  # Longer aliases are usually column aliases
                                    aliases.append(alias)
            
            # Only include short aliases if they appear to be table aliases
            # (this is a heuristic and may need refinement)
            final_aliases = []
            for alias in aliases:
                if alias not in common_table_aliases:
                    final_aliases.append(alias)
        except Exception as e:
            print(f"Warning: Alias extraction error: {e}")
        
        return final_aliases

    def _clean_sql_from_markdown(self, sql):
        """Extract SQL content from markdown code blocks if present"""
        clean_sql = sql
        if '```sql' in sql:
            # Extract only the SQL content between ```sql and ```
            sql_blocks = re.findall(r'```sql\s*\n(.*?)\n```', sql, re.DOTALL)
            if sql_blocks:
                clean_sql = '\n'.join(sql_blocks)
        return clean_sql

    def generate_placeholders(self, tables, columns, strings, functions=None, aliases=None):
        """Enhanced placeholder generation with realistic names and better deduplication"""
        def add_map(d, key, prefix, count, avoid_conflicts=True, generator_func=None):
            if (key and 
                key not in d and 
                not self.is_sql_keyword_or_function(key) and
                len(key.strip()) > 0):
                
                if self.use_realistic_names and generator_func:
                    # Use realistic name generator
                    mask_name = generator_func(key)
                else:
                    # Use generic naming
                    mask_name = f"{prefix}_{count[0]}"
                    if avoid_conflicts and self._has_naming_conflict(key, d):
                        mask_name = f"safe_{prefix}_{count[0]}"
                
                d[key] = {"mask": mask_name, "enabled": True}
                count[0] += 1

        # Reset all mappings
        self.catalog_map, self.schema_map, self.table_map = {}, {}, {}
        self.column_map, self.string_map = {}, {}
        self.function_map, self.alias_map = {}, {}
        
        # Reset name generator for consistent naming
        self.name_generator = RealisticNameGenerator()
        
        c_count = s_count = t_count = col_count = str_count = [1]
        func_count = alias_count = [1]

        # Track items to avoid duplicates across categories
        all_processed_items = set()

        # Process tables with enhanced logic
        for tbl in tables:
            if not tbl or self.is_sql_keyword_or_function(tbl):
                continue
                
            parts = tbl.split('.')
            if len(parts) == 3:
                catalog, schema, table = parts
                if catalog not in all_processed_items:
                    add_map(self.catalog_map, catalog, "catalog", c_count, generator_func=self.name_generator.generate_schema_name)
                    all_processed_items.add(catalog)
                if schema not in all_processed_items:
                    add_map(self.schema_map, schema, "schema", s_count, generator_func=self.name_generator.generate_schema_name)
                    all_processed_items.add(schema)
                if table not in all_processed_items:
                    add_map(self.table_map, table, "table", t_count, generator_func=self.name_generator.generate_table_name)
                    all_processed_items.add(table)
            elif len(parts) == 2:
                schema, table = parts
                if schema not in all_processed_items:
                    add_map(self.schema_map, schema, "schema", s_count, generator_func=self.name_generator.generate_schema_name)
                    all_processed_items.add(schema)
                if table not in all_processed_items:
                    add_map(self.table_map, table, "table", t_count, generator_func=self.name_generator.generate_table_name)
                    all_processed_items.add(table)
            else:
                if tbl not in all_processed_items:
                    add_map(self.table_map, tbl, "table", t_count, generator_func=self.name_generator.generate_table_name)
                    all_processed_items.add(tbl)

        # Process columns - avoid items already processed as tables/schemas
        for col in columns:
            if (col and 
                col != '*' and 
                col not in all_processed_items and
                not self.is_sql_keyword_or_function(col)):
                add_map(self.column_map, col, "column", col_count, generator_func=self.name_generator.generate_column_name)
                all_processed_items.add(col)

        # Process strings with normalized matching
        for s in strings:
            if s and s not in all_processed_items:
                if self.use_realistic_names:
                    mask_name = self.name_generator.generate_string_value(s)
                else:
                    mask_name = f"'string{str_count[0]}'"
                
                self.string_map[s] = {"mask": mask_name, "enabled": True}
                str_count[0] += 1
                all_processed_items.add(s)

        # Process functions - avoid built-in functions
        if functions:
            for func in functions:
                if (func and 
                    func not in all_processed_items and
                    not self.is_sql_keyword_or_function(func)):
                    add_map(self.function_map, func, "function", func_count, generator_func=self.name_generator.generate_function_name)
                    all_processed_items.add(func)

        # Process aliases - be more selective and add prefix to prevent conflicts
        if aliases:
            for alias in aliases:
                if (alias and 
                    alias not in all_processed_items and
                    not self.is_sql_keyword_or_function(alias) and
                    len(alias) > 3):  # Only longer aliases to avoid table alias conflicts
                    
                    if self.use_realistic_names:
                        # Generate realistic alias name
                        mask_name = f"alias_{self.name_generator.generate_column_name(alias)}"
                    else:
                        mask_name = f"alias_{alias_count[0]}"
                    
                    self.alias_map[alias] = {"mask": mask_name, "enabled": True}
                    alias_count[0] += 1
                    all_processed_items.add(alias)

    def _has_naming_conflict(self, key, current_dict):
        """Check if key conflicts with other categories"""
        all_maps = [self.catalog_map, self.schema_map, self.table_map, 
                   self.column_map, self.function_map, self.alias_map]
        
        for map_dict in all_maps:
            if map_dict is not current_dict and key in map_dict:
                return True
        return False

    def prepare_masking(self):
        """Enhanced preparation with better extraction, input validation, and error handling"""
        sql = self.input_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Warning", "Please enter SQL code first.")
            return
        
        # Check if input contains markdown - warn user
        if '```sql' in sql:
            response = messagebox.askyesno(
                "Markdown Detected", 
                "The input appears to contain markdown code blocks. Should I extract just the SQL content?"
            )
            if not response:
                return
            
        try:
            # Enhanced SQL parsing with specific error handling
            try:
                parsed_test = sqlparse.parse(sql)
                if not parsed_test:
                    raise ValueError("No valid SQL statements found")
            except Exception as parse_error:
                error_msg = f"SQL parsing failed: {str(parse_error)}\n\n"
                error_msg += "Suggestions:\n"
                error_msg += "• Check for unmatched quotes or parentheses\n"
                error_msg += "• Ensure all statements end with semicolons\n"
                error_msg += "• Remove any non-SQL content\n"
                error_msg += "• Check for special characters or encoding issues"
                
                messagebox.showerror("SQL Parse Error", error_msg)
                return
            
            self.tables = self.extract_tables(sql)
            self.columns = self.extract_columns(sql)
            self.strings = self.extract_strings(sql)
            self.functions = self.extract_functions(sql)
            self.aliases = self.extract_aliases(sql)
            
            # Debug info
            print(f"Extracted: {len(self.tables)} tables, {len(self.columns)} columns, {len(self.strings)} strings")
            
            self.generate_placeholders(
                self.tables, self.columns, self.strings, 
                self.functions, self.aliases
            )
            self.show_mapping_editor()
        except Exception as e:
            error_msg = f"SQL processing error: {str(e)}\n\n"
            error_msg += "This might be caused by:\n"
            error_msg += "• Complex SQL syntax not fully supported\n"
            error_msg += "• Missing required libraries\n"
            error_msg += "• Corrupted or incomplete SQL statements"
            
            messagebox.showerror("Processing Error", error_msg)
            import traceback
            traceback.print_exc()

    def show_mapping_editor(self):
        """Enhanced mapping editor with more categories and better UI"""
        top = Toplevel(self.root)
        top.title("Edit Mapping Toggles - " + ("Realistic Names" if self.use_realistic_names else "Generic Names"))
        top.geometry("800x700")

        # Add header with naming mode info
        header_frame = tk.Frame(top)
        header_frame.pack(fill="x", padx=10, pady=5)
        
        mode_text = "🎯 Using Realistic Names" if self.use_realistic_names else "📝 Using Generic Names"
        tk.Label(header_frame, text=mode_text, font=('Arial', 12, 'bold'), 
                fg="#4CAF50" if self.use_realistic_names else "#2196F3").pack()

        canvas = tk.Canvas(top)
        scrollbar = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        checkbox_vars = []
        category_vars = {}
        item_vars_by_category = {}
        row = 0

        categories = [
            ("📊 Catalogs", "catalog_map"),
            ("🏗️ Schemas", "schema_map"), 
            ("📋 Tables", "table_map"),
            ("📝 Columns", "column_map"),
            ("💬 Strings", "string_map"),
            ("⚙️ Functions", "function_map"),
            ("🔗 Aliases", "alias_map")
        ]

        for label, attr_key in categories:
            attr = getattr(self, attr_key)
            if not attr:  # Skip empty categories
                continue
                
            category_var = tk.BooleanVar(value=True)
            category_vars[attr_key] = category_var
            item_vars_by_category[attr_key] = []
            
            # Category header with colored background
            category_frame = tk.Frame(scroll_frame, bg="#E3F2FD", relief="ridge", bd=1)
            category_frame.grid(row=row, column=0, sticky='ew', padx=5, pady=2)
            scroll_frame.grid_columnconfigure(0, weight=1)
            
            tk.Checkbutton(
                category_frame, text=f"{label} ({len(attr)} items)", 
                variable=category_var, font=('Arial', 10, 'bold'),
                bg="#E3F2FD"
            ).pack(anchor="w", padx=5, pady=2)
            row += 1
            
            # Items in this category
            for key, val in attr.items():
                var = tk.BooleanVar(value=val["enabled"])
                
                item_frame = tk.Frame(scroll_frame)
                item_frame.grid(row=row, column=0, sticky='ew', padx=15)
                
                cb = tk.Checkbutton(
                    item_frame, text=f"{key} → {val['mask']}", 
                    variable=var, anchor="w", justify="left",
                    font=('Consolas', 9)
                )
                cb.pack(anchor="w")
                
                checkbox_vars.append((var, attr, key, category_var))
                item_vars_by_category[attr_key].append(var)
                row += 1

            def make_callback(item_vars):
                def callback(*_args):
                    value = category_var.get()
                    for v in item_vars:
                        v.set(value)
                return callback
            category_var.trace_add("write", make_callback(item_vars_by_category[attr_key]))

        def apply_and_close():
            for var, d, k, cat_var in checkbox_vars:
                d[k]["enabled"] = var.get() and cat_var.get()
            self.mask_sql()
            self.update_mapping_display()
            # Apply highlighting to show masked items
            self._apply_highlighting('masked_text')
            top.destroy()

        button_frame = tk.Frame(top, bg="#F5F5F5")
        button_frame.pack(fill="x", pady=10)
        
        tk.Button(button_frame, text="✅ Apply & Mask SQL", command=apply_and_close, 
                 bg="#4CAF50", fg="black", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="❌ Cancel", command=top.destroy, 
                 bg="#F44336", fg="black").pack(side=tk.LEFT, padx=5)

    def mask_sql(self):
        """Enhanced SQL masking with better token handling and improved string matching"""
        sql = self.input_text.get("1.0", tk.END).strip()
        if not sql:
            return
            
        try:
            parsed = sqlparse.parse(sql)
            result_sql = ""

            for statement in parsed:
                result_sql += self._mask_statement(statement)

            self.masked_text.delete("1.0", tk.END)
            self.masked_text.insert(tk.END, result_sql)
            
            # Apply syntax highlighting
            self._apply_highlighting('masked_text')
            
        except Exception as e:
            messagebox.showerror("Error", f"SQL masking error: {str(e)}")

    def _mask_statement(self, statement):
        """Recursively mask SQL statement tokens"""
        result = ""
        
        for token in statement.tokens:
            if token.is_group:
                result += self._mask_statement(token)
            else:
                result += self._mask_token(token)
        
        return result

    def _mask_token(self, token):
        """Enhanced token masking logic with improved string matching"""
        token_str = str(token)
        token_type = token.ttype

        # Skip keywords, whitespace, comments, and punctuation
        if (token_type in (Keyword, Whitespace, Comment, Punctuation) or
            self.is_sql_keyword_or_function(token_str.strip())):
            return token_str

        # Handle string literals with improved matching
        if token_type in String.Single or token_str.startswith("'") or token_str.startswith('"'):
            for original, mapping in self.string_map.items():
                if mapping["enabled"]:
                    # Try exact match first
                    if original == token_str:
                        return mapping["mask"]
                    # Try normalized matching (content without quotes)
                    token_normalized = self.normalize_string_quotes(token_str)
                    original_normalized = self.normalize_string_quotes(original)
                    if token_normalized == original_normalized:
                        return mapping["mask"]
            return token_str

        # Handle identifiers (names)
        if token_type in Name or token_type is None:
            # Check all mapping categories in order of specificity
            for mapping_dict in [self.catalog_map, self.schema_map, 
                               self.table_map, self.column_map,
                               self.function_map, self.alias_map]:
                if token_str in mapping_dict and mapping_dict[token_str]["enabled"]:
                    return mapping_dict[token_str]["mask"]

        return token_str

    def unmask_sql(self):
        """Enhanced SQL unmasking with better pattern matching and conflict resolution"""
        sql = self.ai_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Warning", "Please paste AI-modified SQL first.")
            return

        try:
            # Unmask in reverse order of specificity to avoid conflicts
            # Use more specific patterns to prevent incorrect replacements
            
            # First pass: Handle strings (they don't need word boundaries)
            for original, mapping in self.string_map.items():
                if mapping["enabled"]:
                    # Use exact string replacement for string literals
                    sql = sql.replace(mapping["mask"], original)

            # Second pass: Handle identifiers with word boundaries to prevent partial matches
            # Process in order from most specific to least specific
            mapping_order = [
                self.alias_map,     # Most specific (prefixed)
                self.function_map,  # Functions
                self.column_map,    # Columns
                self.table_map,     # Tables  
                self.schema_map,    # Schemas
                self.catalog_map    # Least specific
            ]
            
            for mapping_dict in mapping_order:
                for original, mapping in mapping_dict.items():
                    if mapping["enabled"]:
                        # Use word boundaries for precise replacement of identifiers
                        pattern = rf'\b{re.escape(mapping["mask"])}\b'
                        sql = re.sub(pattern, original, sql)

            self.unmasked_text.delete("1.0", tk.END)
            self.unmasked_text.insert(tk.END, sql)
            
            # Apply syntax highlighting
            self._apply_highlighting('unmasked_text')
            
        except Exception as e:
            messagebox.showerror("Error", f"SQL unmasking error: {str(e)}")

    def save_mapping(self):
        """Export mapping to JSON file for reuse"""
        try:
            # Check if we have any mappings to save
            all_maps = [self.catalog_map, self.schema_map, self.table_map,
                       self.column_map, self.string_map, self.function_map, self.alias_map]
            
            if not any(all_maps):
                messagebox.showwarning("Warning", "No mappings to save. Please mask SQL first.")
                return
            
            # Create mapping data with metadata
            mapping_data = {
                "metadata": {
                    "created_at": datetime.now().isoformat(),
                    "version": "2.0",
                    "description": "SQL Masker mapping file with realistic names",
                    "realistic_names": self.use_realistic_names
                },
                "mappings": {
                    "catalogs": self.catalog_map,
                    "schemas": self.schema_map,
                    "tables": self.table_map,
                    "columns": self.column_map,
                    "strings": self.string_map,
                    "functions": self.function_map,
                    "aliases": self.alias_map
                }
            }
            
            # Ask user for file location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Save Mapping File"
            )
            
            if file_path:
                with open(file_path, "w", encoding='utf-8') as f:
                    json.dump(mapping_data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("Success", f"Mapping saved to {file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save mapping: {str(e)}")

    def load_mapping(self):
        """Import mapping from JSON file"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Load Mapping File"
            )
            
            if not file_path:
                return
                
            with open(file_path, 'r', encoding='utf-8') as f:
                mapping_data = json.load(f)
            
            # Validate file format
            if "mappings" not in mapping_data:
                messagebox.showerror("Error", "Invalid mapping file format.")
                return
            
            mappings = mapping_data["mappings"]
            
            # Load mappings with validation
            self.catalog_map = mappings.get("catalogs", {})
            self.schema_map = mappings.get("schemas", {})
            self.table_map = mappings.get("tables", {})
            self.column_map = mappings.get("columns", {})
            self.string_map = mappings.get("strings", {})
            self.function_map = mappings.get("functions", {})
            self.alias_map = mappings.get("aliases", {})
            
            # Check if this mapping used realistic names
            if "metadata" in mapping_data and "realistic_names" in mapping_data["metadata"]:
                loaded_realistic = mapping_data["metadata"]["realistic_names"]
                if loaded_realistic != self.use_realistic_names:
                    mode_text = "realistic" if loaded_realistic else "generic"
                    response = messagebox.askyesno(
                        "Naming Mode Mismatch",
                        f"This mapping was created using {mode_text} names.\n"
                        f"Would you like to switch to {mode_text} mode?"
                    )
                    if response:
                        self.use_realistic_names = loaded_realistic
                        self.toggle_naming_mode()
            
            # Validate mapping structure
            all_maps = [self.catalog_map, self.schema_map, self.table_map,
                       self.column_map, self.string_map, self.function_map, self.alias_map]
            
            for map_dict in all_maps:
                for key, value in map_dict.items():
                    if not isinstance(value, dict) or "mask" not in value or "enabled" not in value:
                        messagebox.showerror("Error", f"Invalid mapping structure for key: {key}")
                        return
            
            # Show metadata if available
            metadata_info = ""
            if "metadata" in mapping_data:
                metadata = mapping_data["metadata"]
                if "created_at" in metadata:
                    metadata_info += f"Created: {metadata['created_at']}\n"
                if "description" in metadata:
                    metadata_info += f"Description: {metadata['description']}\n"
            
            success_msg = f"Mapping loaded successfully from {os.path.basename(file_path)}"
            if metadata_info:
                success_msg += f"\n\n{metadata_info}"
            
            messagebox.showinfo("Success", success_msg)
            self.update_mapping_display()
            
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON file format.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load mapping: {str(e)}")

    def show_diff(self):
        """Enhanced diff display with syntax highlighting"""
        try:
            masked_sql = self.masked_text.get("1.0", tk.END).strip().splitlines()
            ai_sql = self.ai_text.get("1.0", tk.END).strip().splitlines()
            
            if not masked_sql and not ai_sql:
                diff_output = "No content to compare."
            elif not masked_sql:
                diff_output = "No masked SQL to compare against."
            elif not ai_sql:
                diff_output = "No AI-modified SQL to compare."
            else:
                diff = list(difflib.unified_diff(
                    masked_sql, ai_sql, 
                    fromfile='Masked SQL (Original)', 
                    tofile='AI Modified SQL (Modified)',
                    lineterm='', n=3
                ))
                
                diff_output = '\n'.join(diff) if diff else "No changes detected between masked and AI-modified SQL."
            
            self.diff_text.configure(state='normal')
            self.diff_text.delete("1.0", tk.END)
            self.diff_text.insert(tk.END, diff_output)
            self.diff_text.configure(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Diff generation error: {str(e)}")

    def update_mapping_display(self):
        """Enhanced mapping display with statistics and colors"""
        try:
            self.mapping_text.configure(state='normal')
            self.mapping_text.delete("1.0", tk.END)
            
            # Add header
            mode_text = "🎯 REALISTIC NAMES MODE" if self.use_realistic_names else "📝 GENERIC NAMES MODE"
            self.mapping_text.insert(tk.END, f"{mode_text}\n")
            self.mapping_text.insert(tk.END, "=" * 30 + "\n\n")
            
            categories = [
                ("📊 Catalogs", self.catalog_map),
                ("🏗️ Schemas", self.schema_map),
                ("📋 Tables", self.table_map),
                ("📝 Columns", self.column_map),
                ("💬 Strings", self.string_map),
                ("⚙️ Functions", self.function_map),
                ("🔗 Aliases", self.alias_map)
            ]
            
            total_enabled = total_items = 0
            
            for title, mapping_dict in categories:
                if not mapping_dict:
                    continue
                    
                enabled_count = sum(1 for v in mapping_dict.values() if v["enabled"])
                total_count = len(mapping_dict)
                total_enabled += enabled_count
                total_items += total_count
                
                start_idx = self.mapping_text.index(tk.END)
                self.mapping_text.insert(tk.END, f"{title} ({enabled_count}/{total_count}):\n")
                end_idx = self.mapping_text.index(tk.END)
                self.mapping_text.tag_add("bold", start_idx, end_idx)
                
                for original, mapping in mapping_dict.items():
                    status = "✔️" if mapping["enabled"] else "❌"
                    self.mapping_text.insert(tk.END, f"  {original} → {mapping['mask']} {status}\n")
                self.mapping_text.insert(tk.END, "\n")
            
            # Add summary
            start_idx = self.mapping_text.index(tk.END)
            self.mapping_text.insert(tk.END, f"📊 SUMMARY: {total_enabled}/{total_items} items will be masked\n")
            end_idx = self.mapping_text.index(tk.END)
            self.mapping_text.tag_add("bold", start_idx, end_idx)
            
            self.mapping_text.tag_configure("bold", font=('Consolas', 10, 'bold'))
            self.mapping_text.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Mapping display error: {str(e)}")

    def test_sql_parsing(self):
        """Test SQL parsing and show detailed analysis with enhanced error reporting"""
        sql = self.input_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Warning", "Please enter SQL code first.")
            return
            
        try:
            # Test basic parsing first
            try:
                parsed = sqlparse.parse(sql)
                if not parsed:
                    raise ValueError("No SQL statements could be parsed")
            except Exception as parse_error:
                error_analysis = f"PARSING ERROR: {str(parse_error)}\n\n"
                error_analysis += "Common causes and solutions:\n"
                error_analysis += "• Unmatched quotes: Check for missing ' or \" characters\n"
                error_analysis += "• Unmatched parentheses: Ensure all ( have matching )\n"
                error_analysis += "• Missing semicolons: End statements with ;\n"
                error_analysis += "• Invalid characters: Remove non-SQL content\n"
                error_analysis += "• Encoding issues: Save file as UTF-8\n\n"
                
                # Try to identify specific issues
                if "unterminated" in str(parse_error).lower():
                    error_analysis += "SPECIFIC ISSUE: Unterminated string literal detected\n"
                elif "syntax" in str(parse_error).lower():
                    error_analysis += "SPECIFIC ISSUE: SQL syntax error detected\n"
                
                self._show_analysis_popup("SQL Parsing Error Analysis", error_analysis)
                return
            
            analysis = "SQL Parsing Analysis:\n\n"
            analysis += f"✅ Successfully parsed {len(parsed)} statement(s)\n\n"
            
            # Test extractions
            tables = self.extract_tables(sql)
            columns = self.extract_columns(sql)
            strings = self.extract_strings(sql)
            functions = self.extract_functions(sql)
            aliases = self.extract_aliases(sql)
            
            analysis += "EXTRACTION RESULTS:\n"
            analysis += f"Tables ({len(tables)}): {', '.join(tables[:10])}{'...' if len(tables) > 10 else ''}\n"
            analysis += f"Columns ({len(columns)}): {', '.join(columns[:10])}{'...' if len(columns) > 10 else ''}\n"
            analysis += f"Strings ({len(strings)}): {', '.join(strings[:5])}{'...' if len(strings) > 5 else ''}\n"
            analysis += f"Functions ({len(functions)}): {', '.join(functions[:5])}{'...' if len(functions) > 5 else ''}\n"
            analysis += f"Aliases ({len(aliases)}): {', '.join(aliases[:10])}{'...' if len(aliases) > 10 else ''}\n\n"
            
            # Check for problematic items
            analysis += "QUALITY CHECKS:\n"
            problematic_columns = [col for col in columns if self.is_sql_keyword_or_function(col)]
            problematic_tables = [tbl for tbl in tables if self.is_sql_keyword_or_function(tbl)]
            
            if problematic_columns:
                analysis += f"⚠️  Columns incorrectly identified (should be keywords): {', '.join(problematic_columns)}\n"
            if problematic_tables:
                analysis += f"⚠️  Tables incorrectly identified (should be keywords): {', '.join(problematic_tables)}\n"
            if not problematic_columns and not problematic_tables:
                analysis += "✅ No SQL keywords incorrectly identified as columns/tables\n"
            
            # Check for potential conflicts
            all_items = set(tables + columns + [s.strip('\'"') for s in strings] + functions + aliases)
            duplicates = []
            seen = set()
            for item in all_items:
                if item in seen and item not in duplicates:
                    duplicates.append(item)
                seen.add(item)
            
            if duplicates:
                analysis += f"⚠️  Potential naming conflicts: {', '.join(duplicates)}\n"
            else:
                analysis += "✅ No naming conflicts detected\n"
            
            analysis += "\n"
            
            # Detailed token analysis
            for i, statement in enumerate(parsed):
                analysis += f"Statement {i+1} Analysis:\n"
                analysis += f"Type: {statement.get_type()}\n"
                
                tokens = list(statement.flatten())
                analysis += f"Total tokens: {len(tokens)}\n"
                
                token_types = {}
                for token in tokens:
                    token_type = str(token.ttype) if token.ttype else "None"
                    token_types[token_type] = token_types.get(token_type, 0) + 1
                
                analysis += "Token distribution:\n"
                for token_type, count in sorted(token_types.items()):
                    analysis += f"  {token_type}: {count}\n"
                
                analysis += "\n"
            
            self._show_analysis_popup("SQL Parsing Analysis", analysis)
            
        except Exception as e:
            error_msg = f"Analysis failed: {str(e)}\n\n"
            error_msg += "This could indicate:\n"
            error_msg += "• Extremely complex SQL that exceeds parser capabilities\n"
            error_msg += "• Missing required dependencies\n"
            error_msg += "• Memory or resource limitations\n\n"
            error_msg += "Try simplifying the SQL or contact support."
            
            messagebox.showerror("Analysis Error", error_msg)

    def _show_analysis_popup(self, title, content):
        """Show analysis results in a popup window with syntax highlighting"""
        popup = Toplevel(self.root)
        popup.title(title)
        popup.geometry("1000x700")
        
        text_widget = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=('Consolas', 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add syntax highlighting for analysis content
        text_widget.insert(tk.END, content)
        
        # Apply basic formatting
        text_widget.tag_configure("success", foreground="#4CAF50", font=('Consolas', 10, 'bold'))
        text_widget.tag_configure("warning", foreground="#FF9800", font=('Consolas', 10, 'bold'))
        text_widget.tag_configure("error", foreground="#F44336", font=('Consolas', 10, 'bold'))
        text_widget.tag_configure("header", foreground="#2196F3", font=('Consolas', 11, 'bold'))
        
        # Apply tags to content
        content_lines = content.split('\n')
        for i, line in enumerate(content_lines):
            line_start = f"{i+1}.0"
            line_end = f"{i+1}.end"
            
            if line.startswith("✅"):
                text_widget.tag_add("success", line_start, line_end)
            elif line.startswith("⚠️"):
                text_widget.tag_add("warning", line_start, line_end)
            elif line.startswith("❌") or "ERROR" in line:
                text_widget.tag_add("error", line_start, line_end)
            elif line.endswith(":") and line.isupper():
                text_widget.tag_add("header", line_start, line_end)
        
        text_widget.configure(state='disabled')
        
        # Add copy button
        button_frame = tk.Frame(popup)
        button_frame.pack(pady=5)
        
        def copy_analysis():
            pyperclip.copy(content)
            copy_btn.config(text="✅ Copied!")
            popup.after(2000, lambda: copy_btn.config(text="📋 Copy Analysis"))
        
        copy_btn = tk.Button(button_frame, text="📋 Copy Analysis", command=copy_analysis, 
                           bg="#607D8B", fg="white")
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="❌ Close", command=popup.destroy, 
                 bg="#F44336", fg="black").pack(side=tk.LEFT, padx=5)

    def toggle_ai_features(self):
        """Toggle AI features on/off"""
        self.ai_enabled = not self.ai_enabled
        
        if self.ai_enabled:
            # Check if requests module is available
            if requests is None:
                messagebox.showerror(
                    "Missing Dependency", 
                    "The 'requests' module is required for AI features.\n\n"
                    "Please install it with:\npip install requests\n\n"
                    "Then restart the application."
                )
                self.ai_enabled = False
                return
            
            self.ai_toggle_btn.config(text="🤖 AI Enabled", bg="#4CAF50")
            self.ai_config_btn.config(state='normal')
            
            # Check if API key is configured
            if not self.ai_config['api_key']:
                response = messagebox.askyesno(
                    "AI Features", 
                    "AI features enabled! Would you like to configure your API settings now?"
                )
                if response:
                    self.show_ai_config()
            else:
                self.ai_understand_btn.config(state='normal')
                self.ai_modify_btn.config(state='normal')
                messagebox.showinfo("AI Features", "AI features enabled! You can now use AI to understand and modify code.")
        else:
            self.ai_toggle_btn.config(text="🤖 Enable AI Features", bg="#9E9E9E")
            self.ai_config_btn.config(state='disabled')
            self.ai_understand_btn.config(state='disabled')
            self.ai_modify_btn.config(state='disabled')
            messagebox.showinfo("AI Features", "AI features disabled.")
    
    def show_ai_config(self):
        """Show AI configuration dialog"""
        config_window = Toplevel(self.root)
        config_window.title("AI Configuration")
        config_window.geometry("600x500")
        config_window.resizable(False, False)
        
        # Make it modal
        config_window.transient(self.root)
        config_window.grab_set()
        
        # Header
        header_frame = tk.Frame(config_window, bg="#E3F2FD")
        header_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(header_frame, text="🤖 AI Configuration", font=('Arial', 14, 'bold'), bg="#E3F2FD").pack(pady=5)
        tk.Label(header_frame, text="Configure your AI provider settings", bg="#E3F2FD").pack()
        
        # Main form
        form_frame = tk.Frame(config_window)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # API Provider
        tk.Label(form_frame, text="API Provider:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky="w", pady=5)
        provider_var = tk.StringVar(value=self.ai_config['api_provider'])
        provider_combo = ttk.Combobox(form_frame, textvariable=provider_var, values=['openai', 'anthropic', 'local_llm', 'custom'], state='readonly')
        provider_combo.grid(row=0, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # API Key
        tk.Label(form_frame, text="API Key:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky="w", pady=5)
        api_key_var = tk.StringVar(value=self.ai_config['api_key'])
        api_key_entry = tk.Entry(form_frame, textvariable=api_key_var, show="*", width=40)
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
        tk.Label(form_frame, text="Model:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky="w", pady=5)
        model_var = tk.StringVar(value=self.ai_config['model'])
        model_entry = tk.Entry(form_frame, textvariable=model_var, width=40)
        model_entry.grid(row=2, column=1, sticky="ew", pady=5, padx=(10, 0))
        
        # Base URL (for custom providers)
        tk.Label(form_frame, text="Base URL (optional):", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky="w", pady=5)
        base_url_var = tk.StringVar(value=self.ai_config['base_url'])
        base_url_entry = tk.Entry(form_frame, textvariable=base_url_var, width=40)
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
        
        tk.Label(help_frame, text=help_text, bg="#FFF3E0", justify="left", font=('Arial', 9)).pack(padx=10, pady=10)
        
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
                model_var.set('deepseek-coder-v2:latest')  # Use your available model
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
        
        # Define save_config function first
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
            self.ai_config = {
                'api_key': api_key,
                'api_provider': provider,
                'base_url': base_url,
                'model': model
            }
            
            if self.ai_config['api_key']:
                self.ai_understand_btn.config(state='normal')
                self.ai_modify_btn.config(state='normal')
                messagebox.showinfo("Configuration Saved", "AI configuration saved successfully!")
            else:
                self.ai_understand_btn.config(state='disabled')
                self.ai_modify_btn.config(state='disabled')
                messagebox.showwarning("No API Key", "AI features will remain disabled without an API key.")
            
            config_window.destroy()
        
        # Test connection function
        def test_connection():
            test_config = {
                'api_key': api_key_var.get(),
                'api_provider': provider_var.get(),
                'base_url': base_url_var.get(),
                'model': model_var.get()
            }
            
            if not test_config['api_key']:
                messagebox.showwarning("Test Failed", "Please enter an API key first.")
                return
            
            test_btn.config(text="Testing...", state='disabled')
            
            def run_test():
                try:
                    result = self._test_ai_connection(test_config)
                    config_window.after(0, lambda: (
                        messagebox.showinfo("Test Successful", "✅ Connection successful! AI features are ready to use.") if result
                        else messagebox.showerror("Test Failed", "❌ Connection failed. Please check your settings.")
                    ))
                except Exception as e:
                    config_window.after(0, lambda err=e: messagebox.showerror("Test Error", f"Test failed: {str(err)}"))
                finally:
                    config_window.after(0, lambda: test_btn.config(text="🔍 Test Connection", state='normal'))
            
            threading.Thread(target=run_test, daemon=True).start()
        
        # Buttons
        button_frame = tk.Frame(config_window)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        test_btn = tk.Button(button_frame, text="🔍 Test Connection", command=test_connection, bg="#FF9800", fg="black")
        test_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="💾 Save", command=save_config, bg="#4CAF50", fg="black").pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="❌ Cancel", command=config_window.destroy, bg="#F44336", fg="black").pack(side=tk.RIGHT, padx=5)
    
    def _test_ai_connection(self, config):
        """Test AI API connection"""
        if requests is None:
            messagebox.showerror("Missing Dependency", "The 'requests' module is required for AI features. Please install it with: pip install requests")
            return False
        
        try:
            if config['api_provider'] == 'openai':
                url = config['base_url'] or 'https://api.openai.com/v1/chat/completions'
                headers = {
                    'Authorization': f'Bearer {config["api_key"]}',
                    'Content-Type': 'application/json'
                }
                data = {
                    'model': config['model'],
                    'messages': [{'role': 'user', 'content': 'Hello, this is a test.'}],
                    'max_tokens': 10
                }
            elif config['api_provider'] == 'anthropic':
                url = config['base_url'] or 'https://api.anthropic.com/v1/messages'
                headers = {
                    'x-api-key': config['api_key'],
                    'Content-Type': 'application/json',
                    'anthropic-version': '2023-06-01'
                }
                data = {
                    'model': config['model'],
                    'messages': [{'role': 'user', 'content': 'Hello, this is a test.'}],
                    'max_tokens': 10
                }
            else:  # custom
                if not config['base_url']:
                    raise ValueError("Base URL is required for custom providers")
                url = config['base_url']
                headers = {
                    'Authorization': f'Bearer {config["api_key"]}',
                    'Content-Type': 'application/json'
                }
                data = {
                    'model': config['model'],
                    'messages': [{'role': 'user', 'content': 'Hello, this is a test.'}],
                    'max_tokens': 10
                }
            
            response = requests.post(url, headers=headers, json=data, timeout=10)
            return response.status_code == 200
            
        except Exception as e:
            print(f"AI connection test failed: {e}")
            return False
    
    def choose_data_for_ai(self, title="Choose Data to Send"):
        """Dialog to choose between masked or unmasked data for AI"""
        choice_window = Toplevel(self.root)
        choice_window.title(title)
        choice_window.geometry("600x450")
        choice_window.resizable(False, False)
        
        # Center the window
        choice_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        # Make it modal
        choice_window.transient(self.root)
        choice_window.grab_set()
        
        result = {'choice': None}
        
        # Header
        header_frame = tk.Frame(choice_window, bg="#E8F5E8", relief="ridge", bd=1)
        header_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(header_frame, text="🔒 Data Privacy Choice", font=('Arial', 16, 'bold'), bg="#E8F5E8").pack(pady=8)
        tk.Label(header_frame, text="Choose what data to send to the AI service", font=('Arial', 11), bg="#E8F5E8").pack(pady=(0, 8))
        
        # Main content frame
        content_frame = tk.Frame(choice_window)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Radio button variable
        choice_var = tk.StringVar(value="masked")
        
        # Masked data option
        masked_frame = tk.Frame(content_frame, relief="solid", bd=2, bg="#E3F2FD")
        masked_frame.pack(fill="x", pady=(0, 10))
        
        # Radio button for masked option
        masked_radio_frame = tk.Frame(masked_frame, bg="#E3F2FD")
        masked_radio_frame.pack(fill="x", padx=10, pady=8)
        
        tk.Radiobutton(
            masked_radio_frame, 
            text="🔒 Send Masked Data (Recommended)", 
            font=('Arial', 12, 'bold'), 
            bg="#E3F2FD",
            variable=choice_var,
            value="masked",
            activebackground="#E3F2FD"
        ).pack(anchor="w")
        
        # Description for masked option
        masked_desc = tk.Frame(masked_frame, bg="#E3F2FD")
        masked_desc.pack(fill="x", padx=20, pady=(0, 10))
        
        description_text = """✓ Table and column names are replaced with generic names
✓ String values are anonymized
✓ SQL structure is preserved
✓ Safe for external AI services
✓ Recommended for privacy protection"""
        
        tk.Label(masked_desc, text=description_text, bg="#E3F2FD", justify="left", font=('Arial', 10)).pack(anchor="w")
        
        # Unmasked data option
        unmasked_frame = tk.Frame(content_frame, relief="solid", bd=2, bg="#FFEBEE")
        unmasked_frame.pack(fill="x", pady=0)
        
        # Radio button for unmasked option
        unmasked_radio_frame = tk.Frame(unmasked_frame, bg="#FFEBEE")
        unmasked_radio_frame.pack(fill="x", padx=10, pady=8)
        
        tk.Radiobutton(
            unmasked_radio_frame, 
            text="🔓 Send Original Data (Use with caution)", 
            font=('Arial', 12, 'bold'), 
            bg="#FFEBEE",
            variable=choice_var,
            value="unmasked",
            activebackground="#FFEBEE"
        ).pack(anchor="w")
        
        # Description for unmasked option
        unmasked_desc = tk.Frame(unmasked_frame, bg="#FFEBEE")
        unmasked_desc.pack(fill="x", padx=20, pady=(0, 10))
        
        warning_text = """⚠ Original table and column names included
⚠ Real string values included
⚠ More context for AI analysis
⚠ Only use with trusted AI services
⚠ Consider data sensitivity before choosing"""
        
        tk.Label(unmasked_desc, text=warning_text, bg="#FFEBEE", justify="left", font=('Arial', 10)).pack(anchor="w")
        
        # Buttons
        button_frame = tk.Frame(choice_window)
        button_frame.pack(fill="x", padx=20, pady=15)
        
        def apply_choice():
            result['choice'] = choice_var.get()
            choice_window.destroy()
        
        def cancel_choice():
            result['choice'] = None
            choice_window.destroy()
        
        # Apply button
        tk.Button(
            button_frame, 
            text="✅ Continue", 
            command=apply_choice, 
            bg="#4CAF50", 
            fg="white", 
            font=('Arial', 11, 'bold'),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT, padx=5)
        
        # Cancel button
        tk.Button(
            button_frame, 
            text="❌ Cancel", 
            command=cancel_choice, 
            bg="#F44336", 
            fg="white",
            font=('Arial', 11),
            padx=20,
            pady=5
        ).pack(side=tk.RIGHT, padx=5)
        
        # Wait for user choice
        choice_window.wait_window()
        return result['choice']
    
    def ai_understand_code(self):
        """Use AI to understand and explain the SQL code"""
        if not self.ai_config['api_key']:
            messagebox.showwarning("AI Not Configured", "Please configure AI settings first.")
            self.show_ai_config()
            return
        
        # Get current SQL
        sql = self.input_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("No SQL", "Please enter SQL code first.")
            return
        
        # Choose data type
        data_choice = self.choose_data_for_ai("Understanding Code - Choose Data")
        if not data_choice:
            return
        
        # Get appropriate SQL version
        if data_choice == 'masked':
            if not self.masked_text.get("1.0", tk.END).strip():
                response = messagebox.askyesno("No Masked Data", "No masked SQL available. Would you like to mask the SQL first?")
                if response:
                    self.prepare_masking()
                    return
                else:
                    return
            analysis_sql = self.masked_text.get("1.0", tk.END).strip()
        else:
            analysis_sql = sql
        
        # Create progress window
        progress_window = self._create_progress_window("Understanding SQL Code...")
        
        def analyze_code():
            try:
                prompt = f"""Please analyze and explain this SQL code in detail. Provide:
1. Overall purpose and functionality
2. Key components (tables, joins, filters, etc.)
3. Data flow and logic
4. Any potential issues or improvements
5. Business context if apparent

SQL Code:
{analysis_sql}"""
                
                response = self._call_ai_api(prompt)
                
                if response:
                    progress_window.after(0, lambda: self._show_ai_result("SQL Code Understanding", response, progress_window))
                else:
                    progress_window.after(0, lambda: (
                        progress_window.destroy(),
                        messagebox.showerror("AI Error", "Failed to get AI response. Please check your configuration.")
                    ))
                    
            except Exception as e:
                progress_window.after(0, lambda err=e: (
                    progress_window.destroy(),
                    messagebox.showerror("Error", f"AI analysis failed: {str(err)}")
                ))
        
        threading.Thread(target=analyze_code, daemon=True).start()
    
    def ai_modify_code(self):
        """Use AI to modify SQL code based on natural language instructions"""
        if not self.ai_config['api_key']:
            messagebox.showwarning("AI Not Configured", "Please configure AI settings first.")
            self.show_ai_config()
            return
        
        # Get current SQL
        sql = self.input_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("No SQL", "Please enter SQL code first.")
            return
        
        # Get modification instructions
        instruction_window = self._create_instruction_window()
        if not instruction_window:
            return
        
        instructions = instruction_window['instructions']
        data_choice = instruction_window['data_choice']
        
        # Get appropriate SQL version
        if data_choice == 'masked':
            if not self.masked_text.get("1.0", tk.END).strip():
                response = messagebox.askyesno("No Masked Data", "No masked SQL available. Would you like to mask the SQL first?")
                if response:
                    self.prepare_masking()
                    return
                else:
                    return
            modify_sql = self.masked_text.get("1.0", tk.END).strip()
        else:
            modify_sql = sql
        
        # Create progress window
        progress_window = self._create_progress_window("Modifying SQL Code...")
        
        def modify_code():
            try:
                prompt = f"""Please modify the following SQL code according to these instructions:

Instructions: {instructions}

Original SQL:
{modify_sql}

Please provide:
1. The modified SQL code
2. Explanation of changes made
3. Any assumptions or considerations

Return the modified SQL in a clear, properly formatted way."""
                
                response = self._call_ai_api(prompt)
                
                if response:
                    progress_window.after(0, lambda: self._show_modification_result(response, data_choice, progress_window))
                else:
                    progress_window.after(0, lambda: (
                        progress_window.destroy(),
                        messagebox.showerror("AI Error", "Failed to get AI response. Please check your configuration.")
                    ))
                    
            except Exception as e:
                progress_window.after(0, lambda err=e: (
                    progress_window.destroy(),
                    messagebox.showerror("Error", f"AI modification failed: {str(err)}")
                ))
        
        threading.Thread(target=modify_code, daemon=True).start()
    
    def _create_instruction_window(self):
        """Create window to get modification instructions from user"""
        instruction_window = Toplevel(self.root)
        instruction_window.title("AI Code Modification")
        instruction_window.geometry("600x400")
        
        # Make it modal
        instruction_window.transient(self.root)
        instruction_window.grab_set()
        
        result = {'instructions': None, 'data_choice': None}
        
        # Header
        header_frame = tk.Frame(instruction_window, bg="#E8F5E8")
        header_frame.pack(fill="x", padx=10, pady=10)
        tk.Label(header_frame, text="✏️ AI Code Modification", font=('Arial', 14, 'bold'), bg="#E8F5E8").pack(pady=5)
        tk.Label(header_frame, text="Describe how you want to modify the SQL code", bg="#E8F5E8").pack()
        
        # Instructions input
        tk.Label(instruction_window, text="Modification Instructions:", font=('Arial', 10, 'bold')).pack(anchor="w", padx=20, pady=(10, 5))
        
        instructions_text = scrolledtext.ScrolledText(instruction_window, height=8, font=('Arial', 10))
        instructions_text.pack(fill="both", expand=True, padx=20, pady=5)
        
        # Placeholder text
        placeholder = "Example instructions:\n• Add a WHERE clause to filter by date\n• Include a GROUP BY clause\n• Join with another table\n• Add calculated columns\n• Optimize the query performance\n• Convert to a CTE structure"
        instructions_text.insert("1.0", placeholder)
        instructions_text.bind('<FocusIn>', lambda e: instructions_text.delete("1.0", tk.END) if instructions_text.get("1.0", tk.END).strip() == placeholder else None)
        
        # Data choice
        data_frame = tk.Frame(instruction_window)
        data_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(data_frame, text="Data to send to AI:", font=('Arial', 10, 'bold')).pack(anchor="w")
        
        data_choice_var = tk.StringVar(value="masked")
        tk.Radiobutton(data_frame, text="🔒 Masked data (recommended)", variable=data_choice_var, value="masked").pack(anchor="w")
        tk.Radiobutton(data_frame, text="🔓 Original data (use with caution)", variable=data_choice_var, value="unmasked").pack(anchor="w")
        
        # Buttons
        button_frame = tk.Frame(instruction_window)
        button_frame.pack(fill="x", padx=20, pady=10)
        
        def apply_modification():
            instructions = instructions_text.get("1.0", tk.END).strip()
            if not instructions or instructions == placeholder:
                messagebox.showwarning("No Instructions", "Please provide modification instructions.")
                return
            
            result['instructions'] = instructions
            result['data_choice'] = data_choice_var.get()
            instruction_window.destroy()
        
        tk.Button(button_frame, text="✏️ Modify Code", command=apply_modification, bg="#4CAF50", fg="black", font=('Arial', 10, 'bold')).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="❌ Cancel", command=instruction_window.destroy, bg="#F44336", fg="black").pack(side=tk.RIGHT, padx=5)
        
        # Wait for user input
        instruction_window.wait_window()
        return result if result['instructions'] else None
    
    def _create_progress_window(self, message):
        """Create a progress window for AI operations"""
        progress_window = Toplevel(self.root)
        progress_window.title("AI Processing")
        progress_window.geometry("300x100")
        progress_window.resizable(False, False)
        
        # Make it modal
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        # Center the window
        progress_window.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))
        
        tk.Label(progress_window, text=message, font=('Arial', 10)).pack(pady=20)
        
        # Progress bar
        progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
        progress_bar.pack(pady=10, padx=20, fill="x")
        progress_bar.start()
        
        return progress_window
    
    def _call_ai_api(self, prompt):
        """Make API call to AI service"""
        if requests is None:
            messagebox.showerror("Missing Dependency", "The 'requests' module is required for AI features. Please install it with: pip install requests")
            return None
        
        try:
            config = self.ai_config
            
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
                data = {
                    'model': config['model'],
                    'messages': [{'role': 'user', 'content': prompt}],
                    'max_tokens': 2000,
                    'stream': False
                }
                
                response = requests.post(url, headers=headers, json=data, timeout=60)
                response.raise_for_status()
                return response.json()['choices'][0]['message']['content']
                
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
                
        except Exception as e:
            print(f"AI API call failed: {e}")
            return None
    
    def _show_ai_result(self, title, content, progress_window):
        """Show AI analysis result in a popup window with conversation capability"""
        progress_window.destroy()
        
        result_window = Toplevel(self.root)
        result_window.title(title)
        result_window.geometry("1000x800")
        
        # Make it resizable
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
        tk.Label(input_frame, text="Ask about this SQL:", font=('Arial', 9)).pack(anchor="w")
        question_entry = tk.Text(input_frame, height=3, font=('Arial', 10))
        question_entry.pack(fill="x", pady=2)
        
        # Store conversation history and SQL context
        conversation_history = []
        sql_context = self.input_text.get("1.0", tk.END).strip()
        
        def ask_question():
            question = question_entry.get("1.0", tk.END).strip()
            if not question:
                messagebox.showwarning("Empty Question", "Please enter a question about the SQL.")
                return
            
            # Add question to conversation
            conversation_text.configure(state='normal')
            conversation_text.insert(tk.END, f"\n🙋 You: {question}\n")
            conversation_text.configure(state='disabled')
            conversation_text.see(tk.END)
            
            # Clear input
            question_entry.delete("1.0", tk.END)
            
            # Disable ask button during processing
            ask_btn.config(state='disabled', text="🤔 Thinking...")
            
            def get_ai_response():
                try:
                    # Build conversation context
                    context = f"SQL Code:\n{sql_context}\n\nPrevious Analysis:\n{content}\n\n"
                    if conversation_history:
                        context += "Previous Questions and Answers:\n"
                        for i, (q, a) in enumerate(conversation_history):
                            context += f"Q{i+1}: {q}\nA{i+1}: {a}\n\n"
                    
                    prompt = f"""{context}New Question: {question}

Please answer this specific question about the SQL code. Be concise and focused on the question asked."""
                    
                    response = self._call_ai_api(prompt)
                    
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
                conversation_text.insert(tk.END, f"🤖 AI: {response}\n{'-'*50}\n")
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
        
        ask_btn = tk.Button(question_btn_frame, text="💬 Ask", command=ask_question, bg="#4CAF50", fg="white")
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
                          bg="#2196F3", fg="white", font=('Arial', 8))
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
            pyperclip.copy(full_content)
            copy_btn.config(text="✅ Copied!")
            result_window.after(2000, lambda: copy_btn.config(text="📋 Copy All"))
        
        copy_btn = tk.Button(button_frame, text="📋 Copy All", command=copy_result, bg="#607D8B", fg="white")
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="❌ Close", command=result_window.destroy, bg="#F44336", fg="white").pack(side=tk.RIGHT, padx=5)
        
        # Bind Enter key to ask question
        def on_enter(event):
            if event.state & 0x4:  # Ctrl+Enter
                ask_question()
                return "break"
        
        question_entry.bind("<Control-Return>", on_enter)
    
    def _show_modification_result(self, response, data_choice, progress_window):
        """Show AI modification result with option to apply changes"""
        progress_window.destroy()
        
        result_window = Toplevel(self.root)
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
        
        # Buttons
        button_frame = tk.Frame(result_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        def apply_to_ai_text():
            # Extract SQL from AI response (attempt to find SQL code blocks)
            content = text_widget.get("1.0", tk.END)
            
            # Try to extract SQL from code blocks
            sql_matches = re.finditer(r'```(?:sql)?\s*\n(.*?)\n```', content, re.DOTALL | re.IGNORECASE)
            sql_code = None
            
            for match in sql_matches:
                sql_code = match.group(1).strip()
                break
            
            if not sql_code:
                # If no code blocks found, ask user to select SQL manually
                response_msg = messagebox.askyesno(
                    "Extract SQL", 
                    "No SQL code block found in the response. Would you like to copy the entire response to the AI text area?"
                )
                if response_msg:
                    sql_code = content
                else:
                    return
            
            if data_choice == 'masked':
                # Apply to AI text area (will need unmasking later)
                self.ai_text.delete("1.0", tk.END)
                self.ai_text.insert(tk.END, sql_code)
                self._apply_highlighting('ai_text')
                messagebox.showinfo("Applied", "Modified SQL applied to AI text area. You can now unmask it to see the final result.")
            else:
                # Apply to original input (direct replacement)
                response_msg = messagebox.askyesno(
                    "Replace Original", 
                    "This will replace your original SQL. Do you want to proceed?"
                )
                if response_msg:
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, sql_code)
                    self._apply_highlighting('input_text')
                    messagebox.showinfo("Applied", "Modified SQL applied to original input area.")
            
            result_window.destroy()
        
        def copy_result():
            content = text_widget.get("1.0", tk.END)
            pyperclip.copy(content)
            copy_btn.config(text="✅ Copied!")
            result_window.after(2000, lambda: copy_btn.config(text="📋 Copy"))
        
        copy_btn = tk.Button(button_frame, text="📋 Copy", command=copy_result, bg="#607D8B", fg="white")
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        apply_btn = tk.Button(button_frame, text="✅ Apply Changes", command=apply_to_ai_text, bg="#4CAF50", fg="white")
        apply_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="❌ Close", command=result_window.destroy, bg="#F44336", fg="white").pack(side=tk.RIGHT, padx=5)
    
    def load_file(self):
        """Load SQL file with enhanced error handling and encoding detection"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("SQL files", "*.sql"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if not file_path:
                return
                
            # Try different encodings
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            content = None
            used_encoding = None
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        content = f.read()
                        used_encoding = encoding
                        break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                messagebox.showerror("Error", "Could not read file with any supported encoding.")
                return
            
            # Validate content
            if not content.strip():
                messagebox.showwarning("Warning", "The selected file is empty.")
                return
            
            # Check file size
            if len(content) > 1000000:  # 1MB limit
                response = messagebox.askyesno(
                    "Large File", 
                    f"File is {len(content):,} characters. This may slow down processing. Continue?"
                )
                if not response:
                    return
            
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, content)
            
            # Apply syntax highlighting
            self._apply_highlighting('input_text')
            
            success_msg = f"✅ Loaded {os.path.basename(file_path)}"
            if used_encoding != 'utf-8':
                success_msg += f" (encoding: {used_encoding})"
            
            messagebox.showinfo("Success", success_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"File loading error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedSQLMaskerGUI(root)
    root.mainloop()