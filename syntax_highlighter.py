#!/usr/bin/env python3
"""
SQL Syntax Highlighter Module
Handles SQL syntax highlighting in text widgets
"""

import tkinter as tk
try:
    import sqlparse
    from sqlparse import sql, tokens
    from sqlparse.keywords import KEYWORDS
except ImportError:
    sqlparse = None
    sql = None
    tokens = None
    KEYWORDS = {}


class SQLSyntaxHighlighter:
    """Provides SQL syntax highlighting for Tkinter Text widgets"""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.setup_tags()
    
    def setup_tags(self):
        """Setup text tags for different SQL elements"""
        try:
            # Keywords (blue)
            self.text_widget.tag_config("keyword", foreground="#0000FF", font=('Consolas', 10, 'bold'))
            
            # Strings (green)
            self.text_widget.tag_config("string", foreground="#008000")
            
            # Numbers (red)
            self.text_widget.tag_config("number", foreground="#FF0000")
            
            # Comments (gray)
            self.text_widget.tag_config("comment", foreground="#808080", font=('Consolas', 10, 'italic'))
            
            # Functions (purple)
            self.text_widget.tag_config("function", foreground="#800080", font=('Consolas', 10, 'bold'))
            
            # Operators (dark blue)
            self.text_widget.tag_config("operator", foreground="#000080")
            
            # Punctuation (black)
            self.text_widget.tag_config("punctuation", foreground="#000000")
            
            # Masked elements (highlighted background)
            self.text_widget.tag_config("masked_table", background="#FFE4E1", foreground="#8B0000")
            self.text_widget.tag_config("masked_column", background="#E6E6FA", foreground="#4B0082")
            self.text_widget.tag_config("masked_string", background="#F0FFF0", foreground="#006400")
            
        except Exception:
            # Fallback if tag configuration fails
            pass
    
    def highlight_sql(self, content, highlight_masked=False, mapping_dict=None):
        """Apply SQL syntax highlighting to content"""
        if not content or not content.strip():
            return
        
        try:
            # Clear existing tags
            self._clear_all_tags()
            
            if sqlparse is None:
                # Fallback to simple highlighting if sqlparse not available
                self._simple_highlight(content, highlight_masked, mapping_dict)
                return
            
            # Parse SQL and apply highlighting
            parsed = sqlparse.parse(content)
            current_pos = 1.0
            
            for statement in parsed:
                current_pos = self._highlight_tokens(statement, current_pos, highlight_masked, mapping_dict)
                
        except Exception as e:
            print(f"Error highlighting SQL: {e}")
            # Fall back to simple highlighting
            self._simple_highlight(content, highlight_masked, mapping_dict)
    
    def _clear_all_tags(self):
        """Clear all syntax highlighting tags"""
        tags = ["keyword", "string", "number", "comment", "function", "operator", "punctuation",
                "masked_table", "masked_column", "masked_string"]
        
        for tag in tags:
            try:
                self.text_widget.tag_remove(tag, "1.0", tk.END)
            except Exception:
                pass
    
    def _highlight_tokens(self, statement, start_pos, highlight_masked=False, mapping_dict=None):
        """Highlight individual tokens in a statement"""
        if mapping_dict is None:
            mapping_dict = {}
        
        content = self.text_widget.get("1.0", tk.END)
        current_index = 0
        
        for token in statement.flatten():
            if not hasattr(token, 'value') or not token.value:
                continue
            
            token_text = token.value
            token_length = len(token_text)
            
            # Find the token in the content starting from current position
            token_start = content.find(token_text, current_index)
            if token_start == -1:
                continue
            
            # Convert absolute position to line.char format
            lines_before = content[:token_start].count('\n')
            line_start = content.rfind('\n', 0, token_start) + 1
            char_pos = token_start - line_start
            
            start_pos = f"{lines_before + 1}.{char_pos}"
            end_pos = f"{lines_before + 1}.{char_pos + token_length}"
            
            # Apply appropriate highlighting
            self._apply_token_highlighting(token, start_pos, end_pos, highlight_masked, mapping_dict)
            
            # Update current index
            current_index = token_start + token_length
        
        return "end"
    
    def _apply_token_highlighting(self, token, start_pos, end_pos, highlight_masked, mapping_dict):
        """Apply highlighting to a specific token"""
        token_text = token.value.strip()
        
        if not token_text:
            return
        
        try:
            # Check for masked elements first (if highlighting masked content)
            if highlight_masked and mapping_dict:
                if token_text in mapping_dict.get('tables', {}):
                    self.text_widget.tag_add("masked_table", start_pos, end_pos)
                    return
                elif token_text in mapping_dict.get('columns', {}):
                    self.text_widget.tag_add("masked_column", start_pos, end_pos)
                    return
                elif token_text in mapping_dict.get('strings', {}):
                    self.text_widget.tag_add("masked_string", start_pos, end_pos)
                    return
            
            # Apply syntax highlighting based on token type
            if token.ttype in tokens.Keyword:
                self.text_widget.tag_add("keyword", start_pos, end_pos)
            elif token.ttype in (tokens.String.Single, tokens.String.Symbol, tokens.String):
                self.text_widget.tag_add("string", start_pos, end_pos)
            elif token.ttype in (tokens.Number, tokens.Number.Integer, tokens.Number.Float):
                self.text_widget.tag_add("number", start_pos, end_pos)
            elif token.ttype in (tokens.Comment.Single, tokens.Comment.Multiline):
                self.text_widget.tag_add("comment", start_pos, end_pos)
            elif token.ttype in tokens.Operator:
                self.text_widget.tag_add("operator", start_pos, end_pos)
            elif token.ttype in tokens.Punctuation:
                self.text_widget.tag_add("punctuation", start_pos, end_pos)
            elif token.ttype in tokens.Name and self._is_function_call(token.value):
                self.text_widget.tag_add("function", start_pos, end_pos)
            elif self._is_sql_keyword(token_text):
                self.text_widget.tag_add("keyword", start_pos, end_pos)
                
        except Exception as e:
            print(f"Error applying token highlighting: {e}")
    
    def _is_function_call(self, token_text):
        """Check if token appears to be a function call"""
        return token_text.endswith('(') or (
            hasattr(self.text_widget, 'get') and
            '(' in self.text_widget.get("1.0", tk.END) and
            token_text.lower() in ['count', 'sum', 'avg', 'max', 'min', 'substring', 'concat', 'upper', 'lower']
        )
    
    def _is_sql_keyword(self, token_text):
        """Check if token is a SQL keyword"""
        if not KEYWORDS:
            # Fallback keyword list if sqlparse not available
            common_keywords = {
                'select', 'from', 'where', 'join', 'inner', 'left', 'right', 'outer',
                'on', 'and', 'or', 'not', 'in', 'like', 'between', 'is', 'null',
                'group', 'by', 'order', 'having', 'union', 'insert', 'update',
                'delete', 'create', 'alter', 'drop', 'table', 'index', 'view',
                'distinct', 'all', 'as', 'case', 'when', 'then', 'else', 'end'
            }
            return token_text.lower() in common_keywords
        
        return token_text.upper() in KEYWORDS
    
    def _simple_highlight(self, content, highlight_masked=False, mapping_dict=None):
        """Simple regex-based highlighting when sqlparse is not available"""
        import re
        
        if mapping_dict is None:
            mapping_dict = {}
        
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line_start = f"{line_num}.0"
            
            # Highlight SQL keywords
            keywords = r'\b(SELECT|FROM|WHERE|JOIN|INNER|LEFT|RIGHT|OUTER|ON|AND|OR|NOT|IN|LIKE|BETWEEN|IS|NULL|GROUP|BY|ORDER|HAVING|UNION|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|DISTINCT|AS|CASE|WHEN|THEN|ELSE|END)\b'
            for match in re.finditer(keywords, line, re.IGNORECASE):
                start_pos = f"{line_num}.{match.start()}"
                end_pos = f"{line_num}.{match.end()}"
                try:
                    self.text_widget.tag_add("keyword", start_pos, end_pos)
                except Exception:
                    pass
            
            # Highlight strings
            string_pattern = r"'[^']*'|\"[^\"]*\""
            for match in re.finditer(string_pattern, line):
                start_pos = f"{line_num}.{match.start()}"
                end_pos = f"{line_num}.{match.end()}"
                try:
                    if highlight_masked and match.group() in mapping_dict.get('strings', {}):
                        self.text_widget.tag_add("masked_string", start_pos, end_pos)
                    else:
                        self.text_widget.tag_add("string", start_pos, end_pos)
                except Exception:
                    pass
            
            # Highlight numbers
            number_pattern = r'\b\d+\.?\d*\b'
            for match in re.finditer(number_pattern, line):
                start_pos = f"{line_num}.{match.start()}"
                end_pos = f"{line_num}.{match.end()}"
                try:
                    self.text_widget.tag_add("number", start_pos, end_pos)
                except Exception:
                    pass
            
            # Highlight comments
            comment_pattern = r'--.*$|/\*.*?\*/'
            for match in re.finditer(comment_pattern, line):
                start_pos = f"{line_num}.{match.start()}"
                end_pos = f"{line_num}.{match.end()}"
                try:
                    self.text_widget.tag_add("comment", start_pos, end_pos)
                except Exception:
                    pass
    
    def highlight_search_result(self, search_term, tag_name="search_highlight"):
        """Highlight search results in the text"""
        if not search_term:
            return
        
        # Configure search highlight tag
        try:
            self.text_widget.tag_config(tag_name, background="yellow", foreground="black")
        except Exception:
            pass
        
        # Remove previous search highlights
        try:
            self.text_widget.tag_remove(tag_name, "1.0", tk.END)
        except Exception:
            pass
        
        # Find and highlight all occurrences
        content = self.text_widget.get("1.0", tk.END)
        start = 0
        
        while True:
            pos = content.find(search_term, start)
            if pos == -1:
                break
            
            # Convert position to Tkinter index format
            lines_before = content[:pos].count('\n')
            line_start = content.rfind('\n', 0, pos) + 1
            char_pos = pos - line_start
            
            start_idx = f"{lines_before + 1}.{char_pos}"
            end_idx = f"{lines_before + 1}.{char_pos + len(search_term)}"
            
            try:
                self.text_widget.tag_add(tag_name, start_idx, end_idx)
            except Exception:
                pass
            
            start = pos + 1
    
    def clear_search_highlights(self, tag_name="search_highlight"):
        """Clear search highlights"""
        try:
            self.text_widget.tag_remove(tag_name, "1.0", tk.END)
        except Exception:
            pass


