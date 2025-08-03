#!/usr/bin/env python3
"""
SQL Masking Core Module
Handles SQL parsing, analysis, and masking operations
"""

import random
import string
import re
try:
    import sqlparse
    from sqlparse import sql, tokens
    from sqlparse.keywords import KEYWORDS
except ImportError:
    sqlparse = None
    sql = None
    tokens = None
    KEYWORDS = {}


class NameGenerator:
    """Generates anonymized names for SQL entities"""
    
    def __init__(self):
        self.table_counter = 0
        self.column_counter = 0
        self.schema_counter = 0
        self.function_counter = 0
        self.string_counter = 0
        
        # Common prefixes for different entity types
        self.table_prefixes = ['tbl', 'data', 'info', 'ref', 'dim', 'fact']
        self.column_prefixes = ['col', 'fld', 'attr', 'prop', 'val']
        self.schema_prefixes = ['db', 'schema', 'ns']
        self.function_prefixes = ['func', 'proc', 'fn']
        
        # Word lists for more realistic names
        self.business_words = [
            'account', 'order', 'customer', 'product', 'service', 'item',
            'transaction', 'payment', 'invoice', 'report', 'data', 'record',
            'entry', 'detail', 'summary', 'status', 'type', 'category'
        ]
        
        self.adjectives = [
            'primary', 'secondary', 'main', 'temp', 'staging', 'final',
            'active', 'archived', 'current', 'historical', 'master', 'lookup'
        ]
    
    def generate_table_name(self, original_name=""):
        """Generate anonymized table name"""
        self.table_counter += 1
        
        if random.choice([True, False]):
            # Business-like name
            prefix = random.choice(self.table_prefixes)
            word = random.choice(self.business_words)
            suffix = random.choice(['', '_data', '_info', '_master', '_detail'])
            return f"{prefix}_{word}{suffix}"
        else:
            # Simple numbered name
            return f"table_{self.table_counter:03d}"
    
    def generate_column_name(self, original_name=""):
        """Generate anonymized column name"""
        self.column_counter += 1
        
        if random.choice([True, False]):
            # Business-like name
            adj = random.choice(self.adjectives + [''])
            word = random.choice(self.business_words)
            suffix = random.choice(['_id', '_name', '_code', '_value', '_flag', ''])
            name = f"{adj}_{word}{suffix}" if adj else f"{word}{suffix}"
            return name.lstrip('_')
        else:
            # Simple numbered name
            prefix = random.choice(self.column_prefixes)
            return f"{prefix}_{self.column_counter:03d}"
    
    def generate_schema_name(self, original_name=""):
        """Generate anonymized schema name"""
        self.schema_counter += 1
        prefix = random.choice(self.schema_prefixes)
        return f"{prefix}_{self.schema_counter:02d}"
    
    def generate_function_name(self, original_name=""):
        """Generate anonymized function name"""
        self.function_counter += 1
        prefix = random.choice(self.function_prefixes)
        action = random.choice(['get', 'set', 'calc', 'proc', 'exec', 'run'])
        return f"{prefix}_{action}_{self.function_counter:02d}"
    
    def generate_string_value(self, original_value=""):
        """Generate anonymized string value"""
        self.string_counter += 1
        length = len(original_value.strip("'\"")) if original_value else random.randint(5, 15)
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(max(1, length)))


