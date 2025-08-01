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

class EnhancedSQLMaskerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced SQL Masker for AI Use")
        self.root.geometry("1600x900")

        self.catalog_map = {}
        self.schema_map = {}
        self.table_map = {}
        self.column_map = {}
        self.string_map = {}
        self.function_map = {}
        self.alias_map = {}

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

        self.mapping_text = scrolledtext.ScrolledText(self.root, width=40, state='disabled')
        self.mapping_text.grid(row=1, column=1, rowspan=7, sticky="nsew", padx=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=10, column=0, columnspan=2, pady=10, sticky="ew")
        for i in range(6): btn_frame.columnconfigure(i, weight=1)

        tk.Button(btn_frame, text="Mask SQL", command=self.prepare_masking).grid(row=0, column=0, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Unmask SQL", command=self.unmask_sql).grid(row=0, column=1, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Show Diff", command=self.show_diff).grid(row=0, column=2, padx=5, sticky="ew")
        tk.Button(btn_frame, text="View Mapping", command=self.update_mapping_display).grid(row=0, column=3, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Load SQL File", command=self.load_file).grid(row=0, column=4, padx=5, sticky="ew")
        tk.Button(btn_frame, text="Test SQL", command=self.test_sql_parsing).grid(row=0, column=5, padx=5, sticky="ew")

    def _create_text_section(self, label_text, row, attr_name, readonly=False):
        label = tk.Label(self.root, text=label_text)
        label.grid(row=row, column=0, sticky="w", padx=10, pady=(10, 0))
        text_widget = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=8)
        text_widget.grid(row=row+1, column=0, sticky="nsew", padx=10, pady=5)
        if readonly:
            text_widget.configure(state='disabled')
        setattr(self, attr_name, text_widget)
        self._add_copy_button(text_widget, row+2, 0)

    def _add_copy_button(self, text_widget, row, col):
        btn = tk.Button(self.root, text="Copy")
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

    def extract_tables(self, sql):
        """Enhanced table extraction with error handling and markdown cleanup"""
        try:
            # Clean the SQL first - remove markdown code blocks if present
            clean_sql = sql
            if '```sql' in sql:
                # Extract only the SQL content between ```sql and ```
                sql_blocks = re.findall(r'```sql\s*\n(.*?)\n```', sql, re.DOTALL)
                if sql_blocks:
                    clean_sql = '\n'.join(sql_blocks)
            
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
            clean_sql = sql
            if '```sql' in sql:
                # Extract only the SQL content between ```sql and ```
                sql_blocks = re.findall(r'```sql\s*\n(.*?)\n```', sql, re.DOTALL)
                if sql_blocks:
                    clean_sql = '\n'.join(sql_blocks)
            
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
        """Enhanced string extraction with better regex - only actual SQL strings"""
        # Clean the SQL first - remove markdown code blocks if present
        clean_sql = sql
        if '```sql' in sql:
            # Extract only the SQL content between ```sql and ```
            sql_blocks = re.findall(r'```sql\s*\n(.*?)\n```', sql, re.DOTALL)
            if sql_blocks:
                clean_sql = '\n'.join(sql_blocks)
        
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
        parsed = sqlparse.parse(sql)
        
        for statement in parsed:
            for token in statement.flatten():
                if isinstance(token.parent, Function):
                    func_name = str(token).strip('(')
                    if (not self.is_sql_keyword_or_function(func_name) and 
                        func_name not in functions):
                        functions.append(func_name)
        
        return functions

    def extract_aliases(self, sql):
        """Extract table and column aliases with better filtering"""
        aliases = []
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
        
        return final_aliases

    def generate_placeholders(self, tables, columns, strings, functions=None, aliases=None):
        """Enhanced placeholder generation with better deduplication"""
        def add_map(d, key, prefix, count):
            if (key and 
                key not in d and 
                not self.is_sql_keyword_or_function(key) and
                len(key.strip()) > 0):
                d[key] = {"mask": f"{prefix}_{count[0]}", "enabled": True}
                count[0] += 1

        # Reset all mappings
        self.catalog_map, self.schema_map, self.table_map = {}, {}, {}
        self.column_map, self.string_map = {}, {}
        self.function_map, self.alias_map = {}, {}
        
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
                    add_map(self.catalog_map, catalog, "catalog", c_count)
                    all_processed_items.add(catalog)
                if schema not in all_processed_items:
                    add_map(self.schema_map, schema, "schema", s_count)
                    all_processed_items.add(schema)
                if table not in all_processed_items:
                    add_map(self.table_map, table, "table", t_count)
                    all_processed_items.add(table)
            elif len(parts) == 2:
                schema, table = parts
                if schema not in all_processed_items:
                    add_map(self.schema_map, schema, "schema", s_count)
                    all_processed_items.add(schema)
                if table not in all_processed_items:
                    add_map(self.table_map, table, "table", t_count)
                    all_processed_items.add(table)
            else:
                if tbl not in all_processed_items:
                    add_map(self.table_map, tbl, "table", t_count)
                    all_processed_items.add(tbl)

        # Process columns - avoid items already processed as tables/schemas
        for col in columns:
            if (col and 
                col != '*' and 
                col not in all_processed_items and
                not self.is_sql_keyword_or_function(col)):
                add_map(self.column_map, col, "column", col_count)
                all_processed_items.add(col)

        # Process strings
        for s in strings:
            if s and s not in all_processed_items:
                add_map(self.string_map, s, f"'string{str_count[0]}'", str_count)
                all_processed_items.add(s)

        # Process functions - avoid built-in functions
        if functions:
            for func in functions:
                if (func and 
                    func not in all_processed_items and
                    not self.is_sql_keyword_or_function(func)):
                    add_map(self.function_map, func, "function", func_count)
                    all_processed_items.add(func)

        # Process aliases - be more selective
        if aliases:
            for alias in aliases:
                if (alias and 
                    alias not in all_processed_items and
                    not self.is_sql_keyword_or_function(alias) and
                    len(alias) > 3):  # Only longer aliases to avoid table alias conflicts
                    add_map(self.alias_map, alias, "alias", alias_count)
                    all_processed_items.add(alias)

    def prepare_masking(self):
        """Enhanced preparation with better extraction and input validation"""
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
            messagebox.showerror("Error", f"SQL parsing error: {str(e)}")
            import traceback
            traceback.print_exc()

    def show_mapping_editor(self):
        """Enhanced mapping editor with more categories"""
        top = Toplevel(self.root)
        top.title("Edit Mapping Toggles")
        top.geometry("700x700")

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
            ("Catalogs", "catalog_map"),
            ("Schemas", "schema_map"), 
            ("Tables", "table_map"),
            ("Columns", "column_map"),
            ("Strings", "string_map"),
            ("Functions", "function_map"),
            ("Aliases", "alias_map")
        ]

        for label, attr_key in categories:
            attr = getattr(self, attr_key)
            if not attr:  # Skip empty categories
                continue
                
            category_var = tk.BooleanVar(value=True)
            category_vars[attr_key] = category_var
            item_vars_by_category[attr_key] = []
            
            tk.Checkbutton(
                scroll_frame, text=f"Enable {label} ({len(attr)} items)", 
                variable=category_var, font=('Arial', 10, 'bold')
            ).grid(row=row, column=0, sticky='w', padx=5, pady=3)
            row += 1
            
            for key, val in attr.items():
                var = tk.BooleanVar(value=val["enabled"])
                cb = tk.Checkbutton(
                    scroll_frame, text=f"{key} → {val['mask']}", 
                    variable=var, anchor="w", justify="left"
                )
                cb.grid(row=row, column=0, sticky='w', padx=15)
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
            top.destroy()

        button_frame = tk.Frame(top)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="Apply & Mask SQL", command=apply_and_close).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=top.destroy).pack(side=tk.LEFT, padx=5)

    def mask_sql(self):
        """Enhanced SQL masking with better token handling"""
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
        """Enhanced token masking logic"""
        token_str = str(token)
        token_type = token.ttype

        # Skip keywords, whitespace, comments, and punctuation
        if (token_type in (Keyword, Whitespace, Comment, Punctuation) or
            self.is_sql_keyword_or_function(token_str.strip())):
            return token_str

        # Handle string literals
        if token_type in String.Single or token_str.startswith("'"):
            for original, mapping in self.string_map.items():
                if mapping["enabled"] and original == token_str:
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
        """Enhanced SQL unmasking with better pattern matching"""
        sql = self.ai_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Warning", "Please paste AI-modified SQL first.")
            return

        try:
            # Unmask in reverse order of specificity to avoid conflicts
            for mapping_dict in [self.catalog_map, self.schema_map, 
                               self.table_map, self.column_map,
                               self.function_map, self.alias_map]:
                for original, mapping in mapping_dict.items():
                    if mapping["enabled"]:
                        # Use word boundaries for precise replacement
                        pattern = rf'\b{re.escape(mapping["mask"])}\b'
                        sql = re.sub(pattern, original, sql)

            # Handle strings (no word boundaries needed)
            for original, mapping in self.string_map.items():
                if mapping["enabled"]:
                    sql = sql.replace(mapping["mask"], original)

            self.unmasked_text.delete("1.0", tk.END)
            self.unmasked_text.insert(tk.END, sql)
        except Exception as e:
            messagebox.showerror("Error", f"SQL unmasking error: {str(e)}")

    def show_diff(self):
        """Enhanced diff display"""
        try:
            masked_sql = self.masked_text.get("1.0", tk.END).strip().splitlines()
            ai_sql = self.ai_text.get("1.0", tk.END).strip().splitlines()
            
            diff = list(difflib.unified_diff(
                masked_sql, ai_sql, 
                fromfile='Masked SQL', tofile='AI Modified SQL',
                lineterm=''
            ))
            
            diff_output = '\n'.join(diff) if diff else "No changes detected."
            
            self.diff_text.configure(state='normal')
            self.diff_text.delete("1.0", tk.END)
            self.diff_text.insert(tk.END, diff_output)
            self.diff_text.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Diff generation error: {str(e)}")

    def update_mapping_display(self):
        """Enhanced mapping display with statistics"""
        try:
            self.mapping_text.configure(state='normal')
            self.mapping_text.delete("1.0", tk.END)
            
            categories = [
                ("Catalogs", self.catalog_map),
                ("Schemas", self.schema_map),
                ("Tables", self.table_map),
                ("Columns", self.column_map),
                ("Strings", self.string_map),
                ("Functions", self.function_map),
                ("Aliases", self.alias_map)
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
            self.mapping_text.insert(tk.END, f"Summary: {total_enabled}/{total_items} items will be masked\n")
            end_idx = self.mapping_text.index(tk.END)
            self.mapping_text.tag_add("bold", start_idx, end_idx)
            
            self.mapping_text.tag_configure("bold", font=('TkDefaultFont', 10, 'bold'))
            self.mapping_text.configure(state='disabled')
        except Exception as e:
            messagebox.showerror("Error", f"Mapping display error: {str(e)}")

    def test_sql_parsing(self):
        """Test SQL parsing and show detailed analysis"""
        sql = self.input_text.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Warning", "Please enter SQL code first.")
            return
            
        try:
            # Parse and analyze
            parsed = sqlparse.parse(sql)
            
            analysis = "SQL Parsing Analysis:\n\n"
            analysis += f"Number of statements: {len(parsed)}\n\n"
            
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
            analysis += "KEYWORD CHECK:\n"
            problematic_columns = [col for col in columns if self.is_sql_keyword_or_function(col)]
            problematic_tables = [tbl for tbl in tables if self.is_sql_keyword_or_function(tbl)]
            
            if problematic_columns:
                analysis += f"Columns incorrectly identified (should be keywords): {', '.join(problematic_columns)}\n"
            if problematic_tables:
                analysis += f"Tables incorrectly identified (should be keywords): {', '.join(problematic_tables)}\n"
            if not problematic_columns and not problematic_tables:
                analysis += "✓ No SQL keywords incorrectly identified as columns/tables\n"
            
            analysis += "\n"
            
            for i, statement in enumerate(parsed):
                analysis += f"Statement {i+1}:\n"
                analysis += f"Type: {statement.get_type()}\n"
                
                tokens = list(statement.flatten())
                analysis += f"Total tokens: {len(tokens)}\n"
                
                token_types = {}
                for token in tokens:
                    token_type = str(token.ttype) if token.ttype else "None"
                    token_types[token_type] = token_types.get(token_type, 0) + 1
                
                analysis += "Token types:\n"
                for token_type, count in sorted(token_types.items()):
                    analysis += f"  {token_type}: {count}\n"
                
                analysis += "\n"
            
            # Show in popup
            popup = Toplevel(self.root)
            popup.title("SQL Parsing Analysis")
            popup.geometry("800x600")
            
            text_widget = scrolledtext.ScrolledText(popup, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            text_widget.insert(tk.END, analysis)
            text_widget.configure(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"SQL analysis error: {str(e)}")

    def load_file(self):
        """Load SQL file with error handling"""
        try:
            file_path = filedialog.askopenfilename(
                filetypes=[("SQL files", "*.sql"), ("Text files", "*.txt"), ("All files", "*.*")]
            )
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.input_text.delete("1.0", tk.END)
                    self.input_text.insert(tk.END, content)
                messagebox.showinfo("Success", f"Loaded {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"File loading error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedSQLMaskerGUI(root)
    root.mainloop()