class HighlightedText(tk.Text):
    """A Text widget with built-in SQL syntax highlighting"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.highlighter = SQLSyntaxHighlighter(self)
        
        # Bind events for automatic highlighting
        self.bind('<KeyRelease>', self._on_text_change)
        self.bind('<FocusOut>', self._on_focus_out)
        
        # Delay highlighting to avoid performance issues
        self._highlight_job = None
    
    def _on_text_change(self, event=None):
        """Handle text change events"""
        if self._highlight_job:
            self.after_cancel(self._highlight_job)
        
        # Delay highlighting by 500ms to avoid constant updates
        self._highlight_job = self.after(500, self._delayed_highlight)
    
    def _on_focus_out(self, event=None):
        """Handle focus out events"""
        self._delayed_highlight()
    
    def _delayed_highlight(self):
        """Perform delayed syntax highlighting"""
        try:
            content = self.get("1.0", tk.END)
            self.highlighter.highlight_sql(content)
        except Exception as e:
            print(f"Error in delayed highlighting: {e}")
        finally:
            self._highlight_job = None
    
    def highlight_now(self, highlight_masked=False, mapping_dict=None):
        """Force immediate highlighting"""
        try:
            content = self.get("1.0", tk.END)
            self.highlighter.highlight_sql(content, highlight_masked, mapping_dict)
        except Exception as e:
            print(f"Error in immediate highlighting: {e}")
    
    def search_and_highlight(self, search_term):
        """Search for term and highlight results"""
        self.highlighter.highlight_search_result(search_term)
    
    def clear_search(self):
        """Clear search highlights"""
        self.highlighter.clear_search_highlights()