class SQLAnalyzer:
    """Analyzes SQL code to extract entities for masking"""
    
    def __init__(self):
        # Note: sqlparse will be used if available, fallback to basic analysis if not
        
        # Enhanced SQL keywords including comprehensive coverage
        if KEYWORDS:
            self.sql_keywords = set(kw.lower() for kw in KEYWORDS.keys())
        else:
            self.sql_keywords = set()
        
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
        }
        
        self.sql_keywords.update(additional_keywords)
    
    def is_sql_keyword_or_function(self, token_str):
        """Check if token is a SQL keyword or common function"""
        token_lower = token_str.lower()
        
        # Check against comprehensive keyword list
        if token_lower in self.sql_keywords:
            return True
        
        # Check for common SQL patterns that shouldn't be masked
        sql_patterns = [
            r'^(select|from|where|join|on|group|order|having|union|insert|update|delete|create|alter|drop)$',
            r'^(inner|left|right|full|outer|cross)$',
            r'^(distinct|all|any|some|exists|in|not|and|or|between|like|is|null)$',
            r'^(asc|desc|limit|offset|top|first|last)$',
            r'.*_id$',  # Common ID column pattern
            r'^(get|set|is|has|can|should|will)_.*',  # Common function prefixes
        ]
        
        for pattern in sql_patterns:
            if re.match(pattern, token_lower):
                return True
        
        return False
    
    def _extract_tables_basic(self, sql):
        """Basic table extraction using regex when sqlparse is not available"""
        tables = []
        sql_upper = sql.upper()
        
        # Pattern to match table names after FROM and JOIN keywords
        from_pattern = r'\bFROM\s+([`"]?[a-zA-Z_][a-zA-Z0-9_]*[`"]?)'
        join_pattern = r'\bJOIN\s+([`"]?[a-zA-Z_][a-zA-Z0-9_]*[`"]?)'
        update_pattern = r'\bUPDATE\s+([`"]?[a-zA-Z_][a-zA-Z0-9_]*[`"]?)'
        insert_pattern = r'\bINSERT\s+INTO\s+([`"]?[a-zA-Z_][a-zA-Z0-9_]*[`"]?)'
        
        patterns = [from_pattern, join_pattern, update_pattern, insert_pattern]
        
        for pattern in patterns:
            matches = re.findall(pattern, sql_upper, re.IGNORECASE)
            for match in matches:
                table_name = match.strip('`"[]')
                if '.' in table_name:
                    table_name = table_name.split('.')[-1]
                if table_name and not self.is_sql_keyword_or_function(table_name):
                    tables.append(table_name.lower())
        
        return list(set(tables))
    
    def _extract_columns_basic(self, sql):
        """Basic column extraction using regex when sqlparse is not available"""
        columns = []
        
        # Extract columns from SELECT clause
        select_pattern = r'\bSELECT\s+(.*?)\s+FROM'
        match = re.search(select_pattern, sql, re.IGNORECASE | re.DOTALL)
        
        if match:
            select_clause = match.group(1)
            # Split by comma and clean up
            potential_columns = [col.strip() for col in select_clause.split(',')]
            
            for col in potential_columns:
                # Remove table prefixes, functions, etc.
                col = re.sub(r'^.*\.', '', col)  # Remove table prefix
                col = re.sub(r'\s+AS\s+.*$', '', col, flags=re.IGNORECASE)  # Remove AS alias
                col = col.strip('`"[]')
                
                # Skip if it's a function call, * or keyword
                if (col and not col == '*' and 
                    not re.match(r'.*\(.*\)', col) and
                    not self.is_sql_keyword_or_function(col)):
                    columns.append(col.lower())
        
        # Extract columns from WHERE, ORDER BY, GROUP BY clauses
        where_pattern = r'\bWHERE\s+(.*?)(?:\s+GROUP\s+BY|\s+ORDER\s+BY|\s*$)'
        order_pattern = r'\bORDER\s+BY\s+(.*?)(?:\s+LIMIT|\s*$)'
        group_pattern = r'\bGROUP\s+BY\s+(.*?)(?:\s+HAVING|\s+ORDER\s+BY|\s*$)'
        
        for pattern in [where_pattern, order_pattern, group_pattern]:
            match = re.search(pattern, sql, re.IGNORECASE | re.DOTALL)
            if match:
                clause = match.group(1)
                # Extract identifiers
                identifiers = re.findall(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', clause)
                for identifier in identifiers:
                    if not self.is_sql_keyword_or_function(identifier):
                        columns.append(identifier.lower())
        
        return list(set(columns))
    
    def _extract_strings_basic(self, sql):
        """Basic string extraction using regex when sqlparse is not available"""
        strings = []
        
        # Pattern to match single and double quoted strings
        string_pattern = r"'[^']*'|\"[^\"]*\""
        matches = re.findall(string_pattern, sql)
        
        return matches
    
    def extract_tables(self, sql):
        """Extract table names from SQL"""
        if not sqlparse:
            return self._extract_tables_basic(sql)
        
        tables = []
        try:
            parsed = sqlparse.parse(sql)
            
            for statement in parsed:
                self._extract_tables_from_statement(statement, tables)
        except Exception:
            # Fallback to basic extraction
            return self._extract_tables_basic(sql)
        
        return list(set(tables))  # Remove duplicates
    
    def _extract_tables_from_statement(self, statement, tables):
        """Extract tables from a SQL statement"""
        from_seen = False
        join_seen = False
        
        for token in statement.flatten():
            if token.ttype is tokens.Keyword and token.value.upper() in ('FROM', 'JOIN', 'UPDATE', 'INSERT INTO'):
                from_seen = True
                join_seen = token.value.upper() in ('JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'OUTER JOIN')
                continue
            
            if from_seen and token.ttype is tokens.Name and not self.is_sql_keyword_or_function(token.value):
                # Clean table name (remove quotes, schema prefixes)
                table_name = token.value.strip('`"[]')
                if '.' in table_name:
                    table_name = table_name.split('.')[-1]  # Get table name after schema
                
                if table_name and not self.is_sql_keyword_or_function(table_name):
                    tables.append(table_name)
                
                if not join_seen:
                    from_seen = False
                join_seen = False
    
    def extract_columns(self, sql):
        """Extract column names from SQL"""
        if not sqlparse:
            return self._extract_columns_basic(sql)
        
        columns = []
        try:
            parsed = sqlparse.parse(sql)
            
            for statement in parsed:
                self._extract_columns_from_statement(statement, columns)
        except Exception:
            # Fallback to basic extraction
            return self._extract_columns_basic(sql)
        
        return list(set(columns))  # Remove duplicates
    
    def _extract_columns_from_statement(self, statement, columns):
        """Extract columns from a SQL statement"""
        in_select = False
        in_where = False
        in_order_by = False
        
        for token in statement.flatten():
            token_value = token.value.upper() if hasattr(token, 'value') else str(token).upper()
            
            if token.ttype is tokens.Keyword:
                if token_value == 'SELECT':
                    in_select = True
                elif token_value in ('FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'HAVING'):
                    in_select = False
                    in_where = token_value == 'WHERE'
                    in_order_by = token_value == 'ORDER BY'
                continue
            
            if (in_select or in_where or in_order_by) and token.ttype is tokens.Name:
                if not self.is_sql_keyword_or_function(token.value):
                    # Clean column name
                    col_name = token.value.strip('`"[]')
                    if '.' in col_name:
                        col_name = col_name.split('.')[-1]  # Get column name after table prefix
                    
                    if col_name and not self.is_sql_keyword_or_function(col_name) and col_name != '*':
                        columns.append(col_name)
    
    def extract_strings(self, sql):
        """Extract string literals from SQL"""
        if not sqlparse:
            return self._extract_strings_basic(sql)
        
        strings = []
        try:
            parsed = sqlparse.parse(sql)
            
            for statement in parsed:
                for token in statement.flatten():
                    if token.ttype in (tokens.String.Single, tokens.String.Symbol):
                        strings.append(token.value)
        except Exception:
            # Fallback to basic extraction
            return self._extract_strings_basic(sql)
        
        return strings
    
    def extract_functions(self, sql):
        """Extract user-defined function names from SQL"""
        if not sqlparse:
            return []  # Basic function extraction is complex, skip for now
        
        functions = []
        try:
            parsed = sqlparse.parse(sql)
            
            for statement in parsed:
                for token in statement.flatten():
                    if token.ttype is tokens.Name and token.value.endswith('('):
                        func_name = token.value[:-1]  # Remove the '('
                        if not self.is_sql_keyword_or_function(func_name):
                            functions.append(func_name)
        except Exception:
            return []
        
        return list(set(functions))
    
    def extract_aliases(self, sql):
        """Extract table and column aliases from SQL"""
        if not sqlparse:
            return []  # Basic alias extraction is complex, skip for now
        
        aliases = []
        try:
            parsed = sqlparse.parse(sql)
            
            for statement in parsed:
                self._extract_aliases_from_statement(statement, aliases)
        except Exception:
            return []
        
        return list(set(aliases))
    
    def _extract_aliases_from_statement(self, statement, aliases):
        """Extract aliases from a SQL statement"""
        tokens_list = list(statement.flatten())
        
        for i, token in enumerate(tokens_list):
            if token.ttype is tokens.Keyword and token.value.upper() == 'AS':
                # Look for the alias after AS
                if i + 1 < len(tokens_list):
                    next_token = tokens_list[i + 1]
                    if next_token.ttype is tokens.Name:
                        aliases.append(next_token.value)
            elif token.ttype is tokens.Name and i + 1 < len(tokens_list):
                # Look for implicit aliases (table name followed by alias)
                next_token = tokens_list[i + 1]
                if (next_token.ttype is tokens.Name and 
                    not self.is_sql_keyword_or_function(next_token.value)):
                    aliases.append(next_token.value)


class SQLMasker:
    """Handles SQL masking and unmasking operations"""
    
    def __init__(self, naming_mode='simple', ai_config=None):
        self.naming_mode = naming_mode  # 'simple', 'business_like', or 'ai_enhanced'
        self.name_generator = NameGenerator()
        self.analyzer = SQLAnalyzer()
        self.ai_config = ai_config  # AI configuration for enhanced masking
        
        # Mapping dictionaries
        self.table_mapping = {}
        self.column_mapping = {}
        self.string_mapping = {}
        self.function_mapping = {}
        self.alias_mapping = {}
        
        # Reverse mappings for unmasking
        self.reverse_table_mapping = {}
        self.reverse_column_mapping = {}
        self.reverse_string_mapping = {}
        self.reverse_function_mapping = {}
        self.reverse_alias_mapping = {}
        
        # AI-enhanced masking context
        self.domain_context = {}
        self.semantic_patterns = {}
    
    def analyze_sql(self, sql):
        """Analyze SQL and return extracted entities"""
        try:
            # Clean SQL from markdown if present
            sql = self._clean_sql_from_markdown(sql)
            
            tables = self.analyzer.extract_tables(sql)
            columns = self.analyzer.extract_columns(sql)
            strings = self.analyzer.extract_strings(sql)
            functions = self.analyzer.extract_functions(sql)
            aliases = self.analyzer.extract_aliases(sql)
            
            return {
                'tables': tables,
                'columns': columns,
                'strings': strings,
                'functions': functions,
                'aliases': aliases
            }
        except Exception as e:
            print(f"Error analyzing SQL: {e}")
            return {'tables': [], 'columns': [], 'strings': [], 'functions': [], 'aliases': []}
    
    def _clean_sql_from_markdown(self, sql):
        """Remove markdown code block formatting from SQL"""
        sql = re.sub(r'^```(?:sql|SQL)?\s*\n', '', sql, flags=re.MULTILINE)
        sql = re.sub(r'\n```\s*$', '', sql, flags=re.MULTILINE)
        return sql.strip()
    
    def generate_mappings(self, entities):
        """Generate placeholder mappings for extracted entities"""
        if self.naming_mode == 'ai_enhanced' and self.ai_config and self.ai_config.is_configured():
            self._generate_ai_enhanced_mappings(entities)
        else:
            self._generate_traditional_mappings(entities)
    
    def _generate_traditional_mappings(self, entities):
        """Generate traditional random mappings"""
        # Generate table mappings
        for table in entities.get('tables', []):
            if table not in self.table_mapping:
                masked_name = self.name_generator.generate_table_name(table)
                # Ensure no conflicts
                while masked_name in self.reverse_table_mapping:
                    masked_name = self.name_generator.generate_table_name(table)
                
                self.table_mapping[table] = masked_name
                self.reverse_table_mapping[masked_name] = table
        
        # Generate column mappings
        for column in entities.get('columns', []):
            if column not in self.column_mapping:
                masked_name = self.name_generator.generate_column_name(column)
                # Ensure no conflicts
                while masked_name in self.reverse_column_mapping:
                    masked_name = self.name_generator.generate_column_name(column)
                
                self.column_mapping[column] = masked_name
                self.reverse_column_mapping[masked_name] = column
        
        # Generate string mappings
        for string_val in entities.get('strings', []):
            if string_val not in self.string_mapping:
                # Preserve quotes
                quote_char = string_val[0] if string_val.startswith(('"', "'")) else "'"
                inner_value = string_val.strip("'\"")
                masked_value = self.name_generator.generate_string_value(inner_value)
                masked_string = f"{quote_char}{masked_value}{quote_char}"
                
                self.string_mapping[string_val] = masked_string
                self.reverse_string_mapping[masked_string] = string_val
        
        # Generate function mappings
        for func in entities.get('functions', []):
            if func not in self.function_mapping:
                masked_name = self.name_generator.generate_function_name(func)
                # Ensure no conflicts
                while masked_name in self.reverse_function_mapping:
                    masked_name = self.name_generator.generate_function_name(func)
                
                self.function_mapping[func] = masked_name
                self.reverse_function_mapping[masked_name] = func
        
        # Generate alias mappings
        for alias in entities.get('aliases', []):
            if alias not in self.alias_mapping:
                masked_name = f"alias_{len(self.alias_mapping) + 1:02d}"
                self.alias_mapping[alias] = masked_name
                self.reverse_alias_mapping[masked_name] = alias

    def _generate_ai_enhanced_mappings(self, entities):
        """Generate AI-enhanced semantic mappings"""
        try:
            # Build context for AI
            context = self._build_mapping_context(entities)
            
            # Generate mappings for each entity type
            if entities.get('tables'):
                table_mappings = self._generate_ai_table_mappings(entities['tables'], context)
                self._apply_table_mappings(table_mappings)
            
            if entities.get('columns'):
                column_mappings = self._generate_ai_column_mappings(entities['columns'], context)
                self._apply_column_mappings(column_mappings)
            
            if entities.get('strings'):
                string_mappings = self._generate_ai_string_mappings(entities['strings'], context)
                self._apply_string_mappings(string_mappings)
            
            # For functions and aliases, use traditional approach as they're less contextual
            for func in entities.get('functions', []):
                if func not in self.function_mapping:
                    masked_name = self.name_generator.generate_function_name(func)
                    while masked_name in self.reverse_function_mapping:
                        masked_name = self.name_generator.generate_function_name(func)
                    self.function_mapping[func] = masked_name
                    self.reverse_function_mapping[masked_name] = func
            
            for alias in entities.get('aliases', []):
                if alias not in self.alias_mapping:
                    masked_name = f"alias_{len(self.alias_mapping) + 1:02d}"
                    self.alias_mapping[alias] = masked_name
                    self.reverse_alias_mapping[masked_name] = alias
                    
        except Exception as e:
            print(f"AI mapping generation failed, falling back to traditional: {e}")
            self._generate_traditional_mappings(entities)
    
    def _build_mapping_context(self, entities):
        """Build context information for AI mapping generation"""
        return {
            'table_count': len(entities.get('tables', [])),
            'column_count': len(entities.get('columns', [])),
            'string_count': len(entities.get('strings', [])),
            'tables': entities.get('tables', []),
            'columns': entities.get('columns', []),
            'sample_strings': entities.get('strings', [])[:5],  # Sample for context
            'domain_hints': self._detect_domain_context(entities)
        }
    
    def _detect_domain_context(self, entities):
        """Detect business domain context from entity names"""
        domains = []
        
        # Analyze table and column names for domain indicators
        all_names = entities.get('tables', []) + entities.get('columns', [])
        
        # Common domain indicators
        domain_patterns = {
            'telecom': ['network', 'call', 'mobile', 'phone', 'telecom', 'carrier', 'operator'],
            'finance': ['account', 'payment', 'transaction', 'billing', 'invoice', 'price'],
            'retail': ['product', 'order', 'customer', 'sale', 'inventory', 'item'],
            'hr': ['employee', 'staff', 'department', 'payroll', 'position'],
            'logistics': ['shipment', 'delivery', 'warehouse', 'tracking', 'carrier']
        }
        
        for domain, keywords in domain_patterns.items():
            if any(keyword in name.lower() for name in all_names for keyword in keywords):
                domains.append(domain)
        
        return domains if domains else ['business']  # Default to business domain
    
    def _generate_ai_table_mappings(self, tables, context):
        """Generate AI-enhanced table mappings"""
        if not tables:
            return {}
            
        prompt = f"""Generate semantic table name mappings for anonymization.

Context: {context['domain_hints'][0] if context['domain_hints'] else 'business'} domain with {context['table_count']} tables.

Original tables: {', '.join(tables)}

Requirements:
1. Preserve semantic meaning (e.g., 'customer_data' → 'client_info')
2. Maintain business logic relationships
3. Use consistent naming patterns
4. Keep similar structure/length when possible
5. Avoid real company/sensitive names

Format response as JSON: {{"original_name": "masked_name", ...}}
"""
        
        try:
            response = self.ai_config.call_ai_api(prompt)
            if response:
                # Extract JSON from response
                import json
                # Look for JSON block in response
                json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
                if json_match:
                    mappings = json.loads(json_match.group())
                    # Validate mappings
                    validated_mappings = {}
                    for original, masked in mappings.items():
                        if original in tables and isinstance(masked, str):
                            validated_mappings[original] = masked
                    return validated_mappings
        except Exception as e:
            print(f"AI table mapping failed: {e}")
        
        return {}
    
    def _generate_ai_column_mappings(self, columns, context):
        """Generate AI-enhanced column mappings"""
        if not columns:
            return {}
            
        # Group columns for better context
        column_sample = columns[:10]  # Limit for prompt size
        
        prompt = f"""Generate semantic column name mappings for anonymization.

Context: {context['domain_hints'][0] if context['domain_hints'] else 'business'} domain.
Tables: {', '.join(context['tables'][:3])}

Original columns: {', '.join(column_sample)}

Requirements:
1. Preserve data type hints (e.g., 'created_date' → 'record_timestamp')
2. Maintain field purpose (e.g., 'customer_id' → 'client_ref')
3. Use consistent patterns for similar fields
4. Keep appropriate field naming conventions

Format response as JSON: {{"original_name": "masked_name", ...}}
"""
        
        try:
            response = self.ai_config.call_ai_api(prompt)
            if response:
                import json
                json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
                if json_match:
                    mappings = json.loads(json_match.group())
                    validated_mappings = {}
                    for original, masked in mappings.items():
                        if original in columns and isinstance(masked, str):
                            validated_mappings[original] = masked
                    return validated_mappings
        except Exception as e:
            print(f"AI column mapping failed: {e}")
        
        return {}
    
    def _generate_ai_string_mappings(self, strings, context):
        """Generate AI-enhanced string mappings"""
        if not strings:
            return {}
            
        # Sample strings for AI processing
        string_sample = strings[:5]
        
        prompt = f"""Generate semantic string value mappings for anonymization.

Context: {context['domain_hints'][0] if context['domain_hints'] else 'business'} domain.

Original strings: {', '.join(string_sample)}

Requirements:
1. Preserve structure and format (e.g., 'Company - Division' → 'Provider - Unit')
2. Maintain data patterns (dates, codes, categories)
3. Keep similar length and character types
4. Use generic but meaningful replacements

Format response as JSON: {{"original_string": "masked_string", ...}}
"""
        
        try:
            response = self.ai_config.call_ai_api(prompt)
            if response:
                import json
                json_match = re.search(r'\{[^}]+\}', response, re.DOTALL)
                if json_match:
                    mappings = json.loads(json_match.group())
                    validated_mappings = {}
                    for original, masked in mappings.items():
                        if original in strings and isinstance(masked, str):
                            validated_mappings[original] = masked
                    return validated_mappings
        except Exception as e:
            print(f"AI string mapping failed: {e}")
        
        return {}
    
    def _apply_table_mappings(self, mappings):
        """Apply AI-generated table mappings"""
        for original, masked in mappings.items():
            if original not in self.table_mapping:
                # Ensure no conflicts
                while masked in self.reverse_table_mapping:
                    masked = f"{masked}_{random.randint(1, 99)}"
                
                self.table_mapping[original] = masked
                self.reverse_table_mapping[masked] = original
    
    def _apply_column_mappings(self, mappings):
        """Apply AI-generated column mappings"""
        for original, masked in mappings.items():
            if original not in self.column_mapping:
                # Ensure no conflicts
                while masked in self.reverse_column_mapping:
                    masked = f"{masked}_{random.randint(1, 99)}"
                
                self.column_mapping[original] = masked
                self.reverse_column_mapping[masked] = original
    
    def _apply_string_mappings(self, mappings):
        """Apply AI-generated string mappings"""
        for original, masked in mappings.items():
            if original not in self.string_mapping:
                self.string_mapping[original] = masked
                self.reverse_string_mapping[masked] = original
    
    def mask_sql(self, sql):
        """Apply masking to SQL using current mappings"""
        try:
            # Check if we have existing mappings, if not, analyze first
            if not any([self.table_mapping, self.column_mapping, self.string_mapping, 
                       self.function_mapping, self.alias_mapping]):
                # No mappings exist, analyze SQL first
                entities = self.analyze_sql(sql)
                self.generate_mappings(entities)
            
            if not sqlparse:
                return self._simple_mask_sql(sql)
            
            masked_sql = sql
            
            # Apply mappings in order of specificity (most specific first)
            # 1. String literals (most specific - exact matches with quotes)
            for original, masked in self.string_mapping.items():
                masked_sql = masked_sql.replace(original, masked)
            
            # 2. Function calls (including parentheses to avoid partial matches)
            for original, masked in self.function_mapping.items():
                pattern = r'\b' + re.escape(original) + r'\s*\('
                replacement = masked + '('
                masked_sql = re.sub(pattern, replacement, masked_sql, flags=re.IGNORECASE)
            
            # 3. Table and column names (use word boundaries to avoid partial matches)
            for original, masked in self.table_mapping.items():
                pattern = r'\b' + re.escape(original) + r'\b'
                masked_sql = re.sub(pattern, masked, masked_sql, flags=re.IGNORECASE)
            
            for original, masked in self.column_mapping.items():
                pattern = r'\b' + re.escape(original) + r'\b'
                masked_sql = re.sub(pattern, masked, masked_sql, flags=re.IGNORECASE)
            
            # 4. Aliases (least specific)
            for original, masked in self.alias_mapping.items():
                pattern = r'\b' + re.escape(original) + r'\b'
                masked_sql = re.sub(pattern, masked, masked_sql, flags=re.IGNORECASE)
            
            return masked_sql
            
        except Exception as e:
            print(f"Error masking SQL: {e}")
            return sql
    
    def _simple_mask_sql(self, sql):
        """Simple string replacement masking when sqlparse is not available"""
        # Check if we have existing mappings, if not, analyze first
        if not any([self.table_mapping, self.column_mapping, self.string_mapping, 
                   self.function_mapping, self.alias_mapping]):
            # No mappings exist, analyze SQL first
            entities = self.analyze_sql(sql)
            self.generate_mappings(entities)
        
        masked_sql = sql
        
        # Apply all mappings using simple string replacement
        all_mappings = [
            self.string_mapping,
            self.function_mapping,
            self.table_mapping,
            self.column_mapping,
            self.alias_mapping
        ]
        
        for mapping in all_mappings:
            for original, masked in mapping.items():
                masked_sql = masked_sql.replace(original, masked)
        
        return masked_sql
    
    def unmask_sql(self, masked_sql):
        """Remove masking from SQL using reverse mappings"""
        try:
            unmasked_sql = masked_sql
            
            # Apply reverse mappings
            all_reverse_mappings = [
                self.reverse_string_mapping,
                self.reverse_function_mapping,
                self.reverse_table_mapping,
                self.reverse_column_mapping,
                self.reverse_alias_mapping
            ]
            
            for reverse_mapping in all_reverse_mappings:
                for masked, original in reverse_mapping.items():
                    if isinstance(masked, str) and isinstance(original, str):
                        unmasked_sql = unmasked_sql.replace(masked, original)
            
            return unmasked_sql
            
        except Exception as e:
            print(f"Error unmasking SQL: {e}")
            return masked_sql
    
    def get_all_mappings(self):
        """Get all current mappings"""
        return {
            'tables': dict(self.table_mapping),
            'columns': dict(self.column_mapping),
            'strings': dict(self.string_mapping),
            'functions': dict(self.function_mapping),
            'aliases': dict(self.alias_mapping)
        }
    
    def set_mappings(self, mappings):
        """Set mappings from external source"""
        self.table_mapping = mappings.get('tables', {})
        self.column_mapping = mappings.get('columns', {})
        self.string_mapping = mappings.get('strings', {})
        self.function_mapping = mappings.get('functions', {})
        self.alias_mapping = mappings.get('aliases', {})
        
        # Rebuild reverse mappings
        self.reverse_table_mapping = {v: k for k, v in self.table_mapping.items()}
        self.reverse_column_mapping = {v: k for k, v in self.column_mapping.items()}
        self.reverse_string_mapping = {v: k for k, v in self.string_mapping.items()}
        self.reverse_function_mapping = {v: k for k, v in self.function_mapping.items()}
        self.reverse_alias_mapping = {v: k for k, v in self.alias_mapping.items()}
    
    def clear_mappings(self):
        """Clear all mappings"""
        self.table_mapping.clear()
        self.column_mapping.clear()
        self.string_mapping.clear()
        self.function_mapping.clear()
        self.alias_mapping.clear()
        
        self.reverse_table_mapping.clear()
        self.reverse_column_mapping.clear()
        self.reverse_string_mapping.clear()
        self.reverse_function_mapping.clear()
        self.reverse_alias_mapping.clear()