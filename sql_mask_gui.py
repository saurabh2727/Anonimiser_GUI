import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel
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
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.insert(tk.END, content)
        
        # Parse SQL
        try:
            parsed = sqlparse.parse(content)
            
            for statement in parsed:
                self._highlight_tokens(statement, "1.0", highlight_masked, mapping_dict)
                
        except Exception as e:
            print(f"Highlighting error: {e}")
    
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

    def _create_text_section(self, label_text, row, attr_name, readonly=False):
        label = tk.Label(self.root, text=label_text, font=('Arial', 10, 'bold'))
        label.grid(row=row, column=0, sticky="w", padx=10, pady=(10, 0))
        
        # Create text widget with syntax highlighting support
        text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=8, font=('Consolas', 10))
        text_widget.grid(row=row+1, column=0, sticky="nsew", padx=10, pady=5)
        
        if readonly:
            text_widget.configure(state='disabled')
        
        # Initialize syntax highlighter
        highlighter = SyntaxHighlighter(text_widget)
        self.highlighters[attr_name] = highlighter
        
        setattr(self, attr_name, text_widget)
        self._add_copy_button(text_widget, row+2, 0)
        
        # Bind text change events for real-time highlighting
        if not readonly:
            text_widget.bind('<KeyRelease>', lambda e, attr=attr_name: self._on_text_change(attr))
            text_widget.bind('<Button-1>', lambda e, attr=attr_name: self._delayed_highlight(attr))

    def _on_text_change(self, attr_name):
        """Handle text changes for syntax highlighting"""
        self.root.after(500, lambda: self._apply_highlighting(attr_name))

    def _delayed_highlight(self, attr_name):
        """Apply highlighting after a short delay"""
        self.root.after(100, lambda: self._apply_highlighting(attr_name))

    def _apply_highlighting(self, attr_name):
        """Apply syntax highlighting to text widget"""
        try:
            text_widget = getattr(self, attr_name)
            content = text_widget.get("1.0", tk.END)
            
            if content.strip():
                highlighter = self.highlighters[attr_name]
                
                # Get all mappings for highlighting masked/original items
                all_mappings = {}
                for mapping_dict in [self.catalog_map, self.schema_map, self.table_map,
                                   self.column_map, self.string_map, self.function_map, self.alias_map]:
                    all_mappings.update(mapping_dict)
                
                # Apply highlighting
                highlight_masked = attr_name in ['masked_text', 'ai_text', 'unmasked_text']
                highlighter.highlight_sql(content, highlight_masked, all_mappings)
                
        except Exception as e:
            print(f"Highlighting error for {attr_name}: {e}")

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
        widget.configure(state='normal')
        content = widget.get("1.0", tk.END)
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
            filtered_columns = [col for col in all_columns if not '.' in col and 
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
                def callback(*args):
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
                 bg="#F44336", fg="white").pack(side=tk.LEFT, padx=5)

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